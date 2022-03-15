from __future__ import annotations
from hiphop_bot.dialog_bot.services.query_handling.query_handler import QueryHandler
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.services.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.services.query_handling.tag_condition import (AndTagCondition as And)


class RestartHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [And('restart')]
        self.debug_msg = 'Рестарт'

    def handle(self, query: Query, user: User, dialog: Dialog):
        dialog.output_message = 'Готово!'
        return DialogState.START