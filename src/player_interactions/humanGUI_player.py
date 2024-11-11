"""
GUI интерактивного пользователя с помощью pygame.
Проблема:
GameServer.choose_card_phase, вызывается в ViewGame.model_update и должна вернуть выбранную карту или None
При этом обработка нажатия пользователем на мышь осуществляется в ViewGame.event_processing(event).
А мы только по позиции мыши во время ее нажатия можем сказать на какую карту кликнул пользователь.
Решение:
* В фазе изменения модели мы помечаем карты, которые могут быть выбраны (Card.chooseable).
    * если есть выбранная карта, то возвращаем эту карту из Human.choose_card, иначе
    * кидаем event CHANGE_INTERACTIVE_CARDS, В этот event передаем список карт, которые могут быть выбраны пользователем.
    * Возвращаем "ждем действия пользователя" (нам бы константу именованную вида AWAITING_GUI)
    * и остаемся в той же фазе выбора карты.
* в фазе обработки событий:
    * если приходит событие "пометить карты, которые можно играть", помечаем эти карты.
    * если приходит событие мыши клик внутри помеченной карты, то эта карта помечается как выбранная
    * на момент fly нужно будет снять все пометки, что карты играбельные.
"""


from src.card import Card
from src.hand import Hand
from src.player import Player

from src.player_interaction import PlayerInteraction
from src.ui.event import post_event, CustomEvent


class AWAITING_INTERACTION:
    pass


class HumanGUI(PlayerInteraction):
    @classmethod
    def choose_card(
        cls, hand: Hand, top: Card, hand_counts: list[int] | None = None
    ) -> Card | None | AWAITING_INTERACTION:
        """
        Принимает решение, какую карту с руки играть.
        * если есть выбранная карта, то возвращаем эту карту из Human.choose_card, иначе
        * кидаем event SELECT_INTERACTIVE_CARDS, В этот event передаем список карт, которые могут быть выбраны пользователем.
        * Возвращаем "ждем действия пользователя" (нам бы константу именованную вида AWAITING_INTERACTION)
        """
        playable_cards = hand.playable_cards(top)
        if not playable_cards:
            return None

        # если есть выбранная карта, то возвращаем эту карту
        for card in playable_cards:
            if card.chosen:
                card.chosen = False
                post_event(CustomEvent.SELECT_INTERACTIVE_CARDS, cards=[])
                return card

        # если карта не выбрана
        post_event(CustomEvent.SELECT_INTERACTIVE_CARDS, cards=playable_cards)
        return AWAITING_INTERACTION()


    @classmethod
    def choose_to_play(cls, top: Card, drawn: Card) -> bool:
        """
        Принимает решение играть или не играть взятую из колоды карту.
        """
        return True


