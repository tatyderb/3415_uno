import typing
from dataclasses import dataclass

import pygame
from pygame.event import Event

from src.card import Card
from src.ui.resource import RESOURCE as RSC


class CardView:
    BACK_IMG = None
    CARD_SIZE = (WIDTH, HEIGHT) = (RSC['card_width'], RSC['card_height'])

    def __init__(self, x: int, y: int, card: Card = None, face: bool = False):
        self.__x = x
        self.__y = y
        self.card = card
        self.face = face
        if self.BACK_IMG is None:
            img = pygame.image.load(CardView.image_file_name('back'))
            self.BACK_IMG = pygame.transform.scale(img, self.CARD_SIZE)
        if card is None:
            self.face_image = None
        else:
            img = pygame.image.load(CardView.image_file_name(str(self.card)))
            self.face_image = pygame.transform.scale(img, self.CARD_SIZE)
        self.rect: pygame.Rect = pygame.Rect(self.__x, self.__y, self.WIDTH, self.HEIGHT)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value: int):
        self.__x = value
        self.rect.x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value: int):
        self.__y = value
        self.rect.y = value

    @property
    def image(self):
        return self.face_image if self.face else self.BACK_IMG

    @staticmethod
    def image_file_name(card_name: str):
        return RSC['image']['card_img_base_dir'] + '/' + card_name + '.png'

    def redraw(self, display: pygame.Surface):
        display.blit(self.image, (self.x, self.y, self.WIDTH, self.HEIGHT))

    def event_processing(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # нажата левая кнопка
            # 0 - 1 - 2
            # 0 - 1 - 2 - 3 - 4
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                if self.rect.collidepoint(x, y):
                    self.flip()

    def flip(self):
        self.face = not self.face
        print(f'Flip card {self.card}')


@dataclass
class Fly:
    vcard: CardView | None = None
    start: tuple[int, int] = (0, 0)     # (x, y)
    finish: tuple[int, int] = (0, 0)    # (x, y)
    total_iterations: int = 60      # общая длительность анимации в итерациях (план)
    iteration: int = 0              # сколько итераций уже сделали
    animation_mode: bool = False
    # end_callback: typing.Any = None        # выполняется код end_callback(card) в конце fly

    def fly(self):
        if not self.animation_mode:
            # raise Exception('Не должны были вызывать эту функцию')
            # пока ограничимся тем, что не будем лететь, пока не начали летать или уже закончили
            return

        self.iteration += 1
        if self.iteration >= self.total_iterations:
            self.end()
            return
        x1, y1 = self.start
        x2, y2 = self.finish
        x = x1 + (x2 - x1) * self.iteration // self.total_iterations
        y = y1 + (y2 - y1) * self.iteration // self.total_iterations
        self.vcard.x = x
        self.vcard.y = y

    def end(self):
        print(f'Fly end with {self.vcard}')
        self.vcard.pos = self.finish
        self.animation_mode = False
        # if self.end_callback is not None:
        #     self.end_callback(self.vcard)
        # user_event.post_event(user_event.FLY_END_EVENT)  # result to game.fly_end
        self.vcard = None

    def begin(self, vcard: CardView, to: tuple[int, int], on_end=None, ticks: int = RSC['FPS']):
        self.animation_mode = True
        self.vcard = vcard
        self.start = (vcard.x, vcard.y)
        self.finish = to
        self.total_iterations = ticks
        self.iteration = 0
        print(f'Fly begin with {self.vcard}')
        self.end_callback = on_end

    def flying(self):
        return self.animation_mode

    def redraw(self, display: pygame.Surface):
        if self.flying():
            self.vcard.redraw(display)
