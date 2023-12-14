from two_player import count_lead_changes


def test_count_lead_changes():
    player1_scores = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    player2_scores = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert count_lead_changes(player1_scores, player2_scores) == 0

    player1_scores = [0, 1, 3, 3, 4, 5, 6, 7, 8]
    player2_scores = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert count_lead_changes(player1_scores, player2_scores) == 1

    player1_scores = [0, 1, 3, 3, 4, 4, 4, 7, 8]
    player2_scores = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert count_lead_changes(player1_scores, player2_scores) == 2
