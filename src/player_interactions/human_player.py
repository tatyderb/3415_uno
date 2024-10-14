from src.card import Card
from src.hand import Hand
from src.player import Player

from src.player_interaction import PlayerInteraction


class Human(PlayerInteraction):
    @classmethod
    def choose_card(
        cls, hand: Hand, top: Card, hand_counts: list[int] | None = None
    ) -> Card:
        """
        Принимает решение, какую карту с руки играть.
        Возвращает карту или None, если нельзя играть карту с руки.
        """
        playable_cards = hand.playable_cards(top)
        while True:
            try:
                card_text = input("Choose card: ")
                card = Card.load(card_text)
                if card in playable_cards:
                    return card
                else:
                    print('Эту карту нельзя играть.')
            except ValueError:
                print("Карта задается как g5, где g цвет (r g b y), и номер от 0 до 9.")


    @classmethod
    def choose_to_play(cls, top: Card, drawn: Card) -> bool:
        """
        Принимает решение играть или не играть взятую из колоды карту.
        """
        return True


