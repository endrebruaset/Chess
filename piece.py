from __future__ import annotations
from enum import Enum

class PieceColor(Enum):
    WHITE = 0
    BLACK = 1
    
    @staticmethod
    def opposing_color(color: PieceColor) -> PieceColor:
        return PieceColor.BLACK if color == PieceColor.WHITE else PieceColor.WHITE
    
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