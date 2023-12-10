from game import Game
from game_rules import GameRules
from graphics import Graphics
import pygame

# Initialize GUI
pygame.init()
pygame.display.set_caption("Chess")
running = True

game = Game()
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
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('Click')
            move = graphics.handle_click(mouse_position, game.board, game.turn, game.legal_moves)
            
            if move is not None:
                print(f'{move}')
                game.make_move(move)
            
            graphics.draw_board(game.board)