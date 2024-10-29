#  Connect Four Game with AI and Pygame

import pygame
import sys
import math
import random
from ai import AI

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
TOKEN_RADIUS = 35
GAME_BOARD_WIDTH = 750
GAME_BOARD_HEIGHT = 600
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
# Colors
BACKGROUND_COLOR = "grey"
GAME_BOARD_COLOR = "darkblue"
RED_PLAYER_COLOR = "red"
YELLOW_PLAYER_COLOR = "yellow"
# location trackers
BOARD_OFFSET_X = 500
BOARD_OFFSET_Y = 250

# Global Variables
game_state = [[0 for col in range(COLUMN_COUNT)] for row in range(ROW_COUNT)] # 0 means empty, 1 means red, 2 means yellow

current_player = 1 # Current players turn...  1 means red, 2 means yellow
winning_player = 0 # 0 means no one has won yet or it's a draw
game_over = False # True when the game is over
game_type = 0 # 0 means unselected, 1 means player vs player, 2 means player vs AI, 3 means AI vs AI

# setting variables for AI
pause_for_game_over = True


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
    return True

def reset_game():
    global game_state
    game_state = [[0 for col in range(COLUMN_COUNT)] for row in range(ROW_COUNT)]
    global current_player
    current_player = 1
    global game_over
    game_over = False

def draw_board(board):
    # draws the game board
    pygame.draw.rect(screen, GAME_BOARD_COLOR, (screen.get_width()/2-BOARD_OFFSET_X, screen.get_height()/2-BOARD_OFFSET_Y, GAME_BOARD_WIDTH, GAME_BOARD_HEIGHT))
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            pygame.draw.circle(screen, BACKGROUND_COLOR, (screen.get_width()/2-BOARD_OFFSET_X+75 + col*100, screen.get_height()/2-BOARD_OFFSET_Y+50 + row*100) , TOKEN_RADIUS)
    # draws the current game state
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            if board[row][col] != 0:
                draw_token(row, col, board[row][col])

def draw_token(row, col, token):
    if token == 1:
        pygame.draw.circle(screen, "black", (screen.get_width()/2-BOARD_OFFSET_X+75 + col*100, screen.get_height()/2-BOARD_OFFSET_Y+50 + row*100) , TOKEN_RADIUS)
        pygame.draw.circle(screen, RED_PLAYER_COLOR, (screen.get_width()/2-BOARD_OFFSET_X+75 + col*100, screen.get_height()/2-BOARD_OFFSET_Y+50 + row*100) , TOKEN_RADIUS-2)
        pygame.draw.circle(screen, "black", (screen.get_width()/2-BOARD_OFFSET_X+75 + col*100, screen.get_height()/2-BOARD_OFFSET_Y+50 + row*100) , TOKEN_RADIUS-7)
        pygame.draw.circle(screen, RED_PLAYER_COLOR, (screen.get_width()/2-BOARD_OFFSET_X+75 + col*100, screen.get_height()/2-BOARD_OFFSET_Y+50 + row*100) , TOKEN_RADIUS-9)

    elif token == 2:
        pygame.draw.circle(screen, "black", (screen.get_width()/2-BOARD_OFFSET_X+75 + col*100, screen.get_height()/2-BOARD_OFFSET_Y+50 + row*100) , TOKEN_RADIUS)
        pygame.draw.circle(screen, YELLOW_PLAYER_COLOR, (screen.get_width()/2-BOARD_OFFSET_X+75 + col*100, screen.get_height()/2-BOARD_OFFSET_Y+50 + row*100) , TOKEN_RADIUS-2)
        pygame.draw.circle(screen, "black", (screen.get_width()/2-BOARD_OFFSET_X+75 + col*100, screen.get_height()/2-BOARD_OFFSET_Y+50 + row*100) , TOKEN_RADIUS-7)
        pygame.draw.circle(screen, YELLOW_PLAYER_COLOR, (screen.get_width()/2-BOARD_OFFSET_X+75 + col*100, screen.get_height()/2-BOARD_OFFSET_Y+50 + row*100) , TOKEN_RADIUS-9)

