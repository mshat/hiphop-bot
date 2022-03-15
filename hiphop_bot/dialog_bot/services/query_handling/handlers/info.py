from __future__ import annotations
from hiphop_bot.dialog_bot.services.query_handling.query_handler import QueryHandler
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.recommender_system import interface
from hiphop_bot.dialog_bot.services.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.services.query_handling.tag_condition import (AndTagCondition as And,
                                                                         OrTagCondition as Or,
                                                                         AndNotTagCondition as AndNot,
                                                                         AndMultiTagCondition as AndMulti)
from hiphop_bot.dialog_bot.services.query_handling.handling_tools import get_arguments_by_type


class InfoHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('talk about'), Or('about'), Or('info')]
        self.required_argument_type = 'ArtistArgument'
        self.debug_msg = 'Информация об артисте'

    def handle(self, query: Query, user: User, dialog: Dialog):
        artist_arg = get_arguments_by_type(query, 'ArtistArgument')[0]
        artist = interface.get_artist_by_name(artist_arg.value)
        if not artist:
            dialog.output_message = 'Артист не найден :('
        else:
            sex = "мужской" if artist.gender == "male" else "женский"
            if artist.group_members_number == 1:
                dialog.output_message = f'Артист {artist.name}'
            elif artist.group_members_number == 2:
                dialog.output_message = f'Дуэт {artist.name}'
            else:
                dialog.output_message = f'Группа {artist.name}'
            if artist.group_members_number > 1:
                dialog.output_message = f'Возраст фронтмэна: {artist.age}\n'
                dialog.output_message += f'Пол фронтмэна: {sex}\n'
                dialog.output_message += f'Количество участников: {artist.group_members_number}\n'
            else:
                dialog.output_message = f'Возраст: {artist.age}\n'
                dialog.output_message += f'Пол: {sex}'

        return DialogState.INFO


class InfoAboutBotHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('you'), Or('who'), AndNot('opportunities')]
        self.debug_msg = 'Информация о боте'

    def handle(self, query: Query, user: User, dialog: Dialog):
        dialog.debug_message = 'Информация о боте'
        dialog.output_message = 'Я - ваш помощник в мире русского хипхопа. Меня сделал Шатохин Максим, ИУ7-12М'
        return DialogState.INFO


class InfoAboutBotOpportunitiesHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('opportunities')]
        self.debug_msg = 'Информация о возможностях бота'

    def handle(self, query: Query, user: User, dialog: Dialog):
        dialog.debug_message = 'Возможности бота'
        dialog.output_message = """Вы можете в свободной форме задавать мне вопросы или поручать команды.

Я могу:

1. Подобрать список музкантов, похожих на того, кого вы назовёте
2. Порекомендовать музыкантов по вашим предпочтениям
3. Вывести информацию о музыканте
4. Вывести музкантов в заданном жанре, заданного пола или возраста. 

Я могу отфильтровать результат поиска по количеству участников коллектива.
Например, оставить только соло артистов, дуэты или группы.
А так же по полу, возрасту (старше или младше N лет)

Вы можете ограничить количество выводимых результатов, 
просто попросите меня выводить по N артистов.

Вы можете удалить все наложенные фильтры, попросив меня об этом.

Я могу вывести список всех артистов или жанров, которые знаю.

Чтобы подобрать музкантов по вашим предпочтениям, попросите меня подобрать то, что вам понравится.
"""
        return DialogState.INFO


class InfoAboutBotAlgorithmHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [AndMulti([Or('talk about'), Or('like/how')]), And('you'), And('algorithm')]
        self.debug_msg = 'Информация об устройстве бота'

    def handle(self, query: Query, user: User, dialog: Dialog):
        dialog.debug_message = 'Алгоритм бота'
        dialog.output_message = """Я работаю следующим образом:
Вначале, когда я получаю от вас текстовое сообщение, я удаляю из него лишние пробелы и запятые.
Затем в полученном предложении происходит поиск аргументов. Я имею словари аргументов, таких как
имена музыкантов, названия жанров и пол людей. В первую очередь я извлекаю из текста именно их.
Затем я отбираю из оставшихся слов числа. Аргументы помещаются в специальный словарь для дальнейшего их
использования в обработчиках.

На втором этапе я привожу все оставшиеся в предложении слова к нормальной форме и присваиваю им теги.
Я имею словарь тегов разных категорий, где ключами являются название категории, а значениями списки 
синонимов этого ключевого слова. Если анализируемое слово входит в какой-то список синонимов, ему 
присваеется соответствующий тэг.

Также я имею список шаблонов запросов. Каждый шаблон может иметь список необходимых для запроса аргументов 
(и их количество) и условия наличия или отсутствия во фразе ключевых слов. Далее я примеряю к полученному 
от вас запросу шаблоны. То есть проверяю, имеются ли в запросе необходимые аргументы в нужном количестве
и выполняются ли указанные в шаблоне условия наличия или отсутствия ключевых слов.
В случае, если один из шаблонов подходит, я вызываю привязанный к нему обработчик.

Диалог имеет несколько состояний, в зависимости от которых проверяются те или иные шаблоны фраз.

Отдельно можно сказать о запросе рекомендации артистов, похожих на указанного. В данном сценарии вы 
можете указывать и сам запрос, и фильтры к нему в одном предложении.
"""
        return DialogState.INFO