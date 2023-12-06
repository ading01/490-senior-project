import json
import math
import random
import sys
import time
from datetime import datetime
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
import pygame

HUMAN_TEST = False

# Initialize Pygame
pygame.init()
FONT = pygame.font.Font(None, 36)
INSTRUCTION_FONT = pygame.font.Font(None, 40)

CPU_WAIT_TIME = 0



DO_DRAW = False

# Constants for screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 800

if HUMAN_TEST:
    DO_DRAW = True
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Two Player Game Example")

if DO_DRAW:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Two Player Game Example")



CONSERVATIVE_THRESHOLD = 0
ABSORB_STRIKE_THRESHOLD = 10

PRINT_STUFF = False

# Color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 255)
GREY = (200, 200, 200)
HIGHLIGHT_GREY = (100, 100, 100)
SELECTED_BORDER_COLOR = (0, 0, 0) 

DICE_HEIGHT = 100
DICE_WIDTH = 100

CELL_HEIGHT = 40
CELL_WIDTH = 40 
SPACE_BETWEEN_CELLS = CELL_HEIGHT + 10
ROW_WIDTH = 850
ROW_HEIGHT = 60

    



# Create the main game window
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Two Player Game Example")

# Create cards for the players
player1_card = pygame.Surface((600, 300))
player1_card.fill(GREY)

player2_card = pygame.Surface((600, 300))
player2_card.fill(GREY)

# Create separate game screens (surfaces) for each player
player1_screen = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT))
player2_screen = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT))

# Define background colors for player screens
PLAYER1_COLOR = (255, 0, 0)  # Red
PLAYER2_COLOR = (0, 0, 255)  # Blue

SCORE_MAP = {
    0: 0,
    1: 1,
    2: 3,
    3: 6,
    4: 10,
    5: 15,
    6: 21,
    7: 28,
    8: 36,
    9: 45,
    10: 55,
    11: 66,
    12: 78,
}

class InvalidDeactivate(Exception):
    def __init__(self, message="This cell cannot be selected. Please select again."):
        self.message = message
        super().__init__(self.message)

class InadequateChecks(Exception):
    def __init__(self, message="You are unable to select this cell. You need to have at least 5 checked boxes in this row"):
        self.message = message
        super().__init__(self.message)


class GameState(Enum):
    ROLL_DICE = 1
    OPTIONAL_SELECTION = 2
    COLOR_SELECTION = 3
    GAME_OVER = 4




class Die: 
    def __init__(self, die_id, color, sides=6):
        self.die_id = die_id
        self.sides = sides
        self.color = color
        self.value = None
        self.x_cord = None
        self.y_cord = None

    def roll(self):
        self.value = random.randint(1, self.sides)

    def get_value(self):
        return self.value
    
    def get_color(self):
        return self.color
    
    def get_die_id(self):
        return self.die_id

    def set_x_cord(self, x_cord):
        self.x_cord = x_cord

    def get_x_cord(self, ):
        return self.x_cord
    
    def set_y_cord(self, y_cord):
        self.y_cord = y_cord

    def get_y_cord(self):
        return self.y_cord

class Player:
    def __init__(self, name):
        self.name = name
        self.qwixx_card = QwixxCard(name)
        self.player_surface = None
        self.is_made_move = False
        self.scores = [0]
    
    def record_score(self):
        self.scores.append(self.qwixx_card.score)
    
    def get_player_score(self):
        return self.qwixx_card.score
    
    def get_card(self):
        return self.qwixx_card
    
    def player_select_cell(self, cell):
        self.qwixx_card.selected_cell = cell

    def set_player_surface(self, width, height, color):
        self.player_surface = pygame.Surface((width, height))
        self.player_surface.fill(color)

    def get_player_surface(self):
        play_card_surface = self.qwixx_card.get_play_card_surface()
        self.player_surface.blit(play_card_surface, (90, 200))
        return self.player_surface
    
    def roll_dice(self, game):
        pass

    def make_color_move(self, game):
        pass

    def make_optional_move(self, game):
        pass


    



