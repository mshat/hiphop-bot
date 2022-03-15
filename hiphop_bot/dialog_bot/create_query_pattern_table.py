from hiphop_bot.dialog_bot.services.query_handling.handlers import restart
from hiphop_bot.dialog_bot.services.query_handling.handlers import settings
from hiphop_bot.dialog_bot.services.query_handling.handlers import filtration
from hiphop_bot.dialog_bot.services.query_handling.handlers import like_dislike
from hiphop_bot.dialog_bot.services.query_handling.handlers import number_question
from hiphop_bot.dialog_bot.services.query_handling.handlers import search
from hiphop_bot.dialog_bot.services.query_handling.handlers import genres
from hiphop_bot.dialog_bot.services.query_handling.handlers import info


def create_query_pattern_table():
    query_pattern_strings = []

    # выстроены в порядке вызова при разборе запроса
    handlers = [
        restart.RestartHandler,

        filtration.FilterBySexIncludeHandler,
        filtration.FilterBySexExcludeHandler,
        filtration.FilterByAgeRangeHandler,
        filtration.FilterByAgeIncludeHandler,
        filtration.FilterByAgeExcludeHandler,
        filtration.FilterOutputLenHandler,
        filtration.FilterByMembersCountHandler,
        filtration.RemoveFiltersHandler,
        filtration.RemoveResultLenFilterHandler,

        like_dislike.ExcludeDislikeHandler,
        like_dislike.ExcludeLikeHandler,
        like_dislike.LikeHandler,
        like_dislike.DislikeHandler,

        number_question.NumberWithSexHandler,
        number_question.NumberWithAgeRangeHandler,
        number_question.NumberWithAgeHandler,
        number_question.NumberHandler,

        search.SearchBySexHandler,
        search.SearchByAgeRangeHandler,
        search.SearchByAgeHandler,
        search.SearchByGenreHandler,
        search.SearchByArtistHandler,
        search.RecommendationHandler,
        search.ShowAllArtistsHandler,
        genres.ShowAllGenresHandler,

        settings.SetOutputLenHandler,

        info.InfoHandler,
        info.InfoAboutBotHandler,
        info.InfoAboutBotOpportunitiesHandler,
        info.InfoAboutBotAlgorithmHandler,
    ]
    for handler_class in handlers:
        handler = handler_class()
        query_pattern_strings.append(str(handler))

    with open('query_pattern_strings.txt', 'w', encoding='utf-8') as file:
        for line in query_pattern_strings:
            file.write(f'{line}\n')


if __name__ == '__main__':
    create_query_pattern_table()
