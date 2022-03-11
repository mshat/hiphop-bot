from typing import List
from hiphop_bot.db.model import Model


class Gender:
    def __init__(self, name: str):
        self.name = name


class GenderModel(Model):
    def __init__(self):
        super().__init__('gender', Gender)

        self._get_all_query = (
            "SELECT name "
            f"from {self._table_name}"
        )

    def get_all(self) -> List[Gender]:
        genres = self._select(self._get_all_query)
        return genres

    def get_all_raw(self):
        genres = self._raw_select(self._get_all_query)
        return genres