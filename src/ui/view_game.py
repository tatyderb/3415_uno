import pygame

from src.card import Card
from src.hand import Hand
from src.ui.view_card import ViewCard, Fly
from ui.view_hand import ViewHand


class ViewGame:
    YGAP = 0
    XGAP = 30
    def __init__(self):
        # self.vcard = ViewCard(Card('b', 4), x=20, y=30)
        self.fly = Fly()
        rplayer1, rplayzone, rplayer2 = self.calculate_geom_contants()
        self.vhand = ViewHand(Hand.load('b7 g3 y2 r9'), rplayer1)

    def calculate_geom_contants(self):
        screen_width, screen_height = pygame.display.get_window_size()
        card_width = ViewCard.WIDTH
        card_height = ViewCard.HEIGHT
        self.YGAP = (screen_height - 3 * card_height) / 4
        rplayer1 = pygame.Rect(self.XGAP, self.YGAP, screen_width - 2*self.XGAP, self.YGAP + card_height)
        # заглушки, потом надо написать формулы
        rplayzone = pygame.Rect(0, 0, 0, 0)
        rplayer2 = pygame.Rect(0, 0, 0, 0)
        return rplayer1, rplayzone, rplayer2


    def model_update(self):
        self.fly.fly()

    def redraw(self, display: pygame.Surface):
        display.fill('darkgreen')
        #self.vcard.redraw(display)
        self.vhand.redraw(display)
        self.fly.redraw(display)
        pygame.display.update()

    def event_processing(self, event: pygame.event.Event):
        # пока идет анимация, никакой реакции на действия пользователя!
        if self.fly.animation_mode:
            return
        # self.vcard.event_processing(event)
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
        #     self.fly.begin(vcard=self.vcard, finish=(400, 300))
        self.vhand.event_processing(event)

