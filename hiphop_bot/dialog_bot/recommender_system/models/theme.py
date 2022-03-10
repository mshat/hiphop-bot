import enum
from typing import List

from hiphop_bot.db.model import Model


class Theme(enum.Enum):
    hard_gangsta = 'hard-gangsta'
    workout = 'workout'
    soft_gangsta = 'soft-gangsta'
    feelings = 'feelings'
    fun = 'fun'
    art = 'art'
    conscious = 'conscious'


class ThemeModel(Model):
    def __init__(self):
        super().__init__('theme')

    def get_all(self) -> List[Theme]:
        raw_data = self.get_all_raw()
        themes = []
        for raw_artist in raw_data:
            themes.append(Theme(*raw_artist))
        return themes

    def get_all_raw(self):
        query = (
            "SELECT name "
            f"from {self._table_name}"
        )
        genres = self._select(query)
        return genres