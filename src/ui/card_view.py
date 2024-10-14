import pygame

from src.card import Card
from src.ui.resource import RESOURCE as RSC


class CardView:
    BACK_IMG = None
    CARD_SIZE = (WIDTH, HEIGHT) = (RSC['card_width'], RSC['card_height'])

    def __init__(self, x: int, y: int, card: Card = None, face: bool = False):
        self.x = x
        self.y = y
        self.card = card
        self.face = face
        if self.BACK_IMG is None:
            self.BACK_IMG = pygame.image.load(CardView.image_file_name('back'))
        if card is None:
            self.face_image = None
        else:
            img = pygame.image.load(CardView.image_file_name(str(self.card)))
            self.face_image = pygame.transform.scale(img, self.CARD_SIZE)

    @property
    def image(self):
        return self.face_image if self.face else self.BACK_IMG

    @staticmethod
    def image_file_name(card_name: str):
        return RSC['image']['card_img_base_dir'] + '/' + card_name + '.png'

    def draw(self, display: pygame.Surface):
        display.blit(self.image, (self.x, self.y, self.WIDTH, self.HEIGHT))

