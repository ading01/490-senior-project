import math
import sys
import time

import numpy as np

actions = [0, 1, 2, 3, 4, 5, 6, 7, 8]

def getRightMostInactiveCellInRow(state, action, row_index):
    board = state['valid_cells']
    row = board[row_index]
    for i in range(len(row)):
        if row[i] == 0:
            return i / 11
    return 1

# def getTotalMarkedCellsInRow(state, action, color):
#     pass

def getTotalCellsMissed(state, action, features):
    # get index of most right inactive cell
    
    def get_left_and_right_indices(row):
        l = 12
        r = 12

        for i in range(len(row)):
            if row[i] == 1 and l == 12:
                l = i
                r = i
            elif row[i] == 1:
                r = i
        
        return l, r
    
    board = state['selectable_cells']
    row = board[action // 2]
    l, r = get_left_and_right_indices(row)
    print("left, right", l, r)
    right_most_inactive_cell_in_row = features[action // 2] * 11


    if action % 2 == 0:
        if r - right_most_inactive_cell_in_row >= 0:
            return r - right_most_inactive_cell_in_row 
        else:
            return 12
    else:
        # left
        if l - right_most_inactive_cell_in_row >= 0:
            return l - right_most_inactive_cell_in_row
        else:
            return 12
        

def willActionResultInLock(state, action):
    pass

def willActionResultInFirstStrike(state, action):
    pass

def willActionResultInSecondStrike(state, action):
    pass

def willActionResultInThirdStrike(state, action):
    pass

def willActionResultInFourthStrike(state, action):
    pass

def willActionEndGame(state, action):
    pass

def isCellSelectable(state, action, row, column):
    pass

functions_list = [getRightMostInactiveCellInRow, getTotalCellsMissed, willActionResultInLock, willActionResultInFirstStrike, willActionResultInSecondStrike, willActionResultInThirdStrike, willActionResultInFourthStrike, willActionEndGame]

test_state = []

data = {
    'active_player': 0,
    'game_state': 2,
    'already_moved': False,
    'valid_cells': [
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    'num_crossed_out_cells': [11, 3, 4, 5],
    'selectable_cells': [
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    ],
    'strikes': 2
}

def create_feature_list(state, action):
    features = []
    colors = ["red", "yellow", "green", "blue"]

    for row_index in range(4):
        right_most_inactive_cell_in_row = getRightMostInactiveCellInRow(state, action, row_index)
        features.append(right_most_inactive_cell_in_row)

    num_marked_cells = [num / 11 for num in state['num_crossed_out_cells'] ]
    features.extend(num_marked_cells)

    features.append(getTotalCellsMissed(state, action, features))

    # for row_index in range(4):
    #     total_cells_missed = getTotalCellsMissed(state, action, features[row_index])
    #     features.append(total_cells_missed)
    
    return features

def try_this():
    print(data['active_player'])
    

if __name__ == "__main__":
    print(create_feature_list(data, action=1))
    # try_this()
