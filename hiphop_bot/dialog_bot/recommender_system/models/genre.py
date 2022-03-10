import enum
from typing import List

from hiphop_bot.db.model import Model


class Genre(enum.Enum):
    hiphop = 'hiphop'
    battlerap = 'battlerap'
    freestyle = 'freestyle'
    regular = 'regular'
    hiphopmusic = 'hiphopmusic'
    newschool = 'newschool'
    alternative = 'alternative'
    emo = 'emo'
    raprock = 'raprock'
    electronichiphop = 'electronichiphop'
    cloud = 'cloud'
    club = 'club'
    drill = 'drill'
    electronicvocal = 'electronicvocal'
    grime = 'grime'
    mumble = 'mumble'
    phonk = 'phonk'
    hardcore = 'hardcore'
    horrorcore = 'horrorcore'
    rapcore = 'rapcore'
    underground = 'underground'
    popular = 'popular'
    hookah = 'hookah'
    pop = 'pop'
    oldschool = 'oldschool'
    oldschoolhardcore = 'oldschoolhardcore'
    gangsta = 'gangsta'
    workout = 'workout'
    russianrap = 'russianrap'
    classic = 'classic'
    soft = 'soft'


class GenreModel(Model):
    def __init__(self):
        super().__init__('genre')

    def get_all(self) -> List[Genre]:
        raw_data = self.get_all_raw()
        genres = []
        for raw_artist in raw_data:
            genres.append(Genre(*raw_artist))
        return genres

    def get_all_raw(self):
        query = (
            "SELECT name "
            f"from {self._table_name}"
        )
        genres = self._select(query)
        return genres