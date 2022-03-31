from hiphop_bot.dialog_bot.view.base_view import View
from hiphop_bot.dialog_bot.services.query_solving.dialog import Dialog
from hiphop_bot.dialog_bot.services.query_solving.dialog import DialogState


class ConsoleView(View):
    def __init__(self, line_len: int = 120):
        super().__init__()
        self._line_len = line_len
        self._hello_message = f"{'='*self._line_len}\n{self._hello_message}\n{'='*self._line_len}"

    def get_input_prompt(self, dialog: Dialog):
        input_prompt = 'ФИЛЬТР -> ' if dialog.state == DialogState.FILTER else 'ЗАПРОС -> '
        return input_prompt

    def _send_message(self, msg: str):
        msg = msg.strip()
        print(msg)
        print()

    def send_blank_mgs(self):
        self._send_message('')

    def view_hello_message(self):
        self._send_message(self._hello_message)

    def view_blank_query_answer(self):
        self._send_message(self._blank_query_answer)
