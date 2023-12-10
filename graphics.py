from board import Board
from piece import PieceColor, PieceType
from square import Square
from move import Move
from typing import Optional
from settings import SQUARE_SIZE
import pygame

class Color:
    LIGHT_SQAURE = pygame.Color('#ffffff')
    DARK_SQUARE = pygame.Color('#51753f')
    CHECKED_SQUARE = pygame.Color('#ba4141')
    SELECTED_SQUARE = pygame.Color('#fff785')
    MOVE_CIRCLE = pygame.Color('#000000')

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
        self.background.fill(Color.LIGHT_SQAURE)
        for row in range(0, 8):
            for column in range(0, 8):
                if (row + column) % 2 == 0:
                    pygame.draw.rect(
                        self.background, 
                        Color.DARK_SQUARE, 
                        (row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    )
                    
        # Create move circle
        self.move_circle = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        self.move_circle.set_alpha(100)
        pygame.draw.circle(
            self.move_circle,
            Color.MOVE_CIRCLE,
            center=(SQUARE_SIZE / 2, SQUARE_SIZE / 2),
            radius=SQUARE_SIZE / 5
        )
        
        # Mouse state
        self.selected_square: Optional[Square] = None
        self.selected_square_moves: list[Square] = []
        
    def draw_board(self, board: Board) -> None:
        # Draw empty board
        self.display.blit(self.background, self.background.get_rect())
        
        # Highlight selected square
        if self.selected_square is not None:
            (x, y) = Coordinates.get_coordinates(self.selected_square)
            pygame.draw.rect(
                self.display,
                Color.SELECTED_SQUARE,
                (x, y, SQUARE_SIZE, SQUARE_SIZE)
            )
        
        # Draw pieces
        squares_with_pieces = board.get_squares_with_pieces(PieceColor.WHITE) + board.get_squares_with_pieces(PieceColor.BLACK)
        for square in squares_with_pieces:
            coordinates = Coordinates.get_coordinates(square)
            piece = board[square]
            piece_image = self.piece_images[piece.color][piece.type]
            self.display.blit(piece_image, coordinates)
        
        # Show available moves
        if self.selected_square is not None:
            for square in self.selected_square_moves:
                self.display.blit(self.move_circle, Coordinates.get_coordinates(square))
        
        # Update display
        pygame.display.flip()
        
    def set_cursor(self, coordinates: tuple[int, int], board: Board, turn: PieceColor) -> None:
        square_hovered = Coordinates.get_square(coordinates)
        if square_hovered is None:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
        elif square_hovered in board.get_squares_with_pieces(turn):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            
        elif self.selected_square is not None and square_hovered in self.selected_square_moves:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    def handle_click(self, coordinates: tuple[int, int], board: Board, turn, legal_moves: list[Move]) -> Optional[Move]:               
        move = None
        
        clicked_square = Coordinates.get_square(coordinates)
        print(f'{clicked_square}')
        if clicked_square is None:
            self.selected_square = None
        
        elif clicked_square in board.get_squares_with_pieces(turn):
            print('Clicked own piece')
            self.selected_square = clicked_square
            self.selected_square_moves = [move.end for move in legal_moves if move.start == clicked_square]
        
        elif self.selected_square is not None:
            if clicked_square in self.selected_square_moves:
                move = Move(self.selected_square, clicked_square)
                
            self.selected_square = None
        
        return move
      
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