from board import Board
from square import Square
from piece import Piece, PieceColor, PieceType
from move import Move, MoveType
from typing import Optional
from copy import deepcopy

class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.turn = PieceColor.WHITE
        self.en_passant: Optional[Square] = None
        self.short_castling_rights = { PieceColor.WHITE: True, PieceColor.BLACK: True }
        self.long_castling_rights = { PieceColor.WHITE: True, PieceColor.BLACK: True }
        
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
        moved_piece = self.board[move.start]
        self.board[move.end] = moved_piece
        self.board[move.start] = None
        
        # Check if pawn was captured en passant
        if self.__is_en_passant(move, moved_piece):
            captured_pawn = Square(move.end.row - Board.get_pawn_direction(self.turn), move.end.column)
            self.board[captured_pawn] = None
        
        # Update special moves state
        match move.type:
            case MoveType.ORDINARY:
                self.en_passant = None
                self.__set_castling_rights(move, moved_piece)
                
            case MoveType.DOUBLE_PAWN_PUSH:
                self.en_passant = Square(move.end.row - Board.get_pawn_direction(self.turn), move.end.column)
                
            case MoveType.PAWN_PROMOTION:
                self.board[move.end] = Piece(self.turn, PieceType.QUEEN)
                
            case MoveType.SHORT_CASTLE | MoveType.LONG_CASTLE:
                self.__castle(move)
                self.short_castling_rights[self.turn] = False
                self.long_castling_rights[self.turn] = False   
        
        # Change turn
        self.turn = PieceColor.opposing_color(self.turn)
        
    def simulate_move(self, move: Move) -> Board:
        simulated_board = deepcopy(self.board)
        simulated_board[move.end] = simulated_board[move.start]
        simulated_board[move.start] = None
    
        return simulated_board
    
    def __is_en_passant(self, move: Move, moved_piece: Piece) -> bool:
        return self.en_passant is not None \
            and move.end == self.en_passant \
            and moved_piece.type == PieceType.PAWN
            
    def __castle(self, move: Move) -> None:
        row = move.end.row
        
        if move.type == MoveType.LONG_CASTLE:
            empty_squares = [Square(row, 0), Square(row, 1), Square(row, 4)]
            king_square = Square(row, 2)
            rook_square = Square(row, 3)
        
        elif move.type == MoveType.SHORT_CASTLE:
            empty_squares = [Square(row, 4), Square(row, 7)]
            king_square = Square(row, 6)
            rook_square = Square(row, 5)
        
        self.board[king_square] = Piece(self.turn, PieceType.KING)
        self.board[rook_square] = Piece(self.turn, PieceType.ROOK)
        for empty_square in empty_squares:
            self.board[empty_square] = None
            
    def __set_castling_rights(self, move: Move, moved_piece: Piece) -> None:
        if moved_piece.type == PieceType.KING:
            self.short_castling_rights[self.turn] = False
            self.long_castling_rights[self.turn] = False
        
        elif moved_piece.type == PieceType.ROOK and move.start.column == 0:
            self.long_castling_rights[self.turn] = False
        
        elif moved_piece.type == PieceType.ROOK and move.start.column == 7:
            self.short_castling_rights[self.turn] = False
        