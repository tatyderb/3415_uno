from enum import IntEnum, auto
import pygame

class CustomEvent(IntEnum):
    PLAY_CARD = pygame.USEREVENT + 1   # +2, +3, ....
    DRAW_CARD = auto()
    DECLARE_WINNER = auto()
    SELECT_INTERACTIVE_CARDS = auto()   # надо выделить карты, которые можно будет играть интерактивному игроку
    UNSELECT_INTERACTIVE_CARDS = auto() # надо снять выделение с карт


def post_event(event_type: int, **kwargs):
    """ Посылаем пользовательский event, данные передаем в kwargs. """
    event = pygame.event.Event(event_type)
    event.user_data = kwargs
    pygame.event.post(event)
