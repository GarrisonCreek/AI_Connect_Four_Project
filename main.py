import pygame
from connect_four import ConnectFour
from constants import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
deltaTime = 0

# Initialize ConnectFour game
game = ConnectFour()

# game loop
while running:
    for event in pygame.event.get():
        if not game.handle_event(event):
            running = False

    if not game.game_over:
        game.ai_move()
    elif (game.game_type == 3 or game.game_type == 4) and not game.pause_for_game_over:
        game.reset_game()

    game.render(screen)
    deltaTime = clock.tick(60) / 1000

pygame.quit()