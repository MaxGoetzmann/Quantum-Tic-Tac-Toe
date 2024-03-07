"""Board"""

from typing import Union
from piece import Piece, PieceStates
from player_move import OneQubitMove
from player import PlayerPiece
from gate import Gate
import numpy as np


class Board():
    """
    """

    board: list[list[Union[None, Piece, Gate]]]

    def __init__(self) -> None:
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    def place(self, obj: Union[Piece, Gate], target: OneQubitMove) -> None:
        self.board[target[0]][target[1]] = obj

    def is_piece(self, target: OneQubitMove) -> bool:
        return isinstance(self.board[target[0]][target[1]]) == Piece

    def is_gate(self, target: OneQubitMove) -> bool:
        return isinstance(self.board[target[0]][target[1]]) == Gate

    def get_square(self, target: OneQubitMove) -> Union[Piece, Gate, None]:
        return self.board[target[0]][target[1]]

    def get_owner(self, target: OneQubitMove) -> Union[PlayerPiece, None]:
        if not self.is_piece(target):
            return None
        return self.board[target[0]][target[1]].get_owner()

    def __str__(self) -> str:
        out = ""
        for row in self.board:
            out += "|"
            for col in row:
                if col is None:
                    out += " "
                else:
                    out += str(col)
                out += "|"
            out += "\n"
        return out[:-1]
