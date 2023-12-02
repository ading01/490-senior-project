import json
import math
import sys
import time

import numpy as np

actions = [0, 1, 2, 3, 4, 5, 6, 7, 8]


# actions 0 1 -> row 0
# actions 2 3 -> row 1
# actions 4 5 -> row 2
# actions 6 7 -> row 3
# action 8 -> skip



# ///////////////helper functions///////////////

def get_right_index(row):
    for i in range(len(row) -1, -1, -1):
        if row[i] == 1:
            return i
    return -1

def get_left_index(row):
    for i in range(len(row)):
        if row[i] == 1:
            return i
    return 11

def is_leading(state, action):
    opponent_score = state['opponent_score']
    player_score = state['player_score']

    if player_score > opponent_score:
        return 1
    elif player_score == opponent_score:
        return 0
    else:
        return -1

# ///////////////helper functions///////////////



# How many boxes would the action miss? (negative weight)
# Rightmost box that is crossed off (slightly negative weight) — I might eliminate this one 
# How many boxes are there already crossed off in the row (positive weight)
# Will_action_result_in_first_strike_and_is_leading
# …(same for 2, 3, 4th strike)
# will_action_result_in_lock and leading (neutral? Positive?)
# is_valid_action (extremely negative)
# is_active_player_and_has_not_moved (slightly positive) -> either a 0 or 1



def getRightMostInactiveCellsInRow(state, actiion):
    ans = []
    for row_index in range(4):
        right_most_inactive_cell_in_row = getRightMostInactiveCellInRow(state, action, row_index)
        ans.append(right_most_inactive_cell_in_row)
    return ans

def getRightMostInactiveCellInRow(state, action, row_index):
    board = state['valid_cells']
    row = board[row_index]
    for i in range(len(row)):
        if row[i] == 0:
            return i / 11
    return 0

# def getTotalMarkedCellsInRow(state, action, color):
#     pass


