from src.card import Card
from src.deck import Deck

cards = [Card('b', 3), Card('b', 0), Card('g', 7)]

def test_init():
    d = Deck(cards=cards)
    assert d.cards == cards

def test_save():
    d = Deck(cards=cards)
    assert d.save() == 'b3 b0 g7'

    d = Deck(cards=[])
    assert d.save() == ''

def test_load():
    d = Deck.load('b3 b0 g7')
    expected_deck = Deck(cards)
    print(type(d), d)
    print(type(expected_deck), expected_deck)
    assert d == expected_deck
