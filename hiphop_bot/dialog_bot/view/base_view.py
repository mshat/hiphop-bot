from abc import ABC, abstractmethod
from hiphop_bot.dialog_bot.view.answer_generator import AnswerGenerator
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog
from hiphop_bot.dialog_bot.view.output_message import Output
from hiphop_bot.dialog_bot.services.query_solving.query_solver import QuerySolvingState
from hiphop_bot.dialog_bot.services.query_solving.dialog import DialogState
from hiphop_bot.dialog_bot.config import DEBUG_OUTPUT


class View(ABC):
    _hello_message = (
        "Вас приветствует HipHopBot!\n\n"
        "Я кое-что знаю о русском хип-хопе и готов ответить на ваши вопросы по этой теме.\n\n"
        "Кстати, я не совсем обычный телеграм-бот. У меня нет заранее заданного списка команд.\n"
        "Я буду пытаться понимать вашу естественную речь, например, запросы:\n"
        "'порекомендуй артистов, которые мне понравятся' или 'покажи соло артистов типа касты'.\n"
        "В разговоре со мной не обязательно соблюдать правила пунктуации и писать имена артистов с большой буквы.\n"
    )
    _blank_query_answer = 'Вы что-то хотели?..'
    _unresolved_answer = 'Я вас не понял :('
    _you_can_filter_msg = (
        'Вы можете добавлять фильтры к полученному результату поиска.\n'
        'Например, "оставь только дуэты", "убери артистов старше 30 лет" или "выводи по 5 артистов".\n'
    )

    def __init__(self):
        self._answer_generator = AnswerGenerator()

    def _generate_answer(self, dialog: Dialog, user: User) -> Output:
        self._answer_generator.dialog = dialog
        self._answer_generator.user = user
        output: Output = self._answer_generator.generate_answer()
        return output

    @abstractmethod
    def _send_message(self, msg: str):
        pass

    def view(self, query_solving_res: QuerySolvingState, dialog: Dialog, user: User):
        output: Output = self._generate_answer(dialog=dialog, user=user)

        if query_solving_res == QuerySolvingState.SOLVED:
            if DEBUG_OUTPUT and output.debug_msg:
                self._send_message(output.debug_msg)
            if output.artists:
                if output.filters:
                    self._send_message(output.filters)
                self._send_message(output.artists)

                # сообщение о том, что можно добавить фильтры
                if dialog.state == DialogState.SEARCH:
                    if not user.has_filters:
                        self._send_message(self._you_can_filter_msg)
            if output.genres:
                self._send_message(output.genres)
            if output.info:
                self._send_message(output.info)
        elif query_solving_res == QuerySolvingState.UNSOLVED:
            self._send_message(self._unresolved_answer)
        else:
            raise Exception('Unknown query_solver result')