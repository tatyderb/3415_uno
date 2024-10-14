import pygame as pygame

from ui.resource import RESOURCE as RSC


class Application:
    def __init__(self):
        pygame.init()
        self.size = (self.width, self.height) = (RSC['width'], RSC['height'])
        self.display = pygame.display.set_mode(self.size)

    def run(self):
        running = True
        while running:
            pass


def main():
    print('Start UNO application')
    app = Application()
    app.run()


if __name__ == '__main__':
    main()
