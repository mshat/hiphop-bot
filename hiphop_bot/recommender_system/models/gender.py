from typing import List
from hiphop_bot.db.abstract_model import Model
from hiphop_bot.base_models.model_object_class import ModelObject


class _Gender(ModelObject):
    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'Gender: "{self.__str__()}"'


class GenderModel(Model):
    def __init__(self):
        super().__init__('gender', _Gender)

        self._get_all_query = (
            "SELECT id, name "
            f"from {self._table_name} "
        )

    def get_all(self) -> List[_Gender]:
        return super(GenderModel, self).get_all()

    def get_by_name(self, name: str) -> _Gender | None:
        query = self._get_all_query + f"where gender.name = '{name}'"
        gender = self._select_model_objects(query)
        if len(gender) > 0:
            return gender[0]
        else:
            return None
