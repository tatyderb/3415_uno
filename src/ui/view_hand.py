import pygame

from src.resource import RESOURCE as RSC
from src.hand import Hand
from src.ui.event import CustomEvent
from src.ui.view_card import ViewCard


class ViewHand:
    CARD_XGAP = RSC["card_xgap"]
    def __init__(self, hand: Hand, bound: pygame.Rect):
        self.vcards: list[ViewCard | None] = self.create_view_cards(hand, bound)
        self.bound = bound

    def redraw(self, display: pygame.Surface):
        for vc in self.vcards:
            if vc is None:
                continue
            vc.redraw(display)

    def event_processing(self, event: pygame.event.Event):

        for vc in self.vcards:
            if vc is None:
                continue
            vc.event_processing(event)

    def create_view_cards(self, hand: Hand, bound: pygame.Rect):
        if hand is None:
            return []
        length = len(hand)
        #bx, by, bw, bh = bound
        bx = bound.x
        by = bound.y
        bw = bound.width
        bh = bound.height
        print('Hand Bounds:', bx, by, bw, bh)
        vcards = []
        for n, card in enumerate(hand):
            vcard = ViewCard(card, x=bx + n * (ViewCard.WIDTH + self.CARD_XGAP), y=by)
            print(f'Add view card {vcard}')
            vcards.append(vcard)
        return vcards

    def next_card_position(self) -> tuple[int, int]:
        """Позиция следующей карты в руке, куда ее можно положить."""
        vc_end = self.vcards[-1]
        return vc_end.x + ViewCard.WIDTH + self.CARD_XGAP, vc_end.y







