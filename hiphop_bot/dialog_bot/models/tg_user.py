from typing import List
from hiphop_bot.db.abstract_model import Model, ModelUniqueViolationError, ModelError


class _TelegramUser:
    def __init__(self, db_row_id: int, user_id: int, first_name: str, last_name: str, username: str):
        self.db_row_id = db_row_id
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'TelegramUser: {self.user_id, self.full_name, self.username}'

    def __repr__(self):
        return self.__str__()


class TelegramUserModel(Model):
    def __init__(self):
        super().__init__('tg_user', _TelegramUser)

        self._get_all_query = (
            "SELECT id, user_id, first_name, last_name, username "
            f"from {self._table_name}"
        )

    def get_all(self) -> List[_TelegramUser]:
        return super().get_all()

    def get_by_user_id(self, user_id: int) -> _TelegramUser | None:
        query = self._get_all_query + f' where user_id = {user_id}'
        res = self._select_model_objects(query)
        if res:
            return res[0]
        else:
            return None

    def add_record(self, user_id: int, first_name: str, last_name: str, username: str):
        query = (
            f'insert into {self._table_name} (user_id, first_name, last_name, username) '
            f"VALUES(%s, %s, %s, %s);"
        )
        values = (user_id, first_name, last_name, username)

        try:
            added_records_number = self._insert(query, values)
            if added_records_number < 1:
                raise ModelError('Failed to add record')
        except ModelUniqueViolationError:
            pass

