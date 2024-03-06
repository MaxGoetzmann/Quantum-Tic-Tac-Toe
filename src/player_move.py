"""Player Move"""

from enum import Enum
from typing import Union
from player import Player


class MoveType(Enum):
    """
    All of the different moves a player can make.
    """
    PLACE = 0
    HGATE = 1
    ZGATE = 2
    NOTGATE = 3
    CNOTPLACE = 4
    INVCNOTPLACE = 5


OneQubitMove = tuple(int, int)
TwoQubitMove = tuple(OneQubitMove, OneQubitMove)


class PlayerMove():
    """
    Save what the player move is.
    """
    type: MoveType
    target: Union[OneQubitMove, TwoQubitMove]

    def __init__(self, type: MoveType, target: Union[OneQubitMove, TwoQubitMove], origin: Player, turn: int) -> None:
        pass

    def get_type(self):
        return self.type