class HumanPlayer(Player):
    def __init__(self, name):
        self.name = name
        self.qwixx_card = QwixxCard(name)
        self.player_screen = None
        self.is_made_move = False

    def roll_dice(self, game):
        making_move = True
        while making_move:
            for event in pygame.event.get():
                if game.game_state == GameState.ROLL_DICE:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game.roll_dice()
                            game.draw_game()
                            making_move = False        

    def make_color_move(self, game):

        making_move = True
        game.selected_dice = [None, None]
        game.draw_game()
        # print(game.get_state())

        while making_move:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if game.dice_hit_boxes:
                        for hit_box, die_id in game.dice_hit_boxes:
                            if hit_box.collidepoint(x, y):
                                game.select_die(die_id)
                                if None not in game.selected_dice:
                                    self.qwixx_card.select_valid_cells(game.dice[game.selected_dice[0]], game.dice[game.selected_dice[1]])
                                game.draw_game()
                    if self.qwixx_card.cell_hit_boxes:
                        for hit_box, cell in self.qwixx_card.cell_hit_boxes:
                            if hit_box.collidepoint(x, y):
                                # my_print("row column", cell.row, cell.column)
                                self.qwixx_card.selected_cell = cell  # Update selected_cell with coordinates
                                game.draw_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.qwixx_card.selected_cell and self.qwixx_card.selected_cell in self.qwixx_card.valid_cells:
                            try:
                                self.qwixx_card.cross_out_cell()
                                self.qwixx_card.selected_cell = None
                                self.qwixx_card.valid_cells = []
                                self.is_made_move = True
                                game.selected_dice = [None, None]
                                making_move = False
                            except InvalidDeactivate as e:
                                my_print(f"CustomError: {e}")
                                game.warning_text = "WARNING"
                            except InadequateChecks as e:
                                my_print(f"CustomError: {e}")
                                return False
                            game.draw_game()
                    elif event.key == pygame.K_SPACE:
                        making_move = False
        
    def make_optional_move(self, game):
        

        making_move = True
        card = self.qwixx_card
        # print(game.get_state())
        while making_move:
            for event in pygame.event.get():
                # on mouseclick - select cell
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.qwixx_card.cell_hit_boxes:
                        for hit_box, cell in card.cell_hit_boxes:
                            if hit_box.collidepoint(x, y):
                                my_print("row column", cell.row, cell.column)
                                self.qwixx_card.selected_cell = cell  # Update selected_cell with coordinates
                                game.draw_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.qwixx_card.selected_cell and self.qwixx_card.selected_cell in self.qwixx_card.valid_cells:
                            try:
                                self.qwixx_card.cross_out_cell()
                                self.is_made_move = True
                                making_move = False
                            except InvalidDeactivate as e:
                                my_print(f"CustomError: {e}")
                                print("invalid deactivte")
                                self.qwixx_card.warning_text = "WARNING"
                            except InadequateChecks as e:
                                print("inadeqeut checks")
                                my_print(f"CustomError: {e}")
                                return False
                            game.draw_game()

                            # making_move = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        making_move = False


class AgentPlayer(Player):
    def __init__(self, name):
        self.name = name
        self.qwixx_card = QwixxCard(name)
        self.player_screen = None
        self.is_made_move = False
    
    def roll_dice(self, game):
        game.roll_dice()
    
    def get_state(self, game):
        state = game.get_state()
        return state

    def make_color_move(self, game):
        pass

    def make_optional_move(self, game):
        pass
    

    
class HeuristicPlayer(Player):
    def __init__(self, name):
        self.name = name
        self.qwixx_card = QwixxCard(name)
        self.is_made_move = False
        self.scores = []

    def get_card(self):
        return self.qwixx_card
    
    def roll_dice(self, game):
        game.roll_dice()

    def distance_from_prev_crossed_out_cell(self, cell):
        board = self.qwixx_card.board
        row = cell.row
        for box in board[row].cells:
            if box.is_active:
                return cell.column - box.column
        
        return 100

    def player_select_cell(self, cell):
        self.qwixx_card.selected_cell = cell

            
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

        best_move = self.get_best_move(candidates)

        if best_move is None:
            my_print("1: No best color move in color")
            time.sleep(CPU_WAIT_TIME)
            return
        
        if self.is_made_move:
            if best_move[1] < (CONSERVATIVE_THRESHOLD + 1):
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

    def get_best_move(self, cells):
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
        if max_dist > ABSORB_STRIKE_THRESHOLD:
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
        
        best_optional_choice = self.get_best_move(optional_cells)

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

            best_colored_choice = self.get_best_move(colored_cells)
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
            if best_optional_choice[1] < (CONSERVATIVE_THRESHOLD + 1):
                my_print("making optional move")
                try:
                    self.qwixx_card.selected_cell = best_optional_choice[0]
                    self.qwixx_card.cross_out_cell()
                    game.record_scores()
                except InadequateChecks:
                    return
                finally:
                    time.sleep(CPU_WAIT_TIME)
                    
