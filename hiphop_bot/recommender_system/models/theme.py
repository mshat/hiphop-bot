from typing import List, Tuple
from hiphop_bot.db.model import Model


class _Theme:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'Theme: "{self.__str__()}"'


class ThemeModel(Model):
    def __init__(self):
        super().__init__('theme', _Theme)

        self._get_all_query = (
            "SELECT name "
            f"from {self._table_name}"
        )

    def get_all(self) -> List[_Theme]:
        genres = self._select_model_objects(self._get_all_query)
        return genres

    def get_all_raw(self):
        genres = self._raw_select(self._get_all_query)
        return genres

    def get_theme_names(self) -> List[str]:
        raw_data: List[Tuple] = self.get_all_raw()
        names = [raw_theme[0] for raw_theme in raw_data]
        return names