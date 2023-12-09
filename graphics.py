from board import Board
from piece import PieceColor, PieceType
from square import Square
from typing import Optional
from settings import SQUARE_SIZE
import pygame

class SquareColor:
    LIGHT = pygame.Color('#ffffff')
    DARK = pygame.Color('#51753f')
    CHECK = pygame.Color('#ba4141')
    SELECTED = pygame.Color('#fad96e')
    LATEST_MOVE = pygame.Color('#fcd03d')

class Graphics:
    piece_images = {
        PieceColor.WHITE: {
            PieceType.PAWN:     pygame.image.load('pieces/wP.svg'),
            PieceType.KNIGHT:   pygame.image.load('pieces/wN.svg'),
            PieceType.BISHOP:   pygame.image.load('pieces/wB.svg'), 
            PieceType.ROOK:     pygame.image.load('pieces/wR.svg'), 
            PieceType.QUEEN:    pygame.image.load('pieces/wQ.svg'), 
            PieceType.KING:     pygame.image.load('pieces/wK.svg'), 
        },
        PieceColor.BLACK: {
            PieceType.PAWN:     pygame.image.load('pieces/bP.svg'),
            PieceType.KNIGHT:   pygame.image.load('pieces/bN.svg'),
            PieceType.BISHOP:   pygame.image.load('pieces/bB.svg'), 
            PieceType.ROOK:     pygame.image.load('pieces/bR.svg'), 
            PieceType.QUEEN:    pygame.image.load('pieces/bQ.svg'), 
            PieceType.KING:     pygame.image.load('pieces/bK.svg'), 
        },
    }
    
    def __init__(self) -> None:
        height = width = 8 * SQUARE_SIZE
        self.display = pygame.display.set_mode((height, width))
        
        # Create background
        self.background = pygame.Surface((height, width))
        self.background.fill(SquareColor.LIGHT)
        for row in range(0, 8):
            for column in range(0, 8):
                if (row + column) % 2 == 0:
                    pygame.draw.rect(
                        self.background, 
                        SquareColor.DARK, 
                        (row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    )
        
        # Mouse state
        self.selected_square: Optional[Square] = None
        
    def draw_board(self, board: Board) -> None:
        # Draw empty board
        self.display.blit(self.background, self.background.get_rect())
        
        # Highlight selected square
        if self.selected_square is not None:
            (x, y) = Coordinates.get_coordinates(self.selected_square)
            
            pygame.draw.rect(
                self.display,
                SquareColor.SELECTED,
                (x, y, SQUARE_SIZE, SQUARE_SIZE)
            )
        
        # Draw pieces
        for square, piece in board.board.items():
            if piece is not None:
                coordinates = Coordinates.get_coordinates(square)
                piece_image = self.piece_images[piece.color][piece.type]
                self.display.blit(piece_image, coordinates)
        
        # Update display
        pygame.display.flip()
        
    def set_cursor(self, coordinates: tuple[int, int], board: Board, color: PieceColor) -> None:
        if Mouse.is_own_piece(coordinates, board, color):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    def handle_click(self, coordinates: tuple[int, int], board: Board, turn) -> None:
        if Mouse.is_own_piece(coordinates, board, turn):
            self.selected_square = Coordinates.get_square(coordinates)
            print(f'Set selected piece: {self.selected_square}')
        
        elif self.selected_square is not None:
            squared_to_move_to = Coordinates.get_square(coordinates)
            print(f'Move from {self.selected_square} to {squared_to_move_to}')
            self.selected_square = None
            
        self.draw_board(board)
        
      
class Coordinates:
    @staticmethod
    def get_coordinates(square: Square) -> tuple[int, int]:
        height = 8 * SQUARE_SIZE
        
        x = square.column * SQUARE_SIZE
        y = height - (square.row + 1) * SQUARE_SIZE
        
        return x, y
    
    @staticmethod
    def get_square(coordinates: tuple[int, int]) -> Optional[Square]:
        (x, y) = coordinates
        height = 8 * SQUARE_SIZE
        
        row = (height - y) // SQUARE_SIZE
        column = x // SQUARE_SIZE
        
        if 0 <= row < 8 and 0 <= column < 8: 
            return Square(row, column)
        else: 
            return None
        
class Mouse():
    @staticmethod
    def is_own_piece(coordinates: tuple[int, int], board: Board, color: PieceColor) -> bool:
        square = Coordinates.get_square(coordinates)
        if square is None:
            return False
        
        piece = board.board[square]
        return piece and piece.color == color
    
    