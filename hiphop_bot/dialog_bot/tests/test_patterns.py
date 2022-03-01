from typing import Dict
import unittest
import unittest.mock
from hiphop_bot.dialog_bot.query_solving.dialog import Dialog, DialogState
from hiphop_bot.dialog_bot.query_solving.query_solver import QuerySolver
from hiphop_bot.dialog_bot.sentence_analyzer.sentence_parser import SentenceParser
from hiphop_bot.dialog_bot.query_solving.user import User


class DataForTests:
    search_by_name = {
        "найди похожих исполнителей на крека": 'SearchByArtistHandler',
        "найди похожих на моргенштерна": 'SearchByArtistHandler',
        "похожие на басту": 'SearchByArtistHandler',
        "схожие с кровостоком": 'SearchByArtistHandler',
        'порекомендуй исполнителей, похожих на кизару': 'SearchByArtistHandler',
        'рэперы как рэм': 'SearchByArtistHandler',
        'порекомендуй артистов как гуф': 'SearchByArtistHandler',
        'посоветуй похожих на кизару': 'SearchByArtistHandler',
        'похожие на касту': 'SearchByArtistHandler',
    }
    recommendation = {
        "мне понравится": "RecommendationHandler",
        "порекомендуй по лайкам": "RecommendationHandler",
        "артисты по моим интересам": "RecommendationHandler",
        "порекомендуй по интересам": "RecommendationHandler",
    }
    search_by_genre = {
        "найди исполнителей в жанре грайм": 'SearchByGenreHandler',
        "исполнители в жанре поп": 'SearchByGenreHandler',
        'рекомендация по жанру клуб': 'SearchByGenreHandler',
        'посоветуй клубный рэп': 'SearchByGenreHandler',
        "порекомендуй клубный рэп": 'SearchByGenreHandler',
    }
    search_by_sex = {
        "покажи исполнителей мужчин": 'SearchBySexHandler',
        "артисты мужчины": 'SearchBySexHandler',
        "покажи исполнителей женщин": 'SearchBySexHandler',
        "артисты женщины": 'SearchBySexHandler',
        "покажи исполнителей мужского пола": 'SearchBySexHandler',
        "исполнители женского пола": 'SearchBySexHandler',
        "все рэперы женщины": 'SearchBySexHandler',
    }
    search_by_age = {
        "порекомендуй исполнителей старше 26 лет": 'SearchByAgeHandler',
        "покажи исполнителей старше 25 лет": 'SearchByAgeHandler',
        "выведи исполнителей младше 25 лет": 'SearchByAgeHandler',
        "покажи артистов младше 0 лет": 'SearchByAgeHandler',
        "порекомендуй артистов от 32 до 43 лет": 'SearchByAgeRangeHandler',
        "порекомендуй исполнителей от 49 до 49 лет": 'SearchByAgeRangeHandler',
    }
    search_show_all = {
        "покажи всех исполнителей": 'ShowAllArtistsHandler',
        "покажи всех": 'ShowAllArtistsHandler',
        "все артисты": 'ShowAllArtistsHandler',
        "все рэперы": 'ShowAllArtistsHandler',
        "все певцы": 'ShowAllArtistsHandler',
        "каких артистов ты знаешь?": 'ShowAllArtistsHandler',
        "все исполнители": 'ShowAllArtistsHandler',
        "покажи все жанры": 'ShowAllGenresHandler',
        "все жанры": 'ShowAllGenresHandler',
        "какие жанры ты знаешь?": 'ShowAllGenresHandler',
    }
    test_filter = {
        "оставь исполнителей мужского пола": 'FilterBySexIncludeHandler',
        "оставь женщин": 'FilterBySexIncludeHandler',
        "убери женщин": 'FilterBySexExcludeHandler',
        "выбери женщин": 'FilterBySexIncludeHandler',
        "убери всех исполнителей кроме женского пола": 'FilterBySexIncludeHandler',
        "убери всех кроме женского пола": 'FilterBySexIncludeHandler',
        "оставь только соло исполнителей": 'FilterByMembersCountHandler',
        "убери всех кроме соло исполнителей": 'FilterByMembersCountHandler',
        "оставь только дуэты": 'FilterByMembersCountHandler',
        "убери всех кроме дуэтов": 'FilterByMembersCountHandler',
        "оставь только группы": 'FilterByMembersCountHandler',
        "убери всех кроме групп": 'FilterByMembersCountHandler',
        "убери исполнителей младше чем 20": 'FilterByAgeExcludeHandler',
        "оставь исполнителей старше чем 22": 'FilterByAgeIncludeHandler',
        "убери исполнителей старше чем 30": 'FilterByAgeExcludeHandler',
        "оставь исполнителей младше чем 11": 'FilterByAgeIncludeHandler',
        "оставь исполнителей в возрасте от 32 до 43": 'FilterByAgeRangeHandler',
        "показывай по 10 артистов": 'SetOutputLenHandler',
        "выводи по 5 артистов": 'SetOutputLenHandler',
        "удалить все фильтры": 'RemoveFiltersHandler',
        "убери ограничение на количество артистов": 'RemoveResultLenFilterHandler',
        "выводи всех": 'RemoveResultLenFilterHandler',
    }
    like_dislike = {
        "убери многоточие из списка лайков": 'ExcludeLikeHandler',
        "мне не нравится егор крид": 'DislikeHandler',
        "поставь дизлайк тимати": 'DislikeHandler',
        "добавь моргенштерна в список дизлайков": 'DislikeHandler',
        "убери моргенштерна из списка дизлайков": 'ExcludeDislikeHandler',
        "мне нравится кровосток": 'LikeHandler',
        'люблю нойза': 'LikeHandler',
        'не люблю биг бейби тейпа': 'DislikeHandler',
        "мне нравится исполнитель кровосток": 'LikeHandler',
        "добавь касту в список любимых": 'LikeHandler',
        "поставь лайк касте": 'LikeHandler',
        "мне больше не нравится тимати": 'DislikeHandler',
    }
    number_queries = {
        'какое количество исполнителей в базе?': 'NumberHandler',
        "сколько исполнителей в базе?": 'NumberHandler',
        "сколько исполнителей ты знаешь?": 'NumberHandler',
        "сколько мужчин в базе?": 'NumberWithSexHandler',
        "сколько исполнителей мужчин ты знаешь?": 'NumberWithSexHandler',
        "сколько женщин в базе?": 'NumberWithSexHandler',
        "сколько исполнителей женщин ты знаешь?": 'NumberWithSexHandler',
        "сколько ты знаешь исполнителей старше 26 лет?": 'NumberWithAgeHandler',
        "сколько исполнителей старше 11 лет?": 'NumberWithAgeHandler',
        "сколько ты знаешь исполнителей младше 333 лет?": 'NumberWithAgeHandler',
        "сколько ты знаешь исполнителей от 32 до 43 лет?": 'NumberWithAgeRangeHandler',
        "сколько исполнителей младше 0 лет?": 'NumberWithAgeHandler',
        "вернись в начало": 'RestartHandler',
        "в начало": 'RestartHandler',
    }
    test_info = {
        'расскажи про кровосток': 'InfoHandler',
        'информация про кизару': 'InfoHandler',
        'информация о касте': 'InfoHandler',
        'хочу узнать о многоточии': 'InfoHandler',
        'кто ты?': 'InfoAboutBotHandler',
        'что ты?': 'InfoAboutBotHandler',
        'что ты за программа?': 'InfoAboutBotHandler',
        'что ты можешь?': 'InfoAboutBotOpportunitiesHandler',
        'что ты умеешь?': 'InfoAboutBotOpportunitiesHandler',
        'какие у тебя есть функции?': 'InfoAboutBotOpportunitiesHandler',
        'перечисли свои функции?': 'InfoAboutBotOpportunitiesHandler',
        'расскажи про свой алгоритм': 'InfoAboutBotAlgorithmHandler',
        'какой твой алгоритм?': 'InfoAboutBotAlgorithmHandler',
        'как ты устроен?': 'InfoAboutBotAlgorithmHandler',
        'каково твоё устройство?': 'InfoAboutBotAlgorithmHandler',
        'как ты работаешь?': 'InfoAboutBotAlgorithmHandler',
    }

    def __init__(self):
        self._sentence_handler_pairs = self.get_sentence_handler_pairs

    @property
    def get_sentence_handler_pairs(self) -> Dict[str, str]:
        sentence_handler_pairs = {}
        test_data_sets = [
            self.search_by_name, self.recommendation, self.search_by_genre, self.search_by_sex,
            self.search_by_age, self.search_show_all, self.test_filter, self.like_dislike, self.number_queries,
            self.test_info
        ]
        for test_set in test_data_sets:
            for sentence, handler in test_set.items():
                sentence_handler_pairs.update({sentence: handler})
        return sentence_handler_pairs

    def get_handler_class(self, sentence: str):
        return self._sentence_handler_pairs[sentence]


