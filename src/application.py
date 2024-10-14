import pygame as pygame

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

    def run(self):
        running = True
        self.display.fill('darkgreen', (0, 0, self.width, self.height))
        pygame.display.update(self.window_rect)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    running = False


def main():
    print('Start UNO application')
    app = Application()
    app.run()


if __name__ == '__main__':
    main()
