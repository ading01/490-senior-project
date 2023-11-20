from function import *


# /////////////////////////// TESTS ///////////////////////////
def test_get_right_index(row=[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]):
    ind = get_right_index(row)
    assert ind == 5, "get_right_index() failed" 
    assert get_right_index([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]) == 10, "get_right_index() failed"

def test_get_left_index(row=[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]):
    ind = get_left_index(row)
    assert ind == 5, "get_left_index() failed"
    assert get_left_index([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0, "get_right_index() failed"
    assert get_left_index([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]) == 10, "get_right_index() failed"
    assert get_left_index([0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0]) == 2, "get_right_index() failed"

def test_locking_second_row_ends_game():
    state = {
        'active_player': 0,
        'game_state': 2,
        'already_moved': False,
        'valid_cells': [
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        'num_crossed_out_cells': [4, 3, 5, 0],
        'selectable_cells': [
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        ],
        'strikes': 3,
        "locked_rows": 1
    }
    action = 5
    assert create_feature_list(state, action)[14] == 1, "test_locking_second_row_ends_game() failed"
    assert create_feature_list(state, 4)[14] == 0

def test_action_8_ends_game_by_strike():
    state = {
        'active_player': 0,
        'game_state': 2,
        'already_moved': False,
        'valid_cells': [
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        'num_crossed_out_cells': [11, 3, 5, 5],
        'selectable_cells': [
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        ],
        'strikes': 3,
        "locked_rows": 1
    }
    assert create_feature_list(state, 8)[14] == 1, "test_action_8_ends_game_by_strike() failed"

def test_is_valid_action():
    state = {
        'active_player': 0,
        'game_state': 2,
        'already_moved': False,
        'valid_cells': [
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        'num_crossed_out_cells': [11, 3, 5, 5],
        'selectable_cells': [
            [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        ],
        'strikes': 3,
        "locked_rows": 1
    }
    # pass is valid
    assert create_feature_list(state, 8)[16] == 1, "test_is_valid_action() failed"
    assert create_feature_list(state, 4)[16] == 0, "test left ind is not valid"
    assert create_feature_list(state, 5)[16] == 0, "test right is not valid"
    assert create_feature_list(state, 0)[16] == 0, "test left is not valid"
    assert create_feature_list(state, 1)[16] == 1, "test right is valid"

# //////////END TESTS //////////