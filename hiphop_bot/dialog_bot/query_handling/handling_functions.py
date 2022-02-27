from typing import List
from hiphop_bot.dialog_bot.query_handling.query_handler import Query
from hiphop_bot.dialog_bot.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.tools.debug_print import debug_print
from hiphop_bot.dialog_bot.sentence_analyzer.argument import ArtistArgument, NumArgument, SexArgument, GenreArgument
from hiphop_bot.dialog_bot.query_solving.user import User
from hiphop_bot.dialog_bot.recommender_system import filter
from hiphop_bot.dialog_bot.recommender_system import interface
from hiphop_bot.dialog_bot.config import DEBUG, ENABLE_FILTERS
from hiphop_bot.dialog_bot.data.const import SexFilter, GroupTypeFilter, LINE_LEN
from hiphop_bot.dialog_bot.data.data import GENRES


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


def restart(query: Query, user: User, dialog: Dialog, show=True):
    return DialogState.start


def like(query: Query, user: User, dialog: Dialog, show=True):
    liked_artists = get_arguments_by_type(query, 'ArtistArgument')
    liked_artists = [artist.value for artist in liked_artists]
    for artist in liked_artists:
        user.add_like(artist)
    print(f'Поставлен лайк: {", ".join(liked_artists)}')
    return DialogState.like


def dislike(query: Query, user: User, dialog: Dialog, show=True):
    disliked_artists = get_arguments_by_type(query, 'ArtistArgument')
    disliked_artists = [artist.value for artist in disliked_artists]
    for artist in disliked_artists:
        user.add_dislike(artist)
    print(f'Поставлен дизлайк: {", ".join(disliked_artists)}')
    return DialogState.dislike


def show_all_artists(query: Query, user: User, dialog: Dialog, show=True):
    artists = interface.get_all_artists()
    interface.print_artists(artists)
    print_after_search_message()
    print('Кстати, в запросах вы можете указывать имя артиста или группы на русском языке, даже если тут он '
          'записан на английском')
    return DialogState.search


def show_all_genres(query: Query, user: User, dialog: Dialog, show=True):
    genres = set(GENRES.values())
    interface.print_strings(genres)
    print('Кстати, в фильтрах вы можете указывать название жанра на русском языке')
    return DialogState.start


def search_by_artist(query: Query, user: User, dialog: Dialog, show=True):
    artist = get_arguments_by_type(query, 'ArtistArgument')[0]
    artists = interface.recommend_by_seed(artist.value, disliked_artists=user.dislikes)
    dialog.search_result = artists
    return DialogState.search


def recommendation(query: Query, user: User, dialog: Dialog, show=True):
    if len(user.likes) == 0:
        print('Для начала расскажите, какие музыканты или группы вам нравятся?')
        return DialogState.start
    dialog.search_result = interface.recommend_by_liked_with_disliked(user.dislikes, user.likes, DEBUG)

    print(f'Список лайков: {", ".join(user.likes)}')
    show_recommendations(user, dialog)
    return DialogState.search


def search_by_genre(query: Query, user: User, dialog: Dialog, show=True):
    genre = get_arguments_by_type(query, 'GenreArgument')[0]
    artists = interface.get_artists_by_genre(genre.value)
    interface.print_artists(artists, debug=DEBUG)
    print_after_search_message()
    return DialogState.search


def search_by_sex(query: Query, user: User, dialog: Dialog, show=True):
    sex = get_arguments_by_type(query, 'SexArgument')[0]
    artists = interface.get_all_artists()
    artists = filter.filter_artists(artists, sex=sex.value.value)
    interface.print_artists(artists)
    print_after_search_message()
    return DialogState.search


def search_by_age_range(query: Query, user: User, dialog: Dialog, show=True):
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


def search_by_age(query: Query, user: User, dialog: Dialog, show=True):
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


def info(query: Query, user: User, dialog: Dialog, show=True):
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


def number(query: Query, user: User, dialog: Dialog, show=True):
    artists = interface.get_all_artists()
    print(f'В базе {len(artists)} исполнителя')
    return DialogState.number


def number_with_sex(query: Query, user: User, dialog: Dialog, show=True):
    sex = get_arguments_by_type(query, 'SexArgument')[0]
    artists = interface.get_all_artists()
    artists = filter.filter_artists(artists, sex=sex.value.value)
    if sex.value == SexFilter.male:
        print(f'В базе {len(artists)} исполнителя мужского пола')
    else:
        print(f'В базе {len(artists)} исполнитель женского пола')
    return DialogState.number


def number_with_age_range(query: Query, user: User, dialog: Dialog, show=True):
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


def number_with_age(query: Query, user: User, dialog: Dialog, show=True):
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


def set_output_len(query: Query, user: User, dialog: Dialog, show=True):
    output_len = get_arguments_by_type(query, 'NumArgument')[-1]

    user.output_len = int(output_len.value)

    if show:
        show_recommendations(user, dialog)

    print(f'Буду выводить по {output_len.value} строк')
    return DialogState.start


def filter_by_sex_include(query: Query, user: User, dialog: Dialog, show=True):
    sex = get_arguments_by_type(query, 'SexArgument')[0]
    debug_print(f'Убрать всех, кроме {sex.value.value} пола')

    user.add_sex_filter(sex.value)

    if show:
        show_recommendations(user, dialog)
    return DialogState.filter


def filter_by_sex_exclude(query: Query, user: User, dialog: Dialog, show=True):
    sex_arg = get_arguments_by_type(query, 'SexArgument')[0]
    debug_print(f'Убрать артистов {sex_arg.value} пола')

    sex = SexFilter.male if sex_arg.value == SexFilter.female else SexFilter.female
    user.add_sex_filter(sex)

    if show:
        show_recommendations(user, dialog)

    return DialogState.filter


def filter_by_age_range(query: Query, user: User, dialog: Dialog, show=True):
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


def filter_by_age_include(query: Query, user: User, dialog: Dialog, show=True):
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


def filter_by_age_exclude(query: Query, user: User, dialog: Dialog, show=True):
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


def filter_by_members_count(query: Query, user: User, dialog: Dialog, show=True):
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


def remove_result_len_filter(query: Query, user: User, dialog: Dialog, show=True):
    user.output_len = 1000
    if show:
        show_recommendations(user, dialog)
    return DialogState.filter


def remove_filters(query: Query, user: User, dialog: Dialog, show=True):
    user.set_all_filters_to_default()
    if show:
        show_recommendations(user, dialog)
    return DialogState.filter


def about_bot(query: Query, user: User, dialog: Dialog, show=True):
    debug_print('Информация о боте')
    print('Я - ваш помощник в мире русского хипхопа. Меня сделал Шатохин Максим, ИУ7-12М')
    return DialogState.info


def about_opportunities(query: Query, user: User, dialog: Dialog, show=True):
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


def about_algorithm(query: Query, user: User, dialog: Dialog, show=True):
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
