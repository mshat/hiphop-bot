import enum
from typing import List


class DialogState(enum.Enum):
    START = 1
    SEARCH = 2
    FILTER = 3
    NUMBER = 5
    LIKE = 6
    DISLIKE = 7
    INFO = 8


class Dialog:
    _state: DialogState
    search_result: List | None
    output_message: str | None
    output_genres: List | None
    debug_message: str | None

    def __init__(self):
        self._state = DialogState.START
        self.search_result = None
        self.output_message = None
        self.output_genres = None
        self.debug_message = None

    def reset_search_result(self):
        self.search_result = None

    def reset_output(self):
        if self.state not in (DialogState.SEARCH, DialogState.FILTER):
            self.search_result = None
        self.output_message = None
        self.output_genres = None
        self.debug_message = None

    @property
    def search_result_found(self) -> bool:
        if not (self.search_result is None):
            return True
        else:
            return False

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val: DialogState):
        self._state = val
