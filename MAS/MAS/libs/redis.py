from typing import Any, List, Dict, Optional
from .utils import load_settings, get_csv_file_path
import redis
import json
import csv

class Redis():
    """Redis"""

    def __init__(self):
        """RedisHandlerの初期化"""
        host, port = self.__load_network_settings()
        db_number = 0
        self.__redis = self.__connect_redis(host, port, db_number)


    def __load_network_settings(self) -> tuple[str, int]:
        """ネットワーク設定をロード

        Returns:
            tuple[str, int]: ホストとポートのタプル
        """
        network_config = load_settings('network_config', is_editable=False)
        host = network_config['SETTINGS']['IP']
        port = network_config['SETTINGS']['PORT']
        return (host, port)


    def __connect_redis(self, host: str, port: int, db_number: int) -> redis.Redis:
        """Redisに接続

        Args:
            host (str): Redisサーバーのホスト
            port (int): Redisサーバーのポート

        Returns:
            redis.Redis: Redisインスタンス
        """
        return redis.Redis(host=host, port=port, db=db_number)


    def initialize_database(self) -> None:
        """データベースを初期化"""
        self.__redis.flushdb()


    def set_initial_data(self, file_name_list: List[str]) -> None:
        """初期データを設定

        Args:
            file_name_list (List[str]): ファイル名のリスト
        """
        if file_name_list[0] != "":
            for file_name in file_name_list:
                with open(get_csv_file_path(file_name), 'r', encoding='utf-8') as csvfile:
                    set_data_dict = {row[0]: row[1] for row in csv.reader(csvfile)}
                csvfile.close()
                for element_key, set_value in set_data_dict.items():
                    self.__redis.hset(file_name, element_key, json.dumps(set_value, ensure_ascii=False))


    #************************** 以下、使用可能関数 ********************************#

    def getAllData(self, unique_key: str):
        """指定された一意のキーに関連付けられたすべてのデータをRedisデータベースから取得

        Args:
            unique_key (str): Redisデータベースからデータを取得するための一意の識別子

        Returns:
            Dict: 一意のキーに関連付けられたすべてのデータを含む辞書
                  キーが見つからない場合は空の辞書を返す

        Example:
            >>> Redis = Redis()
            >>> data = Redis.getAllData("任意のキー")
            >>> print(data)
            {'フィールド1': '値1', 'フィールド2': '値2', ...}
        """
        return self.__redis.hgetall(unique_key)


    def getData(self, unique_key: str, element_key: str):
        """指定された一意のキーから指定された要素キーのデータをRedisデータベースから取得

        Args:
            unique_key (str)    : データを取得するための一意の識別子
            element_key (str)   : 取得したい要素のキー

        Returns:
            Dict: 指定された要素キーのデータを含む辞書

        Raises:
            KeyError: 指定された要素キーが見つからない場合に発生

        Example:
            >>> Redis = Redis()

            >>> data = Redis.getData("例のキー", "要素のキー")
            >>> print(data)
            {'フィールド1': '値1', 'フィールド2': '値2', ...}

            >>> data = Redis.getData("例のキー")
            >>> print(data)
            {'フィールド1': {'キー11': '値11', 'キー12': '値12'}, 'フィールド2': {'キー21': '値21', 'キー22': '値22'}, ...}
        """
        get_value = self.__redis.hget(unique_key, element_key)
        if get_value is not None:
            return json.loads(get_value)
        else:
            raise KeyError(f"指定された要素キー '{element_key}' が見つかりません。")


    def setData(self, unique_key: str, element_key, set_value: str):
        """Redisデータベースに指定された一意のキーと要素キーに対応するデータを設定

        Args:
            unique_key (str)    : データを設定するための一意の識別子
            element_key (str)   : 設定したい要素のキー
            set_value (Dict)    : 設定するデータを含む辞書

        Returns:
            None

        Example:
            >>> Redis = Redis()
            >>> data = {'フィールド1': '値1', 'フィールド2': '値2', ...}
            >>> Redis.setData("例のキー", "要素のキー", data)
            # データを追加

        """
        self.__redis.hset(unique_key, element_key, json.dumps(set_value))


    def deleteData(self, unique_key: str, element_key: str):
        """
        Redisデータベースから指定された一意のキーと要素キーに対応するデータを削除

        Args:
            unique_key (str)    : データを削除するための一意の識別子
            element_key (str)   : 削除したい要素のキー

        Returns:
            None

        Example:
            >>> Redis = Redis()
            >>> Redis.deleteData("例のキー", "要素のキー")
            # データを削除

        """
        self.__redis.hdel(unique_key, element_key)
