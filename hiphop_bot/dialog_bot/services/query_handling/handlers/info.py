from __future__ import annotations
from hiphop_bot.dialog_bot.services.query_handling.query_handler import QueryHandler
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.services.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.services.query_handling.tag_condition import (AndTagCondition as And,
                                                                         OrTagCondition as Or,
                                                                         AndNotTagCondition as AndNot,
                                                                         AndMultiTagCondition as AndMulti)
from hiphop_bot.dialog_bot.services.query_handling.handling_tools import get_arguments_by_type
from hiphop_bot.dialog_bot.models import const


class InfoHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('talk about'), Or('about'), Or('info')]
        self.required_argument_type = 'ArtistArgument'
        self.debug_msg = 'Информация об артисте'

    def handle(self, query: Query, user: User, dialog: Dialog):
        artist_arg = get_arguments_by_type(query, 'ArtistArgument')[0]
        artist = self._recommender_system.get_artist_by_name(artist_arg.value)
        if not artist:
            dialog.info = 'Артист не найден :('
        else:
            sex = "мужской" if artist.gender == "male" else "женский"
            if artist.group_members_number == 1:
                dialog.info = f'Артист {artist.name}'
            elif artist.group_members_number == 2:
                dialog.info = f'Дуэт {artist.name}'
            else:
                dialog.info = f'Группа {artist.name}'
            if artist.group_members_number > 1:
                dialog.info = f'Возраст фронтмэна: {artist.age}\n'
                dialog.info += f'Пол фронтмэна: {sex}\n'
                dialog.info += f'Количество участников: {artist.group_members_number}\n'
            else:
                dialog.info = f'Возраст: {artist.age}\n'
                dialog.info += f'Пол: {sex}'

        return DialogState.INFO


class InfoAboutBotHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('you'), Or('who'), AndNot('opportunities')]
        self.debug_msg = 'Информация о боте'

    def handle(self, query: Query, user: User, dialog: Dialog):
        dialog.debug_message = 'Информация о боте'
        dialog.info = 'Я - ваш помощник в мире русского хипхопа'
        return DialogState.INFO


class InfoAboutBotOpportunitiesHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('opportunities')]
        self.debug_msg = 'Информация о возможностях бота'

    def handle(self, query: Query, user: User, dialog: Dialog):
        dialog.debug_message = 'Возможности бота'
        dialog.info = const.BOT_OPPORTUNITIES
        return DialogState.INFO


class InfoAboutBotAlgorithmHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [AndMulti([Or('talk about'), Or('like/how')]), And('you'), And('algorithm')]
        self.debug_msg = 'Информация об устройстве бота'

    def handle(self, query: Query, user: User, dialog: Dialog):
        dialog.debug_message = 'Алгоритм бота'
        dialog.info = const.BOT_ALGORITHM
        return DialogState.INFO