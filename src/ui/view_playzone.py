"""Top and Deck as View."""
import pygame

from src.card import Card
from src.deck import Deck
from src.ui.view_card import ViewCard
from src.resource import RESOURCE as RSC


class ViewPlayzone:
    def __init__(self, top: Card, deck: Deck, bounds: pygame.Rect):
        y, top_x, deck_x = self.calculate_positions(bounds)
        self.vtop = ViewCard(top, x=top_x, y=y)
        self.vdeck = ViewCard(Card('r', 0), x=deck_x, y=y, opened=False)

    @staticmethod
    def calculate_positions(bounds: pygame.Rect):
        center_x, center_y = bounds.center
        card_width = ViewCard.WIDTH
        left_x = center_x - card_width // 2 - RSC['card_xgap'] - card_width
        right_x = center_x + card_width // 2 + RSC['card_xgap']
        y = center_y - ViewCard.HEIGHT // 2
        return y, left_x, right_x

    def redraw(self, display: pygame.Surface):
        self.vtop.redraw(display)
        self.vdeck.redraw(display)

    def event_processing(self, event: pygame.event.Event):
        # действия только на колоде, взять карту, когда время взятия карты
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                if self.vdeck.rect().collidepoint(x, y):
                    # донести, что кликнули на колоду и берем карту
                    pass




