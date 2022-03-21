from typing import List, Tuple, Dict
from hiphop_bot.db.abstract_model import Model, ModelError, ModelUniqueViolationError
from hiphop_bot.base_models.model_object_class import BaseModelObject


class _ArtistsPairsProximityItem(BaseModelObject):
    def __init__(self, db_row_id: int, first_artist_name: str, second_artist_name: str, proximity: float):
        super().__init__(db_row_id)
        self.first_artist_name = first_artist_name
        self.second_artist_name = second_artist_name
        self.proximity = proximity

    def __str__(self):
        return f'ArtistPairsProximityItem {self.first_artist_name} {self.second_artist_name} {self.proximity}'

    def __repr__(self):
        return self.__str__()


class ArtistsPairsProximityModel(Model):
    def __init__(self):
        super().__init__('artist_pairs_proximity', _ArtistsPairsProximityItem)

        self._get_all_query = (
            "SELECT app.id, art1.name, art2.name, proximity "
            f"from {self._table_name} as app "
            f"inner join artist as art1 on app.first_artist_id = art1.id "
            f"inner join artist as art2 on app.second_artist_id = art2.id "
        )

    def get_by_artists_name(self, first_artist_name: str, second_artist_name: str) -> _ArtistsPairsProximityItem | None:
        query = self._get_all_query + f"where art1.name = '{first_artist_name}' and art2.name = '{second_artist_name}'"
        artists_pairs_proximity = self._select_model_objects(query)

        if len(artists_pairs_proximity) > 0:
            return artists_pairs_proximity[0]
        elif len(artists_pairs_proximity) == 0:
            return None
        else:
            raise ModelError('There is more than one record in the database with these names')

    def get_all(self) -> List[_ArtistsPairsProximityItem]:
        return super().get_all()

    def get_artists_proximity_dict(self) -> Dict[str, Dict[str, float]]:
        artists_proximity_dict = {}
        items = self.get_all()
        for item in items:
            first_artist = item.first_artist_name
            second_artist = item.second_artist_name
            proximity = item.proximity
            if first_artist in artists_proximity_dict:
                artists_proximity_dict[first_artist].update({second_artist: proximity})
            else:
                artists_proximity_dict[first_artist] = {second_artist: proximity}
        return artists_proximity_dict

    def add_record(self, first_artist_id: int, second_artist_id: int, proximity: float):
        query = (
            f'insert into {self._table_name} (first_artist_id, second_artist_id, proximity) '
            f"VALUES(%s, %s, %s);"
        )
        values = (first_artist_id, second_artist_id, proximity)

        added_records_number = self._insert(query, values)
        if added_records_number < 1:
            raise ModelError('Failed to add record')

    def update_proximity(self, first_artist_id: int, second_artist_id: int, proximity: float):
        query = (f"update {self._table_name} "
                 f"set proximity = {proximity} "
                 f"where first_artist_id={first_artist_id} and second_artist_id={second_artist_id} ")

        updated_records_number = self._update(query)
        if updated_records_number < 1:
            raise ModelError('Failed to add record')