class Cell:
    def __init__(self, number, row, column, rgb, color, x_cord, y_cord):
        self.number = number
        self.row = row
        self.column = column
        self.x = x_cord
        self.y = y_cord
        self.rgb = rgb
        self.color = color # "green", "red"
        self.is_active = True
        self.crossed_out = False
    
    def __str__(self):
        return f"Cell {self.number} - Color: {self.color}, Coordinates: ({self.row}, {self.column}), is active? {self.is_active}"

    
    def draw_cell(self, screen):
        # cell = pygame.Surface((CELL_HEIGHT, CELL_WIDTH))
        pygame.draw.rect(screen, self.rgb, (self.x + 10, self.y, CELL_WIDTH, CELL_HEIGHT))
        # pygame.draw.rect(screen, self.rgb, (self.x, self.y, 60, 40))
        number = FONT.render(str(self.number), True, BLACK)
        if self.crossed_out:
            number = FONT.render("X", True, BLACK)
        
        screen.blit(number, (self.x + 20, self.y + 5))
        hit_box = pygame.Rect(self.x, self.y, CELL_WIDTH, CELL_HEIGHT)
        return hit_box

    
    
    def set_is_active(self, value):
        self.is_active = value
    
    def is_active(self):
        return self.is_active
    
    def get_coordinates(self):
        return self.x, self.y
    
    def deactivate(self):
        if self.is_active:
            self.is_active = False
            new_rgb = (180 if self.rgb[0] == 255 else 0,
                        180 if self.rgb[1] == 255 else 0,
                        180 if self.rgb[2] == 255 else 0)
            self.rgb = new_rgb

    # def draw_cell(self, screen):
    #     # for i in range(12):
    #     pygame.draw.rect(screen, self.rgb, (self.x, self.y, 60, 40))
    #     text = FONT.render(str(self.number), True, BLACK)
    #     screen.blit(text, (self.x + 20, self.y + 5))
    #     hit_box = pygame.Rect(self.x, self.y, 60, 40)
    #     return (hit_box, self.x, self.y, self.row, self.column) # Include row index (i) in the hit box data




class Row:
    def __init__(self, rgb, string_color, row_number, row_start_index, row_end_index, x_cord, y_cord, reverse):
        self.rgb = rgb
        self.string_color = string_color
        self.number_of_checks = 0
        self.x = x_cord
        self.y = y_cord
        self.is_locked = False
        self.cell_objects = {cell_index: Cell(value, row_number, cell_index, rgb, string_color, x_cord + SPACE_BETWEEN_CELLS * cell_index, y_cord) for cell_index, value in enumerate(range(row_start_index, row_end_index, reverse))}
        self.cells = list(self.cell_objects.values())
        # self.cell_objects = {number: Cell(number, row_number, i, rgb, color, x + (70 * i), y) for i, number in enumerate(range(row_start_index, row_end_index, reverse))}
        
    def display_row(self, screen):
        row = pygame.Surface((ROW_WIDTH, ROW_HEIGHT))
        row.fill(WHITE)
        screen.blit(row, (self.x, self.y))
        cells = []
        for i, cell in enumerate(self.cells):
            cell_hit_box = pygame.Rect(cell.x + 100, cell.y + 200, CELL_WIDTH, CELL_HEIGHT)
            cell.draw_cell(screen)
            cells.append((cell_hit_box, cell))
        return cells
    
    def is_mouse_over_cell(self, x, y):
        for cell in self.cells:
            cell_x, cell_y = cell.get_coordinates()
            if cell_x <= x <= cell_x + CELL_WIDTH and cell_y <= y <= cell_y + CELL_HEIGHT:
                return cell
        return None

        # hit_boxes = []
        # pygame.draw.rect(screen, WHITE, (self.x - 5, self.y - 5, 850, 70))
        # for cell in self.cells:
            
        #     screen.blit(cell.draw_cell(), cell.x, cell.y)

        # if self.is_locked:
        #     new_rgb = (180 if self.rgb[0] == 255 else 0,
        #                 180 if self.rgb[1] == 255 else 0,
        #                 180 if self.rgb[2] == 255 else 0)
        #     pygame.draw.rect(screen, new_rgb, (self.x + 780, self.y , 60, 40))
        # else:
        #     pygame.draw.rect(screen, self.rgb, (self.x + 780, self.y , 60, 40))

        # for cell in self.cells:
        #     hit_boxes.append(cell.draw_cell(screen))
        # return hit_boxes
    
    def deactivate_trailing_cells(self, index):
        if self.cells[index].is_active:

            if index == 10 and self.number_of_checks < 5:
                raise InadequateChecks()
            else:
                self.cells[index].crossed_out = True
                if index == len(self.cells) - 1:
                    self.is_locked = True
                    self.number_of_checks += 1
                self.number_of_checks += 1
                for i in range(index + 1):
                    self.cells[i].deactivate()
        else:
            raise InvalidDeactivate()
        

