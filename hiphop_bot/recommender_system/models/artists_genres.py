from typing import List, Dict, Tuple
from hiphop_bot.db.abstract_model import Model, AlreadyInTheDatabaseError, InsertError
from hiphop_bot.base_models.model_object_class import BaseModelObject
from hiphop_bot.recommender_system.models.genre import GenreModel
from hiphop_bot.dialog_bot.services.tools.debug_print import error_print


class _ArtistsGenres(BaseModelObject):
    def __init__(self, db_row_id: int, artist_id: int, theme_id: int):
        super().__init__(db_row_id)
        self.artist_id = artist_id
        self.genre_id = theme_id

    def __str__(self):
        return f'{self.artist_id} {self.genre_id}'

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

    def get_artist_genres_by_artist_id(self, artist_id: int) -> List[_ArtistsGenres] | None:
        query = self._get_all_query + f"where artist_id = {artist_id}"
        artist_genres_objects: List[_ArtistsGenres] = self._select_model_objects(query)
        if len(artist_genres_objects) < 0:
            return None
        return artist_genres_objects

    def get_genres_names_by_artist_id(self, artist_id: int) -> List[str] | None:
        all_genres: Dict[int, str] = {genre.id: genre.name for genre in GenreModel().get_all()}
        genres_objects = self.get_artist_genres_by_artist_id(artist_id)
        genres_names: List[str] = [all_genres[genre.genre_id] for genre in genres_objects]
        return genres_names

    def get_genres_ids_by_artist_id(self, artist_id: int) -> List[int] | None:
        artist_genres_objects = self.get_artist_genres_by_artist_id(artist_id)
        genres_ids: List[int] = [genre.genre_id for genre in artist_genres_objects]
        return genres_ids

    def _create_add_record_query(self, artist_id: int, genre_id: int) -> Tuple[str, Tuple]:
        artist_genres_ids = self.get_genres_ids_by_artist_id(artist_id)
        if genre_id in artist_genres_ids:
            raise AlreadyInTheDatabaseError(f'Record {artist_id} {genre_id} is already in the database')

        query = (
            f'insert into {self._table_name} (artist_id, genre_id) '
            f"VALUES(%s, %s);"
        )
        values = (artist_id, genre_id)
        return query, values

    def add_record(self, artist_id: int, genre_id: int):
        try:
            query, values = self._create_add_record_query(artist_id, genre_id)
        except AlreadyInTheDatabaseError as e:
            error_print(f'Failed to add record to {self._table_name}: {e}')
            return

        added_records_number = self._insert(query, values)
        if added_records_number < 1:
            raise InsertError('Failed to add record')

    def add_multiple_records(self, artist_id: int, genres_ids: List[int]):
        connection = self._get_connection()
        cursor = self._get_cursor(connection)

        for genre_id in genres_ids:
            try:
                query, values = self._create_add_record_query(artist_id, genre_id)
            except AlreadyInTheDatabaseError as e:
                error_print(f'Failed to add record to {self._table_name}: {e}')
                continue
            added_records_number = self._simple_insert(query, values, connection, cursor)
            if added_records_number < 1:
                raise InsertError(f'Failed to add record to {self._table_name}: {artist_id} {genre_id}')

        self._commit(connection)



