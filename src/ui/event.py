import pygame
from enum import auto, IntEnum


class CustomEvents(IntEnum):
    EVENT_PLAY_CARD = pygame.USEREVENT + 1  # +2, +3, ....
    EVENT_DRAW_CARD = auto()
    EVENT_DECLARE_WINNER = auto()
    EVENT_CHANGE_INTERACTIVE_CARDS = auto()
    AWAITING_GUI = auto()


def post_event(event_type: int, **kwargs):
    """ Посылаем пользовательский event, данные передаем в kwargs. """
    event = pygame.event.Event(event_type)
    event.user_data = kwargs
    pygame.event.post(event)
