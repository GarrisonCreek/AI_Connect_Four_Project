import time
import math
import random

class minimaxAI:
    wins = 0
    losses = 0
    draws = 0
    transposition_table = {}

    def __init__(self, token, time_limit):
        self.token = token  # The AI's token (1 for red, 2 for yellow)
        self.time_limit = time_limit  # Time limit in seconds
        self.transposition_table = {}
        self.start_time = None

    def get_valid_moves(self, board):
        moves = []
        for col in range(len(board[0])):
            if board[0][col] == 0:  # Valid column
                center_col = len(board[0]) // 2
                score = abs(center_col - col)  # Prioritize center
                moves.append((col, score))
        return [col for col, _ in sorted(moves, key=lambda x: x[1])]

    def evaluate_board(self, board):
        self.start_time = time.time()  # Start the timer
        best_score = -math.inf
        best_col = random.choice([c for c in range(len(board[0])) if board[0][c] == 0])  # Fallback

        for col in self.get_valid_moves(board):
            if board[0][col] == 0:  # Check if column is valid
                row = self.get_next_open_row(board, col)
                if row is not None:
                    board[row][col] = self.token
                    score = self.minimax(board, 5, False, -math.inf, math.inf)
                    board[row][col] = 0  # Undo move
                    if score > best_score:
                        best_score = score
                        best_col = col
                    elif score == best_score:  # Randomize between equal scores
                        if random.random() > 0.5:
                            best_col = col
        print ("Best score:", best_score)
        print ("Best col:", best_col)
        return best_col

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        # Check time limit
        if time.time() - self.start_time > self.time_limit:
            return 0  # Neutral score if out of time

        # Check if game is over or depth limit reached
        if depth == 0 or self.check_win(board, 1) or self.check_win(board, 2) or self.check_draw(board):
            return self.score_board(board, self.token)

        if is_maximizing:
            best_score = -math.inf
            for col in self.get_valid_moves(board):
                if board[0][col] == 0:
                    row = self.get_next_open_row(board, col)
                    if row is not None:
                        board[row][col] = self.token
                        score = self.minimax(board, depth - 1, False, alpha, beta)
                        board[row][col] = 0
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = math.inf
            for col in self.get_valid_moves(board):
                if board[0][col] == 0:
                    row = self.get_next_open_row(board, col)
                    if row is not None:
                        board[row][col] = 3 - self.token
                        score = self.minimax(board, depth - 1, True, alpha, beta)
                        board[row][col] = 0
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score

    def score_board(self, board, token):
        score = 0

        # Center column control
        center_col = len(board[0]) // 2
        center_count = sum(row[center_col] == token for row in board)
        score += center_count * 3

        # Scoring horizontal, vertical, and diagonal patterns
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Vertical, horizontal, diagonals
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == token:
                    for dr, dc in directions:
                        score += self.score_window(board, row, col, dr, dc, token)
                elif board[row][col] == 3 - token:
                    for dr, dc in directions:
                        score -= self.score_window(board, row, col, dr, dc, 3 - token)

        return score

    def score_window(self, board, row, col, dr, dc, token):
        score = 0
        opponent = 3 - token
        count = 0
        empty_count = 0
        opponent_count = 0

        for i in range(4):  # Checks 4 cells in the specified direction
            r, c = row + i * dr, col + i * dc
            if 0 <= r < len(board) and 0 <= c < len(board[0]):
                if board[r][c] == token:
                    count += 1
                elif board[r][c] == opponent:
                    opponent_count += 1
                else:
                    empty_count += 1

        # Scoring rules
        if count == 4:
            score += 10000  # Winning move
            return score
        elif count == 3 and empty_count == 1:
            score += 100  # Strong pattern
        elif count == 2 and empty_count == 2:
            score += 50   # Potential pattern

        # Penalize opponent's threats
        if opponent_count == 3 and empty_count == 1:
            score -= 10000  # Block opponent's winning move
        
        if opponent_count == 2 and empty_count == 2:
            score -= 50  # Block opponent's threat

        return score

    def can_win(self, board, token):
        for col in range(len(board[0])):
            row = self.get_next_open_row(board, col)
            if row is not None:
                board[row][col] = token
                if self.check_win(board, token):
                    board[row][col] = 0
                    return True
                board[row][col] = 0
        return False


    def get_next_open_row(self, board, col):
        for row in range(len(board) - 1, -1, -1):
            if board[row][col] == 0:
                return row
        return None

    def check_win(self, board, token):
        # Check all possible win conditions
        for row in range(len(board)):
            for col in range(len(board[0])):
                if self.check_direction(board, row, col, token, 1, 0) or \
                    self.check_direction(board, row, col, token, 0, 1) or \
                    self.check_direction(board, row, col, token, 1, 1) or \
                    self.check_direction(board, row, col, token, 1, -1):
                    return True
        return False

    def check_direction(self, board, row, col, token, delta_row, delta_col):
        count = 0
        for i in range(4):
            r, c = row + i * delta_row, col + i * delta_col
            if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == token:
                count += 1
            else:
                break
        return count == 4


    def check_draw(self, board):
        return all(board[0][col] != 0 for col in range(len(board[0])))