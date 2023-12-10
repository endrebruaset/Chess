from square import Square
from piece import Piece, PieceColor
from typing import Optional

class Board:
    def __init__(self):        
        self.squares = [Square(row, col) for col in range(8) for row in range(8)]
        self.board: dict[Square, Optional[Piece]] = { square: None for square in self.squares }
        
    def __getitem__(self, square: Square):
        if square.is_valid():
            return self.board[square]
        else:
            raise KeyError(f'Invalid square: {square}')
            
    def __setitem__(self, square: Square, piece: Piece):
        if square.is_valid():
            self.board[square] = piece
        else:
            raise KeyError(f'Invalid square: {square}')
    
    def get_squares_with_pieces(self, color: PieceColor) -> list[Square]:
        squares_with_pieces = []
        
        for square in self.squares:
            piece = self.board[square]
            if piece is not None and piece.color == color:
                squares_with_pieces.append(square)
        
        return squares_with_pieces
    
    def get_empty_squares(self) -> list[Square]:
        empty_squares = []
        
        for square in self.squares:
            piece = self.board[square]
            if piece is None:
                empty_squares.append(square)
                
        return empty_squares    