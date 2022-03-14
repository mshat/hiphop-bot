from hiphop_bot.dialog_bot.query_solving.query_solver import QuerySolvingState
from hiphop_bot.dialog_bot.query_solving.dialog import DialogState
from hiphop_bot.dialog_bot.config import DEBUG
from hiphop_bot.dialog_bot.data.const import LINE_LEN
from hiphop_bot.dialog_bot.view.answer_generator import AnswerGenerator
from hiphop_bot.dialog_bot.controller.controller import UserInterfaceController


def main():
    controller = UserInterfaceController()
    answer_generator = AnswerGenerator()

    print(f'{"="*LINE_LEN}\n{controller.hello_message} \n{"="*LINE_LEN}')

    while True:
        input_prompt = 'ФИЛЬТР -> ' if controller.state in (DialogState.SEARCH, DialogState.FILTER) else 'ЗАПРОС -> '

        sentence = input(input_prompt)

        if sentence == '':
            print(controller.blank_query_answer)
            continue

        query_solving_res = controller.solve_query(sentence)

        if query_solving_res == QuerySolvingState.SOLVED:
            answer_generator.dialog = controller.dialog
            answer_generator.user = controller.user
            answer, additional_message = answer_generator.generate_answer()
            print(answer)
            if additional_message:
                print(additional_message)
        elif query_solving_res == QuerySolvingState.UNSOLVED:
            print(controller.unresolved_answer)
        else:
            raise Exception('Unknown query_solver result')

        if DEBUG:
            print('[CURRENT STATE]', controller.state)
        print()


if __name__ == '__main__':
    main()
