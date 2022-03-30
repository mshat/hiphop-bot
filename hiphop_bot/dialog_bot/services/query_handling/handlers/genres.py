from __future__ import annotations
from hiphop_bot.dialog_bot.services.query_handling.query_handler import QueryHandler
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.services.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.services.query_handling.tag_condition import (OrTagCondition as Or,
                                                                         AndMultiTagCondition as AndMulti,
                                                                         AndTagCondition as And)


class ShowAllGenresHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [And('genre'), AndMulti([Or('all'), Or('like/how'), Or('tree')])]
        self.debug_msg = 'Вывести все жанры в базе'

    def handle(self, query: Query, user: User, dialog: Dialog):
        genres_tree = """
Новая школа:
- Альтернатива
--- Эмо
--- Рэп-рок
- Электро
--- Клауд
--- Клубный
--- Дрилл
--- Грайм
--- Мамбл
--- Фонк
- Хардкор
--- Хорроркор
--- Рэпкор
--- Андеграунд
- Поп-рэп
--- Кальянный
--- Поп

Старая школа:
- Олдскул хардкор
--- Гангста
--- Спортивный
- Русский рэп
"""
        dialog.info = 'Дерево жанров русской хип-хоп музыки по моей версии:\n'
        dialog.info += f'{genres_tree}\n'
        return DialogState.START



