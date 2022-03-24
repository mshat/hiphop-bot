from typing import List, Dict, Tuple
from hiphop_bot.db.abstract_model import Model, AlreadyInTheDatabaseError, InsertError
from hiphop_bot.base_models.model_object_class import BaseModelObject
from hiphop_bot.recommender_system.models.theme import ThemeModel
from hiphop_bot.dialog_bot.services.tools.debug_print import error_print


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

    def get_artists_themes_by_artist_id(self, artist_id: int) -> List[_ArtistsThemes] | None:
        query = self._get_all_query + f"where artist_id = {artist_id}"
        artist_themes_objects: List[_ArtistsThemes] = self._select_model_objects(query)
        if len(artist_themes_objects) < 0:
            return None
        return artist_themes_objects

    def get_themes_names_by_artist_id(self, artist_id: int) -> List[str] | None:
        all_themes: Dict[int, str] = {theme.id: theme.name for theme in ThemeModel().get_all()}
        themes_objects = self.get_artists_themes_by_artist_id(artist_id)
        themes_names: List[str] = [all_themes[theme.theme_id] for theme in themes_objects]
        return themes_names

    def get_themes_ids_by_artist_id(self, artist_id: int) -> List[int] | None:
        themes_objects = self.get_artists_themes_by_artist_id(artist_id)
        themes_ids: List[int] = [theme.theme_id for theme in themes_objects]
        return themes_ids

    def _create_add_record_query(self, artist_id: int, theme_id: int) -> Tuple[str, Tuple]:
        artist_genres_ids = self.get_themes_ids_by_artist_id(artist_id)
        if theme_id in artist_genres_ids:
            raise AlreadyInTheDatabaseError(f'Record {artist_id} {theme_id} is already in the database')

        query = (
            f'insert into {self._table_name} (artist_id, theme_id) '
            f"VALUES(%s, %s);"
        )
        values = (artist_id, theme_id)
        return query, values

    def add_record(self, artist_id: int, theme_id: int):
        try:
            query, values = self._create_add_record_query(artist_id, theme_id)
        except AlreadyInTheDatabaseError as e:
            error_print(f'Failed to add record to {self._table_name}: {e}')
            return

        added_records_number = self._insert(query, values)
        if added_records_number < 1:
            raise InsertError(f'Failed to add record to {self._table_name}')

    def add_multiple_records(self, artist_id: int, themes_names: List[str]):
        connection = self._get_connection()
        cursor = self._get_cursor(connection)

        all_themes_ids: Dict[str, int] = {theme.name: theme.id for theme in ThemeModel().get_all()}
        themes_ids = [all_themes_ids[theme_name] for theme_name in themes_names]
        for theme_id in themes_ids:
            try:
                query, values = self._create_add_record_query(artist_id, theme_id)
            except AlreadyInTheDatabaseError as e:
                error_print(f'Failed to add record to {self._table_name}: {e}')
                continue
            added_records_number = self._simple_insert(query, values, connection, cursor)
            if added_records_number < 1:
                raise InsertError(f'Failed to add record to {self._table_name}: {artist_id} {theme_id}')

        self._commit(connection)
