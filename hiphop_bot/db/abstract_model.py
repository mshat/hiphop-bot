from typing import Tuple, List, Callable
from abc import ABC, abstractmethod
from psycopg2 import errors
from hiphop_bot.db.connection_pool import Connection, CONNECTION_POOL
from hiphop_bot.dialog_bot.services.tools import debug_print


class ModelError(Exception): pass


class Model(ABC):
    def __init__(self, table_name, model_class: Callable):
        self._table_name = table_name
        self._check_if_table_exists()
        self._model_class = model_class

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

    def _raw_select(self, query) -> List[Tuple] | List:
        try:
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            connection.put_connection()
            return result
        except errors.UndefinedColumn as e:
            debug_print(f'[db error] {e}')
            return []
        except Exception as e:
            debug_print(f'[db unknown error] {e}')
            return []

    def _select_model_objects(self, query) -> List:
        raw_data = self._raw_select(query)
        objects = self._convert_to_objects(raw_data)
        return objects

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

    def _convert_to_objects(self, raw_data: List[Tuple], model_class: Callable = None) -> List:
        """
        Преобразует список кортежей в объекты классов, соответствующих модели
        """
        if model_class is None:
            model_class = self._model_class
        try:
            objects = []
            for init_arguments in raw_data:
                objects.append(model_class(*init_arguments))
            return objects
        except TypeError as e:
            raise ModelError(f'Conversion type error: {e}')
        except Exception as e:
            raise ModelError(f'Unknown conversion error: {e}')
