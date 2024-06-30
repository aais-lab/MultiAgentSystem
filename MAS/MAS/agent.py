# -*- coding: utf-8 -*-

import sys
from typing import Any, List, Dict, Optional

from libs.agent_message import AgentMessage
from libs.edge_agent import EdgeBaseAgent
from libs.communication_module import CommunicationModule, Input
from libs.utils import get_knowledge_class, create_dynamic_class


class ExpertaAgent(EdgeBaseAgent):
    """エージェントのベースクラス

    Args:
        EdgeBaseAgent (Type): 継承するエージェントのベースクラス
    """

    def __init__(self, agent_name: str, knowledge_list: List[str]) -> None:
        """エージェントの初期化

        Args:
            agent_name (str): エージェントの名前
            knowledge_list (List[str]): 知識のリスト
        """
        super().__init__(agent_name, knowledge_list)
        
        self.__engine = CommunicationModule(self)
        self.__engine.reset()
        self.__engine.run()    


    def set_message(self, to: str = None, req: str = None, type_: str = None, args: Any = None, conts: Any = None) -> None:
        """
        送信メッセージをコミュニケーションモジュールにセット

        Args:
            to (str, optional)   : 宛先。デフォルトは None。
            req (str, optional)  : リクエスト。デフォルトは None。
            type_ (str, optional): タイプ。デフォルトは None。
            args (Any, optional) : 引数。デフォルトは None。
            conts (Any, optional): コンテンツ。デフォルトは None。
        """
        self.__engine.reset()
        self.__engine.message_list = {'To': to, 'Request': req, 'Type': type_, 'Args': args, 'Contents':conts}
        self.__engine.declare(Input(MESSAGE_FLAG=True))
        self.__engine.run()


    def actReturnMessage(self, msg: AgentMessage) -> None:
        """予約済みメッセージの処理

        Args:
            msg (AgentMessage): メッセージオブジェクト
        """
        if msg.Type == 'ERROR':
            self.catch_error_message(msg.From, msg.ErrorType, msg.ErrorContents)
            error_contents = {'target_agent':msg.From, 'target_error':msg.ErrorContents}
            self.send_error_message('USER', 'agent_misconfiguration', error_contents)
    

def main():
    """メイン関数 : エージェントの初期化と起動"""
    agent_name = sys.argv[1]
    knowledge_list = sys.argv[2].split(",")

    knowledge_class_list = []
    for knowledge in knowledge_list:
        knowledge_class_list.append(get_knowledge_class(knowledge))
    dynamic_class = create_dynamic_class(ExpertaAgent, knowledge_class_list)
    knowledge_list.append('ReturnMessage')

    print("\n***************************************************************\n")

    dynamic_class(agent_name, knowledge_list)


if __name__ == "__main__":
    main()