from QAgent import *

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
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        ],
        'strikes': 3,
        "locked_rows": 1,
         "opponent_score": 11,
        "player_score": 12

    }

def test_get_list_of_valid_actions():
    qAgent = QAgent("Allan test")
    qAgent.get_list_of_valid_actions(state)
    assert(qAgent.valid_actions == [1, 2, 4, 5, 6])

    