"""Player Move class and the MoveTypes a player could make"""

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
    # CNOTPLACE = 5
    # INVCNOTPLACE = 6


OneQubitMove = tuple[int]
TwoQubitMove = tuple[OneQubitMove]


class PlayerMove():
    """
    Summary of each move a player made.

    fields:
        type (MoveType): The type of move the player made.
        target (OneQubitMove, TwoQubitMove): Squares the player targeted in the move.
        origin (Player): Player that made the move.

    class methods:
        get_type() -> MoveType
        get_target() -> target
        is_place() -> bool
        is_gate() -> bool

    static methods:
        match_abbr_to_move(str) -> MoveType
    """
    type: MoveType
    target: Union[OneQubitMove, TwoQubitMove]
    origin: Player

    def __init__(self, move: MoveType, target: Union[OneQubitMove, TwoQubitMove],
                 origin: Player) -> None:
        self.type = move
        self.target = target
        self.origin = origin

    def get_type(self) -> MoveType:
        """
        Wrapper to returning type of move.
        """
        return self.type

    def get_target(self) -> Union[OneQubitMove, TwoQubitMove]:
        """
        Wrapper to return target square(s) of move.
        """
        return self.target

    def is_place(self) -> bool:
        """
        Is the move's type the placement of a piece?
        """
        return self.type in (MoveType.PLACE, MoveType.PLACE_SUPERPOS)

    def is_gate(self) -> bool:
        """
        Is the move's type the placement of a gate?
        """
        return self.type in (MoveType.HGATE, MoveType.ZGATE, MoveType.NOTGATE,
                             # MoveType.CNOTPLACE, MoveType.INVCNOTPLACE
                             )

    @staticmethod
    def match_abbr_to_move(abbr: str) -> MoveType:
        """
        Match string input to a corresponding valid MoveType.
        """
        match abbr:
            case "PLACE":
                return MoveType.PLACE
            case "PLACE_SUPERPOS":
                return MoveType.PLACE_SUPERPOS
            case "HGATE":
                return MoveType.HGATE
            case "ZGATE":
                return MoveType.ZGATE
            case "NOTGATE":
                return MoveType.NOTGATE
            # case "CNOTPLACE":
            #     return MoveType.CNOTPLACE

        raise TypeError("Unsupported move type")

    def __str__(self) -> str:
        return f"{self.type} @ ({self.target[0]}, {self.target[1]})"
