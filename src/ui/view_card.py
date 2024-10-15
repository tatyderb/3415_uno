import pygame

from src.card import Card
from src.resource import RESOURCE as RSC


class ViewCard:
    WIDTH = RSC["card_width"]
    HEIGHT = RSC["card_height"]
    IMAGE_BACK = None
    SELECTED_COLOR = 'yellow'
    BORDERX = RSC["border_x"]
    BORDERY = RSC["border_y"]

    def __init__(self, card: Card, x: int = 0, y: int = 0, opened: bool = True):
        self.card = card
        self.x = x
        self.y = y
        self.opened = opened
        self.selected = False
        img = pygame.image.load("img/r2.png")
        # print(img.get_size())
        self.img_front = pygame.transform.scale(img, (ViewCard.WIDTH, ViewCard.HEIGHT))
        if self.IMAGE_BACK is None:
            img = pygame.image.load("img/back.png")
            self.IMAGE_BACK = pygame.transform.scale(img, (ViewCard.WIDTH, ViewCard.HEIGHT))


    def redraw(self, display: pygame.Surface):
        if self.selected:
            r = (
                self.x - self.BORDERX,
                self.y - self.BORDERY,
                self.WIDTH + 2 * self.BORDERX,
                self.HEIGHT + 2 * self.BORDERY
                )
            display.fill(self.SELECTED_COLOR, r)
        # else:
        #     r = (
        #         self.x - self.BORDERX,
        #         self.y - self.BORDERY,
        #         self.WIDTH + 2 * self.BORDERX,
        #         self.HEIGHT + 2 * self.BORDERY
        #         )
        #     display.fill('blue', r)

        if self.opened:
            img = self.img_front
        else:
            img = self.IMAGE_BACK
        display.blit(img, (self.x, self.y))

    def event_processing(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            print(f'Select!')
            self.select()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # нажали на левую кнопку мыши
            # нажата левая кнопка
            # 0 - 1 - 2
            # 0 - 1 - 2 - 3 - 4
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                r = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
                if r.collidepoint(x, y):
                    self.flip()

    def flip(self):
        self.opened = not self.opened

    def select(self):
        self.selected = not self.selected
        print(f'{self.selected=}')

