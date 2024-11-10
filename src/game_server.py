import inspect
import json
import sys
from pathlib import Path

from src.deck import Deck
from src.game_state import GameState
from src.hand import Hand
from src.player import Player
from src.player_interaction import PlayerInteraction
import src.player_interactions as all_player_types
from src.ui.event import post_event, CustomEvents

import logging

import enum

from src.player_interactions import Bot


class GamePhase(enum.StrEnum):
    CHOOSE_CARD = "Choose card"
    DRAW_EXTRA = "Draw extra card"
    CHOOSE_CARD_AGAIN = "Choose card again"
    NEXT_PLAYER = "Switch current player"
    DECLARE_WINNER = "Declare a winner"
    GAME_END = "Game ended"


class GameServer:
    INITIAL_HAND_SIZE = 6

    def __init__(self, player_types, game_state):
        self.game_state: GameState = game_state
        self.player_types: dict = player_types  # {player: PlayerInteractions}
        self.current_phase = GamePhase.CHOOSE_CARD

    @classmethod
    def load_game(cls, filename: str | Path):
        # TODO: выбрать имя файла
        with open(filename, 'r') as fin:
            data = json.load(fin)
            game_state = GameState.load(data)
            print(game_state.save())
            player_types = {}
            for player, player_data in zip(game_state.players, data['players']):
                kind = player_data['kind']
                kind = getattr(all_player_types, kind)
                player_types[player] = kind
            return GameServer(player_types=player_types, game_state=game_state)

    def save(self, filename: str | Path):
        data = self.save_to_dict()
        with open(filename, 'w') as fout:
            json.dump(data, fout, indent=4)

    def save_to_dict(self):
        # {'top': 'r2', 'deck': 'r0 g2 y1', 'current_player_index': 1, 'players': [{'name': 'Alex', 'hand': 'g5 b5', 'score': 0}, {'name': 'Bob', 'hand': 'y7', 'score': 1}]}
        data = self.game_state.save()
        for player_index, player in enumerate(self.player_types.keys()):
            player_interaction = self.player_types[player]
            data['players'][player_index]['kind'] = self.player_types[player].__name__
        return data

    @classmethod
    def get_players(cls):
        player_count = cls.request_player_count()

        player_types = {}
        for p in range(player_count):
            name, kind = cls.request_player()
            player = Player(name, Hand())
            player_types[player] = kind
        return player_types

    @classmethod
    def new_game(cls, player_types: dict):
        # Shuffle the deck and deal the top card
        deck = Deck(cards=None)
        top = deck.draw_card()
        game_state = GameState(list(player_types.keys()), deck, top)

        # Each player starts with 6 cards
        for _ in range(cls.INITIAL_HAND_SIZE):
            for p in player_types.keys():
                p.hand.add_card(deck.draw_card())

        print(game_state.save())

        res = cls(player_types, game_state)
        return res

    def run(self):
        while self.current_phase != GamePhase.GAME_END:
            self.run_one_step()

    def run_one_step(self):
            # 1. Possible code, but with more copy-paste
            # match current_phase:
            #     case CHOOSE_CARD:
            #         current_phase = choose_card_phase()
            #     case DRAW_EXTRA:
            #         current_phase = draw_extra_phase()
            #     case GAME_END:
            #         current_phase = game_end_phase()

            # 2. Suggested code - minimal and still easy to read
            phases = {
                GamePhase.CHOOSE_CARD: self.choose_card_phase,
                GamePhase.CHOOSE_CARD_AGAIN: self.choose_card_again_phase,
                GamePhase.DRAW_EXTRA: self.draw_extra_phase,
                GamePhase.NEXT_PLAYER: self.next_player_phase,
                GamePhase.DECLARE_WINNER: self.declare_winner_phase,
            }
            self.current_phase = phases[self.current_phase]()

            # 3. Can use naming convection to not declare phases explicitly,
            # but this may introduce errors later.
            # Looks over-engineered and is hard to read w/o comments.
            # current_phase = getattr(self, current_phase.name.lower() + "_phase")()

    def declare_winner_phase(self) -> GamePhase:
        print(f"{self.game_state.current_player()} is the winner!")
        post_event(
            CustomEvents.EVENT_DECLARE_WINNER,
            player_index=self.game_state.current_player_index,
        )
        # return GamePhase.GAME_END
        return GamePhase.DECLARE_WINNER

    def next_player_phase(self) -> GamePhase:
        if not self.game_state.current_player().hand.cards:
            return GamePhase.DECLARE_WINNER
        self.game_state.next_player()
        print(f"=== {self.game_state.current_player()}'s turn")
        return GamePhase.CHOOSE_CARD

    def draw_extra_phase(self) -> GamePhase:
        current_player = self.game_state.current_player()
        card = self.game_state.draw_card()
        print(f"Player {current_player} draws {card}")
        self.inform_all("inform_card_drawn", current_player)
        post_event(
            CustomEvents.EVENT_DRAW_CARD,
            card=card,
            player_index=self.game_state.current_player_index,
        )
        return GamePhase.CHOOSE_CARD_AGAIN

    def choose_card_again_phase(self) -> GamePhase:
        current_player = self.game_state.current_player()
        playable_cards = current_player.hand.playable_cards(self.game_state.top)
        if playable_cards:
            # играть может только вновь взятая карта, остальные не подходят
            card = playable_cards[0]
            print(f"Player {current_player} can play drawn card")
            if self.player_types[current_player].choose_to_play(
                self.game_state.top, card
            ):
                print(f"Player {current_player.name} played {card}")
                current_player.hand.remove_card(card)
                self.game_state.top = card
                self.inform_all("inform_card_played", current_player, card)
                post_event(
                    CustomEvents.EVENT_PLAY_CARD,
                    card=card,
                    player_index=self.game_state.current_player_index,
                )
            else:
                print(f"Player decides not to play {card}")

        return GamePhase.NEXT_PLAYER

    def choose_card_phase(self) -> GamePhase:
        current_player = self.game_state.current_player()
        playable_cards = current_player.hand.playable_cards(self.game_state.top)

        print(
            f"Player {current_player.name} with hand {current_player.hand} can play {playable_cards} on top of {self.game_state.top}"
        )

        if not playable_cards:
            print(f"Player {current_player.name} could not play any card")
            return GamePhase.DRAW_EXTRA

        card = self.player_types[current_player].choose_card(
            current_player.hand, self.game_state.top
        )
        if type(card) == CustomEvents:
            assert card == CustomEvents.AWAITING_GUI
            return GamePhase.CHOOSE_CARD

        if card is None:
            print(f"Player {current_player.name} skipped a turn")
            return GamePhase.DRAW_EXTRA

        assert card in playable_cards
        print(f"Player {current_player.name} played {card}")
        current_player.hand.remove_card(card)
        self.game_state.top = card
        self.inform_all("inform_card_drawn", current_player)
        post_event(
            CustomEvents.EVENT_PLAY_CARD,
            card=card,
            player_index=self.game_state.current_player_index,
        )
        return GamePhase.NEXT_PLAYER

    def inform_all(self, method: str, *args, **kwargs):
        """
        Calls player_interaction.method with *args, **kwargs for all players

        self.inform_all(..., player, card=Card('g7'))
          args   : [player]
          kwargs : {"card":Card('g7')}

        self.inform_all(..., player=player, card=Card('g7'))
          args   : []
          kwargs : {"player":player, "card":Card('g7')}
        """
        for p in self.player_types.values():
            getattr(p, method)(*args, **kwargs)

    @staticmethod
    def request_player_count() -> int:
        while True:
            try:
                player_count = int(input("How many players?"))
                if 2 <= player_count <= 10:
                    return player_count
            except ValueError:
                pass
            print("Please input a number between 2 and 10")

    @staticmethod
    def request_player() -> (str, PlayerInteraction):
        """Возвращает имя и тип игрока."""

        """Разрешенные типы игроков из PlayerInteraction."""
        # Getting all names of subclasses of PlayerInteraction from  all_player_types
        player_types = []
        for name, cls in inspect.getmembers(all_player_types):
            if inspect.isclass(cls) and issubclass(cls, PlayerInteraction):
                player_types.append(cls.__name__)
        player_types_as_str = ', '.join(player_types)

        while True:
            name = input("How to call a player?")
            if name.isalpha():
                break
            print("Name must be a single word, alphabetic characters only")

        while True:
            try:
                kind = input(f"What kind of player is it ({player_types_as_str})?")
                kind = getattr(all_player_types, kind)
                break
            except AttributeError:
                print(f"Allowed player types are: {player_types_as_str}")
        return name, kind

    def check_data_for_gui(self):
        """Так как в GUI костыль, то игроков должно быть строго 2 и они - боты."""
        ptypes = self.player_types
        if len(ptypes) != 2:
            raise ValueError(f'Игроков должно быть 2,  по факту {len(ptypes)}')


def __main__():
    load_from_file = False
    if load_from_file:
        server = GameServer.load_game('uno.json')
    else:
        server = GameServer.new_game(GameServer.get_players())
    server.save('uno.json')
    server.run()


if __name__ == "__main__":
    __main__()
