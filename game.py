from board import Board
from square import Square
from piece import Piece, PieceColor, PieceType
from typing import Optional


class Game:
    def __init__(self):
        self.board = Board()
        self.turn = PieceColor.WHITE
        self.double_pawn_push: Optional[Square] = None
        
        # Create starting position
        for row, color in zip([0, 7], [PieceColor.WHITE, PieceColor.BLACK]):
            self.board[Square(row, 0)] = Piece(color, PieceType.ROOK)
            self.board[Square(row, 1)] = Piece(color, PieceType.KNIGHT)
            self.board[Square(row, 2)] = Piece(color, PieceType.BISHOP)
            self.board[Square(row, 3)] = Piece(color, PieceType.QUEEN)
            self.board[Square(row, 4)] = Piece(color, PieceType.KING)
            self.board[Square(row, 5)] = Piece(color, PieceType.BISHOP)
            self.board[Square(row, 6)] = Piece(color, PieceType.KNIGHT)
            self.board[Square(row, 7)] = Piece(color, PieceType.ROOK)
        
        for column in range(8):
            self.board[Square(1, column)] = Piece(PieceColor.WHITE, PieceType.PAWN)
            self.board[Square(6, column)] = Piece(PieceColor.BLACK, PieceType.PAWN)