#  Connect Four Game with AI and Pygame


# this AI is simple and not very smart
# it just tries to win or block the opponent from winning
# it doesn't look ahead to see if it can win in the next move


class AI:

#  stat tracking
    wins = 0
    losses = 0
    draws = 0

    def __init__(self, token):
        self.token = token  # The AI's token (1 for red, 2 for yellow)

    def evaluate_board(self, board):
        # Simple evaluation function to choose a column
        # This AI just tries to win or block the opponent from winning
        for col in range(len(board[0])):
            if self.can_win(board, col, self.token):
                return col
            if self.can_win(board, col, 3 - self.token):  # Opponent's token
                return col
        # If no immediate win or block, choose a random column
        import random
        return random.choice([c for c in range(len(board[0])) if board[0][c] == 0])

    def can_win(self, board, col, token):
        # Check if dropping a token in the column can result in a win
        for row in range(len(board) - 1, -1, -1):
            if board[row][col] == 0:
                board[row][col] = token
                if self.check_win(board, token):
                    board[row][col] = 0
                    return True
                board[row][col] = 0
                break
        return False

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
        # Check a specific direction for a win
        count = 0
        for i in range(4):
            r = row + i * delta_row
            c = col + i * delta_col
            if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == token:
                count += 1
            else:
                break
        return count == 4