TEST_DATA = DataForTests()


class TestQuerySolving(unittest.TestCase):
    def setUp(self) -> None:
        self.query_solver = QuerySolver(User())

    def _test_sentences(self, state: DialogState, sentences: Dict[str, str]):
        for sentence, expected_handler in sentences.items():
            with self.subTest(i=sentence):
                with unittest.mock.patch(
                        f'hiphop_bot.dialog_bot.query_handling.handlers.{expected_handler}.handle'
                ) as patched_handle_method:
                    self.query_solver.state = state
                    query = SentenceParser(sentence).parse(self.query_solver.state)
                    self.query_solver.solve(query)

                    patched_handle_method.assert_called()

    def test_search_by_name(self):
        self._test_sentences(DialogState.start, DataForTests.search_by_name)

    def test_recommend(self):
        self._test_sentences(DialogState.start, DataForTests.recommendation)

    def test_search_by_genre(self):
        self._test_sentences(DialogState.start, DataForTests.search_by_genre)

    def test_search_by_sex(self):
        self._test_sentences(DialogState.start, DataForTests.search_by_sex)

    def test_search_by_age(self):
        self._test_sentences(DialogState.start, DataForTests.search_by_age)

    def test_search_show_all(self):
        self._test_sentences(DialogState.start, DataForTests.search_show_all)

    def test_filter(self):
        self._test_sentences(DialogState.search, DataForTests.test_filter)

    def test_like_dislike(self):
        self._test_sentences(DialogState.start, DataForTests.like_dislike)

    def test_number_queries(self):
        self._test_sentences(DialogState.start, DataForTests.number_queries)

    def test_info(self):
        self._test_sentences(DialogState.start, DataForTests.test_info)