class QwixxCard:
    def __init__(self, player_name):
        self.player_name = player_name
        self.play_card = pygame.Surface((600, 300))
        self.board = self.initalize_board()
        self.score = 0
        self.strikes = 0
        self.selected_cell = None
        self.cell_hit_boxes = []
        self.valid_cells = []
        self.player_offset = None
        # Initialize the card's state (rows and crosses)

    def get_cell_by_x_y(self, row, column):
        row = self.board[row]
        cell = row.cells[column]
        return cell

    def get_right_most_crossed_off_box_in_row(self, row):
        for i, cell in enumerate(row.cells):
            if cell.is_active:
                return i
        return 10
        
    def cross_out_cell(self):
        # multiplier = 1
        reward = 0
        inital_score = self.calculate_score()
        for row in self.board:
            for cell in row.cells:
                if self.selected_cell == cell:
                    curr_row = cell.row
                    r_index = self.get_right_most_crossed_off_box_in_row(self.board[curr_row])
                    index = cell.column
                    
                    reward = (10 - index - r_index) / 10
                    
                    # print("reward, index", reward, index)
                    # multiplier = 11 - index
                    my_print("deactiviating index:", index)
                    self.board[curr_row].deactivate_trailing_cells(index)
        if HUMAN_TEST:
            print(f"{self.player_name}crossed out cell: ", self.selected_cell.row, self.selected_cell.column, self.selected_cell.number)
        
        # if self.is_game_over():
        #     return 30
        
        final_score = self.calculate_score()


        # check if game ended and if won or lost
        # print("reward", reward)
        return reward
        # return final_score - inital_score 

    def select_valid_cells(self, dice1, dice2):
        total = dice1.get_value() + dice2.get_value()
        color = dice2.get_color()

        for row in self.board:
            for cell in row.cells:
                if color == "white":
                    if cell.number == total:
                        self.valid_cells.append(cell)
                else:
                    if cell.number == total and color == cell.color:
                            self.valid_cells = [cell]

    def initalize_board(self):
        board = []
        color_text = ["red", "yellow", "green", "blue"]
        row_colors = [RED, YELLOW, GREEN, BLUE]
        for i in range(len(row_colors)):
            if (i < 2):
                # color, index, start_index, end_index, x, y, reverse
                board.append(Row(row_colors[i], color_text[i], i,  2, 13, 0, 50 + i * SPACE_BETWEEN_CELLS, 1))
            else:
                board.append(Row(row_colors[i], color_text[i], i, 12, 1,  0, 50 + i * SPACE_BETWEEN_CELLS, -1))
        return board
    
    def is_game_over(self):
        if self.strikes >= 4:
            return True
        
        # if two of the rows are locked
        # locked_rows = 0
        # for row in self.board:
        #     if row.is_locked:
        #         locked_rows += 1
        # if locked_rows >= 2:
        #     return True
        return False

    def draw_selected_border(self, surface, selected_color):
        if self.selected_cell is not None:
            cell = self.selected_cell
            x = cell.x 
            y = cell.y 
            border_thickness = 4  # Adjust border thickness as needed
            pygame.draw.rect(surface, selected_color, (x - border_thickness, y - border_thickness, CELL_WIDTH + (2*border_thickness), CELL_HEIGHT + (2*border_thickness)), border_thickness)
    
    def draw_border(self, surface, cell):
        x, y = cell.get_coordinates()
        x = x + 10
        border_thickness = 4
        pygame.draw.rect(surface, GREY, (x - border_thickness, y - border_thickness, CELL_WIDTH + (2*border_thickness), CELL_HEIGHT + (2*border_thickness)), border_thickness)

    def highlight_valid_cells(self, surface):
        if self.valid_cells:
            for cell in self.valid_cells:
                self.draw_border(surface, cell)

    def get_play_card_surface(self):
        self.play_card.fill(GREY)
        score_text = f"Score: {self.calculate_score()}"
        score_label = FONT.render(score_text, True, BLACK)
        strike_text = f"Strikes: {self.strikes}"
        strike_label = FONT.render(strike_text, True, BLACK)
        player_label = FONT.render(f"Player: {self.player_name}", True, BLACK)
        
        cell_hit_boxes = []
        for row in self.board:
            hit_boxes = row.display_row(self.play_card)
            hit_boxes = list(map(lambda hit_box: (hit_box[0].move(self.player_offset, 0), hit_box[1]), hit_boxes))
            cell_hit_boxes.extend(hit_boxes)

        self.highlight_valid_cells(self.play_card)
        
        if self.selected_cell is not None:
            self.draw_selected_border(self.play_card, BLACK)
        self.play_card.blit(score_label, (0, 0))
        self.play_card.blit(strike_label, (0, 20))
        self.play_card.blit(player_label, (0, 270))

        self.cell_hit_boxes = cell_hit_boxes
        return self.play_card
        
    def calculate_score(self):
        # Calculate and return the player's score based on the card's state
        total = 0
        for row in self.board:
            total += SCORE_MAP[row.number_of_checks]

        total = total - (self.strikes * 5)
        self.score = total
        return total

