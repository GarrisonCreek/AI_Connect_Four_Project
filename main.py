#  Connect Four Game with AI and Pygame

import pygame
from minimaxAI import minimaxAI
from multiprocessing import Pool
from constants import *
from graphics import *

# Global Variables
game_state = [[0 for col in range(COLUMN_COUNT)] for row in range(ROW_COUNT)] # 0 means empty, 1 means red, 2 means yellow

current_player = 1 # Current players turn...  1 means red, 2 means yellow
winning_player = 0 # 0 means no one has won yet or it's a draw
game_over = False # True when the game is over
game_type = 0 # 0 means unselected, 1 means player vs player, 2 means player vs AI, 3 means AI vs AI
ai1 = minimaxAI(1, 5) # AI 1, (player number, depth of minimax)
ai2 = minimaxAI(2, 5) # AI 2  (player number, depth of minimax)

# Settings:
pause_for_game_over = True

def select_game_type(selected_game_type):
    global game_type, ai1, ai2
    if selected_game_type == 0:
        print("Selecte a game type")
        game_type = 0
    elif selected_game_type == 1:
        print("Game type selected: Player vs Player")
        game_type = 1
    elif selected_game_type == 2:
        print("Game type selected: Player vs AI")
        game_type = 2
        # ai1 = minimaxAI(2, 5)
    elif selected_game_type == 3:
        print("Game type selected: AI vs AI")
        game_type = 3
        # ai1 = minimaxAI(1, 4)
        # ai2 = minimaxAI(2, 4)

def drop_token(board, col, token):
    for row in range(ROW_COUNT-1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = token
            if check_win(board, token):
                print(f"Player {token} wins!")
                global game_over
                game_over = True

            if row == 0:
                if check_draw(board):
                    print("It's a draw!")
                    game_over = True

            switch_player()
            break

def switch_player():
    global current_player
    if current_player == 1:
        current_player = 2
    else:
        current_player = 1

def check_win(board, token):
    global winning_player
    winning_player = token
    # check horizontal locations for win
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT):
            if board[row][col] == token and board[row][col+1] == token and board[row][col+2] == token and board[row][col+3] == token:
                if game_type == 3 and token == 1:
                    print("AI Wins!")
                    ai1.wins += 1
                    ai2.losses += 1
                elif game_type == 3 and token == 2:
                    print("AI 2 Wins!")
                    ai2.wins += 1
                    ai1.losses += 1
                return True

    # check vertical locations for win
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT-3):
            if board[row][col] == token and board[row+1][col] == token and board[row+2][col] == token and board[row+3][col] == token:
                if game_type == 3 and token == 1:
                    print("AI 1 Wins!")
                    ai1.wins += 1
                    ai2.losses += 1
                elif game_type == 3 and token == 2:
                    print("AI 2 Wins!")
                    ai2.wins += 1
                    ai1.losses += 1
                return True

    # check positively sloped diagonals
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT-3):
            if board[row][col] == token and board[row+1][col+1] == token and board[row+2][col+2] == token and board[row+3][col+3] == token:
                if game_type == 3 and token == 1:
                    print("AI Wins!")
                    ai1.wins += 1
                    ai2.losses += 1
                elif game_type == 3 and token == 2:
                    print("AI 2 Wins!")
                    ai2.wins += 1
                    ai1.losses += 1
                return True

    # check negatively sloped diagonals
    for col in range(COLUMN_COUNT-3):
        for row in range(3, ROW_COUNT):
            if board[row][col] == token and board[row-1][col+1] == token and board[row-2][col+2] == token and board[row-3][col+3] == token:
                if game_type == 3 and token == 1:
                    print("AI Wins!")
                    ai1.wins += 1
                    ai2.losses += 1
                elif game_type == 3 and token == 2:
                    print("AI 2 Wins!")
                    ai2.wins += 1
                    ai1.losses += 1
                return True

    winning_player = 0
    return False

def check_draw(board):
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            if board[row][col] == 0:
                return False
    
    if game_type == 1:
        print("It's a draw!")

    elif game_type == 2:
        print("It's a draw!")
        ai1.draws += 1

    if game_type == 3:
        print("It's a draw!")
        ai1.draws += 1
        ai2.draws += 1
    return True

