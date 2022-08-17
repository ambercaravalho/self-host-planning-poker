from gamestate.deck import Deck
from gamestate.illegal_operation_error import IllegalOperationError
from gamestate.player import Player


class Game:
    """Class representing the state of a game of Planning Poker"""
    def __init__(self, deck: Deck = Deck.FIBONACCI):
        self.__state = {}
        self.deck = deck

    def player_joins(self, uuid: str, player: Player):
        self.__state[uuid] = player

    def player_leaves(self, uuid: str):
        self.__state.pop(uuid)

    def list_players(self) -> [tuple[str, Player]]:
        return list(self.__state.items())

    def list_players_uuid(self) -> [str]:
        return list(self.__state)

    def get_player(self, uuid: str) -> Player:
        if uuid not in self.__state.keys():
            raise IllegalOperationError(f'Player with UUID {uuid} is not in this game')
        return self.__state.get(uuid)
        
    def player_picks(self, uuid: str, card: int):
        if card not in self.deck.value:
            raise IllegalOperationError(f'Card value {card} is not valid. Current deck is {self.deck.name}')
        player: Player = self.get_player(uuid)
        player.set_hand(card)

    def end_turn(self):
        for player in self.__state.values():
            player.clear_hand()

    def is_game_empty(self) -> bool:
        return len(self.__state) == 0

    def has_all_players_picked_card(self) -> bool:
        non_spectators = self.get_non_spectator_players()
        players_that_played_count = sum(1 for p in non_spectators if p.has_picked_card())
        return players_that_played_count == len(non_spectators)

    def get_non_spectator_players(self) -> [Player]:
        return list(filter(lambda p: p.spectator is False, self.__state.values()))

    def state(self) -> [tuple[str, dict]]:
        """Returns the game's state with the players' hands hidden"""
        return list(map(
            lambda i: (i[0], i[1].state()),
            self.list_players()
        ))

    def reveal_hands(self) -> [tuple[str, int]]:
        """Return the players' with their hands"""
        return list(map(
            lambda i: (i[0], i[1].get_hand()),
            filter(lambda p: p[1].spectator is False, self.list_players())
        ))