def getTotalCellsMissed2(state, action):
    if action == 8:
        return 1

    board = state['valid_cells']
    row = board[action // 2]
    right_most_crossed_off_cell = get_right_index(row)
    # if right_most_crossed_off_cell == 0:
    #     right_most_crossed_off_cell = -1
    
    selectable_row = state['selectable_cells'][action // 2]

    if action % 2 == 0:
        # get left
        l_selectable_cell = get_left_index(selectable_row)
        if l_selectable_cell - right_most_crossed_off_cell > 0:
            return (l_selectable_cell - right_most_crossed_off_cell - 1) / 10
        else:
            return 1
    else:
        # get right
        r_selectable_cell = get_right_index(selectable_row)
        if r_selectable_cell - right_most_crossed_off_cell > 0:
            return (r_selectable_cell - right_most_crossed_off_cell - 1)  / 10
        else:
            return 1

def is_trying_to_lock(state, action):
    if action == 8:
        return 0
    
    if action % 2 == 0:
        # left
        r_ind = get_right_index(state['selectable_cells'][action // 2])
        if r_ind == 10:
            return 1
    else:
        l_ind = get_left_index(state['selectable_cells'][action // 2])
        if l_ind == 0:
            return 0
    
    return 0


def willActionResultInLock(state, action):
    if action == 8:
        return 0

    if state["num_crossed_out_cells"][action // 2] < 5:
        return 0
    
    if action % 2 == 1:
        # right
        if get_right_index(state['selectable_cells'][action // 2]) == 10:
            return 1
    else:
        # left
        if get_left_index(state['selectable_cells'][action // 2]) == 10:
            return 1
    return 0


def willActionResultInStrikeAndIsLeading(state, action):
    if action == 8 and state["already_moved"] == False and state["active_player"] == 1:
        leading = is_leading(state, action)
        return (state["strikes"] * leading) / 3
    else:
        return 0


            
def willActionResultInFirstStrike(state, action):
    if action == 8 and state["already_moved"] == False and state["strikes"] == 0:
        return 1
    else:
        return 0

def willActionResultInSecondStrike(state, action):
    if action == 8 and state["already_moved"] == False and state["strikes"] == 1:
        return 1
    else:
        return 0

def willActionResultInThirdStrike(state, action):
    if action == 8 and state["already_moved"] == False and state["strikes"] == 2:
        return 1
    else:
        return 0

def willActionResultInFourthStrike(state, action):
    if action == 8 and state["already_moved"] == False and state["strikes"] == 3:
        return 1
    else:
        return 0

def willActionEndGame(state, action):
    if action == 8 and state["already_moved"] == False and state["strikes"] == 3:
        return 1
    elif willActionResultInLock(state, action) == 1 and state["locked_rows"] == 1:
        return 1
    else:
        return 0

def is_invalid_action(state, action):
    if action == 8:
        return 0

    right_most_inactive_cell_in_row = getRightMostInactiveCellInRow(state, action, action // 2) * 11
    if action % 2 == 0:
        # left
        left_ind = get_left_index(state['selectable_cells'][action // 2])
        # if 12th box and less than 5 checks, return 1

        if left_ind == 10 and state['num_crossed_out_cells'][action // 2] < 5:
            return 1

        if left_ind <= right_most_inactive_cell_in_row:
            return 1
    else:
        right_ind = get_right_index(state['selectable_cells'][action // 2])
        if right_ind == 10 and state['num_crossed_out_cells'][action // 2] < 5:
            return 1
        if right_ind <= right_most_inactive_cell_in_row:
            return 1
    
    return 0

def will_result_in_lock_and_is_leading(state, action):
    leading = is_leading(state, action)
    will_lock = willActionResultInLock(state, action)
    return will_lock * leading



def isCellSelectable(state, action, row, column):
    pass

# functions_list = [getRightMostInactiveCellInRow, getTotalCellsMissed2, willActionResultInLock, willActionResultInFirstStrike, willActionResultInSecondStrike, willActionResultInThirdStrike, willActionResultInFourthStrike, willActionEndGame]

# test_state = []

# data = {
#     'active_player': 0,
#     'game_state': 2,
#     'already_moved': False,
#     'valid_cells': [
#         [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     ],
#     'num_crossed_out_cells': [11, 3, 5, 5],
#     'selectable_cells': [
#         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
#     ],
#     'strikes': 3,
#     "locked_rows": 1
# }


def is_active_player_and_has_not_already_moved(state, action):
    pass

def get_num_boxes_crossed_off(state, action):
    if action == 8:
        return 0
    return state['num_crossed_out_cells'][action // 2] / 10

def get_rightmost_crossed_off_index(state, action):
    if action == 8:
        return 0
    row = state['valid_cells'][action // 2]
    return (get_right_index(row) + 1) / 11

functions = [
    getTotalCellsMissed2,
    get_num_boxes_crossed_off, 
    get_rightmost_crossed_off_index, 
    willActionResultInStrikeAndIsLeading, 
    will_result_in_lock_and_is_leading, 
    is_invalid_action
    ]

def create_feature_list(state, action):
    
    features = []
    feature_values = []
    # print(f"feature_values with action {action}")
    for function in functions:
        feature_value = function(state, action)
        features.append(feature_value)
        feature_values.append((function.__name__, feature_value))
    #     print(f"{function.__name__}: {feature_value}")
    # print("\n")

    # print(f"feature_values with action {action}", feature_values)



    # features = []
    # colors = ["red", "yellow", "green", "blue"]

    

    # for row_index in range(4):
    #     right_most_inactive_cell_in_row = getRightMostInactiveCellInRow(state, action, row_index)
    #     features.append(right_most_inactive_cell_in_row)

    # num_marked_cells = [num / 11 for num in state['num_crossed_out_cells'] ]
    # features.extend(num_marked_cells)

    # features.append(getTotalCellsMissed2(state, action))
    # features.append(willActionResultInLock(state, action))
    # features.append(willActionResultInFirstStrike(state, action))
    # features.append(willActionResultInSecondStrike(state, action))
    # features.append(willActionResultInThirdStrike(state, action))
    # features.append(willActionResultInFourthStrike(state, action))
    # features.append(willActionEndGame(state, action))
    # features.append(is_trying_to_lock(state, action))
    # features.append(is_valid_action(state, action))
    # features.append(state["active_player"])
    # features.append(state["game_state"])
    # features.append(state["already_moved"])
    # features.append(state["locked_rows"])

    # How many boxes would the action miss? (negative weight)
    # Rightmost box that is crossed off (slightly negative weight) — I might eliminate this one 
    # How many boxes are there already crossed off in the row (positive weight)
    # Will_action_result_in_first_strike_and_is_leading
    # …(same for 2, 3, 4th strike)
    # will_action_result_in_lock and leading (neutral? Positive?)
    # s_valid_action (extremely negative)
    # is_active_player_and_has_not_moved (slightly positive) -> either a 0 or 1

    # my_dict = {
    #     "right_most_inactive_cell_in_row": features[0],
    #     "boxes_already_crossed_off": features[1],
    #     "Will_action_result_in_first_strike_and_is_leading": features[2],
        
    # }

    # my_dict = {
    #     "right_most_inactive_cell_in_row": features[0:4],
    #     "num_marked_cells": features[4:8],
    #     "total_cells_missed": features[8],
    #     "will_action_result_in_lock": features[9],
    #     "will_action_result_in_first_strike": features[10],
    #     "will_action_result_in_second_strike": features[11],
    #     "will_action_result_in_third_strike": features[12],
    #     "will_action_result_in_fourth_strike": features[13],
    #     "will_action_end_game": features[14],
    #     "is_trying_to_lock": features[15],
    #     "is_valid_action": features[16],
    #     "active_player": features[17],
    #     "game_state": features[18],
    #     "already_moved": features[19],
    #     "locked_rows": features[20]
    # }


    # json_string = json.dumps(my_dict, indent=2)

    # print(json_string)
    
    return features, feature_values






if __name__ == "__main__":
    for i in actions:
        print(create_feature_list(data, action=i))

"""

Features:
[0]: right_most_inactive_cell_in_red_row
[1]: right_most_inactive_cell_in_yellow_row
[2]: right_most_inactive_cell_in_green_row
[3]: right_most_inactive_cell_in_blue_row
[4]: number_of_marked_boxes_in_red_row
[5]: number_of_marked_boxes_in_yellow_row
[6]: number_of_marked_boxes_in_green_row
[7]: number_of_marked_boxes_in_blue_row

"""