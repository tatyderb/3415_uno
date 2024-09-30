from src.card import Card
from src.hand import Hand


class Bot:
    @classmethod
    def choose_card(cls, hand: Hand, top: Card, hand_counts: list[int] | None = None):
        """
        Принимает решение, какую карту с руки играть.
        Возвращает карту или None, если нельзя играть карту с руки.
        """
        playable_cards = [card for card in hand.cards if card.can_play_on(top)]
        if playable_cards:
            return playable_cards[0]
        else:
            return None

    @classmethod
    def choose_to_play(cls, top: Card, drawn: Card):
        """
        Принимает решение играть или не играть взятую из колоды карту.
        Бот всегда играет карту.
        """
        return True
