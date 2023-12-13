import queue
from threading import Thread

from qwixx import *

TWO_PLAYER_CONSERVATIVE_THRESHOLD = 1
ABSORB_STRIKE_THRESHOLD = 4


class TwoPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def roll_dice(self, game):
        game.roll_dice()

    def get_num_opponent_locked_rows(self, game):
        for player in game.players:
            if player is not self:
                return player.get_num_locked_rows()

    def get_min_score_diff(self, game):
        min_score_diff = 2000

        for player in game.players:
            # TODO maybe make it such that player is not self
            if player is not self:
                score_diff = player.get_card_score() - self.get_card_score()
                if score_diff < min_score_diff:
                    min_score_diff = score_diff
        return min_score_diff

    # def race_to_lock_filter(self):

    # def get_best_move(self, cells, game):
    #     min_score_diff = self.get_min_score_diff(game)
    #     threshold = 4

    #     self_locked_rows = self.get_num_locked_rows()
    #     opponent_locked_rows = self.get_num_opponent_locked_rows(game)

    #     locking_moves = self.get_locking_moves(cells, self.qwixx_card.board)
    #     print("locking moves", locking_moves)
    #     if min_score_diff <= 0:
    #         if self_locked_rows == 1:
    #             # leading and you are close to ending the game
    #             if len(locking_moves) > 0:
    #                 return (locking_moves[0], 0)
    #             # if min_score_diff < 10:
    #             #     threshold = 5
    #             # elif min_score_diff < 20:
    #             #     threshold = 3
    #             # elif min_score_diff < 30:
    #             #     threshold = 10
    #         elif self_locked_rows == 0:

    #             if opponent_locked_rows == 1:
    #                 # leading and opponent is close to ending game
    #                 if min_score_diff < 10:
    #                     threshold = 4
    #                 elif min_score_diff < 20:
    #                     if len(locking_moves) > 0:
    #                         return (locking_moves[0], 0)
    #                     threshold = 4
    #                 elif min_score_diff < 30:
    #                     if len(locking_moves) > 0:
    #                         return (locking_moves[0], 0)
    #                     threshold = 4
    #         else:
    #             print("game should have already ended")
    #             raise Exception("something bad went wrong ehre")
    #     else:
    #         if min_score_diff > 5:
    #             if len(locking_moves) > 0:
    #                 return (locking_moves[0], 0)

    #         # if loing then, try to catch up fast if opponent is close to ending game

    #     max_dist = 100  # can be any number greater than the number of cells per row
    #     candidates = []
    #     my_print("len cells:", len(cells))

    #     if len(cells) == 0:
    #         return None

    #     for valid_cell in cells:
    #         distance = self.distance_from_prev_crossed_out_cell(valid_cell)
    #         if distance == max_dist and valid_cell.is_active:
    #             candidates.append((valid_cell, distance))
    #         elif distance < max_dist and valid_cell.is_active:
    #             max_dist = distance
    #             candidates = [(valid_cell, distance)]

    #     my_print("max dist", max_dist)
    #     # 5 is pretty good
    #     if max_dist > threshold:
    #         my_print("1. max dist")
    #         return None

    #     if len(candidates) == 0:
    #         my_print("2. len(candidates) == 0")
    #         return None

    #     max_checks = 0
    #     farthest_left = 20
    #     choices = []
    #     for candidate in candidates:
    #         row_number = candidate[0].row
    #         number_of_checks = self.qwixx_card.board[row_number].number_of_checks
    #         if number_of_checks == max_checks:
    #             choices.append(candidate)
    #         elif number_of_checks > max_checks:
    #             max_checks = number_of_checks
    #             choices = [candidate]
    #     # for candidate in candidates:
    #     #     box = candidate[0]
    #     #     if box.column < farthest_left:
    #     #         farthest_left = box.column
    #     #         choices = [candidate]
    #     #     elif box.column == farthest_left:
    #     #         choices.append(candidate)

    #     if len(choices) == 0:
    #         my_print("3. len(choices) == 0")
    #         return None
    #     else:
    #         choice_int = random.randint(0, len(choices) - 1)
    #         choice = choices[choice_int]
    #         my_print("4. chioce: ", choice)

    #         return choice

    def get_color_move_options(self, game):
        white_dice = game.dice[0:2]
        colored_dice = game.dice[2:6]
        candidates = []

        for white_die in white_dice:
            for colored_die in colored_dice:
                total = white_die.get_value() + colored_die.get_value()
                color = colored_die.get_color()

                for row in self.qwixx_card.board:
                    for cell in row.cells:
                        if (
                            cell.is_active
                            and cell.number == total
                            and cell.color == color
                        ):
                            candidates.append(cell)
        return candidates

    def get_locking_moves(self, cells, board):
        candidates = []
        for cell in cells:
            if (
                cell.is_active
                and cell.column == 10
                and board[cell.row].number_of_checks >= 5
            ):
                candidates.append(cell)
        return candidates

    def make_color_move(self, game):
        self.n_moves += 1
        white_dice = game.dice[0:2]
        colored_dice = game.dice[2:6]
        candidates = []

        for white_die in white_dice:
            for colored_die in colored_dice:
                total = white_die.get_value() + colored_die.get_value()
                color = colored_die.get_color()

                for row in self.qwixx_card.board:
                    for cell in row.cells:
                        if (
                            cell.is_active
                            and cell.number == total
                            and cell.color == color
                        ):
                            candidates.append(cell)

        best_move = self.get_best_move(candidates, game)

        if best_move is None:
            my_print("1: No best color move in color")
            time.sleep(CPU_WAIT_TIME)
            return

        conservative_threshold = TWO_PLAYER_CONSERVATIVE_THRESHOLD
        min_score_diff = self.get_min_score_diff(game)

        # if min_score_diff <= -30:
        #     conservative_threshold = 10
        # if min_score_diff <= 0:
        #     conservative_threshold = 0
        # elif min_score_diff > 0 and min_score_diff <= 10:
        #     conservative_threshold = 3
        # else:
        #     conservative_threshold = 2

        if self.is_made_move:
            if best_move[1] < (conservative_threshold + 1):
                try:
                    self.qwixx_card.selected_cell = best_move[0]
                    self.qwixx_card.cross_out_cell()
                    game.record_scores()
                except InadequateChecks:
                    my_print("INADEQITE CHECKS")
                    return
                except InvalidDeactivate:
                    my_print("invalid deactivate")
                    return
                finally:
                    time.sleep(CPU_WAIT_TIME)
            else:
                return
        else:
            try:
                self.qwixx_card.selected_cell = best_move[0]
                self.qwixx_card.cross_out_cell()
                game.record_scores()
                self.is_made_move = True
            except InadequateChecks:
                my_print("INADEQITE CHECKS")
                return
            except InvalidDeactivate:
                my_print("invalid deactivate")
                return
            finally:
                time.sleep(CPU_WAIT_TIME)

    def get_best_move(self, cells, game):
        # check if there is a locking move that would win:
        locking_moves = self.get_locking_moves(cells, self.qwixx_card.board)
        min_score_diff = self.get_min_score_diff(game)

        opponent_locked_rows = self.get_num_opponent_locked_rows(game)
        self_locked_rows = self.get_num_locked_rows()
        if self_locked_rows == 1 and min_score_diff <= 6 and len(locking_moves) > 0:
            return (locking_moves[0], -10)

        if self_locked_rows == 0 and min_score_diff <= 6 and len(locking_moves) > 0:
            return (locking_moves[0], -10)

        threshold = ABSORB_STRIKE_THRESHOLD
        if min_score_diff <= 0:
            threshold = 3
        else:
            threshold = 6

        max_dist = 100  # can be any number greater than the number of cells per row
        candidates = []
        my_print("len cells:", len(cells))

        if len(cells) == 0:
            return None

        for valid_cell in cells:
            distance = self.distance_from_prev_crossed_out_cell(valid_cell)
            if distance == max_dist and valid_cell.is_active:
                candidates.append((valid_cell, distance))
            elif distance < max_dist and valid_cell.is_active:
                max_dist = distance
                candidates = [(valid_cell, distance)]

        my_print("max dist", max_dist)
        # 5 is pretty good
        if max_dist > threshold:
            my_print(".   1. max dist")
            return None

        if len(candidates) == 0:
            my_print(".   2. len(candidates) == 0")
            return None

        max_checks = 0
        farthest_left = 20
        choices = []
        for candidate in candidates:
            box = candidate[0]
            if box.column < farthest_left:
                farthest_left = box.column
                choices = [candidate]
            elif box.column == farthest_left:
                choices.append(candidate)
            # row_number = candidate[0].row
            # number_of_checks = self.qwixx_card.board[row_number].number_of_checks
            # if number_of_checks == max_checks:
            #     choices.append(candidate)
            # elif number_of_checks > max_checks:
            #     max_checks = number_of_checks
            #     choices = [candidate]
        if len(choices) == 0:
            my_print(".     3. len(choices) == 0")
            return None
        else:
            choice_int = random.randint(0, len(choices) - 1)
            choice = choices[choice_int]
            my_print(".      4. chioce: ", choice)

            return choice

    def make_optional_move(self, game):
        self.n_moves += 1
        #  computer
        # instead of determining left most, determine which is closest to a cell to ther right
        optional_cells = self.qwixx_card.valid_cells
        if len(optional_cells) == 0:
            time.sleep(CPU_WAIT_TIME)
            return

        best_optional_choice = self.get_best_move(optional_cells, game)

        if best_optional_choice is None:
            my_print("2. no best optional move, skipping")
            time.sleep(CPU_WAIT_TIME)
            return

        if game.players[game.active_player] is self:
            white_dice = game.dice[0:2]
            colored_dice = game.dice[2:6]
            colored_cells = []
            for white_die in white_dice:
                for colored_die in colored_dice:
                    total = white_die.get_value() + colored_die.get_value()
                    color = colored_die.get_color()
                    for row in self.qwixx_card.board:
                        for cell in row.cells:
                            if (
                                cell.is_active
                                and cell.number == total
                                and cell.color == color
                            ):
                                colored_cells.append(cell)

            best_colored_choice = self.get_best_move(colored_cells, game)
            if best_colored_choice is None:
                best_colored_choice = (0, 100000)

            if best_colored_choice[1] < best_optional_choice[1]:
                # skip
                my_print("skipping on turn optional")
                time.sleep(CPU_WAIT_TIME)
                return
            else:
                try:
                    self.qwixx_card.selected_cell = best_optional_choice[0]
                    self.qwixx_card.cross_out_cell()
                    game.record_scores()
                    self.is_made_move = True
                except InadequateChecks:
                    my_print("inadequate checks")
                    return
                finally:
                    time.sleep(CPU_WAIT_TIME)

        else:
            # if CPU does not need to move
            conservative_threshold = TWO_PLAYER_CONSERVATIVE_THRESHOLD
            min_score_diff = self.get_min_score_diff(game)

            # if min_score_diff <= -20:
            #     conservative_threshold = 10
            # if min_score_diff <= 0:
            #     conservative_threshold = 1
            # elif min_score_diff > 0 and min_score_diff <= 10:
            #     conservative_threshold = 3
            # else:
            #     conservative_threshold = 2

            if best_optional_choice[1] < (conservative_threshold + 1):
                my_print("making optional move")
                try:
                    self.qwixx_card.selected_cell = best_optional_choice[0]
                    self.qwixx_card.cross_out_cell()
                    game.record_scores()
                except InadequateChecks:
                    return
                finally:
                    time.sleep(CPU_WAIT_TIME)

    # def make_optional_move(self, game):
    #     optional_cells = self.qwixx_card.valid_cells
    #     if len(optional_cells) == 0:
    #         time.sleep(CPU_WAIT_TIME)
    #         return

    #     best_move = self.get_best_move(optional_cells, game)
    #     if best_move is None:
    #         time.sleep(CPU_WAIT_TIME)
    #         return
    #     print("two_player: best color move:", best_move)
    #     try:
    #         self.qwixx_card.selected_cell = best_move[0]
    #         self.qwixx_card.cross_out_cell()
    #         self.is_made_move = True
    #     except InadequateChecks:
    #         print("inadequate checks")
    #         return
    #     except InvalidDeactivate:
    #         print('invalid deactivate')
    #         return
    #     finally:
    #         time.sleep(CPU_WAIT_TIME)

    # def make_color_move(self, game):
    #     color_moves = self.get_color_move_options(game)
    #     best_move = self.get_best_move(color_moves, game)

    #     if best_move is None:
    #         time.sleep(CPU_WAIT_TIME)
    #         return

    #     print("two_player: best optional move:", best_move)
    #     try:
    #         self.qwixx_card.selected_cell = best_move[0]
    #         self.qwixx_card.cross_out_cell()
    #         self.is_made_move = True
    #     except InadequateChecks:
    #         print("inadequate checks")
    #         return
    #     except InvalidDeactivate:
    #         print('invalid deactivate')
    #         return
    #     finally:
    #         time.sleep(CPU_WAIT_TIME)


