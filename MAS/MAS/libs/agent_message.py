# -*- coding: utf-8 -*-
from typing import List, Dict, Any

import calendar
import datetime
import json


class AgentMessage:
    """エージェントメッセージ構成クラス"""

    def __init__(self, json_text: str = None):
        """エージェントメッセージの初期化

        Args:
            json_text (str, optional): JSON形式のテキスト. デフォルトは None.
        """
        self.Name: str = ""
        self.Type: str = ""
        self.Date:int = 0
        self.From: str = ""
        self.To: str = ""
        self.Action: str = ""
        self.Request: str = ""
        self.Args: Any = None
        self.Contents: Any = None
        self.ContentLanguage: str = ""
        self.ErrorType: str = ""
        self.ErrorContents: Any = ""

        self.Timeout = ""
        self.TimeLimit = ""
        self.Ack = ""
        self.Protocol = ""
        self.Strategy = ""
        self.ButFor = ""
        self.TaskID = ""
        self.ReplyTo = ""
        self.RepeatCount = ""
        self.TaskTimeout = ""
        self.SenderIP = ""
        self.SenderSite = ""
        self.Thru = ""

        if json_text is not None:
            self.__parse(json_text)


    def to_json(self) -> str:
        """エージェントメッセージをJSON形式に変換

        Returns:
            str: JSON形式のエージェントメッセージ
        """
        self.date = self.__generate_unix_time()
        
        fields = ['Type', 'Date', 'From', 'To', 'Request', 'Args', 'Contents', 'ErrorType', 'ErrorContents']
        data = {key: value for key, value in filter(lambda t: t[0] in fields, self.__dict__.items())} # [TODO]
        return json.dumps(data)
    
    
    def validate(self) -> None:
        """エージェントメッセージの検証"""
        pass


    def __generate_unix_time(self) -> int:
        """現在のUTC時間をUnix時間に変換

        Returns:
            int: Unix時間
        """
        now = datetime.datetime.utcnow()
        unix_time = calendar.timegm(now.utctimetuple())
        return unix_time


    def __parse(self, json_text: str) -> None:
        """JSON形式のテキストをエージェントメッセージにパース

        Args:
            json_text (str): JSON形式のテキスト
        """
        data = json.loads(json_text)
        for key, value in data.items():
            self.__dict__[key] = value
