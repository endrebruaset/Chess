from game import Game
from board import Board
from piece import Piece, PieceColor, PieceType
from square import Square
from move import Move, MoveType

class GameRules:
    @staticmethod
    def get_legal_moves(game: Game) -> list[Move]:
        psuedo_legal_moves = GameRules.__get_psuedo_legal_moves(game)
        
        # Remove moves exposing the king to a check
        moves_resulting_in_check = []
        for move in psuedo_legal_moves:
            if GameRules.is_check(game.simulate_move(move), king_color=game.turn):
                moves_resulting_in_check.append(move)
        
        # Castling
        
        return [move for move in psuedo_legal_moves if move not in moves_resulting_in_check]
    
    @staticmethod
    def is_check(board: Board, king_color: PieceColor) -> bool:
        opponent_color = PieceColor.opposing_color(king_color)
        attacked_squares = GameRules.__get_attacked_squares(board, opponent_color)
        
        # Get king position
        king_square = None
        for square in board.get_squares_with_pieces(king_color):
            piece = board[square]
            if piece is not None and piece.type == PieceType.KING:
                king_square = square
        
        if king_square is None:
            raise ValueError('Board has no king')
        
        return king_square in attacked_squares
        
    @staticmethod
    def __get_attacked_squares(board: Board, turn: PieceColor):
        squares_with_own_pieces = board.get_squares_with_pieces(turn)
        
        attacked_squares = []
        for square in squares_with_own_pieces:
            piece = board[square]
            if piece.type == PieceType.PAWN:
                direction = Board.get_pawn_direction(piece.color)           
                capture_squares = [
                    Square(square.row + direction, square.column - 1),
                    Square(square.row + direction, square.column + 1)
                ]
                
                attacked_squares.extend([square for square in capture_squares if square.is_valid()])
                
            else:
                attacked_squares.extend([
                    move.end for move in GameRules.__get_psuedo_legal_moves_for_piece(piece, square, board)
                ])
        
        return attacked_squares
    
    @staticmethod
    def __get_psuedo_legal_moves(game: Game) -> list[Move]:
        squares_with_own_pieces = game.board.get_squares_with_pieces(game.turn)
        
        psuedo_legal_moves = []
        for square in squares_with_own_pieces:
            piece = game.board[square]
            psuedo_legal_moves.extend(
                GameRules.__get_psuedo_legal_moves_for_piece(piece, square, game.board, game.en_passant)
            )
        
        return psuedo_legal_moves
    
    @staticmethod
    def __get_psuedo_legal_moves_for_piece(piece: Piece, start_square: Square, board: Board, en_passant: Square = None) -> list[Move]:
        psuedo_legal_moves = []
        
        opponent_color = PieceColor.opposing_color(piece.color)
        squares_with_opponent_pieces = board.get_squares_with_pieces(opponent_color)
        if en_passant is not None:
            squares_with_opponent_pieces.append(en_passant)
            
        empty_squares = board.get_empty_squares()
        
        match piece.type:
            case PieceType.PAWN:
                direction = Board.get_pawn_direction(piece.color)
                        
                # Captures               
                capture_squares = [
                    Square(start_square.row + direction, start_square.column - 1),
                    Square(start_square.row + direction, start_square.column + 1)
                ]
                for capture_square in capture_squares:
                    if capture_square in squares_with_opponent_pieces:
                        psuedo_legal_moves.append(Move(start_square, capture_square))
                
                # One square forward
                one_square_forward = Square(start_square.row + direction, start_square.column)
                if one_square_forward in empty_squares:
                    psuedo_legal_moves.append(Move(start_square, one_square_forward))
                    
                    # Two squares forward
                    starting_row = Board.get_pawn_starting_row(piece.color)
                    two_squares_forward = Square(start_square.row + 2*direction, start_square.column)
                    if start_square.row == starting_row and two_squares_forward in empty_squares:
                        psuedo_legal_moves.append(Move(start_square, two_squares_forward, MoveType.DOUBLE_PAWN_PUSH))
            
            case PieceType.KNIGHT:
                available_squares = empty_squares + squares_with_opponent_pieces
                moves = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
                
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
                    GameRules.__get_psuedo_legal_moves_for_piece(Piece(piece.color, PieceType.BISHOP), start_square, board) +
                    GameRules.__get_psuedo_legal_moves_for_piece(Piece(piece.color, PieceType.ROOK), start_square, board)
                )                
            
            case PieceType.KING:
                available_squares = empty_squares + squares_with_opponent_pieces
                moves = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
                
                for move in moves:
                    end_square = Square(start_square.row + move[0], start_square.column + move[1])
                    if end_square in available_squares:
                        psuedo_legal_moves.append(Move(start_square, end_square))
            
        return psuedo_legal_moves
            
    