class QwixxGame:
    def __init__(self, players):
        self.players = players
        self.active_player = 0  # Index of the active player
        self.moving_player = 0
        # self.state = GameState.ROLL_DICE
        self.dice_objects = {
            0: Die(0, "white", 6),
            1: Die(1, "white", 6),
            2: Die(2, "red", 6),
            3: Die(3, "yellow", 6), 
            4: Die(4, "green", 6),
            5: Die(5, "blue", 6),
        }
        self.dice = list(self.dice_objects.values())
        # self.dice = [0, 0, 0, 0, 0, 0]  # Six-sided dice
        self.game_state = GameState.ROLL_DICE
        self.dice_hit_boxes = []
        self.selected_dice = [None, None]
        self.selected_cell = None
        self.instruction_text = "Press SPACEBAR to roll dice"
        self.warning_text = ""
        self.game_state_text = ""
        self.winner_text = None

        # Create player screens once during initialization
        self.player1_screen = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200))
        self.player2_screen = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200))
        self.player1_screen.fill(PLAYER1_COLOR)
        self.player2_screen.fill(PLAYER2_COLOR)

    def get_state(self):
        state = {
            "active_player": self.active_player,
            "game_state": self.game_state, # this should be an ENUM of either 1 or 2, but
            # will probably be adjusted to be one-indexed (i.e. 0 or 1)
            "already_moved": self.players[self.moving_player].is_made_move,
            "valid_cells": self.get_valid_cells(),
            "num_crossed_out_cells": self.get_num_crossed_out_cells(),
            "selectable_cells": self.get_selectable_cells(),
            "strikes": self.players[self.moving_player].qwixx_card.strikes, 
            "locked_rows": self.get_locked_rows(),
            "player_score": self.players[1].get_player_score(),
            "opponent_score": self.players[0].get_player_score()

        }
        # json_state = json.dumps(state, indent=4)

        return state

    
    def get_locked_rows(self):
        locked_rows = 0
        for row in self.players[self.moving_player].get_card().board:
            if row.is_locked:
                locked_rows += 1
        return locked_rows
    
    def get_num_crossed_out_cells(self):
        res = []
        board = self.players[self.moving_player].get_card().board

        for row in board:
            res.append(row.number_of_checks)
        
        return res

    def get_valid_cells(self):
        board = []
        for row in self.players[self.moving_player].qwixx_card.board:
            r = []
            for cell in row.cells:
                if not cell.is_active:
                    r.append(1)
                else:
                    r.append(0) 
            board.append(r)
        return board

    def get_selectable_cells(self):
        board = [[0 for i in range(11)] for i in range(4)]
        valid_cells = self.players[self.moving_player].get_card().valid_cells
        for cell in valid_cells:
            board[cell.row][cell.column] = 1
        return board

    def roll_dice(self):
        for die in self.dice:
            die.roll()

    def select_die(self, die_id):
        # self.selected_dice = [self.selected_white_die, self.selected_color_die]
        for i in range(2):
            if self.selected_dice[i] == die_id:
                self.selected_dice[i] = None
                return
        if die_id < 2: 
            self.selected_dice[0] = die_id
        elif die_id >= 2:
            self.selected_dice[1] = die_id
        return

    def draw_cards(self):
        for i, player in enumerate(self.players):
            player_surface = player.get_player_surface()
            screen.blit(player_surface, ((SCREEN_WIDTH // 2) * i, 0))

    def draw_dice(self, screen):
        dice_screen = pygame.Surface((SCREEN_WIDTH, 200))
        dice_screen.fill(GREY)

        dice_hit_boxes = []
        for die in self.dice:
            if die.get_value() is not None:
                image_path = f"die_images/{die.get_color()}/dice_{die.get_color()}_{die.get_value()}.png"
                image = pygame.image.load(image_path)
                resized_image = pygame.transform.scale(image, (DICE_WIDTH, DICE_HEIGHT))
                x = 400 + die.get_die_id() * 150
                y = 50
                dice_screen.blit(resized_image, (x, y))
               
                if die.get_die_id() in self.selected_dice:
                    # Draw a border around selected dice
                    self.draw_selected_border(dice_screen, SELECTED_BORDER_COLOR, x, y, DICE_WIDTH, DICE_HEIGHT)    

                # hit box 
                dice_hit_box = pygame.Rect(400 + die.get_die_id() * 150, 650, DICE_WIDTH, DICE_HEIGHT)
                dice_hit_boxes.append((dice_hit_box, die.die_id))
        screen.blit(dice_screen, (0, SCREEN_HEIGHT - 200))
        return dice_hit_boxes

    def is_game_over(self):
        for player in self.players:
            if player.qwixx_card.is_game_over():
                return True
        return False
    
    
    def change_active_player(self):
        self.active_player = 1 - self.active_player

    def draw_selected_border(self, surface, selected_color, x, y, width, height):
        border_thickness = 4  # Adjust border thickness as needed
        pygame.draw.rect(surface, selected_color, (x - border_thickness, y - border_thickness, width + (2*border_thickness) , height + (2*border_thickness)), border_thickness)
    
    def draw_game(self):
        if DO_DRAW:
            # return
            # display active player name
            self.draw_cards()
            self.dice_hit_boxes = self.draw_dice(screen)
            active_player_text = f"The active player is player number {str(self.active_player)}, {self.players[self.active_player].name}"
            active_player_label = FONT.render(active_player_text, True, BLACK)
            
            moving_player_text = f"The moving player is player number {str(self.moving_player)}, {self.players[self.moving_player].name}"
            moving_player_label = FONT.render(moving_player_text, True, BLACK)
            
            instruction_label = INSTRUCTION_FONT.render("INSTRUCTION: " + self.instruction_text, True, BLACK, WHITE)
            
            warning_label = FONT.render(self.warning_text, True, BLACK)

            game_state_label = FONT.render(f"STAGE: {self.game_state_text}", True, BLACK)
            

            screen.blit(game_state_label, (50,80))
            screen.blit(active_player_label, (0, 0))
            screen.blit(moving_player_label, (0, 20))
            screen.blit(instruction_label, (0, 45))
            screen.blit(warning_label, (0, 60))
            if self.winner_text:
                winner_label = FONT.render(f"WINNER: {self.winner_text}", True, BLACK)
                screen.blit(winner_label, (100, 160))
            

            # self.change_player_button.draw(screen)
            pygame.display.flip()
        else:
            return
    
    def record_scores(self):
        for player in self.players:
            player.record_score()

    def run(self):
        start_time = datetime.now()
        # Game loop
        running = True
        redraw = True

        
        player_colors = [RED, BLUE, GREEN, YELLOW]

        for i in range(len(self.players)):
            self.players[i].set_player_surface(SCREEN_WIDTH // len(self.players), SCREEN_HEIGHT - 200, player_colors[i])
            self.players[i].qwixx_card.player_offset = ((SCREEN_WIDTH // 2) * i)
        
    
        active_player = self.players[self.active_player]
        while running:
                 
            # if not self.is_game_over():
            if self.game_state == GameState.ROLL_DICE:

                self.moving_player = self.active_player
                self.instruction_text = "Press SPACEBAR to roll dice"
                self.game_state_text = "Dice rolling"
                self.draw_game()
                active_player = self.players[self.active_player]
                active_player.roll_dice(self)
                self.game_state = GameState.OPTIONAL_SELECTION
            elif self.game_state == GameState.OPTIONAL_SELECTION:
                self.instruction_text = "Click valid cell. Press RETURN to confirm. Press SPACEBAR to skip."
                self.game_state_text = "Optional selection"
                self.draw_game()
                
                for i in range(self.active_player, len(self.players)):
                    self.moving_player = i
                    player = self.players[i]
                    self.selected_dice = [0, 1]
                    card = player.qwixx_card
                    card.select_valid_cells(self.dice[0], self.dice[1])
                    self.draw_game()
                    
                    # card = active_player = self.players[self.active_player].qwixx_card
                    # card.select_valid_cells(game.dice[0], game.dice[1])

                    player.make_optional_move(self)
                    player.qwixx_card.selected_cell = None
                    player.qwixx_card.valid_cells = []
                for i in range(0, self.active_player):
                    self.moving_player = i
                    player = self.players[i]
                    self.selected_dice = [0, 1]
                    card = player.qwixx_card
                    card.select_valid_cells(self.dice[0], self.dice[1])
                    self.draw_game()
                    player.make_optional_move(self)
                    player.qwixx_card.selected_cell = None
                    player.qwixx_card.valid_cells = []
                self.game_state = GameState.COLOR_SELECTION
                self.moving_player = self.active_player
                self.draw_game()
            elif self.game_state == GameState.COLOR_SELECTION:
                self.game_state_text = "Color selection"
                self.draw_game()
                active_player = self.players[self.active_player]


                active_player.make_color_move(self)
                active_player.qwixx_card.selected_cell = None
                active_player.qwixx_card.valid_cells = []

                if not active_player.is_made_move:
                    active_player.qwixx_card.strikes += 1
                self.game_state = GameState.ROLL_DICE
                for player in self.players:
                    player.is_made_move = False
                self.change_active_player()
                if self.is_game_over():
                    self.game_state = GameState.GAME_OVER
            elif self.game_state == GameState.GAME_OVER:
                max_score = -100
                winner = None
                for player in self.players:
                    if player.qwixx_card.calculate_score() > max_score:
                        winner = player
                        max_score = player.qwixx_card.calculate_score()
                self.winner_text = winner.name
                end_time = datetime.now()
                time_diff = end_time - start_time
                # print("total time", time_diff, "winner:", winner.name, max_score)
                running = False
                if redraw: 
                    self.draw_game()
                    redraw = True
                    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        # Quit Pygame
        # pygame.quit()
        return winner.name, max_score
        # sys.exit()

def my_print(text, *args):
    if PRINT_STUFF:
        print(text, args)

def test_parameters():
    for i in range(11):
        CONSERVATIVE_THRESHOLD = i
        test_heuristic_player()
    CONSERVATIVE_THRESHOLD = 4 
    for i in range(11):
        ABSORB_STRIKE_THRESHOLD = i
        test_heuristic_player()   


def test_heuristic_player():
    n_test_games = 1000
    scores = []

    for _ in range(n_test_games):
        players = [HeuristicPlayer("Allan"), HeuristicPlayer("robot2")]
        game = QwixxGame(players)
        game.run()
        scores.append(players[0].get_player_score())
        scores.append(players[1].get_player_score())


    average_score = np.mean(scores)
    std_deviation = np.std(scores)
    print(CONSERVATIVE_THRESHOLD)
    print("Average Score:", average_score)
    print("Standard Deviation:", std_deviation)

    # Plotting
    # plt.figure(figsize=(8, 6))
    # plt.hist(scores, bins=30, color='blue', alpha=0.7, edgecolor='black')
    # plt.axvline(average_score, color='red', linestyle='dashed', linewidth=2, label='Average Score')
    # plt.axvline(average_score + std_deviation, color='orange', linestyle='dashed', linewidth=2, label='Avg + Std Dev')
    # plt.axvline(average_score - std_deviation, color='orange', linestyle='dashed', linewidth=2, label='Avg - Std Dev')

    # # Annotate the average score and standard deviations
    # plt.text(average_score, 30, f'Avg: {average_score:.2f}', color='red', ha='center')
    # plt.text(average_score + std_deviation, 25, f'Avg + Std Dev: {average_score + std_deviation:.2f}', color='orange', ha='center')
    # plt.text(average_score - std_deviation, 25, f'Avg - Std Dev: {average_score - std_deviation:.2f}', color='orange', ha='center')

    # plt.title(f'Distribution of Heuristic CPU Scores\nConservative threshold: {CONSERVATIVE_THRESHOLD}; Absorbing strike threshold: {ABSORB_STRIKE_THRESHOLD}')

    # plt.xlabel('Total Score')
    # plt.ylabel('Frequency')
    # plt.legend()
    # plt.show()



        
def calculate_uncertainty(player1_scores, player2_scores, M=100):
    # Ensure the lists are of the same length
    if len(player1_scores) != len(player2_scores):
        raise ValueError("Both player1_scores and player2_scores must have the same length.")

    # Calculate the lead history (score difference)
    lead_history = np.array(player1_scores) - np.array(player2_scores)

    # Define the interpolation line points
    interpolation_line = [(0, 0), (M, 1)]

    # Calculate the slope and intercept of the interpolation line
    slope = (interpolation_line[1][1] - interpolation_line[0][1]) / (interpolation_line[1][0] - interpolation_line[0][0])
    intercept = interpolation_line[0][1] - slope * interpolation_line[0][0]

    # Calculate the estimated lead values at each time point
    estimated_lead_values = np.linspace(0, M, len(player1_scores)) * slope + intercept

    # Calculate the distance between the lead history and the interpolation line
    distances = np.abs(lead_history - estimated_lead_values)

    # Calculate the average distance
    average_distance = np.mean(distances)

    return average_distance

def find_area(score_diff, slope):
    total = 0
    for i, score_d in enumerate(score_diff):
        y = i * slope
        total += y - score_d
    return total

def test_uncertainty():
    players = [HeuristicPlayer("Allan"), HeuristicPlayer("robot2")]
    game = QwixxGame(players)
    game.run()

    player1_scores = players[0].scores
    player2_scores = players[1].scores

    print("len", len(player1_scores))
    print("p1, p2 scores", player1_scores, player2_scores)

    uncertainty = calculate_uncertainty(player1_scores, player2_scores)

    time_points = range(1, len(player1_scores) + 1)

    # Plotting the scores
    plt.plot(time_points, player1_scores, label='Player 1', marker='o')
    plt.plot(time_points, player2_scores, label='Player 2', marker='o')

    score_difference = np.array(player1_scores) - np.array(player2_scores)
    plt.plot(time_points, score_difference, label='Score Difference (P1 - P2)', color='red', linestyle='--')    

    # Determine the slope of the grey line (assuming it starts at the origin)
    final_score_highest_player = max(player1_scores[-1], player2_scores[-1])
    slope = final_score_highest_player / len(player1_scores)

    # Plot the grey line from (0, 0) to the last point of the player with the higher score at the end
    plt.plot([0, len(player1_scores)], [0, final_score_highest_player], label='Line to Final Score (Highest Player)', linestyle='-', color='grey')

    # Plot the grey dotted lines from the red line to the grey line
    uncertainty_score = find_area(score_difference, slope)
    print("uncertainty_score", uncertainty_score)
    # for i, time_point in enumerate(time_points):
    #     y_on_grey_line = slope * time_point
    #     upper_limit = min(y_on_grey_line, score_difference[i])
    #     plt.plot([time_point, time_point], [score_difference[i], upper_limit], linestyle=':', color='grey')

    # Adding labels and a legend
    # plt.xlabel('Time')
    # plt.ylabel('Scores')
    # plt.title('Player Scores Over Time with Uncertainty and Line to Final Score')
    # plt.legend()

    # # Display the plot
    # plt.show()
    return uncertainty_score


def test_multiple_uncertainty():
    scores = []
    for i in range(10000):
        score = test_uncertainty()
        scores.append(score)

    average_score = sum(scores) / 10000
    variance = sum((x - average_score) ** 2 for x in scores) / 10000
    standard_deviation = math.sqrt(variance)

    return average_score, standard_deviation


if __name__ == "__main__":
    # players = [HumanPlayer("Allan"), HeuristicPlayer("robot2")]
    # game = QwixxGame(players)
    # game.run()
    # test_parameters()
    # test_heuristic_player()
    # test_uncertainty()
    print(test_multiple_uncertainty())

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
[8]: number_of_boxes_missed
[9]: will_action_result_in_lock
[10]: will_action_result_in_first_strike
[11]: will_action_result_in_second_strike
[12]: will_action_result_in_third_strike
[13]: will_action_result_in_fourth_strike
[14]: will_action_result_in_game_over
[15]: is_move_trying_to_lock
[16]: is_valid_action



total_cells_marked
score
strikes
"""