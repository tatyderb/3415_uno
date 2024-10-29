import pygame

from src.game_server import GameServer
from src.resource import RESOURCE as RSC
from src.ui.view_game import ViewGame


class Application:
    def __init__(self):
        pygame.init()
        self.size = (self.width, self.height) = (RSC['width'], RSC['height'])
        self.display = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Uno")
        try:
            icon_img = pygame.image.load("ui/uno_icon.png")
            pygame.display.set_icon(icon_img)
        except FileNotFoundError:
            # иконка по умолчанию, сделанную где-то потеряла.
            pass

        self.vgame = None


    def run(self):
        clock = pygame.time.Clock()
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
            clock.tick(RSC["FPS"])

    def connect_with_game(self, game_server: GameServer):
        game_server.check_data_for_gui()
        self.vgame = ViewGame(game_server)


if __name__ == '__main__':
    app = Application()
    game_server = GameServer.load_game('uno.json')
    app.connect_with_game(game_server)
    # run строго после связки с game_server
    app.run()
