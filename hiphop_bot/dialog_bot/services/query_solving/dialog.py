import enum
from typing import List
from hiphop_bot.recommender_system.models.artist import _Artist  # Импортируется для аннотаций
from hiphop_bot.recommender_system.recommender_system import RecommendedArtist


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
    _found_artists_with_proximity: List[RecommendedArtist] | None
    info: str | None
    debug_message: str | None
    matched_handler_name: str | None

    def __init__(self):
        self._state = DialogState.START
        self._found_artists = None
        self._found_artists_with_proximity = None
        self.info = None
        self.debug_message = None
        self.matched_handler_name = None

    def reset_search_result(self):
        self._found_artists = None
        self._found_artists_with_proximity = None

    def reset(self):
        if self.state not in (DialogState.SEARCH, DialogState.FILTER):
            self._found_artists = None
            self._found_artists_with_proximity = None
        self.info = None
        self.debug_message = None
        self.matched_handler_name = None

    def _check_artists(self, artists: List[_Artist]) -> None:
        """
        Метод используется для проверки входных данных в сеттере found_artists
        Метод поднимает DialogTypeError если входные данные невалидны
        """
        # Второе условие - проверка на то, что каждый элемент списка имеет тип _Artist
        if not(isinstance(artists, list) and set([isinstance(item, _Artist) for item in artists]) == {True}):
            raise DialogTypeError('Argument must be of type List[_Artist]')

    @property
    def found_artists(self) -> List[_Artist] | None:
        return self._found_artists

    @found_artists.setter
    def found_artists(self, artists: List[_Artist]):
        self._check_artists(artists)
        self._found_artists = artists

    @property
    def found_artists_with_proximity(self) -> List[RecommendedArtist] | None:
        return self._found_artists_with_proximity

    @found_artists_with_proximity.setter
    def found_artists_with_proximity(self, artists: List[RecommendedArtist]):
        self._found_artists_with_proximity = artists

    @property
    def artists_were_found(self) -> bool:
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
