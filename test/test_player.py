from src.hand import Hand
from src.player import Player


def test_init():
    h = Hand.load("y1 g3 b2")
    p = Player(name="Alex", hand=h, score=15)
    assert p.name == "Alex"
    assert p.hand == h
    assert p.score == 15


def test_str():
    h = Hand.load("y1 g3 b2")
    p = Player(name="Alex", hand=h, score=15)
    assert str(p) == "Alex(15): y1 g3 b2"


def test_save():
    h = Hand.load("y1 g3 b2")
    p = Player(name="Alex", hand=h, score=15)
    assert p.save() == {"name": "Alex", "score": 15, "hand": "y1 g3 b2"}


def test_eq():
    h1 = Hand.load("y1 g3 b2")
    h2 = Hand.load("y1 g3 b2")
    p1 = Player(name="Alex", hand=h1, score=15)
    p2 = Player(name="Alex", hand=h2, score=15)
    assert p1 == p2


def test_load():
    data = {"name": "Alex", "score": 15, "hand": "y1 g3 b2"}
    h = Hand.load("y1 g3 b2")
    p_expected = Player(name="Alex", hand=h, score=15)
    p = Player.load(data)
    assert p == p_expected
