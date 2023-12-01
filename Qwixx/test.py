from function import *

# /////////////////////////// TESTS ///////////////////////////

def test_getTotalCellsMissed2():
    state = {
        'active_player': 0,
        'game_state': 2,
        'already_moved': False,
        'valid_cells': [
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        'num_crossed_out_cells': [4, 3, 5, 0],
        'selectable_cells': [
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        ],
        'strikes': 3,
        "locked_rows": 1
    }
    action = 5
    missed_cells = getTotalCellsMissed2(state, action)
    assert missed_cells == 4 / 10

    missed_cells = getTotalCellsMissed2(state, 7)
    assert missed_cells == 10 / 10

    assert getTotalCellsMissed2(state, 4) == 1
    
    assert getTotalCellsMissed2(state, 0) == 0
    assert getTotalCellsMissed2(state, 6) == 0





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

# def test_locking_second_row_ends_game():
#     state = {
#         'active_player': 0,
#         'game_state': 2,
#         'already_moved': False,
#         'valid_cells': [
#             [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#             [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#             [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#         ],
#         'num_crossed_out_cells': [4, 3, 5, 0],
#         'selectable_cells': [
#             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
#             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
#         ],
#         'strikes': 3,
#         "locked_rows": 1
#     }
#     action = 5
#     assert create_feature_list(state, action)[14] == 1, "test_locking_second_row_ends_game() failed"
#     assert create_feature_list(state, 4)[14] == 0
    

# def test_action_8_ends_game_by_strike():
#     state = {
#         'active_player': 0,
#         'game_state': 2,
#         'already_moved': False,
#         'valid_cells': [
#             [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#             [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#             [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#         ],
#         'num_crossed_out_cells': [11, 3, 5, 5],
#         'selectable_cells': [
#             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
#         ],
#         'strikes': 3,
#         "locked_rows": 1
#     }
#     assert create_feature_list(state, 8)[14] == 1, "test_action_8_ends_game_by_strike() failed"

def test_is_invalid_action():
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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        ],
        'strikes': 3,
        "locked_rows": 1
    }
    assert(is_invalid_action(state, 0) == 1)
    assert(is_invalid_action(state, 7) == 0)
    assert(is_invalid_action(state, 3) == 1)
    assert(is_invalid_action(state, 2) == 1)
    # skip should always valid
    assert(is_invalid_action(state, 8) == 0)



    # # pass is valid
    # assert create_feature_list(state, 8)[16] == 1, "test_is_valid_action() failed"
    # assert create_feature_list(state, 4)[16] == 0, "test left ind is not valid"
    # assert create_feature_list(state, 5)[16] == 0, "test right is not valid"
    # assert create_feature_list(state, 0)[16] == 0, "test left is not valid"
    # assert create_feature_list(state, 1)[16] == 1, "test right is valid"

def test_is_leading():
    state = {
        "opponent_score": 11,
        "player_score": 30
    }
    action = 1
    assert(is_leading(state, action) == 1)


    state = {
        "opponent_score": 11,
        "player_score": 11
    }
    action = 8
    assert(is_leading(state, action) == 0)

    state = {
        "opponent_score": 11,
        "player_score": 9
    }
    action = 8
    assert(is_leading(state, action) == -1)


def test_is_leading():
    
    state = {
        "active_player": 1,
        "already_moved": False,
        "strikes": 1,
        "opponent_score": 11,
        "player_score": 9
    }
    action = 8
    assert(willActionResultInStrikeAndIsLeading(state, action) == -1 / 3)

    state = {
        "active_player": 1,
        "already_moved": False,
        "strikes": 2,
        "opponent_score": 11,
        "player_score": 9
    }
    action = 8
    assert(willActionResultInStrikeAndIsLeading(state, action) == -2 / 3)

    state = {
        "active_player": 1,
        "already_moved": False,
        "strikes": 2,
        "opponent_score": 11,
        "player_score": 12
    }
    action = 8
    assert(willActionResultInStrikeAndIsLeading(state, action) == 2 / 3)

    state = {
        "active_player": 1,
        "already_moved": False,
        "strikes": 2,
        "opponent_score": 11,
        "player_score": 11
    }
    action = 8
    assert(willActionResultInStrikeAndIsLeading(state, action) == 0 / 3)

    state = {
        "active_player": 1,
        "already_moved": False,
        "strikes": 2,
        "opponent_score": 11,
        "player_score": 11
    }
    action = 4
    assert(willActionResultInStrikeAndIsLeading(state, action) == 0)
     

def test_willActionResultInLock():
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
        'num_crossed_out_cells': [4, 3, 5, 5],
        'selectable_cells': [
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        ],
        'strikes': 3,
        "locked_rows": 1,
         "opponent_score": 11,
        "player_score": 12

    }
    action = 1
    assert(willActionResultInLock(state, action) == 0)
    assert(willActionResultInLock(state, 5) == 1)


def will_result_in_lock_and_is_leading():
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
        'num_crossed_out_cells': [4, 3, 5, 5],
        'selectable_cells': [
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        ],
        'strikes': 3,
        "locked_rows": 1,
         "opponent_score": 11,
        "player_score": 12

    }
    action = 1
    assert(willActionResultInLock(state, action) == 0)
    assert(willActionResultInLock(state, 5) == 1)

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
        'num_crossed_out_cells': [4, 3, 5, 5],
        'selectable_cells': [
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        ],
        'strikes': 3,
        "locked_rows": 1,
         "opponent_score": 11,
        "player_score": 10
    }
    assert(willActionResultInLock(state, 5) == -1)

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
        'num_crossed_out_cells': [4, 3, 5, 5],
        'selectable_cells': [
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        ],
        'strikes': 3,
        "locked_rows": 1,
         "opponent_score": 11,
        "player_score": 11
    }
    assert(willActionResultInLock(state, 5) == 0)

def test_get_rightmost_crossed_off_index():
    state = {
        'valid_cells': [
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    }
    assert(get_rightmost_crossed_off_index(state, 0) == 4 / 11)
    assert(get_rightmost_crossed_off_index(state, 4) == 11 / 11)
    assert(get_rightmost_crossed_off_index(state, 7) == 0 / 11)
    assert(get_rightmost_crossed_off_index(state, 8) == 0)



def test_create_feature_list():
    state = {
        'active_player': 0,
        'game_state': 2,
        'already_moved': False,
        'valid_cells': [
        #-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        'num_crossed_out_cells': [4, 3, 5, 5],
        'selectable_cells': [
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        ],
        'strikes': 3,
        "locked_rows": 1,
        "opponent_score": 11,
        "player_score": 11
    }
    action = 1
    features = create_feature_list(state, action)
    # total cells missed
    assert(features[0][0] == 6 / 10)
    # num boxees crossed off
    assert(features[0][1] == 4 / 10)
    # right_most index
    assert(features[0][2] == 4 / 11)
    # strike and leading
    assert(features[0][3] == 0)
    # lock and leading
    assert(features[0][4] == 0)
    # is valid
    assert(features[0][5] == 1)

    




    




def test_grace():
    # why yale law school?
    pass

# //////////END TESTS //////////