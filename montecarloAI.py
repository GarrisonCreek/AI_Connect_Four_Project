import random
import math
import copy


class MCTS_AI:
    def __init__(self, player, iterations):
        self.player = player
        self.iterations = iterations
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

        def ucb1(self, total_simulations):
            if self.visits == 0:
                return float('inf')  # Encourage exploration of unvisited nodes
            win_rate = self.wins / self.visits
            exploration_factor = math.sqrt(math.log(total_simulations) / self.visits)
            return win_rate + exploration_factor

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

    def check_win(self, board, player):
        rows, cols = len(board), len(board[0])
        for col in range(cols - 3):  # Horizontal
            for row in range(rows):
                if all(board[row][col + i] == player for i in range(4)):
                    return True
        for col in range(cols):  # Vertical
            for row in range(rows - 3):
                if all(board[row + i][col] == player for i in range(4)):
                    return True
        for col in range(cols - 3):  # Diagonal
            for row in range(rows - 3):
                if all(board[row + i][col + i] == player for i in range(4)):
                    return True
            for row in range(3, rows):
                if all(board[row - i][col + i] == player for i in range(4)):
                    return True
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
            if result == self.player:  # AI wins
                node.wins += 1
            elif result == 3 - self.player:  # AI loses
                node.losses += 1
            # Draws do not affect wins/losses
            node = node.parent

    def best_move(self, root):
        return max(root.children, key=lambda child: child.visits).move

    def evaluate_board(self, board):
        root = self.Node(copy.deepcopy(board))

        # Run simulations
        for iteration in range(self.iterations):
            node = root

            # Selection
            while node.children:
                node = max(node.children, key=lambda child: child.ucb1(root.visits))

            # Expansion
            if node.visits > 0 and not node.children:
                self.expand_node(node)

            if node.children:
                node = random.choice(node.children)

            # # Defensive check: Block immediate win  TODO: Fix this
            # legal_moves = self.get_legal_actions(node.state)
            # for move in legal_moves:
            #     temp_board = copy.deepcopy(node.state)
            #     self.make_move(temp_board, move, 3 - self.player)  # Opponent's move
            #     if self.check_win(temp_board, 3 - self.player):  # If opponent wins
            #         # Force block this move by choosing it
            #         return move

            result = self.simulate_game(copy.deepcopy(node.state), self.player)
            # Backpropagation
            self.backpropagate(node, result)

        print("\n--- MCTS Decision Process ---")
        safe_moves = []
        for child in root.children:
            temp_board = copy.deepcopy(board)
            self.make_move(temp_board, child.move, self.player)

            # Check if the opponent can win immediately after this move
            opponent_can_win = any(
                self.check_win(copy.deepcopy(temp_board), 3 - self.player)
                for move in self.get_legal_actions(temp_board)
            )

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
        print(f"Predicted Win Rate for Best Move: {best_child.wins / best_child.visits:.2f}")
        return best_child.move