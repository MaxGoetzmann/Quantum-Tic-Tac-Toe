"""Piece"""

import numpy as np


class Piece():
    """
    Either an X or an O in superposition.
    """

    state: list[int] = np.array([-1, -1])

    def __init__(self, init_val: int) -> None:
        assert init_val == 0 or init_val == 1

        if init_val == 0:
            self.state = np.array([1, 0])
        else:
            self.state = np.array([0, 1])

    @staticmethod
    def get_state() -> list[int]:
        """
        Return a rounded (-1, -0.5, 0, 0.5, 1) version of the state held in this piece. Rounding is
          done for compatibility with JSON.
        """
