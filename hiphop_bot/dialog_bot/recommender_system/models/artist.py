from typing import List, Tuple
from hiphop_bot.db.model import Model
from hiphop_bot.dialog_bot.recommender_system.models.theme import Theme
from hiphop_bot.dialog_bot.recommender_system.models.gender import Gender
from hiphop_bot.dialog_bot.recommender_system.models.genre import Genre


class Artist:
    theme: Theme
    gender: Gender
    genre: Genre

    def __init__(
            self,
            name: str,
            year_of_birth: int,
            group_members_number: int,
            theme: Theme | str,
            gender: Gender | str,
            genre: Genre | str,
    ):
        self.name = name
        self.year_of_birth = year_of_birth
        self.group_members_number = group_members_number
        self._theme = theme if isinstance(theme, Theme) else Theme(theme)
        self._gender = gender if isinstance(gender, Gender) else Gender(gender)
        self._genre = genre if isinstance(genre, Genre) else Genre(genre)

    @property
    def theme(self):
        return self._theme.name

    @property
    def gender(self):
        return self._gender.name

    @property
    def genre(self):
        return self._genre.name

    def __str__(self):
        return f'{self.name} {self.year_of_birth} {self.group_members_number} {self._theme} {self._gender} ' \
               f'{self._genre}'

    def __repr__(self):
        return f'Artist: "{self.__str__()}"'


class ArtistModel(Model):
    def __init__(self):
        super().__init__('artist', Artist)

        self._get_all_query = (
            "SELECT artist.name, year_of_birth, group_members_num, theme.name, gender.name, genre.name "
            f"from {self._table_name} "
            "inner join theme on artist.theme_id = theme.id "
            "inner join gender on artist.gender_id = gender.id "
            "inner join genre on artist.genre_id = genre.id "
        )

    def get_all(self) -> List[Artist]:
        artists = self._select(self._get_all_query)
        return artists

    def get_all_raw(self) -> List[Tuple]:
        artists = self._raw_select(self._get_all_query)
        return artists

    def get_artist_names(self) -> List[str]:
        raw_data: List[Tuple] = self.get_all_raw()
        names = [raw_artist[0] for raw_artist in raw_data]
        return names

    def get_by_genre(self, genre) -> List[Artist] | List:
        query = self._get_all_query + \
                f"where genre.name = '{genre}'"
        artists = self._select(query)
        return artists