from typing import Tuple, List
from abc import ABC, abstractmethod
from hiphop_bot.db.connection_pool import Connection, CONNECTION_POOL


class ModelError(Exception): pass


class Model(ABC):
    def __init__(self, table_name):
        self._table_name = table_name
        self._check_if_table_exists()

    def _check_if_table_exists(self):
        test_conn = self._get_connection()
        cursor = test_conn.cursor()
        cursor.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'public'""")
        tables = cursor.fetchall()
        tables = [table[0] for table in tables]
        cursor.close()
        test_conn.put_connection()

        if self._table_name not in tables:
            raise ModelError('This table does not exist in the database')

    def _get_connection(self) -> Connection:
        connection = CONNECTION_POOL.get_connection()
        return connection

    def _select(self, query):
        connection = self._get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.put_connection()
        return result

    @abstractmethod
    def get_all_raw(self) -> List[Tuple]:
        """
        Возвращает все записи из таблицы в виде списка кортежей
        """
        pass

    @abstractmethod
    def get_all(self) -> List:
        """
        Возвращает все записи из таблицы в виде списка объектов
        """
        pass
