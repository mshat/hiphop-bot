from typing import List
from hiphop_bot.base_models.abstract_model import Model
from hiphop_bot.base_models.model_object_class import ModelObject


class _Genre(ModelObject):
    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'Genre: "{self.__str__()}"'


class GenreModel(Model):
    def __init__(self):
        super().__init__('genre', _Genre)

        self._get_all_query = (
            "SELECT id, name "
            f"from {self._table_name} "
        )

    def get_all(self) -> List[_Genre]:
        return super(GenreModel, self).get_all()

    def get_by_name(self, name: str) -> _Genre | None:
        query = self._get_all_query + f"where name = '{name}'"
        genre = self._select_model_objects(query)
        if len(genre) > 0:
            return genre[0]
        else:
            return None

    def get_by_id(self, genre_id: int) -> _Genre | None:
        query = self._get_all_query + f"where id = {genre_id}"
        genre = self._select_model_objects(query)
        if len(genre) > 0:
            return genre[0]
        else:
            return None
