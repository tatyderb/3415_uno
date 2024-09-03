import pytest

from src.card import Card


def test_init():
    c = Card('y', 3)
    assert c.color == 'y'
    assert c.number == 3

def test_save():
    c = Card('y', 3)
    assert repr(c) == 'y3'
    assert c.save() == 'y3'

    c = Card('g', 7)
    assert repr(c) == 'g7'
    assert c.save() == 'g7'

def test_eq():
    c1 = Card('y', 3)
    c2 = Card('y', 3)
    c3 = Card('y', 1)
    c4 = Card('g', 3)
    c5 = Card('b', 7)

    assert c1 == c2
    assert c1 != c3
    assert c1 != c4
    assert c1 != c5

def test_load():
    s = 'y3'
    c = Card.load(s)
    assert c == Card('y', 3)

    s = 'b6'
    c = Card.load(s)
    assert c == Card('b', 6)

def test_divzero():
    # пример теста с ловлей исключения
    with pytest.raises(ZeroDivisionError):
        x = 2 / 0
        # y = 3 / 15

def test_validation():
    with pytest.raises(ValueError):
        Card('yellow', 1)
    with pytest.raises(ValueError):
        Card('ф', 1)
    with pytest.raises(ValueError):
        Card('b', 10)
    with pytest.raises(ValueError):
        Card('b', '3')

def test_play_on():
    c1 = Card.load('y1')
    c2 = Card.load('y5')
    c3 = Card.load('g1')
    c4 = Card.load('g6')

    assert c1.can_play_on(c1)
    assert c2.can_play_on(c1)
    assert c1.can_play_on(c2)
    assert c3.can_play_on(c1)
    assert not c4.can_play_on(c1)

