import pygame as pygame

from src.ui.game_view import GameView
from ui.resource import RESOURCE as RSC


class Application:
    def __init__(self):
        pygame.init()

        self.size = (self.width, self.height) = (RSC['width'], RSC['height'])
        self.window_rect = pygame.Rect(0, 0, self.width, self.height)
        self.display = pygame.display.set_mode(self.size)

        pygame.display.set_caption(RSC['title'])
        icon_img = pygame.image.load(RSC['image']['icon'])
        pygame.display.set_icon(icon_img)

        self.vgame = GameView()

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            self.vgame.redraw(self.display)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    running = False
                self.vgame.event_processing(event)
            self.vgame.model_update()
            clock.tick(RSC['FPS'])     # ждать 1/FPS секунды


def main():
    print('Start UNO application')
    app = Application()
    app.run()


if __name__ == '__main__':
    main()
