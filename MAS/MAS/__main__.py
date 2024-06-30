# -*- coding: utf-8 -*-

from .libs.redis import Redis
from .libs.utils import load_settings, create_terminal
import os
from typing import Any, List, Dict, Optional

def initializing_redis(shared_db_list: List[str]) -> None:
    """Redisへの接続とDBの初期化

    Args:
        shared_db_list (List[str]): 初期データとして設定するデータベースリストの文字列
    """
    REDIS = Redis()
    REDIS.initialize_database()
    REDIS.set_initial_data(shared_db_list)
    print("[SYSTEM LOG] Redis Initializing - OK")


def starting_agent(script_dir: str, agent_list: List[str], agent_config: Dict[str, Dict[str, str]]) -> None:
    """エージェントの起動

    Args:
        script_dir (str): スクリプトのディレクトリ
        agent_list (List[str]): 起動するエージェントのリスト
        agent_config (Dict[str, Dict[str, str]]): エージェントの設定を含む辞書
    """
    print(f"[SYSTEM LOG] Startup Agent List : {agent_list}")
    for agent_num, agent_name in enumerate(agent_list):
        xPosition = 480 * agent_num
        yPosition = 0

        knowledge = agent_config['KNOWLEDGE'][agent_name]
        arguments = [agent_name, knowledge]

        create_terminal(agent_name, script_dir, "agent", arguments, xPosition, yPosition)


def starting_user(script_dir: str, agent_list: List[str], user_list: List[str]) -> None:
    """ユーザの起動

    Args:
        script_dir (str): スクリプトのディレクトリ
        agent_list (List[str]): エージェントのリスト
        user_list (List[str]): 起動するユーザのリスト
    """
    print(f"[SYSTEM LOG] Startup User List : {user_list}")
    for user_num, user_name in enumerate(user_list):
        xPosition = 480 * user_num
        yPosition = 420

        arguments = [user_name, ','.join(agent_list)]

        create_terminal(user_name, script_dir, "user", arguments, xPosition, yPosition)


def main() -> None:
    """メイン関数 : 設定ファイルの読み込み、Redisの初期化、エージェントおよびユーザの起動"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    agent_config = load_settings('agent_config', is_editable=True)

    user_list = agent_config['SETTINGS']['user_list'].split(",")
    agent_list = agent_config['SETTINGS']['agent_list'].split(",")
    shared_db_list = agent_config['SETTINGS']['shared_db_list'].split(",")

    if not(agent_list == ['']):
        initializing_redis(shared_db_list)
        starting_agent(script_dir, agent_list, agent_config)
        starting_user(script_dir, agent_list, user_list)

    else:
        print("[SYSTEM LOG] エージェントの名前が設定ファイルに記述されていません")


if __name__ == '__main__':
    main()
