import pygame

EVENT_PLAY_CARD = pygame.USEREVENT + 1   # +2, +3, ....


def post_event(event_type: int, **kwargs):
    """ Посылаем пользовательский event, данные передаем в kwargs. """
    event = pygame.event.Event(event_type)
    event.user_data = kwargs
    pygame.event.post(event)
