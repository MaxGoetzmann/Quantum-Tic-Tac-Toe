"""
AI Opponent class. Is an extension of the player class. Query using game state to get the best
move for the opponent to make. Will try to avoid repetition where possible, but otherwise just
tries not to lose by making random moves.
"""

from typing import Union
from enum import Enum
import jsonpickle
import numpy as np
from game import Game
from player import Player, PlayerPiece
from player_move import PlayerMove, MoveType


class AiMoveWeight(Enum):
    LOSS = 0
    NOT_LOSS = 1
    WIN = 2


MoveEval = dict[PlayerMove, AiMoveWeight]

# TODO: make private if possible? These are just helpers.


def shuffled_seq(n: int):
    return np.random.shuffle(range(n))


def get_move_permutations(last_move: PlayerMove, player: Player) -> MoveEval:
    bases: dict[PlayerMove, AiMoveWeight] = {}
    for move_type in MoveType:
        for row in shuffled_seq(3):
            for col in shuffled_seq(3):
                # No direct repetition of opponent.
                if last_move and \
                        last_move.type == move_type and \
                        last_move.row == row and \
                        last_move.col == col:
                    continue

                move = PlayerMove(move_type, (row, col), player)
                bases[move] = AiMoveWeight.LOSS
    return bases


def probe_moves_helper(game: Game, ai_player: Player, cur_depth: int, max_depth: int) -> AiMoveWeight:
    if cur_depth >= max_depth:
        return AiMoveWeight.NOT_LOSS

    if game.get_current_player() != ai_player:
        cur_depth += 1


def probe_moves(game: Game, max_depth: int) -> PlayerMove:
    bases = get_move_permutations(game, game.get_current_player())
    for base in bases:
        new_game = make_new_game_instance(game)
        val = probe_moves_helper(
            new_game, new_game.get_current_player(), 0, max_depth)
        if val == AiMoveWeight.WIN:
            return base
        bases[base] = val

    for k, v in bases.items():
        if v == AiMoveWeight.NOT_LOSS:
            return k

    # TODO: How to return random key from dictionary
    return bases.pop()


def make_new_game_instance(game: Game) -> Game:
    return jsonpickle.decode(jsonpickle.encode(game))


class AiOpponent(Player):

    max_depth: int
    last_move: Union[PlayerMove, None]

    def __init__(self, piece_selection: PlayerPiece, first: bool, depth: int = 3) -> None:
        super().__init__(piece_selection, first)
        self.max_depth = depth

    def get_move(self, game: Game) -> PlayerMove:
        return probe_moves(game, self.max_depth)

        # search depth max_depth, where (AI makes move, then player) = 1 iteration
        # if find a win for AI, return base immediately
        # if find a win for opponent, prune immediately
        # else just return the last one in the sequence
