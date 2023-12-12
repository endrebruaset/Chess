from square import Square
from enum import Enum

class MoveType(Enum):
    ORDINARY = 0,
    SHORT_CASTLE = 1,
    LONG_CASTLE = 2,
    DOUBLE_PAWN_PUSH = 3,
    PAWN_PROMOTION = 4

class Move:
    def __init__(self, start: Square, end: Square, type: MoveType = MoveType.ORDINARY) -> None:
        self.start = start
        self.end = end
        self.type = type
    
    def __eq__(self, __value: object) -> bool:
        return self.start == __value.start and \
            self.end == __value.end and \
            self.type == __value.type
    