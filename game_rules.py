from game import Game
from board import Board
from piece import Piece, PieceColor, PieceType
from square import Square
from move import Move

class GameRules:
    @staticmethod
    def get_all_legal_moves(game: Game) -> list[Move]:
        return GameRules.__get_all_psuedo_legal_moves(game)
    
    @staticmethod
    def __get_all_psuedo_legal_moves(game: Game) -> list[Move]:
        squares_with_own_pieces = game.board.get_squares_with_pieces(game.turn)
        
        psuedo_legal_moves = []
        for square in squares_with_own_pieces:
            piece = game.board[square]
            psuedo_legal_moves.extend(GameRules.__get_psuedo_legal_moves(piece, square, game.board))
        
        return psuedo_legal_moves
    
    @staticmethod
    def __is_check(board: Board, turn: PieceColor) -> bool:
        pass
    
    @staticmethod
    def __get_psuedo_legal_moves(piece: Piece, start_square: Square, board: Board) -> list[Move]:
        psuedo_legal_moves = []
        
        opponent_color = PieceColor.BLACK if piece.color == PieceColor.WHITE else PieceColor.WHITE
        squares_with_opponent_pieces = board.get_squares_with_pieces(opponent_color)
        empty_squares = board.get_empty_squares()
        
        match piece.type:
            case PieceType.PAWN:
                direction = 1 if piece.color == PieceColor.WHITE else -1
                
                # One square forward
                one_square_forward = Square(start_square.row + direction, start_square.column)
                if one_square_forward in empty_squares:
                    psuedo_legal_moves.append(Move(start_square, one_square_forward))
                    
                    # Two squares forward
                    starting_row = 1 if piece.color == PieceColor.WHITE else 6
                    two_squares_forward = Square(start_square.row + 2*direction, start_square.column)
                    if start_square.row == starting_row and two_squares_forward in empty_squares:
                        psuedo_legal_moves.append(Move(start_square, two_squares_forward))
                        
                # Captures                
                capture_squares = [
                    Square(start_square.row + direction, start_square.column - 1),
                    Square(start_square.row + direction, start_square.column + 1)
                ]
                for capture_square in capture_squares:
                    if capture_square in squares_with_opponent_pieces:
                        psuedo_legal_moves.append(Move(start_square, capture_square))
            
            case PieceType.KNIGHT:
                available_squares = empty_squares + squares_with_opponent_pieces
                moves = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, 1)]
                
                for move in moves:
                    end_square = Square(start_square.row + move[0], start_square.column + move[1])
                    if end_square in available_squares:
                        psuedo_legal_moves.append(Move(start_square, end_square))
            
            case PieceType.BISHOP:
                directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                for direction in directions:
                    steps = 1
                    while True:
                        end_square = Square(start_square.row + direction[0]*steps, start_square.column + direction[1]*steps)
                        if end_square in empty_squares:
                            psuedo_legal_moves.append(Move(start_square, end_square))
                            steps += 1
                        
                        elif end_square in squares_with_opponent_pieces:
                            psuedo_legal_moves.append(Move(start_square, end_square))
                            break
                        
                        else:
                            break
            
            case PieceType.ROOK:
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                for direction in directions:
                    steps = 1
                    while True:
                        end_square = Square(start_square.row + direction[0]*steps, start_square.column + direction[1]*steps)
                        if end_square in empty_squares:
                            psuedo_legal_moves.append(Move(start_square, end_square))
                            steps += 1
                        
                        elif end_square in squares_with_opponent_pieces:
                            psuedo_legal_moves.append(Move(start_square, end_square))
                            break
                        
                        else:
                            break
            
            case PieceType.QUEEN:
                psuedo_legal_moves.extend(
                    GameRules.__get_psuedo_legal_moves(Piece(piece.color, PieceType.BISHOP), start_square, board) +
                    GameRules.__get_psuedo_legal_moves(Piece(piece.color, PieceType.ROOK), start_square, board)
                )                
            
            case PieceType.KING:
                available_squares = empty_squares + squares_with_opponent_pieces
                moves = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
                
                for move in moves:
                    end_square = Square(start_square.row + move[0], start_square.column + move[1])
                    if end_square in available_squares:
                        psuedo_legal_moves.append(Move(start_square, end_square))
            
        return psuedo_legal_moves
            
    