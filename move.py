from square import Square
from enum import Enum

class MoveType(Enum):
    ORDINARY = 0,
    CASTLING = 1,
    DOUBLE_PAWN_PUSH = 2,
    PAWN_PROMOTION = 3

class Move:
    def __init__(self, start: Square, end: Square, move_type: MoveType = MoveType.ORDINARY) -> None:
        self.start = start
        self.end = end
        self.move_type = move_type
        
    def __str__(self) -> str:
        return f'{self.start} to {self.end}'
    
    def __eq__(self, __value: object) -> bool:
        return self.start == __value.start and \
            self.end == __value.end and \
            self.move_type == __value.move_type
    