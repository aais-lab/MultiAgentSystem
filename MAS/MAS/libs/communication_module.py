# -*- coding: utf-8 -*-
from typing import Any, Dict, Optional

from experta import *
from .agent_message import AgentMessage
from .utils import colorize_text


class Input(Fact):
    """エージェントの入力ファクト

    Args:
        Fact (Type): 基底クラスFactを継承。
    """
    pass


class CommunicationModule(KnowledgeEngine):
    """コミュニケーションモジュール

    Args:
        KnowledgeEngine (Type): 基底クラスKnowledgeEngineを継承
    """

    def __init__(self, entity: Any) -> None:
        """コミュニケーションモジュールの初期化

        Args:
            entity (Any): エンティティオブジェクト
        """
        super().__init__()
        self.__entity = entity
        self.message_list: Optional[Dict[str, Any]] = None


    @DefFacts()
    def _initial_action(self):
        """初期ファクトを設定

        Yields:
            Fact: 初期ファクトInputを生成
        """
        yield Input(MESSAGE_FLAG = False)


    # 送信処理
    @Rule(Input(MESSAGE_FLAG = True))
    def to_someone(self):
        """メッセージをエージェントに送信する処理"""
        msg = AgentMessage()
        msg.From = self.__entity.name
        msg.To = self.message_list['To']
        msg.Request = self.message_list['Request']
        msg.Type = self.message_list['Type']
        msg.Args = self.message_list['Args']
        msg.Contents = self.message_list['Contents']
        
        self.__entity.send_message(msg)

        print(f"[{colorize_text('MESSAGE LOG', '94')}]   {msg.To} にメッセージを送信.\n"
               f"                >> Request   : {msg.Request}\n"
               f"                >> Type      : {msg.Type}\n"
               f"                >> Args      : {msg.Args}\n"
               f"                >> Contents  : {msg.Contents}\n"
               "\n---------------------------------------------------------------\n"
            )
