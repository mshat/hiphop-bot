DEBUG = True  # Общий дебаг флаг. Если имеет значение False, отключаются все остальные флаги

SHOW_PROXIMITY_MODE = False

DEBUG_RECOMMENDER_SYSTEM = True  # Флаг для вывода отладочных сообщений рекоммендательной системы

DEBUG_QUERY_HANDLER = True  # Флаг для вывода отладочных сообщений модуля query_handling
DEBUG_QUERY_HANDLER_PATTERN_MATCHING = False  # Флаг для вывода отладочных сообщений паттерн мэтчера

DEBUG_OUTPUT = False  # Флаг для вывода отладочных сообщений в выводе юзера

DEBUG_DB = False  # Флаг для вывода отладочных сообщений модуля connection_pool

DEBUG_MODEL = True  # Флаг для вывода отладочных сообщений моделей БД

DEBUG_TG_INTERFACE = True  # Флаг для вывода отладочных сообщений телеграм интерфейса (принятые сообщения и результат их обработки)

ERROR_PRINT = True  # Флаг для вывода сообщений об ошибках

if not DEBUG:
    DEBUG_RECOMMENDER_SYSTEM = False
    DEBUG_QUERY_HANDLER = False
    DEBUG_QUERY_HANDLER_PATTERN_MATCHING = False
    DEBUG_OUTPUT = False
    DEBUG_DB = False
    DEBUG_MODEL = False
    DEBUG_TG_INTERFACE = False
    ERROR_PRINT = False
    SHOW_PROXIMITY_MODE = False
