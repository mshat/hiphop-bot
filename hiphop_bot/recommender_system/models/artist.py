from typing import List, Tuple
from datetime import datetime
from hiphop_bot.db.abstract_model import Model, ModelError, ModelUniqueViolationError
from hiphop_bot.recommender_system.models.theme import ThemeModel, _Theme  # импортирутеся для аннотации
from hiphop_bot.recommender_system.models.gender import GenderModel, _Gender  # импортирутеся для аннотации
from hiphop_bot.recommender_system.models.genre import GenreModel, _Genre  # импортирутеся для аннотации
from hiphop_bot.recommender_system.models.artist_streaming_service_link import (
    ArtistStreamingServiceLinkModel, _StreamingServiceLinks)
from hiphop_bot.recommender_system.models.model_object_class import _ModelObject


class _Artist(_ModelObject):
    theme: _Theme
    gender: _Gender
    genre: _Genre
    streaming_service_links: _StreamingServiceLinks | None

    def __init__(
            self,
            db_row_id: int,
            name: str,
            year_of_birth: int,
            group_members_number: int,
            theme: _Theme,
            gender: _Gender,
            genre: _Genre,
            streaming_service_links: _StreamingServiceLinks = None
    ):
        super().__init__(db_row_id, name)
        self.name = name
        self.year_of_birth = year_of_birth
        self.group_members_number = group_members_number
        self._theme = theme
        self._gender = gender
        self._genre = genre
        self._streaming_service_links = streaming_service_links

    @property
    def age(self):
        current_year = datetime.now().year
        return current_year - self.year_of_birth

    @property
    def theme(self):
        return self._theme.name

    @property
    def gender(self):
        return self._gender.name

    @property
    def genre(self):
        return self._genre.name

    @property
    def streaming_service_links(self):
        return self._streaming_service_links

    @streaming_service_links.setter
    def streaming_service_links(self, links: _StreamingServiceLinks):
        if isinstance(links, _StreamingServiceLinks):
            self._streaming_service_links = links
        else:
            raise ModelError("Argument must be of type _StreamingServiceLinks")

    def __str__(self):
        return f'{self.name} {self.year_of_birth} {self.group_members_number} {self._theme} {self._gender} ' \
               f'{self._genre} {self.streaming_service_links}'

    def __repr__(self):
        return f'Artist: "{self.__str__()}"'


class ArtistModel(Model):
    def __init__(self):
        super().__init__('artist', _Artist)

        self._get_all_query = (
            "SELECT artist.id, artist.name, year_of_birth, group_members_num, theme.name, gender.name, genre.name "
            f"from {self._table_name} "
            "inner join theme on artist.theme_id = theme.id "
            "inner join gender on artist.gender_id = gender.id "
            "inner join genre on artist.genre_id = genre.id "
        )

    def _select_model_objects(self, query) -> List[_Artist]:
        artists: List[_Artist] = super()._select_model_objects(query)

        streaming_service_link_model = ArtistStreamingServiceLinkModel()
        artist_links = streaming_service_link_model.get_artist_links_dict()

        # добавляем артистам ссылки на стриминговые сервисы
        for artist in artists:
            if artist.name in artist_links:
                artist.streaming_service_links = artist_links[artist.name]
        return artists

    def get_all(self) -> List[_Artist]:
        return super(ArtistModel, self).get_all()

    def get_artist_names(self) -> List[str]:
        raw_data: List[Tuple] = self.get_all_raw()
        names = [raw_artist[0] for raw_artist in raw_data]
        return names

    def get_by_genre(self, genre) -> List[_Artist] | List:
        query = self._get_all_query + f"where genre.name = '{genre}'"
        artists = self._select_model_objects(query)
        return artists

    def get_by_name(self, name) -> _Artist | None:
        query = self._get_all_query + f"where artist.name ='{name}'"
        artists = self._select_model_objects(query)
        if len(artists) > 0:
            return artists[0]
        else:
            return None

    def _add_streaming_service_link(self, artist_name: str, streaming_service_name: str, streaming_service_link: str):
        new_artist_id = self.get_by_name(artist_name).id
        streaming_service_link_model = ArtistStreamingServiceLinkModel()
        streaming_service_link_model.add_record(new_artist_id, streaming_service_name, streaming_service_link)

    def add_record(
            self,
            name: str,
            year_of_birth: int,
            group_members_num: int,
            theme: str,
            gender: str,
            genre: str,
            streaming_service_name: str,
            streaming_service_link: str,
    ):
        if self.get_by_name(name):
            raise ModelError('Failed to add record. This artist already exists')
        theme_model = ThemeModel()
        gender_model = GenderModel()
        genre_model = GenreModel()
        theme_obj: _Theme = theme_model.get_by_name(theme)
        gender_obj: _Gender = gender_model.get_by_name(gender)
        genre_obj: _Genre = genre_model.get_by_name(genre)

        if not (name and year_of_birth and group_members_num and theme_obj and gender_obj and genre_obj):
            raise ModelError('Чего-то не нашлось')

        query = (
            f'insert into {self._table_name} (name, year_of_birth, group_members_num, theme_id, gender_id, genre_id) '
            f"VALUES(%s, %s, %s, %s, %s, %s);"
        )
        values = (name, year_of_birth, group_members_num, theme_obj.id, gender_obj.id, genre_obj.id)

        try:
            added_records_number = self._insert(query, values)
            if added_records_number < 1:
                raise ModelError('Failed to add record')
        except ModelUniqueViolationError:
            pass

        self._add_streaming_service_link(name, streaming_service_name, streaming_service_link)
