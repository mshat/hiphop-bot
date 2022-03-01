class OutputMessage:
    _msg: str

    def __init__(self):
        self._msg = ''

    @property
    def msg(self) -> str:
        return self._msg

    @msg.setter
    def msg(self, val: str):
        self._msg = val
        self._msg += '\n'