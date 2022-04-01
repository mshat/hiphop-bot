from __future__ import annotations
from typing import List, Tuple, Dict
from datetime import datetime
from hiphop_bot.db.abstract_model import (Model, ModelError, ModelUniqueViolationError, DeleteError,
                                          AlreadyInTheDatabaseError)
from hiphop_bot.recommender_system.models.theme import ThemeModel, _Theme  # импортирутеся для аннотации
from hiphop_bot.recommender_system.models.gender import GenderModel, _Gender  # импортирутеся для аннотации
from hiphop_bot.recommender_system.models.genre import GenreModel, _Genre  # импортирутеся для аннотации
from hiphop_bot.recommender_system.models.artists_genres import ArtistsGenresModel, _ArtistsGenres
from hiphop_bot.recommender_system.models.artists_themes import ArtistsThemesModel, _ArtistsThemes
from hiphop_bot.dialog_bot.models.artists_names_aliases import ArtistsNamesAliasesModel
from hiphop_bot.recommender_system.models.artist_pairs_proximity import ArtistsPairsProximityModel
from hiphop_bot.recommender_system.models.artist_streaming_service_link import (
    ArtistStreamingServiceLinkModel, _StreamingServiceLinks)
from hiphop_bot.base_models.model_object_class import ModelObject
from hiphop_bot.dialog_bot.services.tools.debug_print import error_print, debug_print
from hiphop_bot.dialog_bot.config import DEBUG_MODEL
from hiphop_bot.recommender_system.artists_pairs_proximity_loader import update_artist_pairs_proximity


class _Artist(ModelObject):
    themes: List[_Theme]
    gender: _Gender
    genres: List[_Genre]
    streaming_service_links: _StreamingServiceLinks | None
    aliases: List[str]

    def __init__(
            self,
            db_row_id: int,
            name: str,
            year_of_birth: int,
            group_members_number: int,
            gender: _Gender | str,
            streaming_service_links: _StreamingServiceLinks = None
    ):
        super().__init__(db_row_id, name)
        self.name = name
        self.year_of_birth = year_of_birth
        self.group_members_number = group_members_number
        self._themes = None
        self._genres = None
        self._aliases = None

        self._gender = gender if isinstance(gender, _Gender) else GenderModel().get_by_name(gender)
        self._streaming_service_links = streaming_service_links

    @property
    def age(self):
        current_year = datetime.now().year
        return current_year - self.year_of_birth

    @property
    def themes(self) -> List[_Theme]:
        return self._themes

    @themes.setter
    def themes(self, themes: List[_ArtistsThemes]):
        if len(themes) < 1:
            self._themes = []
            return
        if not isinstance(themes[0], _ArtistsThemes):
            raise TypeError('Unexpected argument type')

        self._themes = [ThemeModel().get_by_id(artist_theme.theme_id) for artist_theme in themes]

    @property
    def gender(self) -> str:
        return self._gender.name

    @property
    def genres(self) -> List[_Genre]:
        return self._genres

    @genres.setter
    def genres(self, genres: List[_ArtistsGenres]):
        if len(genres) < 1:
            self._genres = []
            return
        if not isinstance(genres[0], _ArtistsGenres):
            raise TypeError('Unexpected argument type')

        self._genres = [GenreModel().get_by_id(artist_genre.genre_id) for artist_genre in genres]

    @property
    def streaming_service_links(self) -> _StreamingServiceLinks:
        return self._streaming_service_links

    @streaming_service_links.setter
    def streaming_service_links(self, links: _StreamingServiceLinks):
        if isinstance(links, _StreamingServiceLinks):
            self._streaming_service_links = links
        else:
            raise ModelError("Argument must be of type _StreamingServiceLinks")

    @property
    def aliases(self) -> List[str]:
        return self._aliases

    @aliases.setter
    def aliases(self, aliases: List[str]):
        if not aliases or len(aliases) < 1:
            self._aliases = []
            return
        assert isinstance(aliases[0], str)
        self._aliases = aliases

    def __str__(self):
        return f'{self.name} {self.year_of_birth} {self.group_members_number} {self._themes} {self._gender} ' \
               f'{self._genres} {self.streaming_service_links} {self.aliases}'

    def __repr__(self):
        return f'Artist: "{self.__str__()}"'


