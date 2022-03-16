from hiphop_bot.dialog_bot.services.sentence_analyzer.sentence_parser import SentenceParser
from hiphop_bot.dialog_bot.services.query_solving.query_solver import QuerySolver, QuerySolvingState
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog, DialogState


class UserInterfaceController:
    _user: User
    _query_solver: QuerySolver

    def __init__(self, username: str = None):
        self._user = User(username) if username else User()
        self._query_solver = QuerySolver(self.user)

    @property
    def user(self) -> User:
        return self._user

    @property
    def dialog(self) -> Dialog:
        return self._query_solver.dialog

    def solve_query(self, sentence: str) -> QuerySolvingState:
        query = SentenceParser(sentence).parse()
        res = self._query_solver.solve(query)
        return res
