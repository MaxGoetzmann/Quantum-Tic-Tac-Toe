"""Board"""

from typing import Union
from piece import Piece
from player_move import OneQubitMove
from player import PlayerPiece
from gate import Gate


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
        return isinstance(self.get_square(target), Piece)

    def is_gate(self, target: OneQubitMove) -> bool:
        return isinstance(self.get_square(target), Gate)

    def get_square(self, target: OneQubitMove) -> Union[Piece, Gate, None]:
        return self.board[target[0]][target[1]]

    def get_board(self) -> list[list[Union[None, Piece, Gate]]]:
        return self.board

    def get_owner(self, target: OneQubitMove) -> Union[PlayerPiece, None]:
        if not self.is_piece(target):
            return None
        return self.get_square(target).get_owner()

    def str_arr(self) -> list[list[Union[str]]]:
        out = []
        for i in self.board:
            new_row = []
            for j in i:
                new_row.append(str(j))
            out.append(new_row)
        return out

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
