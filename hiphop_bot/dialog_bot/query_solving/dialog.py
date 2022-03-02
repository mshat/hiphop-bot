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
    search_result: List | None
    output_message: str | None
    output_genres: List | None
    debug_message: str | None

    def __init__(self):
        self._state = DialogState.start
        self.search_result = None
        self.output_message = None
        self.output_genres = None
        self.debug_message = None

    def reset_search_result(self):
        self.search_result = None

    def reset_output(self):
        if self.state not in (DialogState.search, DialogState.filter):
            self.search_result = None
        self.output_message = None
        self.output_genres = None
        self.debug_message = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val: DialogState):
        self._state = val