def test_two_player():
    games = 10000
    total_games_won = 0
    for _ in range(games):
        players = [TwoPlayer("two_player"), HeuristicPlayer("robot")]
        game = QwixxGame(players)
        winner_name, winner_score = game.run()
        if winner_name == "two_player":
            total_games_won += 1
    print("total games won:", total_games_won)


def play_x_num_games(num_games):
    game_scores = []
    for _ in range(num_games):
        players = [TwoPlayer("Player1"), TwoPlayer("Player2")]
        game = QwixxGame(players)
        game.run()

        player1_scores = players[0].scores
        player2_scores = players[1].scores

        game_scores.append((player1_scores, player2_scores))

    return game_scores


def calculate_uncertainty(player1_scores, player2_scores):
    if player1_scores[-1] > player2_scores[-1]:
        winning_scores = player1_scores
        losing_scores = player2_scores
    else:
        winning_scores = player2_scores
        losing_scores = player1_scores

    lead_history = np.array(winning_scores) - np.array(losing_scores)

    # Define the interpolation line to intersect the winning player's last point
    interpolation_line = [
        (0, 0),
        (
            len(player1_scores) - 1,
            winning_scores[-1],
        ),  # The last point of winning scores
    ]

    slope = (interpolation_line[1][1] - interpolation_line[0][1]) / (
        interpolation_line[1][0] - interpolation_line[0][0]
    )
    intercept = interpolation_line[0][1] - slope * interpolation_line[0][0]

    x_values = np.linspace(0, len(player1_scores) - 1, len(player1_scores))
    estimated_lead_values = x_values * slope + intercept

    lead_history = np.array(winning_scores) - np.array(losing_scores)

    if len(lead_history) != len(estimated_lead_values):
        raise ValueError(
            "Both lead_history and estimated_scores must have the same length."
        )

    # total = 0
    # for i in range(len(lead_history)):
    #     total += estimated_lead_values[i] - lead_history[i]

    return np.mean(estimated_lead_values) - np.mean(lead_history)


