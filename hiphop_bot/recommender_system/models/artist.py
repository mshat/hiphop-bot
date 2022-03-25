from typing import List, Tuple, Dict
from datetime import datetime
from hiphop_bot.db.abstract_model import Model, ModelError, ModelUniqueViolationError
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
from hiphop_bot.dialog_bot.services.tools.debug_print import error_print


class _Artist(ModelObject):
    themes: List[_Theme]
    gender: _Gender
    genres: List[_Genre]
    streaming_service_links: _StreamingServiceLinks | None

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
    def themes(self, themes: List[_ArtistsThemes] | List[str]):
        if isinstance(themes, str):
            raise Exception('WTTTFFF')
        if isinstance(themes[0], str):
            raise Exception('WTTTFFF')

        if isinstance(themes[0], _ArtistsThemes):
            self._themes = [ThemeModel().get_by_id(artist_theme.theme_id) for artist_theme in themes]
        elif isinstance(themes[0], str):
            self._themes = [ThemeModel().get_by_name(theme) for theme in themes]

    @property
    def gender(self) -> str:
        return self._gender.name

    @property
    def genres(self) -> List[_Genre]:
        return self._genres

    @genres.setter
    def genres(self, genres: List[_ArtistsGenres] | List[str]):
        if isinstance(genres, str):
            raise Exception('WTTTFFF')
        if isinstance(genres[0], str):
            raise Exception('WTTTFFF')

        if isinstance(genres[0], _ArtistsGenres):
            self._genres = [GenreModel().get_by_id(artist_genre.genre_id) for artist_genre in genres]
        elif isinstance(genres[0], str):
            self._genres = [GenreModel().get_by_name(genre) for genre in genres]

    @property
    def streaming_service_links(self) -> _StreamingServiceLinks:
        return self._streaming_service_links

    @streaming_service_links.setter
    def streaming_service_links(self, links: _StreamingServiceLinks):
        if isinstance(links, _StreamingServiceLinks):
            self._streaming_service_links = links
        else:
            raise ModelError("Argument must be of type _StreamingServiceLinks")

    def __str__(self):
        return f'{self.name} {self.year_of_birth} {self.group_members_number} {self._themes} {self._gender} ' \
               f'{self._genres} {self.streaming_service_links}'

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

        # добавляем артистам ссылки на стриминговые сервисы
        for artist in artists:
            if artist.name in artist_links:
                artist.streaming_service_links = artist_links[artist.name]

        # подргужаю жанры и темы из соответствующих таблиц
        for artist in artists:
            if artist.name in artist_links:
                artist.genres = ArtistsGenresModel().get_artist_genres_by_artist_id(artist.id)
                artist.themes = ArtistsThemesModel().get_artists_themes_by_artist_id(artist.id)

        return artists

    def get_all(self) -> List[_Artist]:
        return super(ArtistModel, self).get_all()

    def get_artist_names(self) -> List[str]:
        raw_data: List[Tuple] = self.get_all_raw()
        names = [raw_artist[1] for raw_artist in raw_data]
        return names

    def get_by_genre(self, genre: str) -> List[_Artist] | List:
        query = self._get_all_query + f"where genre.name = '{genre}'"
        artists = self._select_model_objects(query)
        return artists

    def get_by_name(self, name: str) -> _Artist | None:
        query = self._get_all_query + f"where artist.name ='{name}'"
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

    # TODO дописать
    def _add_record_to_artists_pairs_proximity(self, new_user_name, pairs_proximity: Dict[str, float]):
        artists_pairs_proximity_model = ArtistsPairsProximityModel()

    def _add_artist_genres(self, artist_id: int, genres: List[str]):
        artists_genres_model = ArtistsGenresModel()
        artists_genres_model.add_multiple_records(artist_id, genres)

    def _add_artist_themes(self, artist_id: int, themes: List[str]):
        artists_themes_model = ArtistsThemesModel()
        artists_themes_model.add_multiple_records(artist_id, themes)

    def add_record(
            self,
            name: str,
            year_of_birth: int,
            group_members_num: int,
            themes: List[str],
            gender: str,
            genres: List[str],
            streaming_service_name: str,
            streaming_service_link: str,
            artist_name_aliases: List[str]
    ):
        name = name.lower()
        themes = [theme_.lower() for theme_ in themes]
        gender = gender.lower()
        genres = [genre_.lower() for genre_ in genres]
        streaming_service_name = streaming_service_name.lower()
        streaming_service_link = streaming_service_link.lower()
        artist_name_aliases = [alias.lower() for alias in artist_name_aliases]
        if self.get_by_name(name):
            error_print('Failed to add record. This artist already exists')
            return
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
        self._add_streaming_service_link(new_artist_id, streaming_service_name, streaming_service_link)
        self._add_artist_aliases(new_artist_id, artist_name_aliases)
        self._add_artist_genres(new_artist_id, genres)
        self._add_artist_themes(new_artist_id, themes)

