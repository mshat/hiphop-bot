from __future__ import annotations
from hiphop_bot.dialog_bot.services.query_handling.query_handler import QueryHandler
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.services.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.services.query_handling.tag_condition import (AndTagCondition as And,
                                                                         OrTagCondition as Or,
                                                                         AndNotTagCondition as AndNot,
                                                                         AndMultiTagCondition as AndMulti,
                                                                         OrMultiTagCondition as OrMulti)
from hiphop_bot.dialog_bot.services.query_handling.handling_tools import get_arguments_by_type


class SetOutputLenHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [
            OrMulti([Or('show'), Or('restrict')]),
            OrMulti([And('po'), AndMulti([Or('result'), Or('artist'), Or('line')])]),
            AndMulti([AndNot('range'), AndNot('older'), AndNot('younger')]),
        ]
        self.required_argument_type = 'NumArgument'
        self.debug_msg = 'Изменить количество выводимых результатов'

    def handle(self, query: Query, user: User, dialog: Dialog):
        output_len = get_arguments_by_type(query, 'NumArgument')[-1]

        user.max_output_len = int(output_len.value)

        dialog.info = f'Буду выводить по {output_len.value} строк'
        return DialogState.START


class RemoveFiltersHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [And('exclude'), AndMulti([Or('filter'), Or('restrict')])]
        self.debug_msg = 'Удалить все фильтры'

    def handle(self, query: Query, user: User, dialog: Dialog):
        user.set_all_filters_to_default()
        dialog.info = f'Все фильтры удалены'
        return DialogState.START
