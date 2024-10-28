import pygame

from src.card import Card
from src.ui.view_card import ViewCard, Fly


class ViewGame:
    def __init__(self):
        self.vcard = ViewCard(Card('b', 4), x=20, y=30)
        self.fly = Fly()

    def model_update(self):
        self.fly.fly()

    def redraw(self, display: pygame.Surface):
        display.fill('darkgreen')
        self.vcard.redraw(display)
        self.fly.redraw(display)
        pygame.display.update()

    def event_processing(self, event: pygame.event.Event):
        # пока идет анимация, никакой реакции на действия пользователя!
        if self.fly.animation_mode:
            return
        self.vcard.event_processing(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            self.fly.begin(vcard=self.vcard, finish=(400, 300))

