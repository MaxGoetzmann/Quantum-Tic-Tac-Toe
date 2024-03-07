"""Piece"""

from enum import Enum
from typing import Union
from gate import GateMatrix
import numpy as np
from player import Player, PlayerPiece


class PieceStates(Enum):
    """
    Different states and what they mean.
    """
    O_WIN: np.ndarray[np.float32] = [1.0, 0]
    X_WIN: np.ndarray[np.float32] = [0, 1.0]
    O_POS: np.ndarray[np.float32] = np.round(
        [GateMatrix.INV_ROOT_2, GateMatrix.INV_ROOT_2], 1)
    X_NEG: np.ndarray[np.float32] = np.round(
        [GateMatrix.INV_ROOT_2, -GateMatrix.INV_ROOT_2], 1)


class Piece():
    """
    Either an X or an O in superposition.
    """

    state: np.ndarray[np.float32] = np.array([-1.0, -1.0])

    def __init__(self, init_val: PlayerPiece, make_superpos=False) -> None:
        if init_val == PlayerPiece.O:
            self.state = np.array(PieceStates.O_WIN)
        else:
            self.state = np.array(PieceStates.X_WIN)

        if make_superpos:
            self.h_gate()

    def get_state(self) -> np.ndarray[np.float32]:
        """
        Return version of the state held in this piece. Values are in the set 
        (-1, -1/sqrt(2), 0, 1/sqrt(2), 1), rounded to the nearest tenth. Rounding is done for 
        maximum compatibility.
        """

        if self.state[0] < 0:
            self.state = self.state * -1

        out = np.round(self.state, 1)

        return out

    def get_owner(self) -> Union[PlayerPiece, None]:
        """
        Return enum of the player that won.
        """
        if np.array_equal(self.state, PieceStates.O_WIN):
            return PlayerPiece.O
        if np.array_equal(self.state, PieceStates.X_WIN):
            return PlayerPiece.X
        return None

    def h_gate(self) -> None:
        self.state = GateMatrix.H @ self.state

    def not_gate(self) -> None:
        self.state = GateMatrix.NOT @ self.state

    def z_gate(self) -> None:
        self.state = GateMatrix.Z @ self.state

    def any_gate(self, gate) -> None:
        self.state = gate @ self.state

    def __str__(self) -> str:
        if np.array_equal(self.get_state(), PieceStates.O_WIN):
            return "O"
        elif np.array_equal(self.get_state(), PieceStates.X_WIN):
            return "X"
        elif np.array_equal(self.get_state(), PieceStates.O_POS):
            return "+"
        elif np.array_equal(self.get_state(), PieceStates.X_NEG):
            return "-"
