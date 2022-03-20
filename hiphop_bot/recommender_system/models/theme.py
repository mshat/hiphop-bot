from typing import List, Tuple
from hiphop_bot.db.abstract_model import Model
from hiphop_bot.recommender_system.models.model_object_class import _ModelObject


class _Theme(_ModelObject):
    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'Theme: "{self.__str__()}"'


class ThemeModel(Model):
    def __init__(self):
        super().__init__('theme', _Theme)

        self._get_all_query = (
            "SELECT id, name "
            f"from {self._table_name} "
        )

    def get_all(self) -> List[_Theme]:
        themes = self._select_model_objects(self._get_all_query)
        return themes

    def get_all_raw(self) -> List[Tuple[int, str]]:
        return super(ThemeModel, self).get_all_raw()

    def get_theme_names(self) -> List[str]:
        raw_data: List[Tuple[int, str]] = self.get_all_raw()
        names = [raw_theme[1] for raw_theme in raw_data]
        return names

    def get_by_name(self, name: str) -> _Theme | None:
        query = self._get_all_query + f"where name = '{name}'"
        theme = self._select_model_objects(query)
        if len(theme) > 0:
            return theme[0]
        else:
            return None
