from hiphop_bot.dialog_bot.query_handling.query_handler import QueryPattern, QueryHandler
from hiphop_bot.dialog_bot.query_handling.tag_condition import (AndMultiTagCondition as AndMulti, OrMultiTagCondition as OrMulti,
                                                   AndTagCondition as And, OrTagCondition as Or, AndNotTagCondition as AndNot)
from hiphop_bot.dialog_bot.query_handling.query_handler import log_query_pattern_strings
from hiphop_bot.dialog_bot.query_handling.query_pattern import ALL
import hiphop_bot.dialog_bot.query_handling.handling_functions as functions


restart_handler = QueryHandler(
    QueryPattern([And('restart')]),
    functions.restart, 'Рестарт')


set_output_len_handler = QueryHandler(
    QueryPattern([
        OrMulti([Or('show'), Or('restrict')]), OrMulti([And('po'), AndMulti([Or('result'), Or('artist'), Or('line')])]),
        AndMulti([AndNot('range'), AndNot('older'), AndNot('younger')]),
    ],
        'NumArgument'),
    functions.set_output_len, 'Изменить количество выводимых результатов')

filter_by_sex_include_handler = QueryHandler(
    QueryPattern([], 'SexArgument'),
    functions.filter_by_sex_include, 'Фильтр по полу "включить"')

filter_by_sex_exclude_handler = QueryHandler(
    QueryPattern([Or('exclude'), AndNot('except')], 'SexArgument'),
    functions.filter_by_sex_exclude, 'Фильтр по полу "исключить"')

filter_by_age_range_handler = QueryHandler(
    QueryPattern([Or('range'), OrMulti([And('older'), And('younger')])], required_arguments={'NumArgument': 2}),
    functions.filter_by_age_range, 'Фильтр по возрасту в диапазоне')

filter_by_age_include_handler = QueryHandler(
    QueryPattern([AndMulti([Or('older'), Or('younger')])], 'NumArgument'),
    functions.filter_by_age_include, 'Фильтр по возрасту "включить"')

filter_by_age_exclude_handler = QueryHandler(
    QueryPattern([And('exclude'), AndMulti([Or('older'), Or('younger')])], 'NumArgument'),
    functions.filter_by_age_exclude, 'Фильтр по возрасту "исключить"')

filter_output_len_handler = QueryHandler(
    QueryPattern([OrMulti([Or('show'), Or('restrict')]), OrMulti([And('po'), AndMulti([Or('result'), Or('artist'), Or('line')])])], 'NumArgument'),
    functions.set_output_len, 'Фильтр по количеству выводимых результатов')

filter_by_members_count_handler = QueryHandler(
    QueryPattern([Or('group'), Or('solo'), Or('duet')]),
    functions.filter_by_members_count, 'Фильтр по количеству участников коллектива')

remove_filters_handler = QueryHandler(
    QueryPattern([And('exclude'), And('all'), AndMulti([Or('filter'), Or('restrict')])]),
    functions.remove_filters, 'Удалить все фильтры')

remove_result_len_filter_handler = QueryHandler(
    QueryPattern([
        OrMulti([And('exclude'), And('number')]),
        OrMulti([AndMulti([Or('show'), Or('include')]), And('all')])
    ]),
    functions.remove_result_len_filter, 'Удалить ограничение количества выводимых строк')

exclude_dislike_handler = QueryHandler(
    QueryPattern([And('dislike'), And('exclude')], required_arguments={'ArtistArgument': ALL}),
    functions.like, 'Лайк')

exclude_like_handler = QueryHandler(
    QueryPattern([And('like'), And('exclude')], required_arguments={'ArtistArgument': ALL}),
    functions.dislike, 'Дизлайк')

like_handler = QueryHandler(
    QueryPattern([And('like')], required_arguments={'ArtistArgument': ALL}),
    functions.like, 'Лайк')

dislike_handler = QueryHandler(
    QueryPattern([And('dislike')], required_arguments={'ArtistArgument': ALL}),
    functions.dislike, 'Дизлайк')

