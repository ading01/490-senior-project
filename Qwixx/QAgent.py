
import time
from random import randint

import matplotlib.pyplot as plt
import numpy as np

from function import *
from qwixx import *

# from helper import plot


GAMES = 300000

class QAgent(Player):
    def __init__(self, name):
        super().__init__(name)
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.99
        self.weights = [0 for i in range(len(functions))]
    

    def get_state(self, game):
        return game.get_state()

    def player_reset(self):
        self.qwixx_card = QwixxCard(self.name)
        self.is_made_move = False
    
    def roll_dice(self, game):
        game.roll_dice()
    
    def make_color_move(self, game):
        # adapter
        self.highlight_all_selectable_cells(game)
        curr_state = game.get_state()
        action = self.get_action(curr_state)
        self.make_move(game, curr_state, action)

    def make_optional_move(self, game):
        # adapter
        curr_state = game.get_state()
        action = self.get_action(curr_state)
        self.make_move(game, curr_state, action)

    def calculate_dice_combo(self, game, action):
        if game.game_state == 1:
            return 0, 1
        dice = game.dice
        white0 = dice[0]
        white1 = dice[1]
        # if action is even, it's the left
        # the dice value is the action 7 // action + 2
        if action % 2 == 0:
            # left, less
            if white1.get_value() >= white0.get_value():
                return 0, (action // 2) + 2
            else:
                return 1, (action // 2) + 2
        else: 
            if white1.get_value() >= white0.get_value():
                return 1, (action // 2) + 2
            else:
                return 0, (action // 2) + 2
            
    
    # def select_cell(self, state, action):
    #     print("selecting cell", state, action)
    #     # get cell coordinates
    #     # get cell with those coordinates
    #     # select that cell
    #     # cross out the cell

    def add_cell_to_valid_cells(self, x, y, cell=None):
        if cell is not None:
            self.qwixx_card.valid_cells.append(cell)
        else:
            self.qwixx_card.valid_cells.append(self.qwixx_card.get_cell_by_x_y(x, y))
        return
        


    def highlight_all_selectable_cells(self, game):
        dice = game.dice
        white_dice = dice[:2]
        forward_running = dice[2:4]
        backward_running = dice[4:]


        for white_die in white_dice:
            for colored_die in forward_running:
                total = white_die.get_value() + colored_die.get_value()
                column = total - 2
                if colored_die.get_color() == "red":
                    row = 0
                else:
                    row = 1
                self.add_cell_to_valid_cells(row, column)

        for white_die in white_dice:
            for colored_die in backward_running:
                total = white_die.get_value() + colored_die.get_value()
                column = 12 - total
                if colored_die.get_color() == "green":
                    row = 2
                else:
                    row = 3
                self.add_cell_to_valid_cells(row, column)
        
            
        game.draw_game()
        
        time.sleep(CPU_WAIT_TIME)
        
    
                



        
    
    
    def make_move(self, game, curr_state, action):
        
        if action == 8:
            curr_state = game.get_state()
            if curr_state["active_player"] == 1 and curr_state["game_state"].value == 3:
                
                reward = -5
            else: 
                reward = 0
            
            # TODO: FIX THIS should also update on skip
            # maybe add keyword argument
            new_state = game.get_state() 
            self.update_weights(reward, curr_state, action, new_state)
            return

        valid_cells = self.qwixx_card.valid_cells
        
        if len(valid_cells) == 4:
            self.player_select_cell(valid_cells[action // 2])
            # self.qwixx_card.selected_cell = valid_cells[action // 2]
        elif len(valid_cells) == 8:
            self.player_select_cell(valid_cells[action])
            # self.qwixx_card.selected_cell = valid_cells[action]
        
        try:
            reward = self.qwixx_card.cross_out_cell()
            self.is_made_move = True
        except InadequateChecks:
            # print("inadequate checks")
            reward = -40
        except InvalidDeactivate:
            # print("invalid deactivate")
            reward = -40
        finally:
            # print("reward", reward)
            new_state = game.get_state() 
            self.update_weights(reward, curr_state, action, new_state)
            return
        
    def update_weights(self, reward, curr_state, action, new_state):
        features = create_feature_list(curr_state, action)
        for i in range(len(self.weights)):
            self.weights[i] = self.weights[i] + (1 / (self.n_games + 1)) * (reward + self.gamma * self.getMaxQValue(new_state) - self.getQValue(curr_state, action)) * features[i]
        


    
    def get_action(self, state):
        # for now, always make a random move

        # epsilon starts at zero and then increases over time

        if random.randint(0, 100) > self.epsilon:
            # print("explore")
            final_move = randint(0, 8)
            # print("final move", final_move)
        else:
            # print("exploit")
            final_move = self.getMaxAction(state)
            # exploit
        
        self.epsilon = self.epsilon + 0.001
        return final_move
    
    def getMaxQValue(self, state):
        max_Q_value = 0
        # TODO if state is not terminal
        for action in range(9):
            value = self.getQValue(state, action)
            if value > max_Q_value:
                max_Q_value = value
        return max_Q_value

    def getMaxAction(self, state):
        max_action = 0
        max_Q_value = 0
        # TODO if state is not terminal
        for action in range(9):
            q_value = self.getQValue(state, action)
            if q_value > max_Q_value:
                max_Q_value = q_value
                max_action = action
        return max_action
    
    def getQValue(self, state, action):
        weights = self.weights
        features = create_feature_list(state, action)
        # print("len weights and features", len(weights), len(features))
        q_value = np.dot(features, weights)
        return q_value

    

def train():
    n_games = 0
    qAgent = QAgent("QAgentBigBrain")
    total_score = 0
    games = []
    all_scores = []
    mean_scores = []

    while n_games < GAMES:
        game = QwixxGame([HumanPlayer("Robot"), qAgent])
        game.run()
        score = game.players[1].qwixx_card.calculate_score()
        # print("game number", n_games, game.players[1].name, "score", score)
        total_score += score
        all_scores.append(score)
        games.append(n_games)
        n_games += 1
    
        mean_scores.append(total_score / n_games)
        
        qAgent.player_reset()
    plt.plot(all_scores, color = 'r')
    plt.plot(mean_scores, color = 'b')
    plt.show()
    return qAgent.weights

if __name__ == "__main__":
    print(train())


        