from hiphop_bot.dialog_bot.sentence_analyzer.sentence_parser import SentenceParser
from hiphop_bot.dialog_bot.query_solving.query_solver import QuerySolver, QuerySolvingState
from hiphop_bot.dialog_bot.query_solving.user import User


class UserInterface:
    _user: User
    _query_solver: QuerySolver
    # _view:
    hello_message = (
        "Вас приветствует разговорный бот.\n"
        "Я кое-что знаю о русском хип-хопе и готов ответить на ваши вопросы по этой теме.\n"
        "Вы можете узнать о моих возможностях, спросив меня об этом."
    )
    blank_query_answer = 'Вы что-то хотели?..'
    unresolved_answer = 'Я вас не понял :('

    def __init__(self):
        self._user = User()
        self._query_solver = QuerySolver(self.user)

    @property
    def user(self):
        return self._user

    @property
    def dialog(self):
        return self._query_solver.dialog

    @property
    def state(self):
        return self._query_solver.state

    def solve_query(self, sentence: str) -> QuerySolvingState:
        query = SentenceParser(sentence).parse(self._query_solver.state)
        res = self._query_solver.solve(query)
        return res
