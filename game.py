from board import Board
from square import Square
from piece import Piece, PieceColor, PieceType
from move import Move, MoveType
from typing import Optional
from copy import deepcopy

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = PieceColor.WHITE
        self.en_passant: Optional[Square] = None
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
        # Perform move
        self.board[move.end] = self.board[move.start]
        self.board[move.start] = None
        
        # Check if pawn was captured en passant
        if self.__is_en_passant(move):
            captured_pawn = Square(move.end.row - Board.get_pawn_direction(self.turn), move.end.column)
            self.board[captured_pawn] = None
        
        # Update special moves state
        match move.move_type:
            case MoveType.ORDINARY:
                self.en_passant = None
                
            case MoveType.DOUBLE_PAWN_PUSH:
                self.en_passant = Square(move.end.row - Board.get_pawn_direction(self.turn), move.end.column)
                
            case MoveType.PAWN_PROMOTION:
                self.board[move.end] = Piece(self.turn, PieceType.QUEEN)
        
        # Change turn
        self.turn = PieceColor.opposing_color(self.turn)
        
    def simulate_move(self, move: Move) -> Board:
        simulated_board = deepcopy(self.board)
        simulated_board[move.end] = simulated_board[move.start]
        simulated_board[move.start] = None
    
        return simulated_board
    
    def __is_en_passant(self, move: Move):
        moved_piece = self.board[move.end]
        
        return self.en_passant is not None \
            and move.end == self.en_passant \
            and moved_piece.type == PieceType.PAWN
        