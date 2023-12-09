from square import Square
from piece import Piece
from typing import Optional

class Board:
    def __init__(self):        
        squares = [Square(row, col) for col in range(8) for row in range(8)]
        self.board: dict[Square, Optional[Piece]] = { square: None for square in squares }
        
    def __getitem__(self, square: Square):
        if 0 <= square.row < 8 and 0 <= square.column < 8:
            return self.board[square]
        else:
            raise KeyError(f'Invalid square: {square}')
            
    def __setitem__(self, square: Square, piece: Piece):
        if 0 <= square.row < 8 and 0 <= square.column < 8:
            self.board[square] = piece
        else:
            raise KeyError(f'Invalid square: {square}')