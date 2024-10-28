import pygame

from src.card import Card
from src.resource import RESOURCE as RSC
from src.game_server import GameServer
from src.player_interactions import Bot
from src.ui.view_card import ViewCard, Fly
from src.ui.view_hand import ViewHand
from src.ui.view_playzone import ViewPlayzone
import src.ui.user_events as user_event


class ViewGame:
    YGAP = 0
    XGAP = 30
    BOT_THINKING_TIME = RSC['FPS']
    def __init__(self, game_server: GameServer):
        # self.vcard = ViewCard(Card('b', 4), x=20, y=30)
        self.check_restrictions(game_server)
        self.game_server = game_server
        self.fly = Fly()
        rplayer1, rplayzone, rplayer2 = self.calculate_geom_contants()
        game = game_server.game_state
        self.vhand = ViewHand(game.players[0].hand, rplayer1)
        self.vhand_my = ViewHand(game.players[1].hand, rplayer2)
        self.playzone = ViewPlayzone(game.top, game.deck, rplayzone)
        # счетчик сколько должен тупить бот в тиках FPS
        self.stupid_iterations = self.BOT_THINKING_TIME


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
        # пока анимация, никаких изменений состояний
        if self.fly.animation_mode:
            self.fly.fly()
            self.start_thinking()
            return
        # бот должен тупить
        if not self.stupid_bot_pause():
            self.game_server.one_step()

    def stupid_bot_pause(self):
        """True, пока бот думает."""
        self.stupid_iterations -= 1
        return self.stupid_iterations > 0

    def start_thinking(self):
        """Бот начинает думать."""
        self.stupid_iterations = self.BOT_THINKING_TIME


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
        if event.type == user_event.PLAY_CARD_EVENT:
            print(f'{event.user_data=}')
            card = event.user_data['card']
            player_index = event.user_data['player_index']
            self.on_choose_card(card, player_index)

        # self.vcard.event_processing(event)
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
        #     self.fly.begin(vcard=self.vcard, finish=(400, 300))
        self.vhand.event_processing(event)
        self.vhand_my.event_processing(event)
        self.playzone.event_processing(event)

    def on_choose_card(self, card: Card, player_index: int):
        """Карта в руке рисуется пустым местом, начинается полет в отбой. player_index=0 - верхний игрок."""
        vplayer = self.vhand if player_index == 0 else self.vhand_my
        # делаем пустое место в руке
        for vc in vplayer.vcards:
            if vc.card is None:
                continue
            if vc.card == card:
                self.fly.begin(vcard=ViewCard(card, vc.x, vc.y),
                               finish=self.playzone.vtop,
                               on_fly_end=self.card_to_top)
                vc.card = None

    def card_to_top(self):
        card = self.fly.card
        # в модели карта на верху отбоя уже правильная, можем добыть ту же карту из self.game_server.game_state.top
        self.playzone.vtop.card = card
        game = self.game_server.game_state
        self.vhand = ViewHand(game.players[0].hand, self.vhand.bound)
        self.vhand_my = ViewHand(game.players[1].hand, self.vhand_my.bound)

    def check_restrictions(self, game_server: GameServer):
        """Проверяем, что 2 игрока и оба боты, потому что это ограничения текущей реализации."""
        ptypes = game_server.player_types
        if len(ptypes) != 2:
            print("Играть могут только два бота.")
            raise ValueError(f'"Играть могут только два бота. Загружено {len(game_server.player_types)} игрока"')

        for player, ptype in ptypes.items():
            if ptype != Bot:
                raise ValueError(f'"Играть могут только два бота. Игрок {player.name} не бот."')


