import pygame

from src.card import Card
from src.game_server import GameServer
from src.ui.view_card import ViewCard, Fly
from src.ui.view_hand import ViewHand
from src.ui.view_playzone import ViewPlayzone
from src.resource import RESOURCE as RSC
from src.ui.event import post_event, EVENT_PLAY_CARD, EVENT_DRAW_CARD


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
        # таймер обратного отсчета в тиках, сколько тиков осталось думать боту
        self.bot_thinking: int = 0
        self.begin_bot_thinking()  # если Human, то надо ли это?

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
        if self.fly.animation_mode:
            self.fly.fly()
            return
        elif self.stupid_pause():
            return
        self.game.run_one_step()

    def begin_bot_thinking(self):
        self.bot_thinking = RSC['FPS']

    def stupid_pause(self):
        self.bot_thinking -= 1
        if self.bot_thinking > 0:
            return True
        return False

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
        if event.type == EVENT_PLAY_CARD:
            data = event.user_data
            print(f'EVENT_PLAY_CARD user_data={data}')
            card = data['card']
            player_index = data['player_index']
            self.on_play_card(card=card, player_index=player_index)
        if event.type == EVENT_DRAW_CARD:
            data = event.user_data
            print(f'EVENT_PLAY_CARD user_data={data}')
            card = data['card']
            player_index = data['player_index']
            self.on_draw_card(card=card, player_index=player_index)

        # self.vcard.event_processing(event)
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
        #     self.fly.begin(vcard=self.vcard, finish=(400, 300))
        self.vhand.event_processing(event)
        self.vhand_my.event_processing(event)
        self.playzone.event_processing(event)

    def on_play_card(self, card: Card, player_index: int):
        """Начинаем анимацию полета карты с руки в отбой (top)."""
        if player_index == 0:
            vhand = self.vhand
        else:
            vhand = self.vhand_my
        vc = None
        for ivc, vc in enumerate(vhand.vcards):
            if vc.card == card:
                # делаем дырку в руке, не карта, а пусто
                vhand.vcards[ivc] = None
                break
        self.fly.begin(vcard=vc, finish=self.playzone.vtop,
                       on_end=self.end_card_playing, player_index=player_index)

    def on_draw_card(self, card: Card, player_index: int):
        """Начинаем анимацию полета карты (из колоды в конец руки)."""
        if player_index == 0:
            vhand = self.vhand
        else:
            vhand = self.vhand_my

        # deck position
        vdeck = self.playzone.vdeck
        vc = ViewCard(card=card, x=vdeck.x, y=vdeck.y, opened=False)
        # конец руки
        self.fly.begin(vcard=vc, finish=vhand.next_card_position(),
                       on_end=self.end_draw_card, player_index=player_index)

    def end_card_playing(self, **kwargs):
        """В конце анимации игры карты надо перерисовать (для этого пересоздать) VHand этого игрока."""
        player_index = kwargs['player_index']
        player = self.game.game_state.players[player_index]
        if player_index == 0:
            self.vhand = ViewHand(player.hand, self.vhand.bound)
        else:
            self.vhand_my = ViewHand(player.hand, self.vhand_my.bound)
        self.playzone.vtop.card = self.game.game_state.top

    def end_draw_card(self, **kwargs):
        """В конце анимации взятия карты надо перерисовать (для этого пересоздать) VHand этого игрока."""
        player_index = kwargs['player_index']
        player = self.game.game_state.players[player_index]
        if player_index == 0:
            self.vhand = ViewHand(player.hand, self.vhand.bound)
        else:
            self.vhand_my = ViewHand(player.hand, self.vhand_my.bound)


