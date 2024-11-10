from src.card import Card
from src.hand import Hand
from src.player import Player

from src.player_interaction import PlayerInteraction
from src.ui.event import CustomEvents, post_event


class Human(PlayerInteraction):
    @classmethod
    def choose_card(
        cls, hand: Hand, top: Card, hand_counts: list[int] | None = None
    ) -> Card | None | CustomEvents:  # AWAITING_GUI
        """
        Принимает решение, какую карту с руки играть.
        Возвращает карту или None, если нельзя играть карту с руки.
        """
        playable_cards = hand.playable_cards(top)
        # Prepare choice
        post_event(CustomEvents.EVENT_CHANGE_INTERACTIVE_CARDS, cards=playable_cards)
        # Check if 1 card is chosen:
        chosen_card = [card for card in playable_cards if card.chosen]
        if not chosen_card:
            return CustomEvents.AWAITING_GUI

        post_event(CustomEvents.EVENT_CHANGE_INTERACTIVE_CARDS, cards=[])
        return chosen_card[0]

    @classmethod
    def choose_to_play(cls, top: Card, drawn: Card) -> bool:
        """
        Принимает решение играть или не играть взятую из колоды карту.
        """
        return True
