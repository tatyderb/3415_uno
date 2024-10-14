import pygame

from src.card import Card
from src.ui.card_view import CardView


class GameView:
    def __init__(self):
        self.vcard = CardView(x=10, y=20, card=Card('r', 7), face=True)

    def draw(self, display: pygame.Surface):
        self.vcard.draw(display)
        pygame.display.update()
