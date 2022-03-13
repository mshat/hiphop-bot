from typing import List, Tuple
from hiphop_bot.db.model import Model, ModelError
from hiphop_bot.recommender_system.models.theme import _Theme  # импортирутеся для аннотации
from hiphop_bot.recommender_system.models.gender import _Gender  # импортирутеся для аннотации
from hiphop_bot.recommender_system.models.genre import _Genre  # импортирутеся для аннотации
from hiphop_bot.recommender_system.models.artist_streaming_service_link import (
    ArtistStreamingServiceLinkModel, _StreamingServiceLinks)


class _Artist:
    theme: _Theme
    gender: _Gender
    genre: _Genre
    streaming_service_links: _StreamingServiceLinks | None

    def __init__(
            self,
            name: str,
            year_of_birth: int,
            group_members_number: int,
            theme: _Theme | str,
            gender: _Gender | str,
            genre: _Genre | str,
            streaming_service_links: _StreamingServiceLinks = None,
    ):
        self.name = name
        self.year_of_birth = year_of_birth
        self.group_members_number = group_members_number
        self._theme = theme if isinstance(theme, _Theme) else _Theme(theme)
        self._gender = gender if isinstance(gender, _Gender) else _Gender(gender)
        self._genre = genre if isinstance(genre, _Genre) else _Genre(genre)
        self._streaming_service_links = streaming_service_links

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
            raise ModelError("Argument must have _StreamingServiceLinks type")

    def __str__(self):
        return f'{self.name} {self.year_of_birth} {self.group_members_number} {self._theme} {self._gender} ' \
               f'{self._genre} {self.streaming_service_links}'

    def __repr__(self):
        return f'Artist: "{self.__str__()}"'


class ArtistModel(Model):
    def __init__(self):
        super().__init__('artist', _Artist)

        self._get_all_query = (
            "SELECT artist.name, year_of_birth, group_members_num, theme.name, gender.name, genre.name "
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
        artists = self._select_model_objects(self._get_all_query)
        return artists

    def get_all_raw(self) -> List[Tuple]:
        artists = self._raw_select(self._get_all_query)
        return artists

    def get_artist_names(self) -> List[str]:
        raw_data: List[Tuple] = self.get_all_raw()
        names = [raw_artist[0] for raw_artist in raw_data]
        return names

    def get_by_genre(self, genre) -> List[_Artist] | List:
        query = self._get_all_query + \
                f"where genre.name = '{genre}'"
        artists = self._select_model_objects(query)
        return artists
