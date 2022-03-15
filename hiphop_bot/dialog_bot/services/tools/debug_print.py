from hiphop_bot.dialog_bot.config import ERROR_PRINT


def debug_print(debug_flag: bool, *args, **kwargs):
    if debug_flag:
        print('[DEBUG] ', end='')
        print(*args, **kwargs)


def error_print(*args, **kwargs):
    if ERROR_PRINT:
        print('[ERROR] ', end='')
        print(*args, **kwargs)


def debug_message(debug_flag: bool, msg: str):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if debug_flag:
                print(f'[DEBUG] {msg}')
            return function(*args, **kwargs)

        return wrapper
    return decorator