def plot_uncertainty(player1_scores, player2_scores, M=100):
    if player1_scores[-1] > player2_scores[-1]:
        winning_scores = player1_scores
        losing_scores = player2_scores
    else:
        winning_scores = player2_scores
        losing_scores = player1_scores

    lead_history = np.array(winning_scores) - np.array(losing_scores)

    # Define the interpolation line to intersect the winning player's last point
    interpolation_line = [
        (0, 0),
        (
            len(player1_scores) - 1,
            winning_scores[-1],
        ),  # The last point of winning scores
    ]

    slope = (interpolation_line[1][1] - interpolation_line[0][1]) / (
        interpolation_line[1][0] - interpolation_line[0][0]
    )
    intercept = interpolation_line[0][1] - slope * interpolation_line[0][0]

    x_values = np.linspace(0, len(player1_scores) - 1, len(player1_scores))
    estimated_lead_values = x_values * slope + intercept

    plt.axhline(0, color="black", linewidth=1)

    plt.plot(player1_scores, label="Player 1 Scores", color="blue")
    plt.plot(player2_scores, label="Player 2 Scores", color="orange")

    # Plotting the lead history
    plt.plot(lead_history, label="Lead History", color="red", linestyle="dashed")

    # Plotting the interpolation line
    plt.plot(x_values, estimated_lead_values, label="Interpolation Line", color="grey")

    # Plotting the distances as grey dashed lines
    for i in range(len(lead_history)):
        plt.plot(
            [i, i],
            [lead_history[i], estimated_lead_values[i]],
            color="grey",
            linestyle="dashed",
        )

    # Adding legend and labels
    plt.legend()
    plt.xlabel("Turns")
    plt.ylabel("Scores")
    plt.title("Player Scores and Lead History with Interpolation Line")
    plt.show()


