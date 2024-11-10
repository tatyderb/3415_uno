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
        self.img_front = None
        self.card = card
        self.x = x
        self.y = y
        self.opened = opened
        self.selected = False
        self.chooseable = False     # карта тыкабельна мышкой для выбора карты

    @property
    def card(self):
        return self.__card

    @card.setter
    def card(self, value):
        if not isinstance(value, Card):
            raise TypeError(f'Expected Card, got {type(value)}')
        self.__card = value
        img = pygame.image.load(f"img/{self.card.color}{self.card.number}.png")
        # print(img.get_size())
        self.img_front = pygame.transform.scale(img, (ViewCard.WIDTH, ViewCard.HEIGHT))
        if self.IMAGE_BACK is None:
            img = pygame.image.load("img/back.png")
            self.IMAGE_BACK = pygame.transform.scale(img, (ViewCard.WIDTH, ViewCard.HEIGHT))



    def __repr__(self):
        return f'{self.card} ({self.x}, {self.y})'

    def rect(self):
        return pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

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


class Fly:
    def __init__(self, vcard: ViewCard | None = None):
        self.vcard = vcard
        self.start: tuple[int, int] = (0, 0)    # x, y
        self.finish: tuple[int, int] = (0, 0)   # x, y
        self.total_iterations: int = 0          # за сколько итераций пролетим от старта до финиша
        self.iterations: int = 0                # сколько уже пролетели
        self.animation_mode = False
        # callback
        self.on_end = None          # функцию, которую вызовем в конце анимации
        self.on_end_kwargs = {}     # аргументы этой функции

    def begin(self,
              vcard: ViewCard,
              finish: tuple[int, int] | ViewCard,
              total_iterations: int = RSC["FPS"],
              on_end=None,
              **kwargs,
              ):
        self.vcard = vcard
        self.start = (vcard.x, vcard.y)
        if isinstance(finish, ViewCard):
            print(f'Это карта {finish}')
            self.finish = (finish.x, finish.y)
        else:
            print(f'Это позиция {finish}')
            self.finish = finish
        self.total_iterations = total_iterations
        self.iterations = 0
        self.animation_mode = True
        self.on_end = on_end
        self.on_end_kwargs = kwargs

    def redraw(self, display: pygame.Surface):
        if self.animation_mode and self.vcard:
            self.vcard.redraw(display)

    def fly(self):
        if not self.animation_mode:
            return

        self.iterations += 1
        print(f'Fly: {self.vcard}')

        if self.iterations >= self.total_iterations:
            self.end()
            return

        x0, y0 = self.start
        x1, y1 = self.finish
        dx = (x1 - x0) / self.total_iterations
        dy = (y1 - y0) / self.total_iterations
        self.vcard.x = x0 + dx * self.iterations
        self.vcard.y = y0 + dy * self.iterations

    def end(self):
        self.animation_mode = False
        self.vcard.x = self.finish[0]
        self.vcard.y = self.finish[1]
        self.on_end(**self.on_end_kwargs)




