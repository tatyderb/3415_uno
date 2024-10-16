import pygame

from src.resource import RESOURCE as RSC
from src.ui.view_game import ViewGame


class Application:
    def __init__(self):
        pygame.init()
        self.size = (self.width, self.height) = (RSC['width'], RSC['height'])
        self.display = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Uno")
        icon_img = pygame.image.load("ui/uno_icon.png")
        pygame.display.set_icon(icon_img)

        self.vgame = ViewGame()

    def run(self):
        running = True
        self.display.fill('darkgreen', (0, 0, self.width, self.height))
        pygame.display.update()
        while running:
            # изменения модели
            self.vgame.model_update()
            # отрисовка изменений
            self.vgame.redraw(self.display)
            # реакция на клавиши и мышь
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                        event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    running = False
                self.vgame.event_processing(event)


if __name__ == '__main__':
    app = Application()
    app.run()
