from typing import List, Tuple, Dict, Iterable
from hiphop_bot.base_models.abstract_model import Model, ModelError, DeleteError
from hiphop_bot.base_models.model_object_class import BaseModelObject
from psycopg2 import errors
from hiphop_bot.dialog_bot.services.tools.debug_print import error_print, debug_print
from hiphop_bot.dialog_bot.config import DEBUG_MODEL


class Proximity:
    general_proximity: float
    proximities: List[float]

    def __init__(self, general_proximity: float, proximities: List[float]):
        self.general_proximity = general_proximity
        self.proximities = proximities


class _ArtistsPairsProximityItem(BaseModelObject):
    def __init__(
            self,
            db_row_id: int,
            first_artist_name: str,
            second_artist_name: str,
            general_proximity: float,
            proximities: List[float]):
        super().__init__(db_row_id)
        self.first_artist_name = first_artist_name
        self.second_artist_name = second_artist_name
        self.proximity = Proximity(general_proximity, proximities)

    def __str__(self):
        return f'ArtistPairsProximityItem {self.first_artist_name} {self.second_artist_name} {self.proximity}'

    def __repr__(self):
        return self.__str__()


class ArtistsPairsProximityModel(Model):
    def __init__(self):
        super().__init__('artist_pairs_proximity', _ArtistsPairsProximityItem)

        self._get_all_query = (
            "SELECT app.id, art1.name, art2.name, proximity, proximities "
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

    def get_by_first_artist_name(self, first_artist_name: str) -> List[_ArtistsPairsProximityItem] | None:
        query = self._get_all_query + f"where art1.name = '{first_artist_name}'"
        artists_pairs_proximity = self._select_model_objects(query)

        if len(artists_pairs_proximity) > 0:
            return artists_pairs_proximity
        elif len(artists_pairs_proximity) == 0:
            return None

    def get_all(self) -> List[_ArtistsPairsProximityItem]:
        return super().get_all()

    def get_artists_proximity_dict(self) -> Dict[str, Dict[str, Proximity]]:
        artists_proximity_dict = {}
        items = self.get_all()
        for item in items:
            first_artist = item.first_artist_name
            second_artist = item.second_artist_name
            general_proximity = item.proximity
            if first_artist in artists_proximity_dict:
                artists_proximity_dict[first_artist].update({second_artist: general_proximity})
            else:
                artists_proximity_dict[first_artist] = {second_artist: general_proximity}
        return artists_proximity_dict

    def _convert_proximities_list_to_db_array(self, proximities: Iterable[float]) -> str:
        return '{' + ','.join(map(str, proximities)) + '}'

    def add_record(self, first_artist_id: int, second_artist_id: int, proximity: float, proximities: List[float]):
        query = (
            f'insert into {self._table_name} (first_artist_id, second_artist_id, proximity, proximities) '
            f"VALUES(%s, %s, %s, %s);"
        )
        values = (first_artist_id, second_artist_id, proximity, self._convert_proximities_list_to_db_array(proximities))

        added_records_number = self._insert(query, values)
        if added_records_number < 1:
            raise ModelError('Failed to add record')

    def update_proximity(self, first_artist_id: int, second_artist_id: int, proximity: float, proximities: List[float]):
        query = (f"update {self._table_name} "
                 f"set proximity={proximity}, proximities={self._convert_proximities_list_to_db_array(proximities)} "
                 f"where first_artist_id={first_artist_id} and second_artist_id={second_artist_id} ")

        updated_records_number = self._update(query)
        if updated_records_number < 1:
            raise ModelError('Failed to add record')

    def update_multiple_proximities(self, new_artists_pairs_proximity: List[Tuple[int, int, float, List[float]]]):
        connection = self._get_connection()
        cursor = connection.cursor()

        for item in new_artists_pairs_proximity:
            first_artist_id = item[0]
            second_artist_id = item[1]
            proximity = item[2]
            proximities = item[3]

            proximities_ = self._convert_proximities_list_to_db_array(proximities)
            query = (f"update {self._table_name} "
                     f"set proximity={proximity}, proximities='{proximities_}' "
                     f"where first_artist_id={first_artist_id} and second_artist_id={second_artist_id} ")
            try:
                cursor.execute(query)
            except errors.UndefinedColumn as e:
                error_print(f'[db UndefinedColumn] {e}')
            except Exception as e:
                error_print(f'[db unknown error] {e}')

        connection.conn.commit()
        added_records_number = cursor.rowcount
        cursor.close()
        connection.put_connection()
        debug_print(DEBUG_MODEL, f'[MODEL] Обновил {added_records_number} запись в таблице {self._table_name}')

    def delete(self, id_: int, cursor) -> int:
        try:
            return self._raw_delete(
                f"delete from {self._table_name} where first_artist_id = %s or second_artist_id = %s;", (id_, id_), cursor)
        except DeleteError as e:
            raise DeleteError(f'Не смог удалить запись c id {id_} из таблицы {self._table_name}. {e}')
