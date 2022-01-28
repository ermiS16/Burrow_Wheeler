from enum import Enum

class STATE(Enum):
    INIT = "init"
    INIT_FORWARD = "init_forward"
    INIT_BACKWARD = "init_backward"
    F_ROTATION = "f_rotation"
    F_SORT = "f_sort"
    F_ENCODE = "f_encode"
    F_INDEX_SHOW = "f_index_show"
    F_INDEX_SELECT = "f_index_select"
    F_INDEX_FINAL = "f_index_final"
    F_END = "f_end"

class State:
    def __init__(self, state):
        self._state = state

    def setState(self, state):
        self._state = state

    def getState(self):
        return self._state

    def printState(self):
        print(self._state)
