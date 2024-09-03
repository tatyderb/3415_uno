"""Карты UNO."""
from typing import Self


class Card:
    COLORS = ['r', 'g', 'b', 'y']
    NUMBERS = list(range(10))

    def __init__(self, color: str, number: int):
        if color not in Card.COLORS:
            raise ValueError
        if number not in Card.NUMBERS:
            raise ValueError
        self.color = color
        self.number = number

    def __repr__(self):
        # 'r3'
        return f'{self.color}{self.number}'

    def __eq__(self, other):
        return self.color == other.color and self.number == other.number

    def save(self):
        return repr(self)

    @staticmethod
    def load(text: str):
        """From 'y3' to Card('y', 3)."""
        return Card(color=text[0], number=int(text[1]))

    def can_play_on(self, other: Self) -> bool:
        """Можно ли играть карту self на карту other."""
        return self.color == other.color or self.number == other.number