def plot_pie_chart(ax, data, title):
    non_completion_count = sum(data)
    completion_count = len(data) - non_completion_count
    sizes = [completion_count, non_completion_count]
    labels = ["Completion", "Non-Completion"]
    ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=["blue", "orange"],
    )
    ax.axis("equal")  # Equal aspect ratio ensures that pie chart is circular.
    ax.set_title(title)


def get_metrics_for_n_games(n_games):
    uncertainty_scores = []
    all_lead_changes = []
    all_dramas = []
    all_durations = []
    all_completions = []
    winning_scores = []

    for _ in range(n_games):
        (
            uncertainty_score,
            lead_changes,
            drama,
            duration,
            completion,
            winning_score,
        ) = get_metrics()
        uncertainty_scores.append(uncertainty_score)
        all_lead_changes.append(lead_changes)
        all_dramas.append(drama)
        all_durations.append(duration)
        all_completions.append(completion)
        winning_scores.append(winning_score)

    print("uncertainty_score", uncertainty_score)
    print("lead_changes", lead_changes)
    print("drama", drama)
    print("duration", duration)
    print("completion", completion)
    print("winning_score", winning_score)

    fig, axs = plt.subplots(3, 2, figsize=(12, 10))  # Adjusted for better spacing

    # Plotting each metric as histogram
    plot_histogram(
        axs[0, 0],
        uncertainty_scores,
        20,
        f"Uncertainty Scores over {n_games} games",
        "Uncertainty",
    )
    plot_histogram(
        axs[0, 1],
        all_lead_changes,
        range(1, max(all_lead_changes) + 2),
        f"Lead Changes per Game over {n_games} games",
        "Number of Changes",
    )
    plot_histogram(
        axs[1, 0], all_dramas, 20, f"Drama per game over {n_games} games", "Drama Score"
    )
    plot_histogram(
        axs[1, 1],
        all_durations,
        20,
        f"Duration in moves per game over {n_games} games",
        "Duration (moves)",
    )

    plot_pie_chart(axs[2, 0], all_completions, "Completion Rate")

    plot_histogram(
        axs[2, 1],
        winning_scores,
        20,
        f"Winning score per game over {n_games} games",
        "Winning Score",
    )

    # Hide the last subplot (bottom right) as we have only 5 metrics
    # axs[2, 1].axis("off")

    # Adjusting layout for better spacing and visibility
    plt.tight_layout(pad=3.0)

    # Display the plot
    plt.show()


