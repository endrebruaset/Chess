from board import Board
from piece import PieceColor, PieceType
from game_rules import Result
from square import Square
from move import Move
from typing import Optional
from settings import SQUARE_SIZE
import pygame

class Color:
    LIGHT_SQAURE = pygame.Color('#ffffff')
    DARK_SQUARE = pygame.Color('#51753f')
    SELECTED_SQUARE = pygame.Color('#fff785')
    BLACK = pygame.Color('#000000')
    WHITE = pygame.Color('#ffffff')
    GREY = pygame.Color('#bbbbbb')

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
        self.background.fill(Color.DARK_SQUARE)
        for row in range(0, 8):
            for column in range(0, 8):
                if (row + column) % 2 == 0:
                    pygame.draw.rect(
                        self.background, 
                        Color.LIGHT_SQAURE, 
                        (row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    )
                    
        # Create move circle
        self.move_circle = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        self.move_circle.set_alpha(100)
        pygame.draw.circle(
            self.move_circle,
            Color.BLACK,
            center=(SQUARE_SIZE / 2, SQUARE_SIZE / 2),
            radius=SQUARE_SIZE / 5
        )
        
        # Selection state
        self.selected_square: Optional[Square] = None
        self.selected_square_moves: list[Move] = []
        
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
        for square in self.__get_selected_square_moves_end_squares():
            self.display.blit(self.move_circle, Coordinates.get_coordinates(square))
        
        # Update display
        pygame.display.flip()
        
    def handle_click(self, coordinates: tuple[int, int], board: Board, turn, legal_moves: list[Move]) -> Optional[Move]:               
        move = None
        selected_square = None

        clicked_square = Coordinates.get_square(coordinates)
        if clicked_square is not None and clicked_square in self.__get_selected_square_moves_end_squares():
            move = next((move for move in self.selected_square_moves if move.end == clicked_square))
            
        elif clicked_square is not None and clicked_square in board.get_squares_with_pieces(turn):
            selected_square = clicked_square
            self.selected_square_moves = [move for move in legal_moves if move.start == clicked_square]
        
        self.selected_square = selected_square
        return move
        
    def set_cursor(self, coordinates: tuple[int, int], board: Board, turn: PieceColor) -> None:
        square_hovered = Coordinates.get_square(coordinates)
        clickable_squares = board.get_squares_with_pieces(turn) + self.__get_selected_square_moves_end_squares()
        
        if square_hovered is not None and square_hovered in clickable_squares:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    def display_result(self, result: Result) -> None:
        match result:
            case Result.WHITE_WIN:
                text = 'White wins by checkmate!'
                
            case Result.BLACK_WIN:
                text = 'Black wins by checkmate!'
                
            case Result.STALEMATE:
                text = 'Draw by stalemate!'
                
            case Result.INSUFFICIENT_MATERIAL:
                text = 'Draw by insufficient material!'
                
        font = pygame.font.SysFont('Calibri', 32)
        result_surface = font.render(text, True, Color.BLACK, Color.GREY)
        
        padding = 20
        padded_result_surface = pygame.Surface((result_surface.get_width() + padding, result_surface.get_height() + padding))
        padded_result_surface.fill(Color.GREY)
        
        x = (self.display.get_width() - result_surface.get_width()) / 2
        y = (self.display.get_height() - result_surface.get_height()) / 2

        self.display.blit(padded_result_surface, (x - padding / 2, y - padding / 2))
        self.display.blit(result_surface, (x, y))
        
        # Update display
        pygame.display.flip()
        
    def __get_selected_square_moves_end_squares(self) -> list[Square]:
        if self.selected_square is None:
            return []
        
        return [move.end for move in self.selected_square_moves]
      
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
        
        square = Square(row, column)
        return square if square.is_valid() else None