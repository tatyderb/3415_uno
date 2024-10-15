import pygame

from src.card import Card
from src.ui.view_card import ViewCard


class ViewGame:
    def __init__(self):
        self.vcard = ViewCard(Card('b', 4), x=20, y=30)

    def model_update(self):
        pass

    def redraw(self, display: pygame.Surface):
        display.fill('darkgreen')
        self.vcard.redraw(display)
        pygame.display.update()

    def event_processing(self, event: pygame.event.Event):
        self.vcard.event_processing(event)