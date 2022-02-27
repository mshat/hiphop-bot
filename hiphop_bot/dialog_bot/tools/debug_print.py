from hiphop_bot.dialog_bot.config import DEBUG_PRINT


def debug_print(*args, **kwargs):
    if DEBUG_PRINT:
        print(*args, **kwargs)


def debug_print_decorator(function):
    def wrapper(*args, **kwargs):
        if DEBUG_PRINT:
            print(f'[DEBUG] {args[0].debug_msg}')
        return function(*args, **kwargs)

    return wrapper


def debug_print_with_arg(msg: str):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if DEBUG_PRINT:
                print(f'[DEBUG] {msg}')
            return function(*args, **kwargs)

        return wrapper
    return decorator
