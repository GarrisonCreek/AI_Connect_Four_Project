import pygame
from minimaxAI import minimaxAI
from constants import *
from graphics import *
from montecarloAI import MCTS_AI

class ConnectFour:
    def __init__(self):
        self.board = [[0 for col in range(COLUMN_COUNT)] for row in range(ROW_COUNT)]
        self.current_player = 1
        self.winning_player = 0
        self.game_over = False
        self.game_type = 0
        self.pause_for_game_over = True
        self.ai1 = None
        self.ai2 = None

    def select_game_type(self, selected_game_type):
        self.game_type = selected_game_type
        if selected_game_type == 1:
            print("Game type selected: Player vs Player")

        elif selected_game_type == 2:
            print("Game type selected: Player vs AI")
            # self.ai1 = minimaxAI(2, 4)
            self.ai1 = MCTS_AI(2, iterations=2000)

        elif selected_game_type == 3:
            print("Game type selected: AI vs AI")
            # self.ai1 = minimaxAI(1, 4)
            self.ai1 = MCTS_AI(1, iterations=1000)
            # self.ai2 = minimaxAI(2, 4)
            self.ai2 = MCTS_AI(2, iterations=1000)

    def drop_token(self, col):
        for row in range(ROW_COUNT-1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                if self.check_win(self.current_player):
                    print(f"Player {self.current_player} wins!")
                    if self.game_type == 2:
                        self.ai1.wins += 1
                        self.game_over = True
                    elif self.game_type == 3:
                        if self.current_player == 1:
                            self.ai1.wins += 1
                            self.ai2.losses += 1
                        elif self.current_player == 2:
                            self.ai1.losses += 1
                            self.ai2.wins += 1
                        self.game_over = True
                    self.game_over = True
                if row == 0 and self.check_draw():
                    print("It's a draw!")
                    if self.game_type == 2:
                        self.ai1.draws += 1
                        self.game_over = True
                    elif self.game_type == 3:
                        self.ai1.draws += 1
                        self.ai2.draws += 1
                        self.game_over = True
                    self.game_over = True
                self.switch_player()
                break

    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def check_win(self, token):
        self.winning_player = token
        for col in range(COLUMN_COUNT-3): # check for win horizontally
            for row in range(ROW_COUNT):
                if self.board[row][col] == token and self.board[row][col+1] == token and self.board[row][col+2] == token and self.board[row][col+3] == token:
                    return True
        for col in range(COLUMN_COUNT): # check for win vertically
            for row in range(ROW_COUNT-3):
                if self.board[row][col] == token and self.board[row+1][col] == token and self.board[row+2][col] == token and self.board[row+3][col] == token:
                    return True
        for col in range(COLUMN_COUNT-3): # check for win diagonally
            for row in range(ROW_COUNT-3):
                if self.board[row][col] == token and self.board[row+1][col+1] == token and self.board[row+2][col+2] == token and self.board[row+3][col+3] == token:
                    return True
        for col in range(COLUMN_COUNT-3): # check for win diagonally
            for row in range(3, ROW_COUNT):
                if self.board[row][col] == token and self.board[row-1][col+1] == token and self.board[row-2][col+2] == token and self.board[row-3][col+3] == token:
                    return True
        self.winning_player = 0
        return False

    def check_draw(self):
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                if self.board[row][col] == 0:
                    return False
        return True

    def reset_game(self):
        self.board = [[0 for col in range(COLUMN_COUNT)] for row in range(ROW_COUNT)]
        self.current_player = 1
        self.winning_player = 0
        self.game_over = False

    def get_valid_moves(self):
        valid_moves = []
        for col in range(COLUMN_COUNT):
            if self.board[0][col] == 0:
                valid_moves.append(col)
        return valid_moves

    def ai_move(self):
        if self.game_type == 2 and self.current_player == 2:
            col = self.ai1.evaluate_board(self.board)
            self.drop_token(col)
        elif self.game_type == 3:
            if self.current_player == 1:
                col = self.ai1.evaluate_board(self.board)
                self.drop_token(col)
            elif self.current_player == 2:
                col = self.ai2.evaluate_board(self.board)
                self.drop_token(col)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # exit game with 'esc' key
                return False
            elif event.key == pygame.K_r: # reset game with 'r' key
                self.reset_game()
            elif event.key == pygame.K_TAB: # reset game with 'tab' key
                self.reset_game()
                self.select_game_type(0)
            elif event.key == pygame.K_h: # print out all legal moves with 'h' key
                # print(self.get_legal_actions())
                print ("TODO fix tis")
            if self.game_type == 0:
                if event.key == pygame.K_1: # select game type with '1' key
                    self.select_game_type(1)
                elif event.key == pygame.K_2: # select game type with '2' key
                    self.select_game_type(2)
                elif event.key == pygame.K_3: # select game type with '3' key
                    self.select_game_type(3)
            elif self.game_type == 1 or self.game_type == 2 and not self.game_over:
                if event.key == pygame.K_1:
                    self.drop_token(0)
                elif event.key == pygame.K_2:
                    self.drop_token(1)
                elif event.key == pygame.K_3:
                    self.drop_token(2)
                elif event.key == pygame.K_4:
                    self.drop_token(3)
                elif event.key == pygame.K_5:
                    self.drop_token(4)
                elif event.key == pygame.K_6:
                    self.drop_token(5)
                elif event.key == pygame.K_7:
                    self.drop_token(6)
            elif self.game_type == 3:
                if event.key == pygame.K_c: # continue game with 'c' key
                    self.pause_for_game_over = not self.pause_for_game_over
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.game_type == 1 or self.game_type == 2 and not self.game_over:
                mouse_pos = pygame.mouse.get_pos()
                if 175 < mouse_pos[0] < 245:
                    self.drop_token(0)
                elif 275 < mouse_pos[0] < 345:
                    self.drop_token(1)
                elif 375 < mouse_pos[0] < 445:
                    self.drop_token(2)
                elif 475 < mouse_pos[0] < 545:
                    self.drop_token(3)
                elif 575 < mouse_pos[0] < 645:
                    self.drop_token(4)
                elif 675 < mouse_pos[0] < 745:
                    self.drop_token(5)
                elif 775 < mouse_pos[0] < 845:
                    self.drop_token(6)
        return True

    def render(self, screen):
        screen.fill(BACKGROUND_COLOR)
        if self.game_type == 0:
            draw_selection_screen(screen)
        else:
            draw_board(screen, self.board)
            draw_side_panel(screen, self.current_player, self.game_type, self.ai1, self.ai2)
        if self.game_over:
            draw_game_over(screen, self.winning_player)
        pygame.display.flip()