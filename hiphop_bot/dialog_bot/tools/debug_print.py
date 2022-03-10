from hiphop_bot.dialog_bot.config import DEBUG_PRINT


def debug_print(*args, **kwargs):
    if DEBUG_PRINT:
        print('[DEBUG] ', end='')
        print(*args, **kwargs)


def debug_message(msg: str):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if DEBUG_PRINT:
                print(f'[DEBUG] {msg}')
            return function(*args, **kwargs)

        return wrapper
    return decorator
