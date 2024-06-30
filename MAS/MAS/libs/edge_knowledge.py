# -*- coding: utf-8 -*-
from typing import Any, List, Dict, Optional

from .agent_message import AgentMessage
from .utils import colorize_text


class EdgeBaseKnowldge:
    """知識ファイルのベースクラス"""

    def __init__(self) -> None:
        """クラスの初期化"""
        self.__reset()


    def __reset(self) -> None:
        """データをリセット"""
        self.send_to: str = None
        self.send_req: str = None
        self.send_type: str = None
        self.send_args: Any = None
        self.send_conts: Any = None


    @staticmethod
    def knowledge(func):
        """知識デコレータ

        Args:
            func (Callable): 処理関数

        Returns:
            Callable: ラップされた関数
        """
        def _wrapper(self, msg: AgentMessage, *args):
            self.__reset()
            result = func(self, msg)

            if result == 'NotFoundType':
                print(f"[{colorize_text('SYSTEM ERROR', '31')}]  {self.name} は {msg.Type} というタイプに対応していません")
                self.send_error_message(msg.From, 'have_no_type', msg.Type)

        return _wrapper


    def sendMessage(self) -> None:
        """メッセージの送信"""
        self.set_message(
            to = self.send_to,
            req = self.send_req,
            type_ = self.send_type,
            args = self.send_args,
            conts = self.send_conts)
        self.__reset()
        



