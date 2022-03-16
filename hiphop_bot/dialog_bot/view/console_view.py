from hiphop_bot.dialog_bot.view.base_view import View
from hiphop_bot.dialog_bot.services.query_solving.user import User
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog
from hiphop_bot.dialog_bot.view.output_message import Output
from hiphop_bot.dialog_bot.services.query_solving.query_solver import QuerySolvingState
from hiphop_bot.dialog_bot.services.query_solving.dialog import DialogState


class ConsoleView(View):
    LINE_LEN = 120

    def __init__(self):
        super().__init__()

        self._hello_message = f"{'='*self.LINE_LEN}\n{self._hello_message}\n{'='*self.LINE_LEN}"

    def get_input_prompt(self, dialog: Dialog):
        input_prompt = 'ФИЛЬТР -> ' if dialog.state == DialogState.FILTER else 'ЗАПРОС -> '
        return input_prompt

    def view(self, query_solving_res: QuerySolvingState, dialog: Dialog, user: User):
        output: Output = self._generate_answer(dialog=dialog, user=user)

        if query_solving_res == QuerySolvingState.SOLVED:
            if output.debug_msg:
                print(output.debug_msg, end='')
            if output.artists:
                print(output.artists, end='')
            if output.genres:
                print(output.genres, end='')
            if output.info:
                print(output.info, end='')
            if output.additional_msg:
                print(output.additional_msg, end='')
        elif query_solving_res == QuerySolvingState.UNSOLVED:
            print(self._unresolved_answer)
        else:
            raise Exception('Unknown query_solver result')

    def view_hello_message(self):
        print(self._hello_message)

    def view_blank_query_answer(self):
        print(self._blank_query_answer)
