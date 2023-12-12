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

    def make_color_move(self, game):
        game.make_color_move(self.name)

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
                        if cell.is_active and cell.number == total and cell.color == color:
                            candidates.append(cell)
        return candidates

    def get_locking_moves(self, cells, board):
        candidates = []
        for cell in cells:
            if cell.is_active and cell.column == 10 and board[cell.row].number_of_checks >= 5:
                candidates.append(cell)
        return candidates


    def make_color_move(self, game):
        white_dice = game.dice[0:2]
        colored_dice = game.dice[2:6]
        candidates = []

        for white_die in white_dice:
            for colored_die in colored_dice:
                total = white_die.get_value() + colored_die.get_value()
                color = colored_die.get_color()
    
                for row in self.qwixx_card.board:
                    for cell in row.cells:
                        if cell.is_active and cell.number == total and cell.color == color:
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
        print("min score diff", min_score_diff)
        self_locked_rows = self.get_num_locked_rows()
        if self_locked_rows == 1 and min_score_diff <= 6 and len(locking_moves) > 0:
            print("locking move")
            return (locking_moves[0], -10)

        if self_locked_rows == 0 and min_score_diff <= 6 and len(locking_moves) > 0:
            print("locking move")
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
                            if cell.is_active and cell.number == total and cell.color == color:
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
    




if __name__ == "__main__":
    test_two_player()



        
        
            
            
        
        
    
