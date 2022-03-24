from typing import List, Dict
from hiphop_bot.db.abstract_model import Model
from hiphop_bot.base_models.model_object_class import BaseModelObject
from hiphop_bot.recommender_system.models.theme import ThemeModel


class _ArtistsThemes(BaseModelObject):
    def __init__(self, db_row_id: int, artist_id: int, theme_id: int):
        super().__init__(db_row_id)
        self.artist_id = artist_id
        self.theme_id = theme_id

    def __str__(self):
        return f'{self.artist_id} {self.theme_id}'

    def __repr__(self):
        return f'ArtistsThemes: {self.__str__()}'


class ArtistsThemesModel(Model):
    def __init__(self):
        super().__init__('artists_themes', _ArtistsThemes)

        self._get_all_query = (
            "SELECT id, artist_id, theme_id "
            f"from {self._table_name} "
        )

    def get_all(self) -> List[_ArtistsThemes]:
        return super().get_all()

    def get_themes_by_artist_id(self, artist_id: int) -> List[str] | None:
        all_themes: Dict[int, str] = {theme.id: theme.name for theme in ThemeModel().get_all()}
        query = self._get_all_query + f"where artist_id = {artist_id}"
        themes_objects: List[_ArtistsThemes] = self._select_model_objects(query)
        if len(themes_objects) < 0:
            return None
        themes: List[str] = [all_themes[theme.theme_id] for theme in themes_objects]
        return themes
