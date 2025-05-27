# -*- coding: utf-8 -*-

import sys
from typing import Any, List, Dict, Optional

from libs.agent_message import AgentMessage
from libs.edge_agent import EdgeBaseAgent
from libs.communication_module import CommunicationModule, Input
from libs.utils import colorize_text


class ExpertaUser(EdgeBaseAgent):
    """エージェントのベースクラス

    Args:
        EdgeBaseAgent (Type): 継承するエージェントのベースクラス
    """

    def __init__(self, user_name: str, knowledge_list: List[str], agent_list: List[str]) -> None:
        """ユーザの初期化

        Args:
            user_name (str): ユーザの名前
            knowledge_list (List[str]): ユーザの知識リスト
            agent_list (List[str]): エージェントのリスト
        """
        super().__init__(user_name, knowledge_list)

        self.__agent_list = agent_list
        self.__IS_INPUT = False

        self.__engine = CommunicationModule(self)
        self.__engine.reset()
        self.__engine.run()

        self.__input_user_message()
        

    def set_message(self, to: str = None, req: str = None, type_: str = None, args: Any = None, conts: Any=None):
        """送信したいメッセージをコミュニケーションモジュールにセット

        Args:
            to (str, optional)    : 宛先。デフォルトは None。
            req (str, optional)   : リクエスト。デフォルトは None。
            type_ (str, optional) : タイプ。デフォルトは None。
            args (Any, optional)  : 引数。デフォルトは None。
            conts (Any, optional) : コンテンツ。デフォルトは None。
        """
        if (to in self.__agent_list) or (to == 'ALL'):
            self.__engine.reset()
            self.__engine.message_list = {'To': to, 'Request': req, 'Type': type_, 'Args': args, 'Contents':conts}
            self.__engine.declare(Input(MESSAGE_FLAG=True))
            self.__engine.run()
        else:
            self.catch_error_message(to, 'not_found_agent')
            print("\n---------------------------------------------------------------\n")
            if not self.__IS_INPUT:
                self.__input_user_message()


    def __input_user_message(self, to: str = None, request: str = None, type_: str = None) -> None:
            """送信メッセージの入力を受け付け

            Args:
                to (str, optional): 宛先。デフォルトは None.
                request (str, optional): リクエスト。デフォルトは None.
                type_ (str, optional): タイプ。デフォルトは None.
            """
            self.__IS_INPUT = True
            user_inputs = {'To':to, 'Request':request, 'Type':type_, 'Contents':None} # 'Args':None
            for key, value in user_inputs.items():
                if not value:
                    input_data = input(f"[{colorize_text(f'MESSAGE INPUT', '32')}] {key} : ")
                    
                    if input_data.lower() == 'end':
                        self.set_message(to='ALL', req='END')
                        self.stop_program()
                        return
                    else:
                        user_inputs[key] = input_data

            self.__IS_INPUT = False
            self.set_message(to=user_inputs['To'], req=user_inputs['Request'], type_=user_inputs['Type'], conts=user_inputs['Contents']) # ARGS=user_inputs['Args'], 


    def actReturnMessage(self, msg: AgentMessage) -> None:
        """エージェントからの返答メッセージ処理

        Args:
            msg (AgentMessage): メッセージオブジェクト
        """
        match(msg.Type):
            case 'ERROR':
                self.catch_error_message(msg.From, msg.ErrorType, msg.ErrorContents)
            case _:
                print(f"[{colorize_text('MESSAGE LOG', '94')}]   返答 >> {msg.Contents}")
        
        print("\n---------------------------------------------------------------\n")
        if not self.__IS_INPUT:
            self.__input_user_message()


    def actQuestionMessage(self, msg: AgentMessage) -> None:
        """エージェントからの返信要求メッセージ処理

        Args:
            msg (AgentMessage): メッセージオブジェクト
        """
        match(msg.Type):
            case 'ERROR':
                self.catch_error_message(msg.From, msg.ErrorType, msg.ErrorContents)
            case _:
                print(f"[{colorize_text('MESSAGE LOG', '94')}]   返信 >> {msg.Contents}")
        
        print("\n---------------------------------------------------------------\n")
        if not self.__IS_INPUT:
            self.__input_user_message(to=msg.From, request=msg.Args["ReturnRequest"], type_=msg.Args['ReturnType'])


def main() -> None:
    """メイン関数 : ユーザの初期化と起動"""
    user_name = sys.argv[1]
    agent_list = sys.argv[2].split(",")
    knowledge_list = ['ReturnMessage','QuestionMessage']

    print("\n***************************************************************\n")

    ExpertaUser(user_name, knowledge_list, agent_list)


if __name__ == "__main__":
    main()
