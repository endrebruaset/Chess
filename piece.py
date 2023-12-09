from enum import Enum

class PieceColor(Enum):
    WHITE = 0
    BLACK = 1
    
class PieceType(Enum):
    PAWN = 0,
    KNIGHT = 1,
    BISHOP = 2,
    ROOK = 3,
    QUEEN = 4,
    KING = 5

class Piece:
    def __init__(self, color: PieceColor, type: PieceType):
        self.color = color
        self.type = type