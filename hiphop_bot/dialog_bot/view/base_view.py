from abc import ABC, abstractmethod
from hiphop_bot.dialog_bot.view.answer_generator import AnswerGenerator
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog
from hiphop_bot.dialog_bot.view.output_message import Output
from hiphop_bot.dialog_bot.services.query_solving.query_solver import QuerySolvingState


class View(ABC):
    _hello_message = (
        "Вас приветствует HipHopBot!\n\n"
        "Я кое-что знаю о русском хип-хопе и готов ответить на ваши вопросы по этой теме.\n\n"
        "Кстати, я не совсем обычный телеграм-бот. У меня нет заранее заданного списка команд.\n"
        "Я буду пытаться понимать вашу естественную речь, например, просьбу "
        "'порекомендуй артистов, которые мне понравятся' или 'покажи соло артистов типа касты'.\n"
        "В разговоре со мной не обязательно соблюдать правила пунктуации и писать имена артистов с большой буквы.\n"
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
    def _send_message(self, msg: str):
        pass

    def view(self, query_solving_res: QuerySolvingState, dialog: Dialog, user: User):
        output: Output = self._generate_answer(dialog=dialog, user=user)

        if query_solving_res == QuerySolvingState.SOLVED:
            if output.debug_msg:
                self._send_message(output.debug_msg)
            if output.artists:
                self._send_message(output.artists)
            if output.genres:
                self._send_message(output.genres)
            if output.info:
                self._send_message(output.info)
            if output.additional_msg:
                self._send_message(output.additional_msg)
        elif query_solving_res == QuerySolvingState.UNSOLVED:
            self._send_message(self._unresolved_answer)
        else:
            raise Exception('Unknown query_solver result')