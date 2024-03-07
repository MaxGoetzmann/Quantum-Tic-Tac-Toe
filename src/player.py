"""Player"""

from enum import Enum
from typing import Union
import numpy as np


class PlayerPiece(Enum):
    """
    Player pieces they can choose.
    """
    O: int = 0
    X: int = 1


class Player():
    """
    Player piece

    fields:

    functions:
    """

    piece_selection: PlayerPiece
    went_first: bool

    def __init__(self, piece_selection: Union[None, PlayerPiece], first: bool) -> None:
        self.piece_selection = piece_selection
        self.went_first = first

    def get_selection(self) -> PlayerPiece:
        return self.piece_selection

    def __str__(self) -> str:
        if self.piece_selection == PlayerPiece.O:
            return "O"
        return "X"
