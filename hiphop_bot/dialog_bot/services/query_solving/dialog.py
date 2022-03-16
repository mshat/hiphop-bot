import enum
from typing import List
from hiphop_bot.recommender_system.models.artist import _Artist  # Импортируется для аннотаций


class DialogState(enum.Enum):
    START = 1
    SEARCH = 2
    FILTER = 3
    NUMBER = 5
    LIKE = 6
    DISLIKE = 7
    INFO = 8


class DialogTypeError(Exception): pass


class Dialog:
    _state: DialogState
    _found_artists: List[_Artist] | None
    output_message: str | None
    output_genres: List | None
    debug_message: str | None

    def __init__(self):
        self._state = DialogState.START
        self._found_artists = None
        self.output_message = None
        self.output_genres = None
        self.debug_message = None

    def reset_search_result(self):
        self._found_artists = None

    def reset_output(self):
        if self.state not in (DialogState.SEARCH, DialogState.FILTER):
            self._found_artists = None
        self.output_message = None
        self.output_genres = None
        self.debug_message = None

    @property
    def found_artists(self) -> List[_Artist] | None:
        return self._found_artists

    @found_artists.setter
    def found_artists(self, artists: List[_Artist]):
        # Второе условие - проверка на то, что каждый элемент списка имеет тип _Artist
        if isinstance(artists, list) and set([isinstance(item, _Artist) for item in artists]) == {True}:
            self._found_artists = artists
        else:
            raise DialogTypeError('Argument must be of type List[_Artist]')

    @property
    def search_result_found(self) -> bool:
        if not (self.found_artists is None):
            return True
        else:
            return False

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val: DialogState):
        self._state = val