# Function to add mean and std dev to plots
# def add_mean_std(ax, data, color="red"):
#     mean = np.mean(data)
#     std = np.std(data)
#     ax.axvline(
#         mean,
#         color=color,
#         linestyle="dashed",
#         linewidth=1,
#         label=f"Average Score: {mean:.2f}",
#     )
#     ax.axvline(
#         mean + std,
#         color="orange",
#         linestyle="dashed",
#         linewidth=1,
#         label=f"Avg + Std Dev: {mean + std:.2f}",
#     )
#     ax.axvline(
#         mean - std,
#         color="yellow",
#         linestyle="dashed",
#         linewidth=1,
#         label=f"Avg - Std Dev: {mean - std:.2f}",
#     )
#     ax.legend()


def add_mean_std_lines(ax, data, color="orange"):
    mean = np.mean(data)
    std = np.std(data)
    ax.axvline(
        mean, color="red", linestyle="dashed", linewidth=1, label=f"Average: {mean:.2f}"
    )
    ax.axvline(
        mean + std,
        color=color,
        linestyle="dashed",
        linewidth=1,
        label=f"+/- 1 Std Dev: {std:.2f}",
    )
    ax.axvline(mean - std, color=color, linestyle="dashed", linewidth=1)
    ax.legend()


def plot_histogram(ax, data, bins, title, x_label):
    count, bins, ignored = ax.hist(
        data, bins=bins, alpha=0.7, color="blue", edgecolor="black"
    )
    add_mean_std_lines(ax, data)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel("Games")


