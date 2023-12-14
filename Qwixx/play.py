from QAgent import QAgent
from qwixx import *
from two_player import *

if __name__ == "__main__":
    # replace the players array with two of the following:

    # ____________OPTIONS____________________
    # QAgent("QAgent")
    # GreedyHeuristicPlayer("GreedyHeuristicPlayer")
    # HumanPlayer("HumanPlayer")
    # TwoPlayerHeuristic("TwoPlayerHeuristic")

    players = [HumanPlayer("Human"), QAgent("QAgent2")]
    game = QwixxGame(players, keep_showing=True)
    game.run()
