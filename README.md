# AI_Connect_Four_Project
Semester Project for Artificial Intelligence, at IUS

## Project Description

The project is a simple implementation of the Connect Four game written in Python using Pygame.

We have implemented two AI algorithms, Minimax and Monte Carlo Tree Search (MCTS), to play against each other or against a human player.

There are 4 game modes to choose from:
- Player vs Player
- Player vs MCTS AI (Capped at 10 seconds per move)
- MCTS (5 secs) vs Minimax AI
- Minimax AI vs MCTS (5 secs)


## How to run the game

1. Clone the repository
2. Install requirements: pip install pygame
3. Run the game: python main.py


## How to play

esc: Exits the game
tab: Goes back to the selection screen
r: Resets the game
c: Toggles automatic reset after game over in AI modes, for pauses and manual resets in between AI games, reset with r

On the selection screen, keys 1-4 are used to select the game mode.

- 1: Player vs Player
- 2: Player vs MCTS AI
- 3: MCTS AI vs Minimax AI
- 4: Minimax AI vs MCTS AI

After selecting the game mode, the game will start. In modes with player input (1 and 2), the player can use keys 1-7 to select the column to drop the piece. Or alternatively use the mouse to click on the column you want to drop the piece into.

When the game is over (win or draw), you can start a new game by pressing the 'r' key. If you are in an AI mode, you can toggle automatic reset after game over by pressing the 'c' key. This will cause the AI to start a new game immediately after the game is over forever. To manually reset the game in this mode, press the 'r' key.
The tab key can be used at any time to end a game and go back to the selection screen.
To exit the game, press the 'esc' key or close the window.