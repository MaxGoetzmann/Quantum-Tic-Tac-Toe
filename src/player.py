"""Player"""

from enum import Enum
from typing import Union


class PlayerPiece(Enum):
    """
    Player pieces they can choose.
    """
    O = 0
    X = 1


class Player():
    """
    Player piece

    fields:

    functions:
    """

    piece_selection: PlayerPiece
    went_first: bool

    def __init__(self, piece_selection: Union[None, PlayerPiece]) -> None:
        self.piece_selection = piece_selection
