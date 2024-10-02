import random

from src.card import Card
from src.hand import Hand

cards = [Card("b", 3), Card("b", 0), Card("g", 7)]


def test_init():
    d = Hand(cards=cards)
    assert d.cards == cards


def test_save():
    d = Hand(cards=cards)
    assert d.save() == "b3 b0 g7"

    d = Hand(cards=[])
    assert d.save() == ""


def test_load():
    d = Hand.load("b3 b0 g7")
    expected_deck = Hand(cards)
    # print()
    # print(type(d), d)
    # print(type(expected_deck), expected_deck)
    # так можно сравнивать, если нет метода __eq__
    assert str(d) == str(expected_deck)
    # так можно сравнивать, если есть метод __eq__
    assert d == expected_deck


def test_score():
    h = Hand.load("b3 b0 g7")
    assert h.score() == 10

    h = Hand.load("b2 b9")
    assert h.score() == 11


def test_add_card():
    h = Hand.load("b3 b0 g7")
    h.add_card(Card.load("y2"))
    assert repr(h) == "b3 b0 g7 y2"

    h.add_card(Card.load("r8"))
    assert repr(h) == "b3 b0 g7 y2 r8"


def test_remove_card():
    h = Hand.load("b3 b0 g7 y2 r8")
    c = Card.load("g7")
    h.remove_card(c)
    assert repr(h) == "b3 b0 y2 r8"
