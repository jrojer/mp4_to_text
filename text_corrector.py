from completer import Completer


SYSTEM_PROMPT = """\
Вы редактор текста. 
Вам даны фрагменты текста лекции по лингвистике.
Текст получен в результате распознавания речи.
Ваша задача: 
 - исправить ошибки в тексте.
 - удалить несущественные фрагменты
 - записать предложения более лаконично

Текст лекции отредактированный ранее:
'''
{}
'''
"""

MESSAGE_PROMPT = """\
Отредактируйте текст:
'''
{}
'''
"""


class TextCorrector:
    def __init__(self, previous_text: str) -> None:
        self.previous_text = previous_text

    def correct(self, text: str) -> str:
        return Completer(SYSTEM_PROMPT.format(self.previous_text)).complete(
            MESSAGE_PROMPT.format(text)
        )
