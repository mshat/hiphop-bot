from __future__ import annotations
from typing import List
from hiphop_bot.dialog_bot.query_handling.query_handler import QueryHandler
from hiphop_bot.dialog_bot.query_handling.tag_condition import (AndMultiTagCondition as AndMulti,
                                                                OrMultiTagCondition as OrMulti,
                                                                AndTagCondition as And, OrTagCondition as Or,
                                                                AndNotTagCondition as AndNot)
from hiphop_bot.dialog_bot.query_handling.query_pattern import ALL
from hiphop_bot.dialog_bot.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.query_solving.user import User
from hiphop_bot.dialog_bot.recommender_system import filter
from hiphop_bot.dialog_bot.recommender_system import interface
from hiphop_bot.dialog_bot.sentence_analyzer.query import Query
from hiphop_bot.dialog_bot.config import DEBUG, ENABLE_FILTERS
from hiphop_bot.dialog_bot.data.const import SexFilter, GroupTypeFilter, LINE_LEN
from hiphop_bot.dialog_bot.data.data import GENRES
from hiphop_bot.dialog_bot.sentence_analyzer.argument import ArtistArgument, NumArgument, SexArgument, GenreArgument
from hiphop_bot.dialog_bot.tools.debug_print import debug_print


def create_query_pattern_table():
    query_pattern_strings = []
    handlers = [RestartHandler, SetOutputLenHandler, FilterBySexIncludeHandler, FilterBySexExcludeHandler,
                FilterByAgeRangeHandler, FilterByAgeIncludeHandler, FilterByAgeExcludeHandler, FilterOutputLenHandler,
                FilterByMembersCountHandler, RemoveFiltersHandler, RemoveResultLenFilterHandler, ExcludeDislikeHandler,
                ExcludeLikeHandler, LikeHandler, DislikeHandler, NumberWithSexHandler, NumberWithAgeRangeHandler,
                NumberWithAgeHandler, NumberHandler, SearchBySexHandler, SearchByAgeRangeHandler, SearchByAgeHandler,
                SearchByGenreHandler, SearchByArtistHandler, RecommendationHandler, ShowAllArtistsHandler,
                ShowAllGenresHandler, InfoHandler, InfoAboutBotHandler, InfoAboutBotOpportunitiesHandler,
                InfoAboutBotAlgorithmHandler
                ]
    for handler_class in handlers:
        handler = handler_class()
        query_pattern_strings.append(str(handler))

    with open('query_pattern_strings.txt', 'w', encoding='utf-8') as f:
        for line in query_pattern_strings:
            f.write(f'{line}\n')


def print_after_search_message():
    if ENABLE_FILTERS:
        print(f'{"="*LINE_LEN}\n'
              f'Вы находитесь в режиме ФИЛЬТРАЦИИ. Вы можете добавить фильтры к полученному результату поиска.\n'
              'Чтобы задать новый вопрос, скажите мне начать сначала\n'
              f'{"=" * LINE_LEN}'
              )


def filter_search_result(user: User, dialog: Dialog):
    if dialog.search_result:
        return filter.filter_recommendations(
            dialog.search_result,
            group_type=user.group_type_filter.value,
            sex=user.sex_filter.value,
            younger=user.younger_filter,
            older=user.older_filter,
        )


def show_recommendations(user: User, dialog: Dialog):
    filtered = filter_search_result(user, dialog)
    if filtered:
        artists = filtered
    else:
        artists = dialog.search_result

    if artists:
        if user.dislikes:
            print(f'Список дизлайков: {", ".join(user.dislikes)}')
        if user.str_filters != '':
            print(f'Установлены фильтры: {user.str_filters}')

        interface.print_recommendations(artists, output_len=user.output_len, debug=DEBUG)

        if dialog.state in (DialogState.search, DialogState.filter):
            print_after_search_message()


def get_arguments_by_type(query: Query, argument_type: str) \
        -> List[ArtistArgument | NumArgument | SexArgument | GenreArgument]:
    return [argument for type_, arguments in query.arguments.items() for argument in arguments if type_ == argument_type]


class RestartHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [And('restart')]
        self.debug_msg = 'Рестарт'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        return DialogState.start


class SetOutputLenHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [
            OrMulti([Or('show'), Or('restrict')]), OrMulti([And('po'), AndMulti([Or('result'), Or('artist'), Or('line')])]),
            AndMulti([AndNot('range'), AndNot('older'), AndNot('younger')]),
        ]
        self.required_argument_type = 'NumArgument'
        self.debug_msg = 'Изменить количество выводимых результатов'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        output_len = get_arguments_by_type(query, 'NumArgument')[-1]

        user.output_len = int(output_len.value)

        if show:
            show_recommendations(user, dialog)

        print(f'Буду выводить по {output_len.value} строк')
        return DialogState.start


class FilterBySexIncludeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = []
        self.required_argument_type = 'SexArgument'
        self.debug_msg = 'Фильтр по полу "включить"'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        sex = get_arguments_by_type(query, 'SexArgument')[0]
        debug_print(f'Убрать всех, кроме {sex.value.value} пола')

        user.add_sex_filter(sex.value)

        if show:
            show_recommendations(user, dialog)
        return DialogState.filter


class FilterBySexExcludeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('exclude'), AndNot('except')]
        self.required_argument_type = 'SexArgument'
        self.debug_msg = 'Фильтр по полу "исключить"'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        sex_arg = get_arguments_by_type(query, 'SexArgument')[0]
        debug_print(f'Убрать артистов {sex_arg.value} пола')

        sex = SexFilter.male if sex_arg.value == SexFilter.female else SexFilter.female
        user.add_sex_filter(sex)

        if show:
            show_recommendations(user, dialog)

        return DialogState.filter


class FilterByAgeRangeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('range'), OrMulti([And('older'), And('younger')])]
        self.required_arguments = {'NumArgument': 2}
        self.debug_msg = 'Фильтр по возрасту в диапазоне'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        age = get_arguments_by_type(query, 'NumArgument')
        if len(age) >= 2:
            from_age, to_age = sorted([int(age[0].value), int(age[1].value)])
            debug_print(f'фильтр от {from_age} до {to_age} лет')

            user.older_filter = from_age
            user.younger_filter = to_age

            if show:
                show_recommendations(user, dialog)
        else:
            return DialogState.filter
        return DialogState.filter


class FilterByAgeIncludeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [AndMulti([Or('older'), Or('younger')])]
        self.required_argument_type = 'NumArgument'
        self.debug_msg = 'Фильтр по возрасту "включить"'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        age = get_arguments_by_type(query, 'NumArgument')[0]
        age = int(age.value)
        if 'younger' in query.query_tag_structure:
            debug_print(f'фильтр до {age} лет')
            user.younger_filter = age
        elif 'older' in query.query_tag_structure:
            debug_print(f'фильтр от {age} лет')
            user.older_filter = age
        else:
            return DialogState.filter

        if show:
            show_recommendations(user, dialog)
        return DialogState.filter


class FilterByAgeExcludeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [And('exclude'), AndMulti([Or('older'), Or('younger')])]
        self.required_argument_type = 'NumArgument'
        self.debug_msg = 'Фильтр по возрасту "исключить"'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        age = get_arguments_by_type(query, 'NumArgument')[0]
        age = int(age.value)
        if 'younger' in query.query_tag_structure:
            debug_print(f'фильтр от {age} лет')
            user.older_filter = age
        elif 'older' in query.query_tag_structure:
            debug_print(f'фильтр до {age} лет')
            user.younger_filter = age
        else:
            return DialogState.filter

        if show:
            show_recommendations(user, dialog)
        return DialogState.filter


class FilterOutputLenHandler(SetOutputLenHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [OrMulti([Or('show'), Or('restrict')]), OrMulti([And('po'), AndMulti([Or('result'), Or('artist'), Or('line')])])]
        self.required_argument_type = 'NumArgument'
        self.debug_msg = 'Фильтр по количеству выводимых результатов'


class FilterByMembersCountHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('group'), Or('solo'), Or('duet')]
        self.debug_msg = 'Фильтр по количеству участников коллектива'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        tags = query.query_tag_structure
        if 'group' in tags:
            user.group_type_filter = GroupTypeFilter.group
        elif 'solo' in tags:
            user.group_type_filter = GroupTypeFilter.solo
        elif 'duet' in tags:
            user.group_type_filter = GroupTypeFilter.duet
        else:
            return DialogState.filter

        if show:
            show_recommendations(user, dialog)
        debug_print(f'оставить {user.group_type_filter}')
        return DialogState.filter


class RemoveFiltersHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [And('exclude'), And('all'), AndMulti([Or('filter'), Or('restrict')])]
        self.debug_msg = 'Удалить все фильтры'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        user.set_all_filters_to_default()
        if show:
            show_recommendations(user, dialog)
        return DialogState.filter


class RemoveResultLenFilterHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [
            OrMulti([And('exclude'), And('number')]),
            OrMulti([AndMulti([Or('show'), Or('include')]), And('all')])
            ]
        self.debug_msg = 'Удалить ограничение количества выводимых строк'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        user.output_len = 1000
        if show:
            show_recommendations(user, dialog)
        return DialogState.filter


class ExcludeDislikeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [And('dislike'), And('exclude')]
        self.required_arguments = {'ArtistArgument': ALL}
        self.debug_msg = 'Лайк'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        liked_artists = get_arguments_by_type(query, 'ArtistArgument')
        liked_artists = [artist.value for artist in liked_artists]
        for artist in liked_artists:
            user.add_like(artist)
        print(f'Поставлен лайк: {", ".join(liked_artists)}')
        return DialogState.like


class LikeHandler(ExcludeDislikeHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [And('like')]
        self.required_arguments = {'ArtistArgument': ALL}
        self.debug_msg = 'Лайк'


class ExcludeLikeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [And('like'), And('exclude')]
        self.required_arguments = {'ArtistArgument': ALL}
        self.debug_msg = 'Дизлайк'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        disliked_artists = get_arguments_by_type(query, 'ArtistArgument')
        disliked_artists = [artist.value for artist in disliked_artists]
        for artist in disliked_artists:
            user.add_dislike(artist)
        print(f'Поставлен дизлайк: {", ".join(disliked_artists)}')
        return DialogState.dislike


class DislikeHandler(ExcludeLikeHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [And('dislike')]
        self.required_arguments={'ArtistArgument': ALL}
        self.debug_msg = 'Дизлайк'


class NumberWithSexHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('number'), Or('how many')]
        self.required_argument_type = 'SexArgument'
        self.debug_msg = 'Количество артистов указанного пола в базе'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        sex = get_arguments_by_type(query, 'SexArgument')[0]
        artists = interface.get_all_artists()
        artists = filter.filter_artists(artists, sex=sex.value.value)
        if sex.value == SexFilter.male:
            print(f'В базе {len(artists)} исполнителя мужского пола')
        else:
            print(f'В базе {len(artists)} исполнитель женского пола')
        return DialogState.number


class NumberWithAgeRangeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [AndMulti([Or('number'), Or('how many')]), AndMulti([Or('range'), OrMulti([And('older'), And('younger')])])]
        self.required_arguments = {'NumArgument': 2}
        self.debug_msg = 'Количество артистов от X до Y лет в базе'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        age = get_arguments_by_type(query, 'NumArgument')
        if len(age) >= 2:
            from_age, to_age = sorted([int(age[0].value), int(age[1].value)])
            debug_print(f'количество артистов от {from_age} до {to_age} лет')

            artists = interface.get_all_artists()
            artists = filter.filter_artists(artists, older=from_age, younger=to_age)

            print(f'Количество исполнителей от {from_age} до {to_age} лет: {len(artists)}')
        else:
            return
        return DialogState.number


class NumberWithAgeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [AndMulti([Or('number'), Or('how many')]), AndMulti([Or('older'), Or('younger')])]
        self.required_argument_type = 'NumArgument'
        self.debug_msg = 'Количество артистов указанного возраста в базе'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        age = get_arguments_by_type(query, 'NumArgument')[0]
        age = int(age.value)

        artists = interface.get_all_artists()

        if 'younger' in query.query_tag_structure:
            artists = filter.filter_artists(artists, younger=age)
            print(f'Количество артистов до {age} лет: {len(artists)}')
        elif 'older' in query.query_tag_structure:
            artists = filter.filter_artists(artists, older=age)
            print(f'Количество артистов от {age} лет: {len(artists)}')
        return DialogState.number


class NumberHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('number'), Or('how many')]
        self.debug_msg = 'Количество артистов в базе'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        artists = interface.get_all_artists()
        print(f'В базе {len(artists)} исполнителя')
        return DialogState.number


class SearchBySexHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('artist'), Or('recommend'), Or('show')]
        self.required_argument_type = 'SexArgument'
        self.debug_msg = 'Вывести исполнителей указанного пола'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        sex = get_arguments_by_type(query, 'SexArgument')[0]
        artists = interface.get_all_artists()
        artists = filter.filter_artists(artists, sex=sex.value.value)
        interface.print_artists(artists)
        print_after_search_message()
        return DialogState.search


class SearchByAgeRangeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [AndMulti([Or('artist'), Or('recommend'), Or('show')]), AndMulti([Or('range'), OrMulti([And('older'), And('younger')])])]
        self.required_arguments = {'NumArgument': 2}
        self.debug_msg = 'Вывести исполнителей в диапазоне возраста'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        age = get_arguments_by_type(query, 'NumArgument')
        if len(age) >= 2:
            from_age, to_age = sorted([int(age[0].value), int(age[1].value)])
            debug_print(f'количество артистов от {from_age} до {to_age} лет')

            artists = interface.get_all_artists()
            artists = filter.filter_artists(artists, older=from_age, younger=to_age)
            interface.print_artists(artists)
            dialog.search_result = artists
        else:
            return DialogState.start
        print_after_search_message()
        return DialogState.search


class SearchByAgeHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [AndMulti([Or('artist'), Or('recommend'), Or('show')]), AndMulti([Or('older'), Or('younger')])]
        self.required_argument_type = 'NumArgument'
        self.debug_msg = 'Вывести исполнителей в указанном возрасте'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        age = get_arguments_by_type(query, 'NumArgument')[0]
        age = int(age.value)

        artists = interface.get_all_artists()

        if 'younger' in query.query_tag_structure:
            debug_print(f'фильтр до {age} лет')
            artists = filter.filter_artists(artists, younger=age)
        elif 'older' in query.query_tag_structure:
            debug_print(f'фильтр от {age} лет')
            artists = filter.filter_artists(artists, older=age)

        interface.print_artists(artists)
        dialog.search_result = artists
        print_after_search_message()
        return DialogState.search


class SearchByGenreHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('genre'), Or('recommend'), Or('show')]
        self.required_argument_type = 'GenreArgument'
        self.debug_msg = 'Вывести артистов в определённом жанре'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        genre = get_arguments_by_type(query, 'GenreArgument')[0]
        artists = interface.get_artists_by_genre(genre.value)
        interface.print_artists(artists, debug=DEBUG)
        print_after_search_message()
        return DialogState.search


class SearchByArtistHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('search'), Or('like/how'), Or('recommend'), Or('show')]
        self.required_argument_type = 'ArtistArgument'
        self.debug_msg = 'Рекомендация по артисту'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        artist = get_arguments_by_type(query, 'ArtistArgument')[0]
        artists = interface.recommend_by_seed(artist.value, disliked_artists=user.dislikes)
        dialog.search_result = artists
        return DialogState.search


class RecommendationHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [OrMulti([AndMulti([Or('search'), Or('recommend'), Or('show'), Or('artist')]), AndMulti([Or('to me'), Or('like')])]), OrMulti([And('to me'), And('like')])]
        self.debug_msg = 'Рекомендация по интересам'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        if len(user.likes) == 0:
            print('Для начала расскажите, какие музыканты или группы вам нравятся?')
            return DialogState.start
        dialog.search_result = interface.recommend_by_liked_with_disliked(user.dislikes, user.likes, DEBUG)

        print(f'Список лайков: {", ".join(user.likes)}')
        show_recommendations(user, dialog)
        return DialogState.search


class ShowAllArtistsHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [AndMulti([Or('all'), Or('like/how')]), AndNot('genre'), AndMulti([Or('include'), Or('artist'), Or('show')])]
        self.debug_msg = 'Вывести всех артистов в базе'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        artists = interface.get_all_artists()
        interface.print_artists(artists)
        print_after_search_message()
        print('Кстати, в запросах вы можете указывать имя артиста или группы на русском языке, даже если тут он '
              'записан на английском')
        return DialogState.search


class ShowAllGenresHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [AndMulti([Or('all'), Or('like/how')]), AndMulti([Or('include'), Or('genre'), Or('show')])]
        self.debug_msg = 'Вывести все жанры в базе'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        genres = set(GENRES.values())
        interface.print_strings(genres)
        print('Кстати, в фильтрах вы можете указывать название жанра на русском языке')
        return DialogState.start


class InfoHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('talk about'), Or('about'), Or('info')]
        self.required_argument_type = 'ArtistArgument'
        self.debug_msg = 'Информация об артисте'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        artist_arg = get_arguments_by_type(query, 'ArtistArgument')[0]
        artist = interface.get_artist_by_name(artist_arg.value)
        if not artist:
            print('Артист не найден :(')
        else:
            sex = "мужской" if artist.male_or_female == 1 else "женский"
            if artist.group_members_number == 1:
                print(f'Артист {artist.name}')
            elif artist.group_members_number == 2:
                print(f'Дуэт {artist.name}')
            else:
                print(f'Группа {artist.name}')
            if artist.group_members_number > 1:
                print(f'Возраст фронтмэна: {artist.age}')
                print(f'Пол фронтмэна: {sex}')
                print(f'Количество участников: {artist.group_members_number}')
            else:
                print(f'Возраст: {artist.age}')
                print(f'Пол: {sex}')

        return DialogState.info


class InfoAboutBotHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('you'), Or('who'), AndNot('opportunities')]
        self.debug_msg = 'Информация о боте'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        debug_print('Информация о боте')
        print('Я - ваш помощник в мире русского хипхопа. Меня сделал Шатохин Максим, ИУ7-12М')
        return DialogState.info


class InfoAboutBotOpportunitiesHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [Or('opportunities')]
        self.debug_msg = 'Информация о возможностях бота'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        debug_print('Возможности бота')
        print("""Вы можете в свободной форме задавать мне вопросы или поручать команды.
        Я могу выполнять следующие действия:

        1. Рекомендация по артисту                       
        2. Рекомендация по интересам                     
        3. Вывести всех артистов в базе
        4. Вывести все известные боту жанры                  
        5. Вывести всех исполнителей указанного пола          
        6. Вывести всех исполнителей в указанном возрасте     
        7. Вывести всех исполнителей в диапазоне возраста     
        8. Вывести всех артистов в определённом жанре         
        9. Поставить лайк (можно несколько сразу)                                          
        10. Поставить дизлайк (можно несколько сразу)                                                                       
        11. Фильтр по полу                                     
        12. Фильтр по возрасту                           
        13. Фильтр по возрасту в диапазоне                
        14. Фильтр по количеству участников коллектива    
        15. Фильтр по количеству выводимых результатов    
        16. Удалить ограничение количества выводимых строк
        17. Удалить все фильтры                           
        18. Изменить количество выводимых результатов     
        19. Вывести количество артистов в базе                    
        20. Вывести количество артистов указанного пола в базе    
        21. Вывести количество артистов указанного возраста в базе
        22. Вывести количество артистов в указанном диапазоне возраста    
        23. Вывести информацию об артисте                         
        24. Вывести информацию о боте                             
        25. Вывести информацию о возможностях бота                
        26. Вывести информацию об устройстве бота                 
        27. Вернуться к начальному состоянию"""
              )
        return DialogState.info


class InfoAboutBotAlgorithmHandler(QueryHandler):
    def __init__(self):
        super().__init__()
        self.conditions = [AndMulti([Or('talk about'), Or('like/how')]), And('you'), And('algorithm')]
        self.debug_msg = 'Информация об устройстве бота'

    def handle(self, query: Query, user: User, dialog: Dialog, show=True):
        debug_print('Алгоритм бота')
        print("""Я работаю следующим образом:
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

        Список шаблонов с условиями вы можете увидеть в файле query_pattern_strings.txt. Он генерируется автоматически при 
        запуске handlers.py.
        """)
        return DialogState.info
