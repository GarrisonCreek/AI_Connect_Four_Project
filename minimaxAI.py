import math
import random

class minimaxAI:
    # Stat tracking
    wins = 0
    losses = 0
    draws = 0
    depth = 4 # default search depth
    transposition_table = {} # Store board states to avoid redundant calculations

    def __init__(self, token, depth):
        self.token = token  # The AI's token (1 for red, 2 for yellow)
        self.depth = depth
        self.transposition_table = {}

    def get_valid_moves(self, board):
        moves = []
        for col in range(len(board[0])):
            if board[0][col] == 0:  # Valid column
                center_col = len(board[0]) // 2
                score = abs(center_col - col)  # Prioritize center
                moves.append((col, score))
        return [col for col, _ in sorted(moves, key=lambda x: x[1])]

    def evaluate_board(self, board):
        # Perform minimax to determine the best move
        best_score = -math.inf
        best_col = random.choice([c for c in range(len(board[0])) if board[0][c] == 0])  # Fallback

        for col in self.get_valid_moves(board):
            if board[0][col] == 0:  # Check if column is valid
                row = self.get_next_open_row(board, col)
                if row is not None:
                    board[row][col] = self.token
                    score = self.minimax(board, self.depth - 1, False, -math.inf, math.inf)
                    board[row][col] = 0  # Undo move
                    if score > best_score:
                        best_score = score
                        best_col = col
                    elif score == best_score:  # Randomize between equal scores
                        if random.random() > 0.5:
                            best_col = col
        return best_col

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        board_key = tuple(tuple(row) for row in board)  # Hashable board state
        if board_key in self.transposition_table:
            return self.transposition_table[board_key]

        if self.check_win(board, self.token):
            return 1000 - depth  # Encourage quicker wins
        elif self.check_win(board, 3 - self.token):
            return -1000 + depth  # Discourage delayed losses
        elif depth == 0 or all(board[0][c] != 0 for c in range(len(board[0]))):
            return self.score_position(board)  # Heuristic evaluation

        if is_maximizing:
            max_eval = -math.inf
            for col in range(len(board[0])):
                if board[0][col] == 0:
                    row = self.get_next_open_row(board, col)
                    if row is not None:
                        board[row][col] = self.token
                        eval = self.minimax(board, depth - 1, False, alpha, beta)
                        board[row][col] = 0
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            self.transposition_table[board_key] = max_eval
            return max_eval
        else:
            min_eval = math.inf
            for col in range(len(board[0])):
                if board[0][col] == 0:
                    row = self.get_next_open_row(board, col)
                    if row is not None:
                        board[row][col] = 3 - self.token
                        eval = self.minimax(board, depth - 1, True, alpha, beta)
                        board[row][col] = 0
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            self.transposition_table[board_key] = min_eval
            return min_eval

    def score_position(self, board):
        score = 0

        # Center column control
        center_col = len(board[0]) // 2
        center_count = sum(row[center_col] == self.token for row in board)
        score += center_count * 3

        # Score based on patterns
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == self.token:
                    score += self.score_window(board, row, col, self.token)
                elif board[row][col] == 3 - self.token:
                    score -= self.score_window(board, row, col, 3 - self.token)

        return score

    def score_window(self, board, row, col, token):
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Vertical, horizontal, diagonals
        for dr, dc in directions:
            count = 0
            for i in range(4):
                r, c = row + i * dr, col + i * dc
                if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == token:
                    count += 1
            if count == 4:
                score += 100
            elif count == 3:
                score += 10
            elif count == 2:
                score += 1
        return score

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
