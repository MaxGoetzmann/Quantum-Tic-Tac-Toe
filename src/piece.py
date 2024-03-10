"""
Piece class for the pieces currently placed on the board. Also contains and enum for the 
game-relevant states that a piece can be in.
"""

from typing import Union
import numpy as np
from gate import GateMatrix
from player import PlayerPiece


class PieceStates():
    """
    Different constant quantum states translated to their meaning.
    """
    O_WIN: np.ndarray[np.float32] = [1.0, 0]
    X_WIN: np.ndarray[np.float32] = [0, 1.0]
    O_POS: np.ndarray[np.float32] = np.round(
        [GateMatrix.INV_ROOT_2, GateMatrix.INV_ROOT_2], 1)
    X_NEG: np.ndarray[np.float32] = np.round(
        [GateMatrix.INV_ROOT_2, -GateMatrix.INV_ROOT_2], 1)


class Piece():
    """
    A piece on the gameboard that is either an X or an O in superposition.

    fields:
        Quantum state of the piece in vector notation. 0 is equivalent to O and X is to 1.
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

        out = np.round(self.state, 1)

        if out[0] <= 0.1:
            out = out * -1

        return out

    def get_owner(self) -> Union[PlayerPiece, None]:
        """
        Return the player that won if there is one.
        """
        if np.array_equal(self.get_state(), PieceStates.O_WIN):
            return PlayerPiece.O
        if np.array_equal(self.get_state(), PieceStates.X_WIN):
            return PlayerPiece.X
        return None

    def h_gate(self) -> None:
        """
        Apply the H gate to the state of this piece.
        """
        self.state = GateMatrix.H @ self.state

    def not_gate(self) -> None:
        """
        Apply the NOT/X gate to the state of this piece.
        """
        self.state = GateMatrix.NOT @ self.state

    def z_gate(self) -> None:
        """
        Apply the Z gate to the state of this piece.
        """
        self.state = GateMatrix.Z @ self.state

    def any_gate(self, gate) -> None:
        """
        Apply an arbitrary single-qubit gate to this piece.
        """
        self.state = gate @ self.state

    def __str__(self) -> str:
        state = np.abs(self.get_state())
        if np.array_equal(state, PieceStates.O_WIN):
            return "O"
        elif np.array_equal(state, PieceStates.X_WIN):
            return "X"
        elif np.array_equal(state, PieceStates.O_POS):
            return "+"
        elif np.array_equal(state, PieceStates.X_NEG):
            return "-"
