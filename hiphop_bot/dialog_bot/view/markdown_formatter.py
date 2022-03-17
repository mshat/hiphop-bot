from typing import List


class MarkdownFormatter:
    def __init__(self, text: str = None):
        if text:
            self._text = text
            self._escape_markdown_reserved_characters()
        else:
            self._text = None

    @property
    def raw_text(self) -> str | None:
        return self._text

    @raw_text.setter
    def raw_text(self, val: str):
        self._text = val
        self._escape_markdown_reserved_characters()

    @property
    def formatted_text(self) -> str:
        res = ''
        if self._text:
            res = self._text
            self._text = None
        return res

    def _escape_markdown_reserved_characters(self) -> None:
        markdown_reserved = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in markdown_reserved:
            self._text = self._text.replace(char, f'\{char}')

    def make_bold_lines(self, line_nums: List[int]) -> None:
        msg_lines = self._text.split('\n')
        for line_num in line_nums:
            msg_lines[line_num] = f'*{msg_lines[line_num]}*'
        self._text = '\n'.join(msg_lines)