def draw_game_over():
    global winning_player
    font = pygame.font.Font(None, 74)
    if winning_player == 1:
        text = font.render("Player 1 Wins!", True, "black")
    elif winning_player == 2:
        text = font.render("Player 2 Wins!", True, "black")
    else:
        text = font.render("It's a Draw!", True, "black")

    text_rect = text.get_rect(center=(screen.get_width()/2 - BOARD_OFFSET_X/4, screen.get_height()/2 - BOARD_OFFSET_Y-50))
    screen.blit(text, text_rect)

def draw_side_panel():
    x_loc = SCREEN_WIDTH-300
    y_loc = 0
    # draws the side panel
    pygame.draw.rect(screen, "black", (SCREEN_WIDTH-300, 0, 300, SCREEN_HEIGHT))
    # draws the current player
    font = pygame.font.Font(None, 40)
    text = font.render(f"Player {current_player}'s Turn", True, "white")
    text_rect = text.get_rect(center=(x_loc + 150, y_loc + 50))
    screen.blit(text, text_rect)

    # draws ai1 stats
    if game_type == 3:
        font = pygame.font.Font(None, 40)
        text = font.render("AI 1", True, "white")
        text_rect = text.get_rect(center=(x_loc + 150, y_loc + 150))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 40)
        text = font.render(f"Wins: {ai1.wins}", True, "white")
        text_rect = text.get_rect(center=(x_loc + 150, y_loc + 200))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 40)
        text = font.render(f"Losses: {ai1.losses}", True, "white")
        text_rect = text.get_rect(center=(x_loc + 150, y_loc + 250))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 40)
        text = font.render(f"Draws: {ai1.draws}", True, "white")
        text_rect = text.get_rect(center=(x_loc + 150, y_loc + 300))
        screen.blit(text, text_rect)

    # draws ai2 stats
    if game_type == 3:
        font = pygame.font.Font(None, 40)
        text = font.render("AI 2", True, "white")
        text_rect = text.get_rect(center=(x_loc + 150, y_loc + 400))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 40)
        text = font.render(f"Wins: {ai2.wins}", True, "white")
        text_rect = text.get_rect(center=(x_loc + 150, y_loc + 450))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 40)
        text = font.render(f"Losses: {ai2.losses}", True, "white")
        text_rect = text.get_rect(center=(x_loc + 150, y_loc + 500))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 40)
        text = font.render(f"Draws: {ai2.draws}", True, "white")
        text_rect = text.get_rect(center=(x_loc + 150, y_loc + 550))
        screen.blit(text, text_rect)

def draw_selection_screen():
    # draws the selection screen
    font = pygame.font.Font(None, 74)
    text = font.render("Connect Four", True, "black")
    text_rect = text.get_rect(center=(screen.get_width()/2, screen.get_height()/2-200))
    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 40)
    text = font.render("Select Game Type", True, "black")
    text_rect = text.get_rect(center=(screen.get_width()/2, screen.get_height()/2-100))
    screen.blit(text, text_rect)
    # draws the player vs player button
    pygame.draw.rect(screen, "black", (screen.get_width()/2-125-325, screen.get_height()/2, 250, 100))
    font = pygame.font.Font(None, 40)
    text = font.render("Player vs Player", True, "white")
    text_rect = text.get_rect(center=(screen.get_width()/2-325, screen.get_height()/2+50))
    screen.blit(text, text_rect)
    # draws the player vs AI button
    pygame.draw.rect(screen, "black", (screen.get_width()/2-125, screen.get_height()/2, 250, 100))
    font = pygame.font.Font(None, 40)
    text = font.render("Player vs AI", True, "white")
    text_rect = text.get_rect(center=(screen.get_width()/2, screen.get_height()/2+50))
    screen.blit(text, text_rect)
    # draws the AI vs AI button
    pygame.draw.rect(screen, "black", (screen.get_width()/2-125+325, screen.get_height()/2, 250, 100))
    font = pygame.font.Font(None, 40)
    text = font.render("AI vs AI", True, "white")
    text_rect = text.get_rect(center=(screen.get_width()/2+325, screen.get_height()/2+50))
    screen.blit(text, text_rect)


# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
deltaTime = 0

# game loop
while running:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # close window
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # exit game
                running = False
            elif event.key == pygame.K_r: # reset game
                reset_game()
            elif event.key == pygame.K_TAB: # switch game type
                reset_game()
                game_type = 0

            # selection screen
            if game_type == 0:
                if event.key == pygame.K_1: # select player vs player
                    game_type = 1
                elif event.key == pygame.K_2: # select player vs AI
                    game_type = 2
                    # initialize AI
                    ai = AI(2)
                elif event.key == pygame.K_3: # select AI vs AI
                    game_type = 3
                    # initialize AI
                    ai1 = AI(1)
                    ai2 = AI(2)

            # player vs player
            elif game_type == 1:
                if event.key == pygame.K_1 and not game_over and game_type == 1:
                    drop_token(game_state, 0, current_player)
                elif event.key == pygame.K_2 and not game_over and game_type == 1:
                    drop_token(game_state, 1, current_player)
                elif event.key == pygame.K_3 and not game_over and game_type == 1:
                    drop_token(game_state, 2, current_player)
                elif event.key == pygame.K_4 and not game_over and game_type == 1:
                    drop_token(game_state, 3, current_player)
                elif event.key == pygame.K_5 and not game_over and game_type == 1:
                    drop_token(game_state, 4, current_player)
                elif event.key == pygame.K_6 and not game_over and game_type == 1:
                    drop_token(game_state, 5, current_player)
                elif event.key == pygame.K_7 and not game_over and game_type == 1:
                    drop_token(game_state, 6, current_player)

            # player vs AI
            elif game_type == 2 and current_player == 1:
                if event.key == pygame.K_1 and not game_over:
                    drop_token(game_state, 0, current_player)
                elif event.key == pygame.K_2 and not game_over:
                    drop_token(game_state, 1, current_player)
                elif event.key == pygame.K_3 and not game_over:
                    drop_token(game_state, 2, current_player)
                elif event.key == pygame.K_4 and not game_over:
                    drop_token(game_state, 3, current_player)
                elif event.key == pygame.K_5 and not game_over:
                    drop_token(game_state, 4, current_player)
                elif event.key == pygame.K_6 and not game_over:
                    drop_token(game_state, 5, current_player)
                elif event.key == pygame.K_7 and not game_over:
                    drop_token(game_state, 6, current_player)

            # AI vs AI
            elif game_type == 3:
                if event.key == pygame.K_c: # disable pause for game over
                    pause_for_game_over = not pause_for_game_over
        #  check for mouse click to drop token
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over and game_type == 1:
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

            if not game_over and game_type == 2 and current_player == 1:
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

    # Play Game
    if not game_over:
        if game_type == 2 and current_player == 2: # player vs AI - AI's turn
            col = ai.evaluate_board(game_state)
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

    # Selection Screen Logic
    if game_type == 0:
        draw_selection_screen()
        # check for mouse click
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if 190 < mouse_pos[0] < 440 and 360 < mouse_pos[1] < 460:
                game_type = 1
            elif 515 < mouse_pos[0] < 765 and 360 < mouse_pos[1] < 460:
                game_type = 2
                # initialize AI
                ai = AI(2)
            elif 840 < mouse_pos[0] < 1090 and 360 < mouse_pos[1] < 460:
                game_type = 3
                # initialize AI
                ai1 = AI(1)
                ai2 = AI(2)
    else:
        draw_board(game_state)
        draw_side_panel()


    if game_over:
        draw_game_over()

    pygame.display.flip() # updates the screen with the new rendering

    deltaTime = clock.tick(60) / 1000 # 60 FPS

pygame.quit()