from typing import List, Tuple
from hiphop_bot.db.abstract_model import Model


class _StreamingService:
    name: str

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'StreamingService {self.name}'

    def __repr__(self):
        return self.__str__()


class StreamingServiceModel(Model):
    def __init__(self):
        super().__init__('streaming_service', _StreamingService)

        self._get_all_query = (
            "SELECT name "
            f"from {self._table_name};"
        )

    def get_all(self) -> List[_StreamingService]:
        streaming_services = self._select_model_objects(self._get_all_query)
        return streaming_services

    def get_all_raw(self) -> List[Tuple]:
        return super(StreamingServiceModel, self).get_all_raw()

    def get_streaming_services_names(self) -> List[str]:
        raw_data: List[Tuple] = self.get_all_raw()
        names = [raw_artist[0] for raw_artist in raw_data]
        return names
