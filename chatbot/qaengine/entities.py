__author__ = 'roloprogramating'


class Question:
    def __init__(self, id, text, answer=None):
        self._id = id
        self._text = text
        self._answer = answer

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def id(self):
        return self._id

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, ans):
        self._answer = ans


class Answer:
    def __init__(self, type, text, content):
        self._type = type
        self._text=text
        self._content = content

    @property
    def type(self):
        return self._type

    @property
    def text(self):
        return self._text

    @property
    def content(self):
        return self._content

