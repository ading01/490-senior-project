
import time
from random import randint

from function import *
from qwixx import *

GAMES = 10

class QAgent(Player):
    def __init__(self, name):
        super().__init__(name)
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0
        self.weights = []
    

    def get_state(self, game):
        return game.get_state()

   
    
    def roll_dice(self, game):
        game.roll_dice()
    
    def make_color_move(self, game):
        # adapter
        self.highlight_all_selectable_cells(game)
        curr_state = self.get_state(game)
        action = self.get_action(curr_state)
        self.make_move(game, curr_state, action)

    def make_optional_move(self, game):
        # adapter
        curr_state = self.get_state(game)
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
        print('Qagent curr state', curr_state)
        
        if action == 8:
            return

        valid_cells = self.qwixx_card.valid_cells
        
        if len(valid_cells) == 4:
            self.player_select_cell(valid_cells[action // 2])
            # self.qwixx_card.selected_cell = valid_cells[action // 2]
        elif len(valid_cells) == 8:
            self.player_select_cell(valid_cells[action])
            # self.qwixx_card.selected_cell = valid_cells[action]
        
        try:
            self.qwixx_card.cross_out_cell()
            self.is_made_move = True
        except InadequateChecks:
            print("inadequate checks")
            return
        except InvalidDeactivate:
            print("invalid deactivate")
            return

        # self.qwixx_card.valid_cells = []
            





        # calculate which dice will cross out
        # if action == 0:
        #     # red left
        #     pass
        # elif action == 1:
        #     # red right
        #     pass
        # elif action == 2:
        #     # yellow left
        #     pass
        # elif action == 3:
        #     # yellow right
        #     pass
        # elif action == 4:
        #     # green left
        #     pass
        # elif action == 5:
        #     # green right
        #     pass
        # elif action == 6:
        #     # green right
        #     pass
        # elif action == 7:
        #     # blue left
        #     pass
        # elif action == 8:
        #     # blue right
        #     pass

        # select dice
        # cross out cell
        # get_reward
        # adjust weights


        # possibily implment a switch case here

        # depending on the action, select the proper dice
        # cross out cell
        # check for errors raised
        # return reward for action
        # points scored = scored points
        # strike - 5 points
        # skip - 0 points
        # invalid move - -100 points
        # win game - 10 points 
    
    def get_action(self, state):
        # for now, always make a random move

        final_move = randint(0, 8)
        print("final move", final_move)
        return final_move

    

def train():
    n_games = 0
    qAgent = QAgent("QAgentBigBrain")

    while n_games < GAMES:
        game = QwixxGame([HumanPlayer("Allan"), QAgent("QAgent")])
        qAgent.weights.append(game.run())
        n_games += 1
        print("gmae done")
    
    return qAgent.weights

if __name__ == "__main__":
    print(train())


        