from hiphop_bot.dialog_bot.query_solving.query_solver import QuerySolvingState
from hiphop_bot.dialog_bot.query_solving.dialog import DialogState
from hiphop_bot.dialog_bot.config import DEBUG
from hiphop_bot.dialog_bot.data.const import LINE_LEN
from hiphop_bot.base_user_interface.view import AnswerGenerator
from hiphop_bot.base_user_interface.user_interface import UserInterface


def main():
    interface = UserInterface()
    answer_generator = AnswerGenerator()

    print(f'{"="*LINE_LEN}\n{interface.hello_message} \n{"="*LINE_LEN}')

    while True:
        input_prompt = 'ФИЛЬТР -> ' if interface.state in (DialogState.search, DialogState.filter) else 'ЗАПРОС -> '

        sentence = input(input_prompt)

        if sentence == '':
            print(interface.blank_query_answer)
            continue

        query_solving_res = interface.solve_query(sentence)

        if query_solving_res == QuerySolvingState.solved:
            answer_generator.dialog = interface.dialog
            answer_generator.user = interface.user
            answer = answer_generator.generate_answer()
            print(answer)
        elif query_solving_res == QuerySolvingState.unsolved:
            print(interface.unresolved_answer)
        else:
            raise Exception('Unknown query_solver result')

        if DEBUG: print('[CURRENT STATE]', interface.state)
        print()


if __name__ == '__main__':
    main()
