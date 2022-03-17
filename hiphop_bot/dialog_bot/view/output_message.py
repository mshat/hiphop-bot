class OutputMessageError(Exception): pass


class OutputMessage:
    _msg: str

    def __init__(self):
        self._msg = ''

    @property
    def msg(self) -> str:
        return self._msg

    @msg.setter
    def msg(self, val: str):
        if not isinstance(val, str):
            raise OutputMessageError('Argument must be of type str')
        if val != '':
            self._msg = val
            self._msg += '\n'


class Output:
    def __init__(self):
        self._artists = OutputMessage()
        self._genres = OutputMessage()
        self._info = OutputMessage()
        self._debug_msg = OutputMessage()

    @property
    def artists(self) -> str:
        return self._artists.msg

    @artists.setter
    def artists(self, msg: str) -> None:
        self._artists.msg = msg

    @property
    def genres(self) -> str:
        return self._genres.msg

    @genres.setter
    def genres(self, msg: str) -> None:
        self._genres.msg = msg

    @property
    def info(self) -> str:
        return self._info.msg

    @info.setter
    def info(self, msg: str) -> None:
        self._info.msg = msg

    @property
    def debug_msg(self) -> str:
        return self._debug_msg.msg

    @debug_msg.setter
    def debug_msg(self, msg: str) -> None:
        self._debug_msg.msg = msg
