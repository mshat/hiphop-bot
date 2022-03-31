from abc import ABC
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.services.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.models.const import SexFilter, GroupTypeFilter
from hiphop_bot.dialog_bot.services.query_handling.tag_condition import (AndTagCondition as And,
                                                                         OrTagCondition as Or,
                                                                         AndNotTagCondition as AndNot,
                                                                         AndMultiTagCondition as AndMulti,
                                                                         OrMultiTagCondition as OrMulti)
from hiphop_bot.dialog_bot.services.query_handling.handling_tools import get_arguments_by_type
from hiphop_bot.dialog_bot.services.query_handling.query_handler import QueryHandler


class FilterQueryHandler(QueryHandler, ABC):
    def __init__(self):
        super().__init__()
        self._next_state = DialogState.FILTER


class FilterBySexIncludeHandler(FilterQueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = []  # срабатывает по аргументу пола, без доп условий
        self.required_argument_type = 'SexArgument'
        self.debug_msg = 'Фильтр по полу "включить"'

    def handle(self, query: Query, user: User, dialog: Dialog):
        sex = get_arguments_by_type(query, 'SexArgument')[0]
        dialog.debug_message = f'Убрать всех, кроме {sex.value.value} пола'

        user.add_sex_filter(sex.value)
        return self._next_state


class FilterBySexExcludeHandler(FilterQueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('exclude'), AndNot('except')]
        self.required_argument_type = 'SexArgument'
        self.debug_msg = 'Фильтр по полу "исключить"'

    def handle(self, query: Query, user: User, dialog: Dialog):
        sex_arg = get_arguments_by_type(query, 'SexArgument')[0]
        dialog.debug_message = f'Убрать артистов {sex_arg.value} пола'

        sex = SexFilter.MALE if sex_arg.value == SexFilter.FEMALE else SexFilter.FEMALE
        user.add_sex_filter(sex)
        return self._next_state


class FilterByAgeRangeHandler(FilterQueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('range'), OrMulti([And('older'), And('younger')])]
        self.required_arguments = {'NumArgument': 2}
        self.debug_msg = 'Фильтр по возрасту в диапазоне'

    def handle(self, query: Query, user: User, dialog: Dialog):
        age = get_arguments_by_type(query, 'NumArgument')
        if len(age) >= 2:
            from_age, to_age = sorted([int(age[0].value), int(age[1].value)])
            dialog.debug_message = f'фильтр от {from_age} до {to_age} лет'

            user.older_filter = from_age
            user.younger_filter = to_age

        return self._next_state


class FilterByAgeIncludeHandler(FilterQueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [AndMulti([Or('older'), Or('younger')])]
        self.required_argument_type = 'NumArgument'
        self.debug_msg = 'Фильтр по возрасту "включить"'

    def handle(self, query: Query, user: User, dialog: Dialog):
        age = get_arguments_by_type(query, 'NumArgument')[0]
        age = int(age.value)
        if 'younger' in query.query_tag_structure:
            dialog.debug_message = f'фильтр до {age} лет'
            user.younger_filter = age
        elif 'older' in query.query_tag_structure:
            dialog.debug_message = f'фильтр от {age} лет'
            user.older_filter = age
        return self._next_state


class FilterByAgeExcludeHandler(FilterQueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [And('exclude'), AndMulti([Or('older'), Or('younger')])]
        self.required_argument_type = 'NumArgument'
        self.debug_msg = 'Фильтр по возрасту "исключить"'

    def handle(self, query: Query, user: User, dialog: Dialog):
        age = get_arguments_by_type(query, 'NumArgument')[0]
        age = int(age.value)
        if 'younger' in query.query_tag_structure:
            dialog.debug_message = f'фильтр от {age} лет'
            user.older_filter = age
        elif 'older' in query.query_tag_structure:
            dialog.debug_message = f'фильтр до {age} лет'
            user.younger_filter = age
        return self._next_state


class FilterByMembersCountHandler(FilterQueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('group'), Or('solo'), Or('duet')]
        self.debug_msg = 'Фильтр по количеству участников коллектива'

    def handle(self, query: Query, user: User, dialog: Dialog):
        tags = query.query_tag_structure
        if 'group' in tags:
            user.group_type_filter = GroupTypeFilter.GROUP
        elif 'solo' in tags:
            user.group_type_filter = GroupTypeFilter.SOLO
        elif 'duet' in tags:
            user.group_type_filter = GroupTypeFilter.DUET
        else:
            return self._next_state

        dialog.debug_message = f'оставить {user.group_type_filter}'
        return self._next_state


class RemoveResultLenFilterHandler(FilterQueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [
            OrMulti([And('exclude'), And('number')]),
            OrMulti([AndMulti([Or('show'), Or('include')]), And('all')])
            ]
        self.debug_msg = 'Удалить ограничение количества выводимых строк'

    def handle(self, query: Query, user: User, dialog: Dialog):
        user.max_output_len = 1000

        return self._next_state


class RemoveFiltersHandler(FilterQueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [And('exclude'), AndMulti([Or('filter'), Or('restrict')])]
        self.debug_msg = 'Удалить все фильтры'

    def handle(self, query: Query, user: User, dialog: Dialog):
        user.reset_filters()
        return self._next_state


class FilterOutputLenHandler(FilterQueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [
            OrMulti([Or('show'), Or('restrict')]),
            OrMulti([And('po'), AndMulti([Or('result'), Or('artist'), Or('line')])])
        ]
        self.required_argument_type = 'NumArgument'
        self.debug_msg = 'Фильтр по количеству выводимых результатов'

    def handle(self, query: Query, user: User, dialog: Dialog):
        output_len = get_arguments_by_type(query, 'NumArgument')[-1]

        user.max_output_len = int(output_len.value)
        return self._next_state