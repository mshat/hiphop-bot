from typing import List, Dict
from hiphop_bot.db.abstract_model import Model
from hiphop_bot.base_models.model_object_class import BaseModelObject
from hiphop_bot.recommender_system.models.genre import GenreModel


class _ArtistsGenres(BaseModelObject):
    def __init__(self, db_row_id: int, artist_id: int, theme_id: int):
        super().__init__(db_row_id)
        self.artist_id = artist_id
        self.theme_id = theme_id

    def __str__(self):
        return f'{self.artist_id} {self.theme_id}'

    def __repr__(self):
        return f'ArtistsThemes: {self.__str__()}'


class ArtistsGenresModel(Model):
    def __init__(self):
        super().__init__('artists_genres', _ArtistsGenres)

        self._get_all_query = (
            "SELECT id, artist_id, genre_id "
            f"from {self._table_name} "
        )

    def get_all(self) -> List[_ArtistsGenres]:
        return super().get_all()

    def get_genres_by_artist_id(self, artist_id: int) -> List[str] | None:
        all_genres: Dict[int, str] = {genre.id: genre.name for genre in GenreModel().get_all()}
        query = self._get_all_query + f"where artist_id = {artist_id}"
        themes_objects: List[_ArtistsGenres] = self._select_model_objects(query)
        if len(themes_objects) < 0:
            return None
        themes: List[str] = [all_genres[theme.theme_id] for theme in themes_objects]
        return themes