class TestIntegrationStates(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User()
        self.dialog = Dialog()

    def check_next_states(self, state, allowed_sentences: list, disallowed_sentences: list):
        query_solver = QuerySolver(self.user)

        sentences = {
            'allowed': allowed_sentences,
            'disallowed': disallowed_sentences,
        }

        for allowed_disallowed, sentences_ in sentences.items():
            for sentence in sentences_:
                expected_handler = TEST_DATA.get_handler_class(sentence)
                with self.subTest(i=expected_handler):
                    query_solver.state = state
                    with unittest.mock.patch(
                            f'hiphop_bot.dialog_bot.query_handling.handlers.{expected_handler}.handle'
                    ) as patched_handle_method:
                        query = SentenceParser(sentence).parse(query_solver.state)
                        query_solver.solve(query)

                        if allowed_disallowed == 'allowed':
                            patched_handle_method.assert_called()
                        else:
                            self.assertFalse(patched_handle_method.called)

    def test_next_states_start(self):
        """ Проверяет в какие состояния можно перейти из состояния start"""
        allowed = [
            "найди похожих исполнителей на крека",
            "убери моргенштерна из списка дизлайков",
            "сколько исполнителей в базе?",
            "информация о касте"
        ]
        disallowed = [
            "оставь исполнителей мужского пола",
        ]

        self.check_next_states(DialogState.start, allowed, disallowed)

    def test_next_states_search(self):
        """ Проверяет в какие состояния можно перейти из состояния search"""
        allowed = [
            "оставь исполнителей мужского пола",
        ]
        disallowed = [
            "убери моргенштерна из списка дизлайков",
            "сколько исполнителей в базе?",
            "информация о касте",
            "артисты мужчины",
        ]

        self.check_next_states(DialogState.search, allowed, disallowed)

    def test_next_states_filter(self):
        """ Проверяет в какие состояния можно перейти из состояния filter"""
        allowed = [
            "оставь исполнителей мужского пола",
        ]
        disallowed = [
            "убери моргенштерна из списка дизлайков",
            "сколько исполнителей в базе?",
            "информация о касте",
            "артисты мужчины",
        ]

        self.check_next_states(DialogState.filter, allowed, disallowed)

    def test_next_states_like(self):
        """ Проверяет в какие состояния можно перейти из состояния like"""
        allowed = [
            "найди похожих исполнителей на крека",
            "убери моргенштерна из списка дизлайков",
            "сколько исполнителей в базе?",
            "информация о касте"
        ]
        disallowed = [
            "оставь исполнителей мужского пола",
        ]

        self.check_next_states(DialogState.like, allowed, disallowed)

    def test_next_states_dislike(self):
        """ Проверяет в какие состояния можно перейти из состояния dislike"""
        allowed = [
            "найди похожих исполнителей на крека",
            "убери моргенштерна из списка дизлайков",
            "сколько исполнителей в базе?",
            "информация о касте"
        ]
        disallowed = [
            "оставь исполнителей мужского пола",
        ]

        self.check_next_states(DialogState.dislike, allowed, disallowed)

    def test_next_states_number(self):
        """ Проверяет в какие состояния можно перейти из состояния number"""
        allowed = [
            "найди похожих исполнителей на крека",
            "убери моргенштерна из списка дизлайков",
            "сколько исполнителей в базе?",
            "информация о касте"
        ]
        disallowed = [
            "оставь исполнителей мужского пола",
        ]

        self.check_next_states(DialogState.number, allowed, disallowed)

    def test_next_states_info(self):
        """ Проверяет в какие состояния можно перейти из состояния info"""
        allowed = [
            "найди похожих исполнителей на крека",
            "убери моргенштерна из списка дизлайков",
            "сколько исполнителей в базе?",
            "информация о касте"
        ]
        disallowed = [
            "оставь исполнителей мужского пола",
        ]

        self.check_next_states(DialogState.info, allowed, disallowed)

    @unittest.skip('.solve больще не возвращает дебаг значения')
    def test_repeat_states(self):
        """ Проверяет, что можно делать подряд несколько запросов для одного состояния"""
        query_solver = QuerySolver(self.user)

        sentences = [
            "найди похожих исполнителей на крека",
            "все исполнители",
            "найди исполнителей в жанре грайм",

            "оставь исполнителей мужского пола",
            "оставь только соло исполнителей",

            "убери моргенштерна из списка дизлайков",
            "добавь моргенштерна в список дизлайков",

            "сколько исполнителей мужчин ты знаешь?",
            "сколько исполнителей в базе?",

            "информация о касте",
        ]

        for sentence in sentences:
            expected_handler = TEST_DATA.get_handler_class(sentence)
            with self.subTest(i=expected_handler):
                query = SentenceParser(sentence).parse(query_solver.state)
                res = query_solver.solve(query)
                self.assertEqual(res, expected_handler)

    @unittest.skip('.solve больще не возвращает дебаг значения')
    def test_states_integration(self):
        """
        Проверяет корректную обработку запросов для разных состояний
        QuerySolver принимает по порядку следующие состояния:
        поиск, фильтрация, лайк, дизлайк, количественный запрос, информационный запрос
        """
        query_solver = QuerySolver(self.user)

        sentences = [
            "найди похожих исполнителей на крека",

            "оставь исполнителей мужского пола",

            "убери моргенштерна из списка дизлайков",

            "добавь моргенштерна в список дизлайков",

            "сколько исполнителей в базе?",

            "информация о касте",
        ]

        for sentence in sentences:
            expected_handler = TEST_DATA.get_handler_class(sentence)
            with self.subTest(i=expected_handler):
                query = SentenceParser(sentence).parse(query_solver.state)
                res = query_solver.solve(query)
                self.assertEqual(res, expected_handler)


