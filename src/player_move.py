"""Player Move"""

from enum import Enum
from typing import Union
from player import Player


class MoveType(Enum):
    """
    All of the different moves a player can make.
    """
    PLACE = 0
    PLACE_SUPERPOS = 1
    HGATE = 2
    ZGATE = 3
    NOTGATE = 4
    CNOTPLACE = 5
    INVCNOTPLACE = 6


OneQubitMove = tuple[int]
TwoQubitMove = tuple[OneQubitMove]


class PlayerMove():
    """
    Save what the player move is.
    """
    type: MoveType
    target: Union[OneQubitMove, TwoQubitMove]
    origin: Player
    turn: int

    def __init__(self, type: MoveType, target: Union[OneQubitMove, TwoQubitMove], origin: Player, turn: int) -> None:
        self.type = type
        self.target = target
        self.origin = origin
        self.turn = turn

    def get_type(self) -> MoveType:
        return self.type

    def get_target(self) -> Union[OneQubitMove, TwoQubitMove]:
        return self.target

    def is_place(self) -> bool:
        return self.type in (MoveType.PLACE, MoveType.PLACE_SUPERPOS)

    def is_gate(self) -> bool:
        return self.type in (MoveType.HGATE, MoveType.ZGATE, MoveType.NOTGATE,
                             MoveType.CNOTPLACE, MoveType.INVCNOTPLACE)

    def __str__(self) -> str:
        return f"{self.type} @ ({self.target[0]}, {self.target[1]})"
