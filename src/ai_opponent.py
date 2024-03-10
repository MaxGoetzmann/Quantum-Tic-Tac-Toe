"""
AI Opponent class. Is an extension of the player class. Query using game state to get the best
move for the opponent to make. Will try to avoid repetition where possible, but otherwise just
tries not to lose by making random moves.
"""

from typing import Union
import jsonpickle
import numpy as np
from game import Game
from player import Player, PlayerPiece
from player_move import PlayerMove, MoveType


class AiOpponent(Player):

    max_depth: int
    last_move: Union[PlayerMove, None]

    def __init__(self, piece_selection: PlayerPiece, first: bool, depth: int = 3) -> None:
        super().__init__(piece_selection, first)
        self.max_depth = depth

    @staticmethod
    def _make_new_game_instance(game: Game) -> Game:
        return jsonpickle.decode(jsonpickle.encode(game))

    @staticmethod
    def _probe_moves():
        pass

    def get_move(self, game: Game) -> PlayerMove:
        new_game = AiOpponent._make_new_game_instance(game)

        # generate list of random moves, where do not repeat gates of
        # opponents last move
        # search depth max_depth, where (AI makes move, then player) = 1 iteration
        # if find a win for AI, return base immediately
        # if find a win for opponent, prune immediately
        # else just return the last one in the sequence
