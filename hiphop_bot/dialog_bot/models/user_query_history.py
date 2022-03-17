import datetime
from typing import List, Tuple, Dict
from hiphop_bot.db.abstract_model import Model, ModelUniqueViolationError, ModelError
from hiphop_bot.dialog_bot.services.tools.debug_print import debug_print
from hiphop_bot.dialog_bot.config import DEBUG_MODEL
from hiphop_bot.dialog_bot.models.tg_user import _TelegramUser, TelegramUserModel
from hiphop_bot.dialog_bot.services.query_solving.query_solver import QuerySolvingState


class _HistoryItem:
    def __init__(self, raw_query: str, query_solving_state: QuerySolvingState, datetime_, matched_handler: str):
        self.raw_query = raw_query
        self.query_solving_state = query_solving_state
        self.datetime_ = datetime_
        self.matched_handler = matched_handler

    def __str__(self):
        return f'Запрос: [{self.raw_query}] ' \
               f'Результат распознавания {self.query_solving_state}. Handler {self.matched_handler}. {self.datetime_}'

    def __repr__(self):
        return self.__str__()


class _UserQueryHistory:
    def __init__(self, tg_user: _TelegramUser, history: List[_HistoryItem]):
        self.tg_user = tg_user
        self.history = history

    def __str__(self):
        return f'UserQueryHistory: {self.tg_user} {self.history}'

    def __repr__(self):
        return self.__str__()


class UserQueryHistoryModel(Model):
    def __init__(self):
        super().__init__('user_history', _UserQueryHistory)

        self._get_all_query = (
            "select u.user_id, qss.state, query, query_time, matched_handler "
            f"from {self._table_name} as h "
            "inner join tg_user as u on h.user_id = u.id "
            "inner join query_solving_state as qss on h.query_solving_state_id = qss.id "
        )

    def _select_model_objects(self, query) -> List[_UserQueryHistory]:
        raw_data = self._raw_select(query)
        if not raw_data:
            return []

        tg_user_model = TelegramUserModel()
        tg_users = tg_user_model.get_all()

        # словарь с ключами user_id и значениям _TelegramUser
        tg_users_dict = {}
        for user in tg_users:
            tg_users_dict[user.user_id] = user

        raw_user_query_history_items: Dict[int, Tuple[_TelegramUser, List[_HistoryItem]]] = {}
        # добавляем тг юзеров в _UserQueryHistory объекты
        for raw_user_history_item in raw_data:
            user_id = raw_user_history_item[0]
            state = raw_user_history_item[1]
            state = QuerySolvingState.SOLVED if state == 'solved' else QuerySolvingState.UNSOLVED
            user_query = raw_user_history_item[2]
            datetime_ = raw_user_history_item[3]
            matched_handler = raw_user_history_item[4]

            tg_user = tg_users_dict[user_id]
            history_item = _HistoryItem(user_query, state, datetime_, matched_handler)
            if user_id in raw_user_query_history_items:
                raw_user_query_history_items[user_id][1].append(history_item)
            else:
                raw_user_query_history_items[user_id] = (tg_user, [history_item])

        objects = self._convert_to_objects(list(raw_user_query_history_items.values()))
        return objects

    def get_all(self) -> List[_UserQueryHistory]:
        return super().get_all()

    def add_record(
            self,
            tg_user: _TelegramUser,
            query_solving_state: QuerySolvingState,
            user_query: str,
            matched_handler: str | None,
            query_time: datetime.datetime = None):
        query_time = query_time if query_time else datetime.datetime.now()
        query = (
            f'insert into {self._table_name} (user_id, query_solving_state_id, query, query_time, matched_handler) '
            f"VALUES(%s, %s, %s, %s, %s);"
        )
        query_solving_state = 0 if query_solving_state == QuerySolvingState.SOLVED else 1
        values = (tg_user.db_row_id, query_solving_state, user_query, query_time, matched_handler)

        try:
            added_records_number = self._insert(query, values)
            if added_records_number < 1:
                raise ModelError('Failed to add record')
            debug_print(DEBUG_MODEL, f'[MODEL] Добавил {added_records_number} запись в таблицу {self._table_name}')
        except ModelUniqueViolationError:
            pass

    def get_all_unresolved_queries(self) -> List[_UserQueryHistory]:
        query = self._get_all_query + "where qss.state = 'unsolved'"
        objects = self._select_model_objects(query)
        return objects

    def get_user_history(self, tg_user: _TelegramUser) -> List[_UserQueryHistory]:
        query = self._get_all_query + f'where u.user_id = {tg_user.user_id}'
        objects = self._select_model_objects(query)
        return objects
