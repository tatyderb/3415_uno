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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self.flip()

    def flip(self):
        self.face = not self.face
        print(f'Flip card {self.card}')


