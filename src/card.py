"""Карты UNO."""


class Card:
    def __init__(self, color: str, number: int):
        self.color = color
        self.number = number

    def __repr__(self):
        # 'r3'
        return f'{self.color}{self.number}'

    def save(self):
        return repr(self)

