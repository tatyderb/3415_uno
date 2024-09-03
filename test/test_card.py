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



