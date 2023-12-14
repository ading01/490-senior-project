# CPSC 490: Senior Project

## Game Quality and Strategy Analysis Comparison for Qwixx and Two Qwixx Variants

This project aims to analyze and compare game quality and strategy effectiveness across the original game of Qwixx and two of its variants using various player types including AI and human players.

## Files Description

- `play.py`: The main script for playing the game. It provides access to different types of players:

  - `HumanPlayer`: A human-playable player that allows a person to interact with the game.
  - CPU Players:
    - `GreedyPlayer`: Attempts to maximize the number of points each turn.
    - `TwoPlayer`: Focuses on maximizing points and triggering end-game conditions when leading.
    - `QAgent`: A machine learning agent that learns to improve its gameplay over time. Currently set to a level that beats the GreedyPlayer approximately 40% of the time.
  - You can mix and match these players in any two-player combination.

- `QAgent.py`: Contains the code to train the Q-learning agent.

  - To train the agent, set `exploit` to `False` and run `python3.11 QAgent.py`.
  - For faster training, set `DO_DRAW` to `False` in `qwixx.py` to disable drawing the game state.

- `qwixx.py`: Contains primary gameplay mechanics, human player interface, and heuristic-based CPU player implementation.

- `two_player.py`: Implements the two-player heuristic strategy and includes methods for gathering gameplay metrics.

  - Run `python3.11 two_player.py` to watch two heuristic players compete, play a series of games, and display gathered metrics.

- `single_player.py`: An initial prototype created to learn the basics of Pygame.

## Running Tests

To run the test suite, navigate to the project directory and execute pytest:

```sh
cd Qwixx
pytest
```
