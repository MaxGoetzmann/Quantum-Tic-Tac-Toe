"""Board"""

from typing import Union
from piece import Piece
from player import Player


class Board():

    board: list[list[Union[None, Piece]]]

    def __init__(self) -> None:
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    def check_win(self) -> Union[Player, None]:
        return None
