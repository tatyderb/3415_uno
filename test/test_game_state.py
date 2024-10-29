from src.card import Card
from src.deck import Deck
from src.game_state import GameState
from src.player import Player

data = {
    "top": "y7",
    "current_player_index": 1,
    "deck": "g2 y6 b0",
    "players": [
        {"name": "Alex", "hand": "y3 b6", "score": 5},
        {"name": "Bob", "hand": "g5", "score": 1},
        {"name": "Charley", "hand": "g7 g1 b2", "score": 3},
    ],
}

alex = Player.load(data["players"][0])
bob = Player.load(data["players"][1])
charley = Player.load(data["players"][2])
full_deck = Deck(None)


def test_init():
    players = [alex, bob, charley]
    game = GameState(
        players=players, deck=full_deck, current_player=1, top=Card.load("y7")
    )
    assert game.players == players
    assert game.deck == full_deck
    assert game.current_player() == bob
    assert str(game.top) == "y7"


def test_current_player():
    players = [alex, bob, charley]
    game = GameState(players=players, deck=full_deck, top=Card.load("y7"))
    assert game.current_player() == alex

    game = GameState(
        players=players, deck=full_deck, top=Card.load("y7"), current_player=1
    )
    assert game.current_player() == bob

    game = GameState(
        players=players, deck=full_deck, top=Card.load("y7"), current_player=2
    )
    assert game.current_player() == charley


def test_eq():
    players = [alex, bob, charley]
    game1 = GameState(players=players, deck=full_deck, top=Card.load("y7"))
    game1_copy = GameState(players=players.copy(), deck=Deck(game1.deck.cards.copy()), top=Card.load("y7"))
    game2 = GameState(players=players.copy(), deck=Deck(None), top=Card.load("y7"))
    # надо бы еще game с отличающимися на 1 другой параметр и всеми отличающимися
    game3 = GameState(players=players, deck=Deck.load("g2 y6 b0"), top=Card.load("y7"))
    assert game1 == game1_copy
    assert game1 != game2       # shuffled Deck
    assert game1 != game3       # different Deck


def test_save():
    players = [alex, bob, charley]
    game = GameState(
        players=players,
        deck=Deck.load(data["deck"]),
        top=Card.load(data["top"]),
        current_player=1,
    )
    assert game.save() == data


def test_load():
    game = GameState.load(data)
    assert game.save() == data


def test_next_player():
    game = GameState.load(data)
    assert game.current_player() == bob

    game.next_player()
    assert game.current_player() == charley

    game.next_player()
    assert game.current_player() == alex

    game.next_player()
    assert game.current_player() == bob


def test_draw_card():
    game = GameState.load(data)
    assert game.deck == "g2 y6 b0"
    assert game.current_player().hand == "g5"

    game.draw_card()
    assert game.deck == "g2 y6"
    assert game.current_player().hand == "g5 b0"


def test_play_card():
    players = [alex, bob, charley]
    game = GameState(
        players=players, deck=full_deck, top=Card.load("y7"), current_player=2
    )

    assert game.current_player().hand == "g7 g1 b2"
    assert game.top == "y7"

    game.play_card(Card.load("g1"))
    assert game.current_player().hand == "g7 b2"
    assert game.top == "g1"
