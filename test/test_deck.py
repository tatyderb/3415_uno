import random

from src.card import Card
from src.deck import Deck

cards = [Card('b', 3), Card('b', 0), Card('g', 7)]

def test_init():
    d = Deck(cards=cards)
    assert d.cards == cards

def test_init_shuffle():
    """Проверяем, что карт столько же, но они в другом порядке."""
    full_deck1 = Deck(None)
    full_deck2 = Deck(None)
    assert full_deck1.cards != full_deck2.cards
    assert sorted(full_deck1.cards) == sorted(full_deck2.cards)


def test_save():
    d = Deck(cards=cards)
    assert d.save() == 'b3 b0 g7'

    d = Deck(cards=[])
    assert d.save() == ''

def test_load():
    d = Deck.load('b3 b0 g7')
    expected_deck = Deck(cards)
    # print()
    # print(type(d), d)
    # print(type(expected_deck), expected_deck)
    # так можно сравнивать, если нет метода __eq__
    assert str(d) == str(expected_deck)
    # так можно сравнивать, если есть метод __eq__
    assert d == expected_deck

def test_draw_card():
    d1 = Deck.load('b3 b0 g7')
    d2 = Deck.load('b3 b0')
    c = d1.draw_card()
    assert c == Card.load('g7')
    assert d1 == d2


def test_shuffle_1():
    cards = Card.all_cards(['b', 'r'], numbers=[5, 2, 9])
    deck = Deck(cards=cards)
    deck_list = [deck.save()]
    for i in range(5):
        deck.shuffle()
        s = deck.save()
        assert s not in deck_list
        deck_list.append(s)

def test_shuffle_2():
    random.seed(3)

    cards = Card.all_cards(['b', 'r'], numbers=[5, 2, 9])
    deck = Deck(cards=cards)
    deck_list = [deck.save()]

    deck.shuffle()
    assert deck.save() == 'b5 b9 r5 r9 r2 b2'

    deck.shuffle()
    assert deck.save() == 'b9 r9 r5 b5 r2 b2'

    deck.shuffle()
    assert deck.save() == 'r2 b2 b9 r9 r5 b5'


