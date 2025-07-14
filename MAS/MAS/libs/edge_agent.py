# -*- coding: utf-8 -*-

from .agent_message import AgentMessage
from .utils import colorize_text
from typing import Any, List, Dict, Optional

import redis
import configparser
import time
import os


class EdgeBaseAgent:
    def __init__(self, name: str, knowledge: List[str] = None, auto_load: bool = True):
        """エージェントの初期化

        Args:
            name (str): エージェントの名前
            knowledge (List[str], optional): エージェントの知識リスト. デフォルトは None.
            auto_load (bool, optional): 自動読み込みフラグ. デフォルトは True.
        """

        self.name = name
        
        if knowledge:
            self.__knowledge_list = {item: "act" + item[0].upper() + item[1:] for item in knowledge}
        else:
            self.__knowledge_list = {}

        self.__load_settings()
        print(f"[SYSTEM LOG] Load Settings - OK")

        if auto_load:
            self.__start()
            self.IS_SYSTEM = True


    def __load_settings(self) -> None:
        """設定の読み込み"""
        config = configparser.ConfigParser()
        config.read('config/network_config.ini')

        channel = config['SETTINGS']['CHANNEL']
        self.__host = config['SETTINGS']['IP']
        self.__port = config['SETTINGS']['PORT']
        self.__topic = 'coterie-' + channel


    def __start(self) -> None:
        """起動"""
        self.__connect_network()
        self.__initialize()
        self.__initialized()


    def __initialize(self) -> None:
        """初期化"""
        pass


    def __initialized(self) -> None:
        """初期化完了"""
        pass


    def __reconnect(self) -> None:
        """ネットワーク再接続"""
        self.__connect_network()


    def __stop(self) -> None:
        """停止"""
        self.__thread.stop()
        print(f"[SYSTEM LOG] プログラムは1秒後に停止します.")
        time.sleep(1)
        print(f"[SYSTEM LOG] さようなら.")
        os._exit(-1)


    def __connect_network(self, db_index: int = 0) -> None:
        """ネットワーク接続

        Args:
            db_index (int, optional): db接続の番号 . デフォルトは 0.
        """
        self.__blackboard = redis.StrictRedis(host=self.__host, port=self.__port, db=db_index)
        pubsub = self.__blackboard.pubsub()
        pubsub.psubscribe(**{self.__topic: self.__on_message})
        self.__thread = pubsub.run_in_thread(sleep_time=0.01)

        print(f"[SYSTEM LOG] Network Access - OK")

        print(f"[SYSTEM LOG] Host : {self.__host}, Port :{self.__port}, DB : {db_index}\n"
              f"[SYSTEM LOG] Subscribe Topic : {self.__topic}\n"
              f"[SYSTEM LOG] Knowledge List : {self.__knowledge_list}")
        print("\n===============================================================\n"
              f"{self.__name} CONSOLE"
              "\n===============================================================\n")


    def __on_message(self, msg: Dict) -> None:
        """メッセージの受信

        Args:
            msg (Dict): 受信したメッセージ
        """
        get_message = AgentMessage(msg['data'].decode())
        if get_message.To in (self.__name, "ALL") and get_message.From != self.__name:
            self.__receive_message(get_message)


    def __receive_message(self, msg: AgentMessage) -> None:
        """受信メッセージ処理

        Args:
            msg (AgentMessage): 受信したメッセージ
        """
        if msg.Request and msg.Request.lower() == 'end':
            self.stop_program()

        elif msg.Request in self.__knowledge_list:
            print(f"[{colorize_text('MESSAGE LOG', '94')}]   {msg.From} からメッセージを受信.")
            request = self.__knowledge_list[msg.Request]

            try:
                method = getattr(self, request)
                print(f"[{colorize_text('MESSAGE LOG', '94')}]   {msg.From} からのリクエストは '{msg.Request}'.")
            except AttributeError:
                print(f"[{colorize_text('SYSTEM ERROR', '31')}]  {msg.From} は '{request}' というリクエストを処理できません.\n"
                      f"[{colorize_text('SYSTEM ERROR', '31')}]  知識フォルダ（/MAS/work/knowledge/{request}.py)に'act{request.capitalize()}というメソッドがあるかどうか確認してください.")
                self.send_error_message(msg.From, 'have_no_function', request)
            
            method(msg)

        else:
            print(f"[{colorize_text('SYSTEM ERROR', '31')}]  {msg.From} は {msg.Request} というリクエストに対応できる知識を持っていません.")
            self.send_error_message(msg.From, 'have_no_knowledge', msg.Request)


    def send_message(self, msg: AgentMessage) -> None:
        """メッセージの送信

        Args:
            msg (AgentMessage): 送信するメッセージ
        """
        self.__blackboard.publish(self.__topic, msg.to_json())


    def catch_error_message(self, agent_name: str, error_type: str, error_contents: Dict = None) -> None:
        """エージェントからのエラーメッセージ

        Args:
            agent_name (str): エージェントの名前
            error_type (str): エラーの種類
            error_contents (Dict, optional): エラーの内容. デフォルトはNone.
        """
        match error_type:
            case 'have_no_function':
                print(f"[{colorize_text('MESSAGE ERROR', '31')}] {agent_name} は '{error_contents}' という関数を持っていません.")
            case 'have_no_knowledge':
                print(f"[{colorize_text('MESSAGE ERROR', '31')}] {agent_name} は '{error_contents}' という知識を持っていません.")
            case 'have_no_type':
                print(f"[{colorize_text('MESSAGE ERROR', '31')}] {agent_name} は '{error_contents}' というタイプに対応していません.")
            case 'not_found_agent':
                print(f"[{colorize_text('MESSAGE ERROR', '31')}] '{agent_name}' というエージェントは存在しません.")
            case 'agent_misconfiguration':
                target_agent = error_contents['target_agent']
                target_error = error_contents['target_error']
                print(f"[{colorize_text('MESSAGE ERROR', '31')}] '{target_agent} に送信される {target_error} の内容にミスがあります. または {target_agent} に {target_error}を設定していません.")


    def send_error_message(self, to: str, error_type: str, error_contents: Any) -> None:
        """エラーメッセージの送信関数

        Args:
            to (str): 宛先
            error_type (str): エラーの種類
            error_contents (Any): エラーの内容
        """
        msg = AgentMessage()
        msg.From = self.__name
        msg.To = to
        msg.Request = "ReturnMessage"
        msg.Type = "ERROR"
        msg.ErrorType = error_type
        msg.ErrorContents = error_contents
        self.send_message(msg)

        print(f"[{colorize_text('MESSAGE LOG', '31')}]   {to} にエラーメッセージを送信.")
        print("\n---------------------------------------------------------------\n")


    def stop_program(self) -> None:
        """コードの終了変数"""
        self.__stop()
        self.IS_SYSTEM = False


    def on_connect(self) -> None:
        """挨拶"""
        msg = AgentMessage()
        msg.Type = "INFORM"
        msg.From = self.__name
        msg.To = "ALL"
        msg.Request = "HELLO"
        msg.Args = ""
        self.send_message(msg)


    # --- Properties ---
    @property
    def name(self) -> str:
        """エージェントの名前を取得

        Returns:
            str: エージェントの名前
        """
        return self.__name


    @name.setter
    def name(self, name: str) -> None:
        """エージェントの名前を設定

        Args:
            name (str): エージェントの名前
        """
        self.__name = name
        