def reset_game():
    global game_state, current_player, winning_player, game_over
    game_state = [[0 for col in range(COLUMN_COUNT)] for row in range(ROW_COUNT)]
    current_player = 1
    winning_player = 0
    game_over = False

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
deltaTime = 0

# game loop
while running:
    # Checks for mouse / keyboard events to play the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # close window
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # exit game with 'esc' key
                running = False
            elif event.key == pygame.K_r: # reset game with 'r' key
                reset_game()
            elif event.key == pygame.K_TAB: # switch game type with 'tab' key
                reset_game()
                select_game_type(0)

            # selection screen
            if game_type == 0:
                if event.key == pygame.K_1: # select player vs player
                    select_game_type(1)
                elif event.key == pygame.K_2: # select player vs AI
                    select_game_type(2)
                elif event.key == pygame.K_3: # select AI vs AI
                    select_game_type(3)
            # Plaver vs Player or Player vs AI Key Controls
            elif game_type == 1 or game_type == 2 and not game_over:
                if event.key == pygame.K_1:
                    drop_token(game_state, 0, current_player)
                elif event.key == pygame.K_2:
                    drop_token(game_state, 1, current_player)
                elif event.key == pygame.K_3:
                    drop_token(game_state, 2, current_player)
                elif event.key == pygame.K_4:
                    drop_token(game_state, 3, current_player)
                elif event.key == pygame.K_5:
                    drop_token(game_state, 4, current_player)
                elif event.key == pygame.K_6:
                    drop_token(game_state, 5, current_player)
                elif event.key == pygame.K_7:
                    drop_token(game_state, 6, current_player)

            # AI vs AI Key Controls
            elif game_type == 3:
                if event.key == pygame.K_c: # disable pause for game over
                    pause_for_game_over = not pause_for_game_over
        #  Player vs Player or Player vs AI Mouse Controls
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_type == 1 or game_type == 2 and not game_over:
                mouse_pos = pygame.mouse.get_pos()
                if 175 < mouse_pos[0] < 245:
                    drop_token(game_state, 0, current_player)
                elif 275 < mouse_pos[0] < 345:
                    drop_token(game_state, 1, current_player)
                elif 375 < mouse_pos[0] < 445:
                    drop_token(game_state, 2, current_player)
                elif 475 < mouse_pos[0] < 545:
                    drop_token(game_state, 3, current_player)
                elif 575 < mouse_pos[0] < 645:
                    drop_token(game_state, 4, current_player)
                elif 675 < mouse_pos[0] < 745:
                    drop_token(game_state, 5, current_player)
                elif 775 < mouse_pos[0] < 845:
                    drop_token(game_state, 6, current_player)

    # Game Loop
    if not game_over:
        if game_type == 2 and current_player == 2: # player vs AI - AI's turn
            col = ai1.evaluate_board(game_state)
            drop_token(game_state, col, current_player)

        elif game_type == 3: # AI vs AI
            if current_player == 1:
                col = ai1.evaluate_board(game_state)
                drop_token(game_state, col, current_player)
            elif current_player == 2:
                col = ai2.evaluate_board(game_state)
                drop_token(game_state, col, current_player)
    elif game_type == 3 and not pause_for_game_over:
        reset_game()

    # Render Game
    screen.fill(BACKGROUND_COLOR) # fills the screen with a color to wipe away anything from last frame

    # Selection screen logic + rendering
    if game_type == 0:
        draw_selection_screen(screen)
        # check for mouse click
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if 190 < mouse_pos[0] < 440 and 360 < mouse_pos[1] < 460: # Player selects player vs player
                select_game_type(1)
            elif 515 < mouse_pos[0] < 765 and 360 < mouse_pos[1] < 460: # Player selects player vs AI
                select_game_type(2)
            elif 840 < mouse_pos[0] < 1090 and 360 < mouse_pos[1] < 460: # Player selects AI vs AI
                select_game_type(3)
    else:
        draw_board(screen, game_state)
        draw_side_panel(screen, current_player, game_type, ai1, ai2)

    # Game Over screen logic + rendering
    if game_over:
        draw_game_over(screen, winning_player)

    pygame.display.flip() # updates the screen with the new rendering
    deltaTime = clock.tick(60) / 1000 # 60 FPS

pygame.quit()