import pygame

from src.deck import Deck
from src.card import Card
from src.game_server import GameServer
from src.hand import Hand
from src.ui.view_card import ViewCard, Fly
from src.ui.view_hand import ViewHand
from src.ui.view_playzone import ViewPlayzone


class ViewGame:
    YGAP = 0
    XGAP = 30
    def __init__(self, game_server: GameServer):
        # self.vcard = ViewCard(Card('b', 4), x=20, y=30)
        self.game = game_server
        self.fly = Fly()
        rplayer1, rplayzone, rplayer2 = self.calculate_geom_contants()
        game = game_server.game_state
        self.playzone = ViewPlayzone(top=game.top, deck=game.deck, bounds=rplayzone)
        self.vhand = ViewHand(game.players[0].hand, rplayer1)
        self.vhand_my = ViewHand(game.players[1].hand, rplayer2)


    def calculate_geom_contants(self):
        screen_width, screen_height = pygame.display.get_window_size()
        card_width = ViewCard.WIDTH
        card_height = ViewCard.HEIGHT
        self.YGAP = (screen_height - 3 * card_height) // 4
        rplayer1 = pygame.Rect(self.XGAP, self.YGAP, screen_width - 2*self.XGAP, card_height)
        # заглушки, потом надо написать формулы
        rplayzone = pygame.Rect(self.XGAP, self.YGAP*2 + card_height, screen_width - 2*self.XGAP, card_height)
        rplayer2 = pygame.Rect(self.XGAP, self.YGAP*3 + 2*card_height, screen_width - 2*self.XGAP, card_height)
        return rplayer1, rplayzone, rplayer2


    def model_update(self):
        self.fly.fly()

    def redraw(self, display: pygame.Surface):
        display.fill('darkgreen')
        #self.vcard.redraw(display)
        self.vhand.redraw(display)
        self.vhand_my.redraw(display)
        self.playzone.redraw(display)
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
        self.vhand_my.event_processing(event)
        self.playzone.event_processing(event)


