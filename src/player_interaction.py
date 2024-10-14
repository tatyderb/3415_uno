from abc import ABC, abstractmethod

from src.card import Card
from src.hand import Hand
from src.player import Player


class PlayerInteraction(ABC):
    @classmethod
    @abstractmethod
    def choose_card(
            cls, hand: Hand, top: Card, hand_counts: list[int] | None = None
    ) -> Card:
        pass

    @classmethod
    @abstractmethod
    def choose_to_play(cls, top: Card, drawn: Card) -> bool:
        """
        Принимает решение играть или не играть взятую из колоды карту.
        """
        pass

    @classmethod
    def inform_card_drawn(cls, player: Player):
        """
        Сообщает, что игрок взял карту.
        """
        pass

    @classmethod
    def inform_card_played(cls, player: Player, card: Card):
        """
        Сообщает, что игрок сыграл карту.
        """
        pass


