from typing import List

from hiphop_bot.db.model import Model


class ArtistPairsProximity:
    def __init__(self, first_artist: str, second_artist: str, proximity: float):
        self.first_artist = first_artist
        self.second_artist = second_artist
        self.proximity = proximity


class ArtistPairsProximityModel(Model):
    def __init__(self):
        super().__init__('artist_pairs_proximity')

    def get_all(self) -> List[ArtistPairsProximity]:
        raw_data = self.get_all_raw()
        artists_pairs_proximity = []
        for raw_artist in raw_data:
            artists_pairs_proximity.append(ArtistPairsProximity(*raw_artist))
        return artists_pairs_proximity

    def get_all_raw(self):
        query = (
            "SELECT art1.name, art2.name, proximity "
            f"from {self._table_name} "
            f"inner join artist as art1 on {self._table_name}.first_artist_id = art1.id "
            f"inner join artist as art2 on {self._table_name}.second_artist_id = art2.id "
        )
        genres = self._select(query)
        return genres