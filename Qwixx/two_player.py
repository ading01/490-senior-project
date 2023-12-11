from qwixx import Player


class TwoPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    
    def roll_dice(self, game):
         game.roll_dice()

    def make_color_move(self, game):
        game.make_color_move(self.name)

    def get_min_score_diff(self, game):
        min_score_diff = 2000
        for player in game.players:
            if player.name != self.name:
                score_diff = player.score - self.score
                if score_diff < min_score_diff:
                    min_score_diff = score_diff
        return min_score_diff

    def get_best_move(self, cells, absorb_strike_threshold):
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
        if max_dist > absorb_strike_threshold:
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

    def make_color_move(self, game):
        min_score_diff = self.get_min_score_diff(game)
        if min_score_diff < 0:
            winning = True
        else:
            winning = False
        
        if winning and min_score_diff < -20:
            game.make_color_move(self.name)
            
        
        
    