class ArtistModel(Model):
    def __init__(self):
        super().__init__('artist', _Artist)

        self._get_all_query = (
            "SELECT artist.id, artist.name, year_of_birth, group_members_num, gender.name "
            f"from {self._table_name} "
            "inner join gender on artist.gender_id = gender.id "
        )

    def _select_model_objects(self, query) -> List[_Artist]:
        artists: List[_Artist] = super()._select_model_objects(query)

        streaming_service_link_model = ArtistStreamingServiceLinkModel()
        artist_links = streaming_service_link_model.get_artist_links_dict()

        for artist in artists:
            if artist.name in artist_links:
                # добавляем артистам ссылки на стриминговые сервисы
                artist.streaming_service_links = artist_links[artist.name]
                # подргужаю жанры и темы из соответствующих таблиц
                artist.genres = ArtistsGenresModel().get_artist_genres_by_artist_id(artist.id)
                artist.themes = ArtistsThemesModel().get_artists_themes_by_artist_id(artist.id)
                # добавляем алиасы
                artist.aliases = ArtistsNamesAliasesModel().get_by_artist_name(artist.name)

        return artists

    def get_all(self) -> List[_Artist]:
        return super(ArtistModel, self).get_all()

    def get_artist_names(self) -> List[str]:
        raw_data: List[Tuple] = self.get_all_raw()
        names = [raw_artist[1] for raw_artist in raw_data]
        return names

    def get_by_genre(self, genre: str) -> List[_Artist] | List:
        query = self._get_all_query
        query += (f"inner join artists_genres as a_g on a_g.artist_id = artist.id "
                  "inner join genre on a_g.genre_id = genre.id "
                  f"where genre.name = '{genre}'")
        artists = self._select_model_objects(query)
        return artists

    def get_by_name(self, name: str) -> _Artist | None:
        query = self._get_all_query + f"where artist.name ='{name}'"
        artists = self._select_model_objects(query)
        if len(artists) > 0:
            return artists[0]
        else:
            return None

    def get_by_id(self, id_: int) -> _Artist | None:
        query = self._get_all_query + f"where artist.id ='{id_}'"
        artists = self._select_model_objects(query)
        if len(artists) > 0:
            return artists[0]
        else:
            return None

    def _add_streaming_service_link(self, new_artist_id: int, streaming_service_name: str, streaming_service_link: str):
        streaming_service_link_model = ArtistStreamingServiceLinkModel()
        streaming_service_link_model.add_record(new_artist_id, streaming_service_name, streaming_service_link)

    def _add_artist_aliases(self, new_artist_id: int, aliases: List[str]):
        artist_names_aliases = ArtistsNamesAliasesModel()
        artist_names_aliases.add_record(new_artist_id, aliases)

    def recalc_artists_pairs_proximity(self):
        all_artists = self.get_all()
        if len(all_artists) > 1:
            update_artist_pairs_proximity(all_artists)

    def _add_artist_genres(self, artist_id: int, genres: List[str]):
        artists_genres_model = ArtistsGenresModel()
        artists_genres_model.add_multiple_records(artist_id, genres)

    def _add_artist_themes(self, artist_id: int, themes: List[str]):
        artists_themes_model = ArtistsThemesModel()
        artists_themes_model.add_multiple_records(artist_id, themes)

    def delete(self, id_: int):
        connection = self._get_connection()
        cursor = self._get_cursor(connection)

        if ArtistsPairsProximityModel().get_by_first_artist_name(self.get_by_id(id_).name):
            ArtistsPairsProximityModel().delete(id_, cursor)
        ArtistsThemesModel().delete(id_, cursor)
        ArtistsGenresModel().delete(id_, cursor)
        ArtistStreamingServiceLinkModel().delete(id_, cursor)
        ArtistsNamesAliasesModel().delete(id_, cursor)

        try:
            self._raw_delete(f"delete from {self._table_name} where id = %s", (id_,), cursor)
        except DeleteError as e:
            error_print(f'Не смог удалить артиста с id: {id_}. Изменения не будут сохранены. {e}')
        except Exception as e:
            raise DeleteError(f'Неизвестная ошибка при попытке удаления артиста с id: {id_}: {e}')
        else:
            self._commit(connection)
            self._close_cursor_and_connection(cursor, connection)
            debug_print(DEBUG_MODEL, f'[MODEL] Удалил артиста с id {id_}')

    def add_record(
            self,
            name: str,
            year_of_birth: int,
            group_members_num: int,
            themes: List[str],
            gender: str,
            genres: List[str],
            streaming_service_names: List[str],
            streaming_service_links: List[str],
            artist_name_aliases_: List[str],
            update_if_exist=False,
            recalc_artists_pairs_proximity=True
    ):
        """
        Метод для добавления или обновления артиста в БД
        :param update_if_exist: обновлять данные, если артист с таким именем существует в БД
        :param recalc_artists_pairs_proximity: пересчитывать значения близости всех артистов со всеми. При множественном
        добавлении лучше задать False и по его окончании самостоятельно вызвать метод _recalc_artists_pairs_proximity
        """
        name = name.lower()
        themes = [theme_.lower() for theme_ in themes]
        gender = gender.lower()
        genres = [genre_.lower() for genre_ in genres]
        streaming_service_names = list(map(str.lower, streaming_service_names))
        streaming_service_links = list(map(str.lower, streaming_service_links))
        artist_name_aliases = []
        [artist_name_aliases.append(a.lower()) for a in artist_name_aliases_ if a not in artist_name_aliases]
        existing_record = self.get_by_name(name)
        if existing_record:
            if update_if_exist:
                # TODO при обновлении записи может произойти ошибка, а удаление уже будет закоммичено
                self.delete(existing_record.id)
                assert self.get_by_name(name) is None
            else:
                raise AlreadyInTheDatabaseError(f'Failed to add record. Artist {name} already exists')

        theme_model = ThemeModel()
        gender_model = GenderModel()
        genre_model = GenreModel()
        themes_obj: List[_Theme] = [theme_model.get_by_name(theme) for theme in themes]
        gender_obj: _Gender = gender_model.get_by_name(gender)
        genres_obj: List[_Genre] = [genre_model.get_by_name(genre) for genre in genres]

        for field_name, field in {'name': name, 'year_of_birth': year_of_birth, 'group_members_num': group_members_num,
                                  'gender_obj': gender_obj}.items():
            if not field:
                raise ModelError(f'Error adding artist: {field_name} field is None ')
        if len(themes_obj) != len(themes):
            raise ModelError(f'Error adding artist: one or more themes not found ')
        if len(genres_obj) != len(genres):
            raise ModelError(f'Error adding artist: one or more genres not found ')

        query = (
            f'insert into {self._table_name} (name, year_of_birth, group_members_num, gender_id) '
            f"VALUES(%s, %s, %s, %s);"
        )
        values = (name, year_of_birth, group_members_num, gender_obj.id)

        try:
            added_records_number = self._insert(query, values)
            if added_records_number < 1:
                raise ModelError('Failed to add record')
        except ModelUniqueViolationError:
            pass

        new_artist_id = self.get_by_name(name).id
        for name, link in zip(streaming_service_names, streaming_service_links):
            if name != '' and link != '':
                self._add_streaming_service_link(new_artist_id, name, link)
        self._add_artist_aliases(new_artist_id, artist_name_aliases)
        self._add_artist_genres(new_artist_id, genres)
        self._add_artist_themes(new_artist_id, themes)
        if recalc_artists_pairs_proximity:
            self.recalc_artists_pairs_proximity()
