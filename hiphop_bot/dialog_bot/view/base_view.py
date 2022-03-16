from abc import ABC, abstractmethod
from hiphop_bot.dialog_bot.view.answer_generator import AnswerGenerator
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog
from hiphop_bot.dialog_bot.view.output_message import Output
from hiphop_bot.dialog_bot.services.query_solving.query_solver import QuerySolvingState


class View(ABC):
    _hello_message = (
        "Вас приветствует разговорный бот.\n"
        "Я кое-что знаю о русском хип-хопе и готов ответить на ваши вопросы по этой теме.\n"
        "Вы можете узнать о моих возможностях, спросив меня об этом.\n"
    )
    _blank_query_answer = 'Вы что-то хотели?..'
    _unresolved_answer = 'Я вас не понял :('

    def __init__(self):
        self._answer_generator = AnswerGenerator()

    def _generate_answer(self, dialog: Dialog, user: User) -> Output:
        self._answer_generator.dialog = dialog
        self._answer_generator.user = user
        output: Output = self._answer_generator.generate_answer()
        return output

    @abstractmethod
    def view(self, query_solving_res: QuerySolvingState, dialog: Dialog, user: User):
        pass