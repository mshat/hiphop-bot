DEBUG = True

DEBUG_QUERY_HANDLER = True
DEBUG_QUERY_HANDLER_PATTERN_MATCHING = False

DEBUG_OUTPUT = False

DEBUG_DB = False

DEBUG_TG_INTERFACE = True

ERROR_PRINT = True

if not DEBUG:
    DEBUG_QUERY_HANDLER = False
    DEBUG_QUERY_HANDLER_PATTERN_MATCHING = False
    DEBUG_OUTPUT = False
    DEBUG_DB = False
    DEBUG_TG_INTERFACE = False
    ERROR_PRINT = False
