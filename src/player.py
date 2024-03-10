"""
Player class and pieces the player could be
"""

from enum import Enum


class PlayerPiece(Enum):
    """
    Player pieces they can choose.
    """
    O: int = 0
    X: int = 1


class Player():
    """
    Player controlling one of the letters the game.

    fields:
        piece_selection (PlayerPiece): Xs or Os.
        went_first (bool): Did this player make the first move?

    methods:
        get_selection() -> PlayerPiece
    """

    piece_selection: PlayerPiece
    went_first: bool

    def __init__(self, piece_selection: PlayerPiece, first: bool) -> None:
        """
        parameters:
            piece_selection (PlayerPiece): Pick Xs or Os.
            first (bool): Does this player go first?

        returns: 
            None
        """
        self.piece_selection = piece_selection
        self.went_first = first

    def get_selection(self) -> PlayerPiece:
        """
        Return whether this player is an X or O.

        parameters:
            None

        returns: 
            PlayerPiece
        """
        return self.piece_selection

    def get_went_first(self) -> bool:
        """
        Wrapper for returning if player went first.
        """
        return self.went_first

    def __str__(self) -> str:
        if self.piece_selection == PlayerPiece.O:
            return "O"
        return "X"
