from board import Board
from square import Square
from piece import Piece, PieceColor, PieceType
from move import Move
from typing import Optional
from copy import deepcopy

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = PieceColor.WHITE
        self.double_pawn_push: Optional[Square] = None
        self.castling_rights = {
            PieceColor.WHITE: { "a": True, "h": True },
            PieceColor.BLACK: { "a": True, "h": True }
        }
        
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
        
    def make_move(self, move: Move) -> None:
        self.board[move.end] = self.board[move.start]
        self.board[move.start] = None
        self.turn = PieceColor.opposing_color(self.turn)
        
    def simulate_move(self, move: Move) -> Board:
        simulated_board = deepcopy(self.board)
        simulated_board[move.end] = simulated_board[move.start]
        simulated_board[move.start] = None
    
        return simulated_board
        