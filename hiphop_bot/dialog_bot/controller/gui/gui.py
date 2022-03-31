import PySimpleGUI as sg
from hiphop_bot.dialog_bot.controller.controller import UserInterfaceController
from hiphop_bot.dialog_bot.view.console_view import ConsoleView


input_frame = sg.Frame('Input', [[sg.InputText(key='_input_', size=(62, 1))]])
output_frame = sg.Frame('Output', [[sg.Multiline(key='_output_', size=(60, 35))]])
layout = [
    [input_frame],
    [output_frame],
    [sg.Submit('Отправить'), sg.Button('Очистить')]
]


class Gui:
    def __init__(self):
        self.window = sg.Window('Hiphop dialog bot', layout, font=("Helvetica, 12")).Finalize()
        self.window.move(self.window.CurrentLocation()[0], 0)

        self.controller = UserInterfaceController()
        self.view = ConsoleView(0)
        self.view._send_message = self.print_msg

        self.view.view_hello_message()

    def _print(self, msg: str):
        self.window['_output_'].print(msg)

    def print_msg(self, msg: str):
        msg = msg.strip()
        self._print(msg)
        self._print('')

    def clean_input(self):
        self.window['_input_'].Update('')

    def clean_output(self):
        self.window['_output_'].Update('')

    def handle_message(self, input_msg: str):
        if input_msg == '':
            self.view.view_blank_query_answer()
            return
        query_solving_res = self.controller.solve_query(input_msg)
        self.view.view(query_solving_res, self.controller.dialog, self.controller.user)

    def show(self):
        while True:
            event, values = self.window.read()

            if event in (sg.WIN_CLOSED, None, 'Exit', 'Cancel'):
                break
            if not event and not values:
                continue

            if event == 'Очистить':
                self.clean_input()
                self.clean_output()

            if event == 'Отправить':
                query = f" {values['_input_']} "
                self._print(query.center(60, '='))
                self.clean_input()
                self.handle_message(values['_input_'])

        self.window.close()


def run():
    gui = Gui()
    gui.show()


if __name__ == '__main__':
    run()

