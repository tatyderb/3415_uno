import pygame

from src.card import Card
from src.ui.card_view import CardView, Fly


class GameView:
    def __init__(self):
        self.vcard = CardView(x=10, y=20, card=Card('r', 7), face=True)
        self.fly = Fly()

    def redraw(self, display: pygame.Surface):
        self.vcard.redraw(display)
        self.fly.redraw(display)
        pygame.display.update()

    def event_processing(self, event: pygame.event.Event):
        self.vcard.event_processing(event)
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_z:
                    self.vcard.flip()
                case pygame.K_SPACE:
                    self.fly.begin(vcard=self.vcard, to=(400, 300))


    def model_update(self):
        self.fly.fly()
