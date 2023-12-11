from game import Game
from game_rules import GameRules
from graphics import Graphics
import pygame

# Initialize GUI
pygame.init()
pygame.display.set_caption("Chess")
running = True
game_over = False
result = None

game = Game()
legal_moves = GameRules.get_legal_moves(game)
graphics = Graphics()
graphics.draw_board(game.board)

# Run game
while running:
    # Read mouse position and set cursor
    mouse_position = pygame.mouse.get_pos()
    graphics.set_cursor(mouse_position, game.board, game.turn)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            move = graphics.handle_click(mouse_position, game.board, game.turn, legal_moves)
            
            if move is not None:
                game.make_move(move)
                legal_moves = GameRules.get_legal_moves(game)
                result = GameRules.get_game_result(game) 
                game_over = result is not None              
            
            graphics.draw_board(game.board)
            
    if game_over:
        graphics.display_result(result)