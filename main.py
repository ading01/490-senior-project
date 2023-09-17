



import pygame
import sys
import random
from enum import Enum


# Initialize Pygame
pygame.init()

class GameState(Enum):
    ROLL_DICE = 0
    # INSTRUCTIONS: PRESS DOWN ARROW TO ROLL DICE
    
    # OPTIONAL: USE THE VALUE OF THE TWO WHITE DICE TO SELECT A BOX
        #PROMPT THE USER THAT THEY ARE UNABLE TO SELECT A BOX
    # PRESS SPACE TO CONTINUE 
    OPTIONAL_SELECTION = 1

    # SELECT ONE OF THE WHITE DICE AND ONE OF THE COLORED DICE TO FILL
    # PROMPT THE USER THAT THEY HAVE BEEN AWARDED A STRIKE IF NECESSARY
    # PRESS SPACE TO CONTINUE
    COLOR_SELECTION = 2

    # CHECK NUM ROWS CHECKED OFF.
    # CHECK NUMBER OF STRIKES
    GAME_OVER = 3

# game states:
    # roll dices (active dice only)
    # choose optional two white dice
        # if yes, put into one of the rows if possible
    # check if any more numbers are crossed off.
    # choose a combination of one of the white and colored dice
        # see if you can cross off the box
    # check if any rows are crossed off

# Constants for colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)
HIGHLIGHT_GREY = (100, 100, 100)
SELECTED_BORDER_COLOR = (0, 0, 0)  # Green border color for selected dice

# DEACTIVATED_RED = (180, 0, 0)
# DEACTIVATED_YELLOW = (180, 180, 0)
# DEACTIVATED_GREEN = (0, 180, 0)
# DEACTIVATED_BLUE = (0, 0, 180)
class InvalidDeactivate(Exception):
    def __init__(self, message="This cell cannot be selected. Please select again."):
        self.message = message
        super().__init__(self.message)

class InadequateChecks(Exception):
    def __init__(self, message="You are unable to select this cell. You need to have at least 5 checked boxes in this row"):
        self.message = message
        super().__init__(self.message)


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


# Constants for screen dimensions and fonts
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
FONT = pygame.font.Font(None, 36)

class Die: 
    def __init__(self, die_id, color, sides=6):
        self.die_id = die_id
        self.sides = sides
        self.color = color
        self.value = None

    def roll(self):
        self.value = random.randint(1, self.sides)

    def get_value(self):
        return self.value
    
    def get_color(self):
        return self.color
    
    def get_die_id(self):
        return self.die_id
    

class Cell:
    def __init__(self, number, row, column, rgb, color, x, y):
        self.number = number
        self.row = row
        self.column = column
        self.x = x
        self.y = y
        self.rgb = rgb
        self.color = color
        self.is_active = True

    
    
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

    def draw_cell(self, screen):
        # for i in range(12):
        pygame.draw.rect(screen, self.rgb, (self.x, self.y, 60, 40))
        text = FONT.render(str(self.number), True, BLACK)
        screen.blit(text, (self.x + 20, self.y + 5))
        hit_box = pygame.Rect(self.x, self.y, 60, 40)
        return (hit_box, self.x, self.y, self.row, self.column) # Include row index (i) in the hit box data


class Row:
    def __init__(self, rgb, color, row_index, start_index, end_index, x, y, reverse):
        self.rgb = rgb
        self.row_index = row_index
        self.number_of_checks = 0
        self.is_locked = False
        self.x = x
        self.y = y
        self.cell_objects = {number: Cell(number, row_index, i, rgb, color, x + (70 * i), y) for i, number in enumerate(range(start_index, end_index, reverse))}
        self.cells = list(self.cell_objects.values())
        
    def display_row(self, screen):
        hit_boxes = []
        pygame.draw.rect(screen, GREY, (self.x - 5, self.y - 5, 850, 70))
        # if self.is_locked:
        pygame.draw.rect(screen, self.rgb, (self.x + 780, self.y , 60, 40))
        for cell in self.cells:
            hit_boxes.append(cell.draw_cell(screen))
        return hit_boxes
    
    def deactivate_cell(self, index):
        if self.cells[index].is_active:
            if index == len(self.cells) - 1 and self.number_of_checks < 5:
                raise InadequateChecks()
            else:
                self.cells[index].number = "X"
                if index == len(self.cells) - 1:
                    self.is_locked = True
                    self.number_of_checks += 1
                self.number_of_checks += 1
                for i in range(index + 1):
                    self.cells[i].deactivate()
        else:
            raise InvalidDeactivate()
        