def get_metrics():
    players = [TwoPlayer("Player1"), TwoPlayer("Player2")]
    game = QwixxGame(players)
    winning_name, winning_score = game.run()

    player1_scores = players[0].scores
    player2_scores = players[1].scores

    uncertainty_score = calculate_uncertainty(player1_scores, player2_scores)
    print("uncertainty_score", uncertainty_score)
    lead_changes = count_lead_changes(player1_scores, player2_scores)
    print("lead_changes", lead_changes)
    drama = calculate_drama(player1_scores, player2_scores)
    # drama2 = calculate_drama1(player1_scores, player2_scores)
    print("drama", drama)
    # print("drama2", drama2)

    duration = test_duration(players[0].n_moves, players[1].n_moves)
    completion = test_completion(player1_scores, player2_scores)
    # plot_uncertainty(player1_scores, player2_scores)

    return uncertainty_score, lead_changes, drama, duration, completion, winning_score


def count_lead_changes(player1_score, player2_score):
    lead_changes = 0
    current_leader = None

    for score1, score2 in zip(player1_score, player2_score):
        if score1 > score2:
            new_leader = "player1"
        elif score2 > score1:
            new_leader = "player2"
        else:
            new_leader = "tie"

        if current_leader and new_leader != current_leader and new_leader != "tie":
            lead_changes += 1

        current_leader = new_leader

    return lead_changes


def test_lead_change(player1_scores, player2_scores):
    return count_lead_changes(player1_scores, player2_scores)


def test_killer_moves():
    pass


def test_completion(player1_scores, player2_scores):
    if player1_scores[-1] == player2_scores[-1]:
        return 1
    return 0

    # change code around to say that if there is a tie, return something else


def test_duration(player1_n_moves, player2_n_moves):
    return player1_n_moves + player2_n_moves


# def calculate_drama(player1_score, player2_score):
#     # find area that the winning player was losing
#     pass


def test_drama():
    # find area that the winning player was losing
    pass


def calculate_drama(player1_scores, player2_scores):
    # Convert lists to numpy arrays if necessary
    player1_scores = np.array(player1_scores)
    player2_scores = np.array(player2_scores)

    # Determining the eventual winner and loser
    if player1_scores[-1] > player2_scores[-1]:
        E_w = player1_scores
        E_l = player2_scores
    else:
        E_w = player2_scores
        E_l = player1_scores

    # Initialize sum of severity for losing positions
    sum_severity_losing_positions = 0
    # Initialize count of losing positions
    count_losing_positions = 0

    # Go through each move to calculate the parts of the drama index
    for n in range(len(E_w)):
        if E_w[n] < E_l[n]:  # Check if the winner is in a losing position at move n
            sum_severity_losing_positions += np.sqrt(E_l[n] - E_w[n])
            count_losing_positions += 1

    # Calculate the drama index
    A_dram = (
        sum_severity_losing_positions / count_losing_positions
        if count_losing_positions != 0
        else 0
    )

    if A_dram == 0:
        return 1

    return A_dram


# def calculate_drama(player1_scores, player2_scores):
#     # Determining the eventual winner and loser
#     if player1_scores[-1] > player2_scores[-1]:
#         winner = player1_scores
#         loser = player2_scores
#     else:
#         winner = player2_scores
#         loser = player1_scores

#     winner = np.array(winner)
#     loser = np.array(loser)

#     # Calculating the number of moves where the eventual winner was in a losing position
#     losing_positions = winner < loser
#     count_losing_positions = np.sum(losing_positions)

#     # Calculating the severity of each losing position
#     severity_of_positions = np.sqrt(np.abs(winner - loser)) * losing_positions

#     # Calculating the drama score
#     A_dram = (
#         np.sum(severity_of_positions) / count_losing_positions
#         if count_losing_positions != 0
#         else 0
#     )

#     return A_dram


def calculate_drama1(player1_scores, player2_scores):
    if len(player1_scores) != len(player2_scores):
        raise ValueError("Both player scores must have the same length.")

    if player1_scores[-1] > player2_scores[-1]:
        winning_scores = player1_scores
        losing_scores = player2_scores
    else:
        winning_scores = player2_scores
        losing_scores = player1_scores

    lead_history = np.array(winning_scores) - np.array(losing_scores)

    total_negatives = 0
    num_negatives = 0

    for points in lead_history:
        if points < 0:
            total_negatives += points
            num_negatives += 1

    # Define the interpolation line to intersect the winning player's last point

    # total = 0
    # for i in range(len(lead_history)):
    #     total += estimated_lead_values[i] - lead_history[i]

    return total_negatives


if __name__ == "__main__":
    # test_two_player()
    # get_metrics()
    get_metrics_for_n_games(10000)
