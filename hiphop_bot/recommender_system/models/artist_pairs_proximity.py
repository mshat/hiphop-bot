from typing import List, Tuple, Dict
from hiphop_bot.db.abstract_model import Model, ModelError


class _ArtistPairsProximity:
    artists_proximity: Dict[str, Dict[str, float]]  # {artist1: {artist2: 0.3, artist3: 0.2}, artist2...}

    def __init__(self, raw_data: List[Tuple[int, str, str, float]]):
        self.artists_proximity = {}
        for first_artist, second_artist, proximity in raw_data:
            if first_artist in self.artists_proximity:
                self.artists_proximity[first_artist].update({second_artist: proximity})
            else:
                self.artists_proximity[first_artist] = {second_artist: proximity}

        self._pairs_len = len(raw_data)
        
    def get_proximity(self, first_artist: str, second_artist: str) -> float:
        try:
            return self.artists_proximity[first_artist][second_artist]
        except KeyError as e:
            raise Exception(f'Artist not found: {e}')

    def __str__(self):
        return f'ArtistPairsProximity: with {self._pairs_len} pairs'

    def __repr__(self):
        return self.__str__()


class ArtistPairsProximityModel(Model):
    def __init__(self):
        super().__init__('artist_pairs_proximity', _ArtistPairsProximity)

        self._get_all_query = (
            "SELECT art1.name, art2.name, proximity "
            f"from {self._table_name} "
            f"inner join artist as art1 on {self._table_name}.first_artist_id = art1.id "
            f"inner join artist as art2 on {self._table_name}.second_artist_id = art2.id "
        )

    def _convert_to_objects(self, raw_data: List[Tuple]) -> _ArtistPairsProximity:
        """
        Преобразует список кортежей в объект класса ArtistPairsProximity
        """
        try:
            object_ = self._model_class(raw_data)
            return object_
        except TypeError as e:
            raise ModelError(f'Conversion type error: {e}')
        except Exception as e:
            raise ModelError(f'Unknown conversion error: {e}')

    def _select_model_objects(self, query) -> _ArtistPairsProximity:
        raw_data = self._raw_select(query)
        objects = self._convert_to_objects(raw_data)
        return objects

    def get_all(self) -> _ArtistPairsProximity:
        genres = self._select_model_objects(self._get_all_query)
        return genres

    def get_all_raw(self):
        genres = self._raw_select(self._get_all_query)
        return genres
