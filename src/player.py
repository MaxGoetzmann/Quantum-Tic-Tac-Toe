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
    O_WIN_STATE: np.ndarray[np.float32] = [1.0, 0]
    X_WIN_STATE: np.ndarray[np.float32] = [0, 1.0]


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
