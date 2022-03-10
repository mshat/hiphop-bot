from typing import List

from hiphop_bot.db.model import Model
from hiphop_bot.dialog_bot.recommender_system.models.theme import Theme
from hiphop_bot.dialog_bot.recommender_system.models.gender import Gender
from hiphop_bot.dialog_bot.recommender_system.models.genre import Genre


class Artist:
    def __init__(
            self,
            name: str,
            year_of_birth: int,
            group_members_num: int,
            theme: Theme,
            gender: Gender,
            genre: Genre,
    ):
        self.name = name
        self.year_of_birth = year_of_birth
        self.group_members_num = group_members_num
        self.theme = theme
        self.gender = gender
        self.genre = genre

    def __str__(self):
        return f'{self.name} {self.year_of_birth} {self.group_members_num} {self.theme} {self.gender} {self.genre}'

    def __repr__(self):
        return f'Artist: "{self.__str__()}"'


class ArtistModel(Model):
    def __init__(self):
        super().__init__('artist')

    def get_all(self) -> List[Artist]:
        raw_artists = self.get_all_raw()
        artists = []
        for raw_artist in raw_artists:
            artists.append(Artist(*raw_artist))
        return artists

    def get_all_raw(self):
        query = (
            "SELECT artist.name, year_of_birth, group_members_num, theme.name, gender.name, genre.name "
            f"from {self._table_name} "
            "inner join theme on artist.theme_id = theme.id "
            "inner join gender on artist.gender_id=gender.id "
            "inner join genre on artist.genre_id = genre.id"
        )
        artists = self._select(query)
        return artists