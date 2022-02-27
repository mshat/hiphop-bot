import enum
from typing import List


class DialogState(enum.Enum):
    start = 1
    search = 2
    filter = 3
    number = 5
    like = 6
    dislike = 7
    info = 8


class Dialog:
    _state: DialogState
    search_result: List

    def __init__(self):
        self._state = DialogState.start
        self.search_result = []

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val: DialogState):
        self._state = val