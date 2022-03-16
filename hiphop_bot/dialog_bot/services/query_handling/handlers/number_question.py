from __future__ import annotations
from hiphop_bot.dialog_bot.services.query_handling.query_handler import QueryHandler
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.services.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.models.const import SexFilter
from hiphop_bot.dialog_bot.services.query_handling.tag_condition import (AndTagCondition as And,
                                                                         OrTagCondition as Or,
                                                                         AndMultiTagCondition as AndMulti,
                                                                         OrMultiTagCondition as OrMulti)
from hiphop_bot.dialog_bot.services.query_handling.handling_tools import get_arguments_by_type


class NumberWithSexHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('number'), Or('how many')]
        self.required_argument_type = 'SexArgument'
        self.debug_msg = 'Количество артистов указанного пола в базе'

    def handle(self, query: Query, user: User, dialog: Dialog):
        sex = get_arguments_by_type(query, 'SexArgument')[0]
        artists = self._recommender_system.get_all_artists()
        artists = self._recommender_system.filter_artists(artists, sex=sex.value.value)
        if sex.value == SexFilter.MALE:
            dialog.output_message = f'В базе {len(artists)} исполнителя мужского пола'
        else:
            dialog.output_message = f'В базе {len(artists)} исполнитель женского пола'
        return DialogState.NUMBER


class NumberWithAgeRangeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [
            AndMulti([Or('number'), Or('how many')]),
            AndMulti([Or('range'), OrMulti([And('older'), And('younger')])])
        ]
        self.required_arguments = {'NumArgument': 2}
        self.debug_msg = 'Количество артистов от X до Y лет в базе'

    def handle(self, query: Query, user: User, dialog: Dialog):
        age = get_arguments_by_type(query, 'NumArgument')
        if len(age) >= 2:
            from_age, to_age = sorted([int(age[0].value), int(age[1].value)])
            dialog.debug_message = f'количество артистов от {from_age} до {to_age} лет'

            artists = self._recommender_system.get_all_artists()
            artists = self._recommender_system.filter_artists(artists, older=from_age, younger=to_age)

            dialog.output_message = f'Количество исполнителей от {from_age} до {to_age} лет: {len(artists)}'
        else:
            return dialog.state
        return DialogState.NUMBER


class NumberWithAgeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [AndMulti([Or('number'), Or('how many')]), AndMulti([Or('older'), Or('younger')])]
        self.required_argument_type = 'NumArgument'
        self.debug_msg = 'Количество артистов указанного возраста в базе'

    def handle(self, query: Query, user: User, dialog: Dialog):
        age = get_arguments_by_type(query, 'NumArgument')[0]
        age = int(age.value)

        artists = self._recommender_system.get_all_artists()

        if 'younger' in query.query_tag_structure:
            artists = self._recommender_system.filter_artists(artists, younger=age)
            dialog.output_message = f'Количество артистов до {age} лет: {len(artists)}'
        elif 'older' in query.query_tag_structure:
            artists = self._recommender_system.filter_artists(artists, older=age)
            dialog.output_message = f'Количество артистов от {age} лет: {len(artists)}'
        return DialogState.NUMBER


class NumberHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('number'), Or('how many')]
        self.debug_msg = 'Количество артистов в базе'

    def handle(self, query: Query, user: User, dialog: Dialog):
        artists = self._recommender_system.get_all_artists()
        dialog.output_message = f'В базе {len(artists)} исполнителя'
        return DialogState.NUMBER