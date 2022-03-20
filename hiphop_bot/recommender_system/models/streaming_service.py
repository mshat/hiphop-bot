from typing import List, Tuple
from hiphop_bot.db.abstract_model import Model
from hiphop_bot.recommender_system.models.model_object_class import _ModelObject


class _StreamingService(_ModelObject):
    def __str__(self):
        return f'StreamingService {self.name}'

    def __repr__(self):
        return self.__str__()


class StreamingServiceModel(Model):
    def __init__(self):
        super().__init__('streaming_service', _StreamingService)

        self._get_all_query = (
            "SELECT id, name "
            f"from {self._table_name} "
        )

    def get_all(self) -> List[_StreamingService]:
        streaming_services = self._select_model_objects(self._get_all_query)
        return streaming_services

    def get_all_raw(self) -> List[Tuple[int, str]]:
        return super(StreamingServiceModel, self).get_all_raw()

    def get_streaming_services_names(self) -> List[str]:
        raw_data: List[Tuple[int, str]] = self.get_all_raw()
        names = [raw_artist[1] for raw_artist in raw_data]
        return names

    def get_by_name(self, name: str) -> _StreamingService | None:
        query = self._get_all_query + f"where name ='{name}'"
        streaming_services = self._select_model_objects(query)
        if len(streaming_services) > 0:
            return streaming_services[0]
        else:
            return None
