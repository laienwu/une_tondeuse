from enum import IntEnum


class Direction(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3


class Rotation(IntEnum):
    # Clockwise
    G = -1
    D = 1
