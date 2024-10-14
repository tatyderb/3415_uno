import pygame

from src.card import Card
from src.ui.card_view import CardView


class GameView:
    def __init__(self):
        self.vcard = CardView(x=10, y=20, card=Card('r', 7), face=True)

    def redraw(self, display: pygame.Surface):
        self.vcard.redraw(display)
        pygame.display.update()

    def event_processing(self, event: pygame.event.Event):
        self.vcard.event_processing(event)

    def model_update(self):
        pass
