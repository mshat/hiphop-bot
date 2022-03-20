from abc import ABC, abstractmethod


class _ModelObject(ABC):
    def __init__(self, db_row_id: int, name: str):
        self._db_row_id = db_row_id
        self.name = name

    @property
    def id(self) -> int:
        return self._db_row_id

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass