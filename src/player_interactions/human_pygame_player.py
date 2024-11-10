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

from src.player_interaction import PlayerInteraction
from src.ui.event import post_event, CustomEvent


# класс-метка, будет показывать, что choose_card может вернуть состояние "нужно ждать куда ткнет мышью игрок"
class AWAITING_INTERACTION:
    pass


class HumanGUI(PlayerInteraction):
    @classmethod
    def choose_card(
        cls, hand: Hand, top: Card, hand_counts: list[int] | None = None
    ) -> Card | None | AWAITING_INTERACTION:
        """
        Ищет играбельные карты.
        Если играбельных карт нет (придется брать карту из колоды),
            возвращает None.
        Если карта уже выбрана,
            то возвращает эту карту.
        Бросает event "пометить все играбельные карты".
        Возвращает, что мы в состоянии "ожидаем ввода игрока"
        """
        playable_cards = hand.playable_cards(top)
        # должны были отсечь раньше, но последний рубеж:
        # если карт играбельных нет, то выбирать нечего, надо брать карту из колоды.
        if not playable_cards:
            return None

        # если карта уже выбрана, то её вернем, выделение с карт снимем
        for card in playable_cards:
            if card.chosen:
                post_event(CustomEvent.UNSELECT_INTERACTIVE_CARDS)
                card.chosen = False
                return card

        # кидаем event, чтобы выделить играбельные карты
        post_event(CustomEvent.SELECT_INTERACTIVE_CARDS, cards=playable_cards)
        # теперь ждем, когда пользователь таки ткнет в нужную карту
        return AWAITING_INTERACTION()

    @classmethod
    def choose_to_play(cls, top: Card, drawn: Card) -> bool:
        """
        Принимает решение играть или не играть взятую из колоды карту.
        """
        return True

