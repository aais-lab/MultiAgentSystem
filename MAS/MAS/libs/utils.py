# -*- coding: utf-8 -*-
from typing import Any, List, Dict, Optional

import configparser
import os
import csv
import subprocess
from typing import Type, List, Any


# Exception
class FileNotFoundError(Exception):
    """指定されたファイルが見つからない場合の例外"""
    pass


class FolderNotFoundError(Exception):
    """指定されたフォルダが見つからない場合の例外"""
    pass



# Utils
def load_settings(file_name: str, is_editable: bool) -> Dict[str, Dict[str, str]]:
    """設定ファイルを読み込む

    Args:
        file_name (str): 設定ファイル名
        is_editable (bool): 編集可能かどうか

    Returns:
        Dict: 設定データ
    """
    config = configparser.ConfigParser()
    config.optionxform = str
    folder = 'work' if is_editable else ''
    config.read(os.path.join(os.path.dirname(__file__), '..', folder, 'config', f'{file_name}.ini'))

    settings_data = {}
    for section in config.sections():
        settings_data[section] = {}
        for key, value in config.items(section):
            settings_data[section][key] = value
            
    return settings_data


def colorize_text(text: str, color_code: str) -> str:
    """テキストを色付けする

    Args:
        text (str): 色付けするテキスト
        color_code (str): 色コード

    Returns:
        str: 色付けされたテキスト
    """
    return f"\033[{color_code}m{text}\033[0m"



def get_csv_file_path(file_name: str) -> str:
    """CSVファイルのパスを取得する

    Args:
        file_name (str): ファイル名

    Returns:
        str: ファイルパス

    Raises:
        FileNotFoundError: 指定されたファイルが見つからない場合
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', 'work', 'database', f'{file_name}.csv')
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"指定されたファイル '{file_name}.csv' が見つかりません。")
    return file_path


def getStateClass(folder_name: str, class_name: str) -> Type[Any]:
    """状態クラスを取得する

    Args:
        folder_name (str): フォルダ名
        class_name (str): クラス名

    Returns:
        Type[Any]: 状態クラス

    Raises:
        FolderNotFoundError: 指定されたフォルダまたはクラスが見つからない場合
    """
    state_name = class_name + 'State'
    try:
        state_module = __import__(f"work.state_folders.{folder_name}.{class_name}", fromlist=[state_name]) # fromlist=[class_name.upper()
    except:
        raise FolderNotFoundError(f"指定されたフォルダ '{folder_name}' もしくは 指定されたクラス'{class_name}'が見つかりません。")
    return getattr(state_module, state_name)


def create_terminal(window_name: str, script_dir: str, startup_type: str, arguments: List[str], x_position: int, y_position: int) -> None:
    """ターミナルを作成してスクリプトを実行する

    Args:
        window_name (str): ウィンドウ名
        script_dir (str): スクリプトディレクトリ
        startup_type (str): スタートアップタイプ
        arguments (List[str]): 引数リスト
        x_position (int): x座標
        y_position (int): y座標
    """
    applescript_code = f"""
                        tell application "Terminal"
                            activate
                            set newWindow to do script "cd '{script_dir}' && python '{startup_type}.py' {' '.join(arguments)}"
                            set custom title of newWindow to "{window_name}"
                            set bounds of front window to {x_position, y_position, x_position + 480, y_position + 384}
                        end tell
                        """

    subprocess.run(["osascript", "-e", applescript_code])

    print(f"[SYSTEM LOG] starting {window_name} - OK")


def get_knowledge_class(class_name: str) -> Type:
    """
    知識クラスの取得

    Args:
        class_name (str): 取得するクラス名

    Returns:
        Type: 取得したクラス
    """
    module = __import__(f"work.knowledge.{class_name}", fromlist=['KNOWLEDGE'])
    return getattr(module, 'KNOWLEDGE')


def create_dynamic_class(base_class: Type, add_classes: List[Type]) -> Type:
    """
    動的にクラスを作成

    Args:
        base_class (Type): ベースとなるクラス
        add_classes (List[Type]): 追加するクラスのリスト

    Returns:
        Type: 作成された動的クラス
    """
    class_list = [base_class] + add_classes

    def dynamicClassConstructor(self, *args, **kwargs):
        for CLASS in class_list:
            if CLASS == base_class:
                base_class.__init__(self, *args, **kwargs)
            else:
                CLASS.__init__(self)
                
    return type("DynamicClass", tuple(class_list), {"__init__": dynamicClassConstructor})