number_with_sex_handler = QueryHandler(
    QueryPattern([Or('number'), Or('how many')], 'SexArgument'),
    functions.number_with_sex, 'Количество артистов указанного пола в базе')

number_with_age_range_handler = QueryHandler(
    QueryPattern(
        [AndMulti([Or('number'), Or('how many')]), AndMulti([Or('range'), OrMulti([And('older'), And('younger')])])],
        required_arguments={'NumArgument': 2}
    ),
    functions.number_with_age_range, 'Количество артистов от X до Y лет в базе')

number_with_age_handler = QueryHandler(
    QueryPattern(
        [AndMulti([Or('number'), Or('how many')]), AndMulti([Or('older'), Or('younger')])],
        'NumArgument'
    ),
    functions.number_with_age, 'Количество артистов указанного возраста в базе')

number_handler = QueryHandler(
    QueryPattern([Or('number'), Or('how many')]),
    functions.number, 'Количество артистов в базе')

search_by_sex_handler = QueryHandler(
    QueryPattern([Or('artist'), Or('recommend'), Or('show')], 'SexArgument'),
    functions.search_by_sex, 'Вывести исполнителей указанного пола')

search_by_age_range_handler = QueryHandler(
    QueryPattern(
        [AndMulti([Or('artist'), Or('recommend'), Or('show')]), AndMulti([Or('range'), OrMulti([And('older'), And('younger')])])],
        required_arguments={'NumArgument': 2}),
    functions.search_by_age_range, 'Вывести исполнителей в диапазоне возраста')

search_by_age_handler = QueryHandler(
    QueryPattern([AndMulti([Or('artist'), Or('recommend'), Or('show')]), AndMulti([Or('older'), Or('younger')])], 'NumArgument'),
    functions.search_by_age, 'Вывести исполнителей в указанном возрасте')

search_by_genre_handler = QueryHandler(
    QueryPattern([Or('genre'), Or('recommend'), Or('show')], 'GenreArgument'),
    functions.search_by_genre, 'Вывести артистов в определённом жанре')

search_by_artist_handler = QueryHandler(
    QueryPattern([Or('search'), Or('like/how'), Or('recommend'), Or('show')], 'ArtistArgument'),
    functions.search_by_artist, 'Рекомендация по артисту')

recommendation_handler = QueryHandler(
    QueryPattern([OrMulti([AndMulti([Or('search'), Or('recommend'), Or('show'), Or('artist')]), AndMulti([Or('to me'), Or('like')])]), OrMulti([And('to me'), And('like')])]),
    functions.recommendation, 'Рекомендация по интересам')

show_all_artists_handler = QueryHandler(
    QueryPattern([AndMulti([Or('all'), Or('like/how')]), AndNot('genre'), AndMulti([Or('include'), Or('artist'), Or('show')])]),
    functions.show_all_artists, 'Вывести всех артистов в базе')

show_all_genres_handler = QueryHandler(
    QueryPattern([AndMulti([Or('all'), Or('like/how')]), AndMulti([Or('include'), Or('genre'), Or('show')])]),
    functions.show_all_genres, 'Вывести все жанры в базе')

info_handler = QueryHandler(
    QueryPattern([Or('talk about'), Or('about'), Or('info')], 'ArtistArgument'),
    functions.info, 'Информация об артисте')

info_about_bot_handler = QueryHandler(
    QueryPattern([Or('you'), Or('who'), AndNot('opportunities')]),
    functions.about_bot, 'Информация о боте')

info_about_bot_opportunities_handler = QueryHandler(
    QueryPattern([Or('opportunities')]),
    functions.about_opportunities, 'Информация о возможностях бота')

info_about_bot_algorithm_handler = QueryHandler(
    QueryPattern([AndMulti([Or('talk about'), Or('like/how')]), And('you'), And('algorithm')]),
    functions.about_algorithm, 'Информация об устройстве бота')


if __name__ == "__main__":
    log_query_pattern_strings()