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
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_qP:
                    running = False


def main():
    print('Start UNO application')
    app = Application()
    app.run()


if __name__ == '__main__':
    main()
