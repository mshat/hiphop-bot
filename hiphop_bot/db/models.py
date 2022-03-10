from hiphop_bot.db.model import Model


class ArtistModel(Model):
    def __init__(self):
        super().__init__('artist')

    def get_all(self):
        query = (
            "SELECT artist.name, year_of_birth, group_members_num, theme.name, gender.name, genre.name "
            f"from {self._table_name} "
            "inner join theme on artist.theme_id = theme.id "
            "inner join gender on artist.gender_id=gender.id "
            "inner join genre on artist.genre_id = genre.id"
        )
        artists = self._select(query)
        return artists


class GenreModel(Model):
    def __init__(self):
        super().__init__('genre')

    def get_all(self):
        query = (
            "SELECT name "
            f"from {self._table_name}"
        )
        genres = self._select(query)
        return genres


class GenderModel(Model):
    def __init__(self):
        super().__init__('gender')

    def get_all(self):
        query = (
            "SELECT name "
            f"from {self._table_name}"
        )
        genres = self._select(query)
        return genres


class ThemeModel(Model):
    def __init__(self):
        super().__init__('theme')

    def get_all(self):
        query = (
            "SELECT name "
            f"from {self._table_name}"
        )
        genres = self._select(query)
        return genres


class ArtistPairsProximityModel(Model):
    def __init__(self):
        super().__init__('artist_pairs_proximity')

    def get_all(self):
        query = (
            "SELECT art1.name, art2.name, proximity "
            f"from {self._table_name} "
            f"inner join artist as art1 on {self._table_name}.first_artist_id = art1.id "
            f"inner join artist as art2 on {self._table_name}.second_artist_id = art2.id "
        )
        genres = self._select(query)
        return genres