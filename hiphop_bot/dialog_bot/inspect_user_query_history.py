from typing import List
from hiphop_bot.dialog_bot.models.tg_user import TelegramUserModel
from hiphop_bot.dialog_bot.models.user_query_history import UserQueryHistoryModel, _UserQueryHistory


def show_user_query_history(user_history: List[_UserQueryHistory]):
    for user_history in user_history:
        for history_item in user_history.history:
            print(f'{user_history.tg_user.full_name} {user_history.tg_user.user_id} {history_item}')


def print_all_unresolved_queries():
    model = UserQueryHistoryModel()

    unresolved = model.get_all_unresolved_queries()
    show_user_query_history(unresolved)


def print_user_history(user_id):
    model = UserQueryHistoryModel()
    tg_user_model = TelegramUserModel()
    tg_user = tg_user_model.get_by_user_id(user_id)
    user_history = model.get_user_history(tg_user)
    show_user_query_history(user_history)


if __name__ == '__main__':
    # print_user_history(459519389)
    print_all_unresolved_queries()
