import os
from typing import Any, List, Dict, Optional

class State:
    def __init__(self, model):
        self.model = model
        self._parent = None
        self._current_child_state_id = None
        self._current_child_state = None
        self.child_state_table = {}

        state_name = os.path.splitext(os.path.basename(__file__))[0]
        print(f"[SYSTEM  LOG]   Load {state_name} State - OK")

    def update(self):
        self.execute()

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value if value != self._parent else self._parent

    @property
    def childState(self):
        return self._current_child_state

    def enter(self):
        pass

    def execute(self):
        pass

    def exit(self):
        pass

    def addChildState(self, state_id, state):
        # 親状態を自身に設定
        self.parent = self
        # 子状態をテーブルに登録
        self.child_state_table[state_id] = state

    def changeState(self, next_status):
        if self._parent is None:
            raise Exception("Not set parent.")
        # 親状態のchangeChildStateメソッドを呼び出して遷移を行う
        self._parent.changeChildState(next_status)


    # 子状態の遷移を行うメソッド
    def changeChildState(self, next_status):
        # 次の状態が子状態テーブルに存在しない場合は例外を発生
        if next_status not in self.child_state_table:
            raise Exception("Can not transit state. " + str(next_status))

        # 現在の子状態を取得し、一時的なリストに格納
        childs = []
        temp_state = self._current_child_state
        while temp_state is not None:
            childs.insert(0, temp_state)
            temp_state = temp_state.childState

        # すべての子状態から順にexit()を呼び出す
        for c in childs:
            c.exit()

        # 新しい子状態IDを設定し、新しい子状態を取得してenter()を呼び出す
        self._current_child_state_id = next_status
        self._current_child_state = self.child_state_table[next_status]
        self._current_child_state.enter()

        # 必要であれば、一度呼び出す
        #self._current_child_state.execute()
