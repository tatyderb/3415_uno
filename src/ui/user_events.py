import pygame

PLAY_CARD_EVENT = pygame.USEREVENT + 1
DRAW_CARD_EVENT = pygame.USEREVENT + 2
PLAY_CARD_AGAIN_EVENT = pygame.USEREVENT + 3
NEXT_PLAYER_EVENT = pygame.USEREVENT + 4
FLY_BEGIN_EVENT = pygame.USEREVENT + 5
FLY_END_EVENT = pygame.USEREVENT + 6


def post_event(event_type: int, **kwargs):
    """ Посылаем пользовательский event, данные передаем в kwargs. """
    event = pygame.event.Event(event_type)
    event.user_data = kwargs
    pygame.event.post(event)
