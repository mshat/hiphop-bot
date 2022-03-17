from hiphop_bot.dialog_bot.controller.controller import UserInterfaceController
from hiphop_bot.dialog_bot.view.console_view import ConsoleView


def main():
    controller = UserInterfaceController()
    view = ConsoleView()

    view.view_hello_message()

    while True:
        sentence = input(view.get_input_prompt(controller.dialog))

        if sentence == '':
            view.view_blank_query_answer()
            continue
        query_solving_res = controller.solve_query(sentence)
        view.view(query_solving_res, controller.dialog, controller.user)
        view.send_blank_mgs()


if __name__ == '__main__':
    main()
