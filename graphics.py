import pygame
from constants import *

def draw_board(screen, board):
    # draws the game board
    pygame.draw.rect(screen, GAME_BOARD_COLOR, (screen.get_width()/2-BOARD_OFFSET_X, screen.get_height()/2-BOARD_OFFSET_Y, GAME_BOARD_WIDTH, GAME_BOARD_HEIGHT))
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            pygame.draw.circle(screen, BACKGROUND_COLOR, (screen.get_width()/2-BOARD_OFFSET_X+75 + col*100, screen.get_height()/2-BOARD_OFFSET_Y+50 + row*100) , TOKEN_RADIUS)
    # draws the current game state
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            if board[row][col] != 0:
                draw_token(row, col, board[row][col], screen)

def draw_token(row, col, token, screen):
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

def draw_game_over(screen, winning_player):
    font = pygame.font.Font(None, 74)
    if winning_player == 1:
        text = font.render("Player 1 Wins!", True, "black")
    elif winning_player == 2:
        text = font.render("Player 2 Wins!", True, "black")
    else:
        text = font.render("It's a Draw!", True, "black")

    text_rect = text.get_rect(center=(screen.get_width()/2 - BOARD_OFFSET_X/4, screen.get_height()/2 - BOARD_OFFSET_Y-50))
    screen.blit(text, text_rect)

def draw_side_panel(screen, current_player, game_type, ai1, ai2):
    x_loc = SCREEN_WIDTH-300
    y_loc = 0
    # draws the side panel
    pygame.draw.rect(screen, "black", (SCREEN_WIDTH-300, 0, 300, SCREEN_HEIGHT))
    # draws the current player
    font = pygame.font.Font(None, 40)
    text = font.render(f"Player {current_player}'s Turn", True, "white")
    text_rect = text.get_rect(center=(x_loc + 150, y_loc + 50))
    screen.blit(text, text_rect)

    if game_type == 2:
        font = pygame.font.Font(None, 40)
        text = font.render("Player 2", True, "white")
        text_rect = text.get_rect(center=(x_loc + 150, y_loc + 400))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 40)
        text = font.render(f"Wins: {ai1.wins}", True, "white")
        text_rect = text.get_rect(center=(x_loc + 150, y_loc + 450))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 40)
        text = font.render(f"Losses: {ai1.losses}", True, "white")
        text_rect = text.get_rect(center=(x_loc + 150, y_loc + 500))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 40)
        text = font.render(f"Draws: {ai1.draws}", True, "white")
        text_rect = text.get_rect(center=(x_loc + 150, y_loc + 550))
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

def draw_selection_screen(screen):
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
