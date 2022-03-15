from __future__ import annotations
from hiphop_bot.dialog_bot.services.query_handling.query_handler import QueryHandler
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.services.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.models.data import GENRES
from hiphop_bot.dialog_bot.services.query_handling.tag_condition import (OrTagCondition as Or,
                                                                         AndMultiTagCondition as AndMulti)


class ShowAllGenresHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [AndMulti([Or('all'), Or('like/how')]), AndMulti([Or('include'), Or('genre'), Or('show')])]
        self.debug_msg = 'Вывести все жанры в базе'

    def handle(self, query: Query, user: User, dialog: Dialog):
        genres = set(GENRES.values())
        dialog.output_genres = genres
        dialog.output_message = 'Кстати, в фильтрах вы можете указывать название жанра на русском языке'
        return DialogState.START