class Game:
    def __init__(self, screen_width=1000, screen_height=1000, font=pygame.font.Font(None, 36)):
        self.dice = {
            1: Die(1, "white"),
            2: Die(2, "white"),
            3: Die(3, "red"),
            4: Die(4, "blue"),
            5: Die(5, "yellow"),
            6: Die(6, "green"),
        }
        self.hit_boxes = None
        self.dice_hit_boxes = None
        self.board = self.get_board()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.screen = None
        self.active_dice = list(self.dice.values())
        self.selected_dice = [None, None]
        self.selected_white_die = None
        self.selected_color_die = None
        self.selected_hit_box = None
        self.error_message = None
        self.game_state = GameState.ROLL_DICE
        self.instruction_text = None
        self.valid_cells = []
    
    # def reset_game(self):
    #     for row in self.board:
            

    def get_board(self):
        board = []
        color_text = ["red", "yellow", "green", "blue"]
        row_colors = [RED, YELLOW, GREEN, BLUE]
        for i in range(len(row_colors)):
            if (i < 2):
                # color, index, start_index, end_index, x, y, reverse
                board.append(Row(row_colors[i], color_text[i], i,  2, 13, 100, 100 + i * 50, 1))
            else:
                board.append(Row(row_colors[i], color_text[i], i, 12, 1, 100, 100 + i * 50, -1))
        return board
    
    def display_board(self):
        hit_boxes = []
        for row in self.board:
            hit_boxes.extend(row.display_row(self.screen))
        return hit_boxes

    def draw_selected_border(self, selected_color, x, y, width, height):
        border_thickness = 4  # Adjust border thickness as needed
        pygame.draw.rect(self.screen, selected_color, (x - border_thickness, y - border_thickness, width + (2*border_thickness) , height + (2*border_thickness)), border_thickness)

        
    def set_selected(self, die_id):
        # self.selected_dice = [self.selected_white_die, self.selected_color_die]
        for i in range(2):
            if self.selected_dice[i] == die_id:
                self.selected_dice[i] = None
                return
        if die_id < 3: 
            self.selected_dice[0] = die_id
        elif die_id >= 3:
            self.selected_dice[1] = die_id
        return
        
    
        
            


        # if die_id not in self.selected_dice:
        #     if len(self.selected_dice) >= 2:
        #         self.selected_dice.pop(0)
        #     self.selected_dice.append(die_id)
        # elif remove:
        #     self.selected_dice.remove(die_id)
        

    def deactivate_cells(self):
        row_number = self.selected_hit_box[3]
        self.board[row_number].deactivate_cell(self.selected_hit_box[4])
        # print(self.selected_hit_box[3], self.selected_hit_box[2])

    def get_score(self):
        total = 0
        for row in self.board:
            total += SCORE_MAP[row.number_of_checks]
        return total

    def display_score(self):
        score_text = FONT.render(f"score: {self.get_score()}", False, (0,0,0))
        self.screen.blit(score_text, (0,0))

    def display_instructions(self):
        instruction_text = FONT.render(f"Instructions: {self.instruction_text}", False, (0,0,0))
        self.screen.blit(instruction_text, (0,15))

    def highlight_valid_cells(self):
        
        if len(self.selected_dice) == 2 and None not in self.selected_dice:
            sum = self.dice[self.selected_dice[0]].get_value() + self.dice[self.selected_dice[1]].get_value()
            color = self.dice[self.selected_dice[1]].get_color()
        # print(sum)
            for row in self.board:
                for cell in row.cells:
                    if color == "white":
                        if cell.number == sum:
                            print("hello")
                            print(cell.number, cell.x, cell.y)

                            self.valid_cells.append((cell.number, cell.x, cell.y))
                    else:
                        print("hi")
                        print(f"number: {sum}, color: {color}")
                        print(f"c: {cell.number}, c: {cell.color}")
                        if cell.number == sum and color == cell.color:
                            print(cell.number, cell.x, cell.y)
                            self.valid_cells = [(cell.number, cell.x, cell.y)]
            
        

            
        
        
        
        

        
        


    # Define the game board
    def draw_board(self):
        self.screen.fill(WHITE)  # Fill the background with white

        # Define the colors for the rows
        row_colors = [RED, YELLOW, GREEN, BLUE]

        # Store hit boxes for each number and their associated row
        hit_boxes = []
        dice_hit_boxes = []


        hit_boxes = self.display_board()
        
        
        # press

        #score

        self.display_score()
        self.display_instructions()
        if len(self.valid_cells) > 0:
            for cell in self.valid_cells:
                self.draw_selected_border(HIGHLIGHT_GREY, cell[1], cell[2], 60, 40)
            

        if self.selected_hit_box is not None:
            self.draw_selected_border(BLACK, self.selected_hit_box[1], self.selected_hit_box[2], 60, 40)
            


        if self.error_message is not None:
            # my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = FONT.render(f"{self.error_message}", False, (0, 0, 0))
            self.screen.blit(text_surface, (0,20))


        x = 100
        y = 400
        new_width = 100
        new_height = 100
        for die in self.active_dice:
            if die.get_value() is not None:
                image_path = f"die_images/{die.get_color()}/dice_{die.get_color()}_{die.get_value()}.png"
                image = pygame.image.load(image_path)
                resized_image = pygame.transform.scale(image, (new_width, new_height))
                # dice_images[value] = resized_image
                hit_box = pygame.Rect(x, y, new_width, new_width)
                dice_hit_boxes.append((hit_box, die.get_die_id(), die.get_value()))

                if die.get_die_id() in self.selected_dice:
                    # Draw a border around selected dice
                    self.draw_selected_border(SELECTED_BORDER_COLOR, x, y, new_width, new_height)     
                self.screen.blit(resized_image, (x, y))
                x += 150
        for selected_die in self.selected_dice:
            for die in self.active_dice:
                if die.get_color() == selected_die:
                    print(die.get_color())
        pygame.display.flip()
        return hit_boxes, dice_hit_boxes
    
    def roll_dice(self):
        for die in self.active_dice:
            die.roll()
            self.selected_dice = [None, None]

    def run(self):
        # Initialize the screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Clickable Quixx Board")

        # Main game loop
        running = True
        
        redraw = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.game_state == GameState.ROLL_DICE:
                    self.instruction_text = "Press SPACEBAR to roll dice."
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.roll_dice()
                            self.game_state = GameState.OPTIONAL_SELECTION
                            redraw = True
                elif self.game_state == GameState.OPTIONAL_SELECTION:

                    self.instruction_text = "OPTIONAL: USE THE SUM OF THE WHITE DICE TO SELECT A NUMBER TO CHECK OFF"
                    self.selected_dice = [1, 2]
                    self.highlight_valid_cells()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.hit_boxes:
                            x, y = event.pos
                            for hit_box, xcord, ycord, row, column in self.hit_boxes:
                                if hit_box.collidepoint(x, y):
                                    self.selected_hit_box = (hit_box, xcord, ycord, row, column)
                                    redraw = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if self.selected_hit_box:
                                try: 
                                    self.deactivate_cells()
                                    redraw = True
                                except InvalidDeactivate as e:
                                    print(f"CustomError: {e}")
                                    self.error_message = e
                                except InadequateChecks as e:
                                    print(f"CustomError: {e}")
                                    self.error_message = e
                            self.game_state = GameState.COLOR_SELECTION
                            self.selected_dice = [None, None]
                            redraw = True
                            self.valid_cells = []
                elif self.game_state == GameState.COLOR_SELECTION:
                    
                    self.instruction_text = "Please select one white dice and one colored dice"
                    redraw = True

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        for hit_box, die_id, value in self.dice_hit_boxes:
                            if hit_box.collidepoint(x, y):
                                self.set_selected(die_id)
                        self.highlight_valid_cells()


                    # if event.type == pygame.MOUSEBUTTONDOWN:
                        # if self.dice_hit_boxes:
                        #     for hit_box, die_id, value in self.dice_hit_boxes:
                        #         if hit_box.collidepoint(x, y):
                        #             # self.set_selected(die_id)
                                    
                        #             # # print(f"color: {die_id}, value: {value}")
                        #             if die_id in self.selected_dice:
                        #                 self.set_selected(die_id, True)
                        #             else:
                        #                 self.set_selected(die_id)
                    
                elif self.game_state == GameState.GAME_OVER:
                    pass
                
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     if self.hit_boxes:
                #         x, y = event.pos
                #         for hit_box, xcord, ycord, row, column in self.hit_boxes:
                #             if hit_box.collidepoint(x, y):
                #                 self.selected_hit_box = (hit_box, xcord, ycord, row, column)
                #                 print(f"Clicked on number {row} in row {column}")
                #                 redraw = True
                #     if self.dice_hit_boxes:
                #         for hit_box, die_id, value in self.dice_hit_boxes:
                #             if hit_box.collidepoint(x, y):
                #                 print(f"color: {die_id}, value: {value}")

                #                 if die_id in self.selected_dice:
                #                     self.set_selected(die_id, True)
                #                 else:
                #                     self.set_selected(die_id)
        
                #                 redraw = True
                # elif event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_DOWN:
                #         pass
                #     if event.key == pygame.K_RETURN:
                #         if self.selected_hit_box:
                #             try: 
                #                 self.deactivate_cells()
                #             except InvalidDeactivate as e:
                #                 print(f"CustomError: {e}")
                #                 self.error_message = e
                #             except InadequateChecks as e:
                #                 print(f"CustomError: {e}")
                #                 self.error_message = e
                
            # Draw the board and store hit boxes once
            if not self.hit_boxes or redraw or not self.dice_hit_boxes:
                self.hit_boxes, self.dice_hit_boxes = self.draw_board()
            redraw = False

        # Quit Pygame
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.run()
    
