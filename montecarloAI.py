import random
import math
import copy
from constants import *
import time

class MCTS_AI:
    def __init__(self, player, time_limit=5):
        self.player = player
        self.iterations = 0
        self.time_limit = time_limit
        self.wins = 0
        self.losses = 0
        self.draws = 0

    class Node:
        def __init__(self, state, parent=None, move=None):
            self.state = state
            self.parent = parent
            self.move = move
            self.children = []
            self.visits = 0
            self.wins = 0
            self.losses = 0

        def ucb1(self, total_simulations): # Upper Confidence Bound 1
            if self.visits == 0:
                return math.inf
            exploitation = self.wins / self.visits
            exploration = math.sqrt(2 * math.log(total_simulations) / self.visits)
            return exploitation + exploration

    def get_legal_actions(self, board):
        legal_moves = [col for col in range(len(board[0])) if board[0][col] == 0]
        return legal_moves

    def simulate_game(self, board, current_player):
        while True:
            legal_moves = self.get_legal_actions(board)
            if not legal_moves:
                return 0  # Draw

            # Defensive heuristic: Block opponent's winning move
            if current_player != self.player:
                for move in legal_moves:
                    temp_board = copy.deepcopy(board)
                    self.make_move(temp_board, move, current_player)
                    if self.check_win(temp_board, current_player):
                        return 3 - self.player  # Opponent wins

            # Offensive heuristic: Try to win if possible
            for move in legal_moves:
                temp_board = copy.deepcopy(board)
                self.make_move(temp_board, move, current_player)
                if self.check_win(temp_board, current_player):
                    return current_player  # Current player wins

            # Choose a random move if no better move found
            move = random.choice(legal_moves)
            self.make_move(board, move, current_player)

            if self.check_win(board, current_player):
                return current_player  # Current player wins

            current_player = 3 - current_player

    def make_move(self, board, col, player):
        for row in reversed(range(len(board))):
            if board[row][col] == 0:
                board[row][col] = player
                return

    def check_win(self, board, token):
        self.winning_player = token
        for col in range(COLUMN_COUNT-3): # check for win horizontally
            for row in range(ROW_COUNT):
                if board[row][col] == token and board[row][col+1] == token and board[row][col+2] == token and board[row][col+3] == token:
                    return True
        for col in range(COLUMN_COUNT): # check for win vertically
            for row in range(ROW_COUNT-3):
                if board[row][col] == token and board[row+1][col] == token and board[row+2][col] == token and board[row+3][col] == token:
                    return True
        for col in range(COLUMN_COUNT-3): # check for win diagonally
            for row in range(ROW_COUNT-3):
                if board[row][col] == token and board[row+1][col+1] == token and board[row+2][col+2] == token and board[row+3][col+3] == token:
                    return True
        for col in range(COLUMN_COUNT-3): # check for win diagonally
            for row in range(3, ROW_COUNT):
                if board[row][col] == token and board[row-1][col+1] == token and board[row-2][col+2] == token and board[row-3][col+3] == token:
                    return True
        self.winning_player = 0
        return False

    def expand_node(self, node):
        legal_moves = self.get_legal_actions(node.state)
        for move in legal_moves:
            next_state = copy.deepcopy(node.state)
            self.make_move(next_state, move, self.player)
            child_node = self.Node(next_state, node, move)
            node.children.append(child_node)

    def backpropagate(self, node, result):
        while node:
            node.visits += 1
            if result == self.player:
                node.wins += 1
            else:
                node.losses += 1
            node = node.parent

    def best_move(self, root):
        return max(root.children, key=lambda child: child.visits).move

    def evaluate_board(self, board):
        root = self.Node(copy.deepcopy(board))
        start_time = time.time()  # Record the start time

        # Run simulations until the time limit is reached
        while time.time() - start_time < self.time_limit:
            self.iterations += 1
            node = root

            # Selection
            while node.children:
                node = max(node.children, key=lambda child: child.ucb1(root.visits))

            # Expansion
            if node.visits == 0:
                self.expand_node(node)
                node = random.choice(node.children)

            # Simulation
            result = self.simulate_game(copy.deepcopy(node.state), self.player)

            # Backpropagation
            self.backpropagate(node, result)

        print("\n--- MCTS Decision Process ---")
        safe_moves = []
        for child in root.children:
            temp_board = copy.deepcopy(board)
            self.make_move(temp_board, child.move, self.player)

            # Check if the opponent can win immediately after this move
            opponent_can_win = False
            for move in self.get_legal_actions(temp_board):
                temp_board2 = copy.deepcopy(temp_board)
                self.make_move(temp_board2, move, 3 - self.player)
                if self.check_win(temp_board2, self.player):
                    print("Overiding for insta win") # TODO: REMOVE THIS LINE
                    return child.move
                if self.check_win(temp_board2, 3 - self.player):
                    opponent_can_win = True
                    break

            if opponent_can_win:
                print(f"Move {child.move} allows opponent to win! Ignoring this move.")
            else:
                safe_moves.append(child)

        # Select the best move among safe options
        if safe_moves:
            best_child = max(safe_moves, key=lambda child: (child.wins / child.visits, child.visits))
        else:
            best_child = max(root.children, key=lambda child: (child.wins / child.visits, child.visits))

        # Print out the statistics for each move
        for child in root.children:
            win_rate = child.wins / child.visits
            loss_rate = child.losses / child.visits
            print(f"Move: {child.move}, Visits: {child.visits}, Wins: {child.wins}, "
                f"Losses: {child.losses}, Win Rate: {win_rate:.2f}, "
                f"Loss Rate: {loss_rate:.2f}, UCB1: {child.ucb1(root.visits):.2f}")

        print(f"Selected Move: {best_child.move}")
        print(f"Total Iterations: {self.iterations}")
        print(f"Predicted Win Rate for Best Move: {best_child.wins / best_child.visits:.2f}")
        self.iterations = 0 # Reset the iteration count
        return best_child.move