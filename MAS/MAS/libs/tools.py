from typing import Any, List, Dict, Optional

from .utils import *
from .state_machine import State
import queue
import threading
import redis
import json
import csv

# ステートマシンで使うモデル
class Model:
    def __init__(self):
        self.state = None
        #self.state_list = {}
        self.send_message_queue = queue.Queue()
        self.IS_STATE_MACHINE = True

# ステートマシンの立ち上げ
def buildStateMachine(model, file_name, has_child_state=False):
    _model = model
    _state_folder_name = file_name[:-len('_config')]

    # 親ステートを設定
    _root_state = State(None)
    _model.state = _root_state

    # ステートマシンの設定読み込み
    _state_config  = load_settings(file_name, is_editable=True)

    # ステートマシンの組み立て
    # 親ステートの設定
    parent_state_list = _state_config['PARENT_STATE']['parent_state_list'].split(",")
    for parent_state_name in parent_state_list:
        #_model.state_list[parent_state_name] = []
        ParentState = getStateClass(_state_folder_name, parent_state_name)
        _root_state.addChildState(parent_state_name, ParentState(_model))

        # 子ステートの設定
        if has_child_state:
            child_state_list = _state_config['CHILD_STATE'][parent_state_name].split(",")
            for child_state_name in child_state_list:
                #_model.state_list[parent_state_name].append(child_state_name)
                if child_state_name != '':
                    ChildState = getStateClass(_state_folder_name, child_state_name)
                    _root_state.child_state_table[parent_state_name].addChildState(child_state_name, ChildState(_model))

    # 初期ステートの設定
    initial_state = _state_config['INITIAL_STATE']['initial_state']
    _root_state.changeChildState(initial_state)

    # ステートマシンの実行
    # ステートマシン
    thread_StateMachine = threading.Thread(target=__startStateMachine, args=(_model, _root_state))
    thread_StateMachine.start()

    print("[SYSTEM  LOG]   Build State Machine - OK")
    print("\n===============================================================\n")
    return _model


# ステートマシンの実行
def __startStateMachine(model, root_state):
    print("[SYSTEM  LOG]   ステートマシンを起動.")
    while model.IS_STATE_MACHINE:
        root_state.childState.update()
    print("[SYSTEM  LOG]   ステートマシンを停止.")


# 辞書を作成する関数
def createDictFromCsv(file_name, key_column, value_column='ALL'):
    """指定されたCSVファイルから辞書を生成

    Parameters:
    file_name (str)                 : CSVファイルの名前（拡張子なし）
    key_column (str)                : 辞書のキーとして使用する列の名前
    value_column (str, optional)    : 辞書の値として使用する列の名前
                                      デフォルトは 'ALL' で、すべての列を辞書の値として格納

    Returns:
    Dict: 生成された辞書

    Example:
    # 'data.csv' ファイルから辞書を生成し、'name' 列をキーとして使用
    data = createDictFromCsv("data", "name")

    # 'data.csv' ファイルから辞書を生成し、'name' 列をキーとして使用し、'age' 列を値として使用
    data = createDictFromCsv("data", "name", "age")
    """
    file_path = get_csv_file_path(file_name)
    data_dict = {}
    with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)

        if value_column == 'ALL':
            for row in reader:
                value_list = {}
                for key, value in row.items():
                    if key != key_column:
                        value_list[key] = value
                data_dict[row[key_column]] = value_list
        else:
            for row in reader:
                data_dict[row[key_column]] = row[value_column]
    csvfile.close()
    return data_dict