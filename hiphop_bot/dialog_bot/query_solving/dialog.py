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
    output_message: str
    output_artists: List
    output_genres: List
    debug_message: str

    def __init__(self):
        self._state = DialogState.start
        self.search_result = []
        self.output_message = ''
        self.output_genres = []
        self.output_artists = []
        self.debug_message = ''

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val: DialogState):
        self._state = val