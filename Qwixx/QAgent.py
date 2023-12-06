
import time
from random import randint

import matplotlib.pyplot as plt
import numpy as np

from function import *
from qwixx import *

# from helper import plot

PRINT_GAME_INFO = True

GAMES = 10000
RECHECK = GAMES // 10
INVALID_MOVE_REWARD = -13
PENALTY_FOR_NO_ACTIONS = -15

HUMAN_TEST = False

EXPLOIT_ONLY = True

HUMAN_PRINT = False

def human_print(string, *args):
    if HUMAN_PRINT:
        print(string, args)

class QAgent(Player):
    def __init__(self, name):
        super().__init__(name)
        self.action_counts = [0 for i in range(9)]
        self.n_explores = 0
        self.n_exploits = 0
        self.n_games = 0
        self.invalid_moves = 0
        self.InadequateChecks = 0 
        self.InvalidDeactivates = 0


        self.learning_rate = 0.001
        self.epsilon = 0
        self.gamma = 0.99
        self.step = 0.00005
        if EXPLOIT_ONLY:
            self.weights = [-14.183727143778377, -4.578589520344524, -3.0740653481647584]
        else:
            self.weights = [0 for i in range(len(functions))]
        self.best_weights = None
        
        self.valid_actions = []
    

    def get_state(self, game):
        return game.get_state()

    def player_reset(self):
        self.n_explores = 0
        self.invalid_moves = 0
        self.n_exploits = 0
        self.action_counts = [0 for i in range(9)]
        self.qwixx_card = QwixxCard(self.name)
        self.is_made_move = False
        self.InadequateChecks = 0 
        self.InvalidDeactivates = 0
    
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
    
    def assign_dice(self, white1, white2):
        if white1.get_value() <= white2.get_value():
            return [white1, white2]
        else:
            return [white2, white1]


    def highlight_all_selectable_cells(self, game):
        # print("called highlighted")
        dice = game.dice
        # white_dice = dice[:2]
        forward_running = dice[2:4]
        backward_running = dice[4:]

        white_dice = self.assign_dice(dice[0], dice[1])

    
        for colored_die in forward_running:
            for white_die in white_dice:
                total = white_die.get_value() + colored_die.get_value()
                column = total - 2
                if colored_die.get_color() == "red":
                    row = 0
                else:
                    row = 1
                self.add_cell_to_valid_cells(row, column)

    
        for colored_die in backward_running:
            for white_die in reversed(white_dice):
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
        # print("\n")
        # print(game.get_state())
        # print("curr_state", curr_state)
        # print("action", action)
        self.action_counts[action] += 1
        
        if action == 8:
            curr_state = game.get_state()
            if curr_state["active_player"] == 1 and curr_state["game_state"].value == 3:
                
                reward = PENALTY_FOR_NO_ACTIONS
            else: 
                reward = -10
            
            # TODO: FIX THIS should also update on skip
            # maybe add keyword argument
            # print("reward", reward)
            new_state = game.get_state() 
            self.update_weights(reward, curr_state, action, new_state)
            return

        valid_cells = self.qwixx_card.valid_cells
        # print("here valid cells")
        # for valid_cell in valid_cells:
        #     print(valid_cell)
        
        if len(valid_cells) == 4:
            self.player_select_cell(valid_cells[action // 2])
            # print("valid cell after selection", valid_cells[action // 2])
            # self.qwixx_card.selected_cell = valid_cells[action // 2]
        elif len(valid_cells) == 8:
            # print("valid cell after selection", valid_cells[action])
            self.player_select_cell(valid_cells[action])
            # self.qwixx_card.selected_cell = valid_cells[action]
        
        try:
            reward = self.qwixx_card.cross_out_cell()
            self.is_made_move = True
        except InadequateChecks:
            # print("inadequate checks")
            self.InadequateChecks += 1
            reward = INVALID_MOVE_REWARD
        except InvalidDeactivate:
            # print("invalid deactivate")
            self.InvalidDeactivates += 1
            reward = INVALID_MOVE_REWARD
        finally:
            # print("reward", reward)
            new_state = game.get_state() 
            self.update_weights(reward, curr_state, action, new_state)
            # print(self.weights)
            return
        
    def update_weights(self, reward, curr_state, action, new_state):
        if EXPLOIT_ONLY:
            return
        features, feature_values = create_feature_list(curr_state, action)
        human_print(feature_values)
        for i in range(len(self.weights)):
            self.weights[i] = self.weights[i] + self.learning_rate * (reward + self.gamma * self.getMaxQValue(new_state) - self.getQValue(curr_state, action)) * features[i]
        

    def set_list_of_valid_actions(self, state):
        valid_actions = []
        # active_boxes = state["valid_cells"]
        for action in range(4):
            row = state["selectable_cells"][action]
            l_ind = get_left_index(row)
            r_ind = get_right_index(row)

            active_row = state["valid_cells"][action]

            if l_ind == r_ind and l_ind < 11 and l_ind > -1 and active_row[l_ind] == 0:
                valid_actions.append(action * 2)
            else:
                if l_ind < 11 and active_row[l_ind] == 0:
                    valid_actions.append(action * 2)
                
                if r_ind > -1 and active_row[r_ind] == 0:
                    valid_actions.append(action * 2 + 1)
        
        valid_actions.append(8)
        self.valid_actions = valid_actions




    
    def get_action(self, state):
        # for now, always make a random move
        self.set_list_of_valid_actions(state)
        if EXPLOIT_ONLY:
            return self.getMaxAction(state)
            
        # print("valid actions", self.valid_actions)

        # epsilon starts at zero and then increases over time

        if random.randint(0, 100) > self.epsilon:
            human_print("explore")
            self.n_explores += 1
            randnum = randint(0, len(self.valid_actions) - 1)
            final_move = self.valid_actions[randnum]
            # print("final move", final_move)
        else:
            human_print("exploit")
            self.n_exploits += 1
            final_move = self.getMaxAction(state)
            # exploit
        
        self.epsilon = self.epsilon + self.step
        human_print("making move", final_move)
        return final_move
    
    def getMaxQValue(self, state):
        # print("getMaxQValue")
        max_Q_value = 0
        # TODO if state is not terminal
        for action in range(9):
            value = self.getQValue(state, action)
            if value > max_Q_value:
                max_Q_value = value
        return max_Q_value

    def getMaxAction(self, state):
        # print("getMaxAction")
        max_action = 0
        max_Q_value = -100
        # TODO if state is not terminal
        # for action in range(8, -1, -1):
        for action in self.valid_actions:
            q_value = self.getQValue(state, action)
            if q_value > max_Q_value:
                max_Q_value = q_value
                max_action = action
        return max_action
    
    def getQValue(self, state, action):
        weights = self.weights
        features, feature_values = create_feature_list(state, action)
        # print("len weights and features", len(weights), len(features))
        q_value = np.dot(features, weights)
        return q_value

    def get_best_weights(self):
        return ["{:.2f}".format(value) for value in self.best_weights]


def train():
    n_games = 0
    qAgent = QAgent("QAgentBigBrain")
    total_score = 0
    games = []
    all_scores = []
    mean_scores = []

    prev_average_score = -100
    counter = 0

    total_exploits = 0
    total_explores = 0

    mean_exploits = []
    mean_explores = []
    best_average_score = -100

    total_invalid_moves = 0
    invalid_moves = []



    while n_games < GAMES:
        
            
        # HeuristicPlayer
        if HUMAN_TEST:
            game = QwixxGame([HumanPlayer("Robot"), qAgent])
        else:
            game = QwixxGame([HeuristicPlayer("Robot"), qAgent])

        game.run()
        score = game.players[1].qwixx_card.calculate_score()
        # print("game number", n_games, game.players[1].name, "score", score)
        total_score += score
        all_scores.append(score)
        games.append(n_games)
        n_games += 1

        average_score = total_score / n_games
        mean_scores.append(average_score)

        if average_score >= best_average_score:
            best_average_score = average_score
            qAgent.best_weights = qAgent.weights



        # if n_games == GAMES // 2:
        #     midway_score = total_score / n_games
        # if n_games == (GAMES // 4) * 3:
        #     if total_score / n_games < midway_score:
        #         break

        
        if not EXPLOIT_ONLY and counter >= RECHECK:
            counter = 0
            if total_score / n_games < prev_average_score:
                break
            else:
                prev_average_score = total_score / n_games
            
            
        
        counter += 1
        

        # Plot scores in real-time
        # plt.plot(all_scores, color='r', label='Scores')
        # plt.plot(mean_scores, color='b', label='Mean Scores')
        # plt.legend()
        # plt.pause(0.001)  # Pause for a short time to update the plot
        total_exploits += qAgent.n_exploits
        total_explores += qAgent.n_explores
        total_invalid_moves += qAgent.invalid_moves
        mean_exploits.append(total_exploits / n_games)
        mean_explores.append(total_explores / n_games)

        
        invalid_moves.append(total_invalid_moves / n_games)


        if PRINT_GAME_INFO:
            print(f"Game {n_games:5} QAgent score: {score:3} | Explores: {qAgent.n_explores:3} | Exploits: {qAgent.n_exploits:3} InadequateChecks: {qAgent.InadequateChecks:3} | InvalidDeactivates: {qAgent.InvalidDeactivates:3}")
            print(qAgent.weights)
            print(qAgent.action_counts)
            
        # print("Game ", n_games, "QAgent score: ", score, "| Explores: ", qAgent.n_explores, "| Exploits: ", qAgent.n_exploits, "Invalid_moves", qAgent.invalid_moves)
        
        qAgent.player_reset()
    
    if EXPLOIT_ONLY:
        plt.title(f'Average Score of Agent over {n_games} games\nWeights used: {qAgent.get_best_weights()}')
    else:
        plt.title(f'Average Score of Agent over {n_games} episodes\n LR:{qAgent.learning_rate}; Step: {qAgent.step}\n Best weights: {qAgent.get_best_weights()}')
    plt.xlabel('Episodes')
    plt.ylabel('Frequency')
    plt.plot(all_scores, color='r', label='Scores')
    plt.plot(mean_scores, color='b', label='Mean Scores')
    if not EXPLOIT_ONLY:
        plt.plot(mean_exploits, color='g', label='Exploits')
        plt.plot(mean_explores, color='m', label='Explores')
        plt.plot(invalid_moves, color='orange', label='Invalid moves')
    plt.text(n_games, average_score, f'{average_score:.2f}', color='b', fontsize=8, ha='left', va='bottom')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    plt.tight_layout()

    plt.show()
    print("average score:", average_score)
    print("best weights:", qAgent.best_weights)
    return qAgent.weights

# def train():
#     n_games = 0
#     qAgent = QAgent("QAgentBigBrain")
#     total_score = 0
#     games = []
#     all_scores = []
#     mean_scores = []

#     while n_games < GAMES:
#         game = QwixxGame([HumanPlayer("Robot"), qAgent])
#         game.run()
#         score = game.players[1].qwixx_card.calculate_score()
#         # print("game number", n_games, game.players[1].name, "score", score)
#         total_score += score
#         all_scores.append(score)
#         games.append(n_games)
#         n_games += 1
    
#         mean_scores.append(total_score / n_games)
        
#         qAgent.player_reset()
#     plt.plot(all_scores, color = 'r')
#     plt.plot(mean_scores, color = 'b')
#     plt.show()
#     return qAgent.weights

if __name__ == "__main__":
    print(train())


        