import enum
from typing import List

from hiphop_bot.db.model import Model


class Gender(enum.Enum):
    male = 'male'
    female = 'female'


class GenderModel(Model):
    def __init__(self):
        super().__init__('gender')

    def get_all(self) -> List[Gender]:
        raw_data = self.get_all_raw()
        genders = []
        for raw_artist in raw_data:
            genders.append(Gender(*raw_artist))
        return genders

    def get_all_raw(self):
        query = (
            "SELECT name "
            f"from {self._table_name}"
        )
        genres = self._select(query)
        return genres