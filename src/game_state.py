import typing

from src.card import Card
from src.deck import Deck
from src.player import Player


class GameState:
    def __init__(
        self, players: list[Player], deck: Deck, top: Card, current_player: int = 0
    ):
        self.players: list[Player] = players
        self.deck: Deck = deck
        self.top: Card = top
        self.__current_player: int = current_player

    @property
    def current_player_index(self):
        return self.__current_player

    def current_player(self) -> Player:
        return self.players[self.__current_player]

    def __eq__(self, other):
        # return self.players == other.players and self.deck == other.deck and self.top == other.top and \
        #         self._current_player == other._current_player
        if self.players != other.players:
            return False
        if self.deck != other.deck:
            return False
        if self.top != other.top:
            return False
        if self.__current_player != other.__current_player:
            return False
        return True

    def save(self) -> dict:
        return {
            "top": str(self.top),
            "deck": str(self.deck),
            "current_player_index": self.__current_player,
            "players": [p.save() for p in self.players],
        }

    @classmethod
    def load(cls, data: dict):
        """
        data = {
            'top': 'y7',
            'current_player_index': 1,
            'deck': 'g2 y6 b0',
            'players': [
                {
                    'name': 'Alex',
                    'hand': 'y3 b6',
                    'score': 5
                },
                {
                    'name': 'Bob',
                    'hand': 'g5',
                    'score': 1
                },
                {
                    'name': 'Charley',
                    'hand': 'g7 g1 b2',
                    'score': 3
                }
            ]
        }
        """
        players = [Player.load(d) for d in data["players"]]

        return cls(
            players=players,
            deck=Deck.load(data["deck"]),
            top=Card.load(data["top"]),
            current_player=int(data["current_player_index"]),
        )

    def next_player(self):
        """Ход переходит к следующему игроку."""
        n = len(self.players)
        self.__current_player = (self.__current_player + 1) % n

    def draw_card(self) -> Card:
        """Текущий игрок берет карту из колоды."""
        card = self.deck.draw_card()
        self.current_player().hand.add_card(card)
        return card

    def play_card(self, card: Card):
        """Карта card от текущего игрока переходит в top."""
        self.current_player().hand.remove_card(card)
        self.top = card
