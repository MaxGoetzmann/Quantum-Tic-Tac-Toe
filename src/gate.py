from enum import Enum
import numpy as np


inv_root_2 = 1/np.sqrt(2)


class GateType(Enum):
    H = 0
    Z = 1
    NOT = 2


class GateMatrix(Enum):
    INV_ROOT_2 = inv_root_2
    H = np.array([
        [inv_root_2, inv_root_2],
        [inv_root_2, -inv_root_2]
    ])
    NOT = np.array([
        [0, 1],
        [1, 0]
    ])
    Z = np.array([
        [1, 0],
        [0, -1]
    ])


class Gate():

    type: GateType

    def __init__(self, type: GateType) -> None:
        self.type = type

    def __str__(self) -> str:
        if self.type == GateType.H:
            return "H"
        elif self.type == GateType.NOT:
            return "~"
        elif self.type == GateType.Z:
            return "Z"

    def mat(self) -> np.ndarray[np.float32]:
        if self.type == GateType.H:
            return GateMatrix.H
        elif self.type == GateType.NOT:
            return GateMatrix.NOT
        elif self.type == GateType.Z:
            return GateMatrix.Z
