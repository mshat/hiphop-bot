import os
import psycopg2
from typing import Callable
from abc import ABC
from psycopg2 import pool
from hiphop_bot.dialog_bot.services.tools.randomword import randomword
from hiphop_bot.dialog_bot.services.tools.debug_print import debug_message, debug_print
from hiphop_bot.dialog_bot.config import DEBUG_DB, DEBUG
from dotenv import dotenv_values


if 'MODE' in os.environ:
    debug_print(DEBUG, f'[INFO] ENV MODE: {os.environ["MODE"]}')
    if os.environ['MODE'] == 'docker':
        DB_USER = os.environ['DB_USER']
        DB_PASSWORD = os.environ['DB_PASSWORD']
        DB_HOST = os.environ['DB_HOST']
        DB_PORT = os.environ['DB_PORT']
        DB_NAME = os.environ['DB_NAME']
    elif os.environ['MODE'] == 'heroku':
        DB_USER = os.environ['HEROKU_DB_USER']
        DB_PASSWORD = os.environ['HEROKU_DB_PASSWORD']
        DB_HOST = os.environ['HEROKU_DB_HOST']
        DB_PORT = os.environ['HEROKU_DB_PORT']
        DB_NAME = os.environ['HEROKU_DB_NAME']
    else:
        raise Exception('DB environ values error!')
else:
    debug_print(DEBUG, f'[INFO] No key "MODE" in env')
    current_dir = os.path.dirname(os.path.realpath(__file__))
    ENV = dotenv_values(f"{current_dir}/../env")
    if ENV['MODE'] == 'local':
        DB_USER = ENV['DB_USER']
        DB_PASSWORD = ENV['DB_PASSWORD']
        DB_HOST = ENV['DB_HOST']
        DB_PORT = ENV['DB_PORT']
        DB_NAME = ENV['DB_NAME']
    elif ENV['MODE'] == 'heroku_local':
        DB_USER = ENV['HEROKU_DB_USER']
        DB_PASSWORD = ENV['HEROKU_DB_PASSWORD']
        DB_HOST = ENV['HEROKU_DB_HOST']
        DB_PORT = ENV['HEROKU_DB_PORT']
        DB_NAME = ENV['HEROKU_DB_NAME']
    else:
        raise Exception('DB environ values error!')
debug_print(DEBUG, f'[INFO] db settings: {DB_USER} {DB_NAME} {DB_HOST}')


class Connection:
    def __init__(self, conn, pool_):
        self.conn = conn
        self._pool = pool_
        self._closed = False
        self._name = randomword(6)

        debug_print(DEBUG_DB, f"[DB] Cоединение {self._name} создано")

    def put_connection(self):
        if self.conn:
            self._pool.putconn(self.conn)
            self._closed = True

        debug_print(DEBUG_DB, f"[DB] Cоединение {self._name} вернулось в пул")

    def cursor(self):
        return self.conn.cursor()

    def __del__(self):
        if not self._closed:
            self.put_connection()


class ConnectionPoolError(Exception): pass


class AbstractConnectionPool(ABC):
    def __init__(self, connection_pool_class: Callable, minconn: int = 1, maxconn: int = 10):
        self.pool = None
        try:
            self.pool = connection_pool_class(minconn, maxconn, user=DB_USER, password=DB_PASSWORD, host=DB_HOST,
                                              port=DB_PORT, database=DB_NAME)
        except psycopg2.DatabaseError as error:
            raise ConnectionPoolError(f"Ошибка при подключении к БД: {error}")
        else:
            debug_print(DEBUG_DB, '[DB] Пул соединений создан')

    def get_connection(self):
        return Connection(self.pool.getconn(), self.pool)

    @debug_message(DEBUG_DB, "[DB] Пул соединений БД закрыт")
    def __del__(self):
        if self.pool:
            self.pool.closeall()


class SimpleConnectionPool(AbstractConnectionPool):
    def __init__(self, minconn: int = 1, maxconn: int = 10):
        super().__init__(psycopg2.pool.SimpleConnectionPool, minconn, maxconn)


class ThreadedConnectionPool(AbstractConnectionPool):
    def __init__(self, minconn: int = 1, maxconn: int = 10):
        super().__init__(psycopg2.pool.ThreadedConnectionPool, minconn, maxconn)


CONNECTION_POOL = ThreadedConnectionPool()
