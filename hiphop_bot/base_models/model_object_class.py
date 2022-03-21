from abc import ABC, abstractmethod


class BaseModelObject(ABC):
    def __init__(self, db_row_id: int):
        self._db_row_id = db_row_id

    @property
    def id(self) -> int:
        return self._db_row_id

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class ModelObject(BaseModelObject, ABC):
    def __init__(self, db_row_id: int, name: str):
        super().__init__(db_row_id)
        self.name = name

