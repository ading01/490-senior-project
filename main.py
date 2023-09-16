



import pygame
import sys
import random

# Initialize Pygame
pygame.init()

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
    def __init__(self, number, row, column, color, x, y):
        self.number = number
        self.row = row
        self.column = column
        self.x = x
        self.y = y
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
            new_color = (180 if self.color[0] == 255 else 0,
                        180 if self.color[1] == 255 else 0,
                        180 if self.color[2] == 255 else 0)
            self.color = new_color

    def draw_cell(self, screen):
        # for i in range(12):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 60, 40))
        text = FONT.render(str(self.number), True, BLACK)
        screen.blit(text, (self.x + 20, self.y + 5))
        hit_box = pygame.Rect(self.x, self.y, 60, 40)
        return (hit_box, self.x, self.y, self.row, self.column) # Include row index (i) in the hit box data


class Row:
    def __init__(self, color, row_index, start_index, end_index, x, y, reverse):
        self.color = color
        self.row_index = row_index
        self.number_of_checks = 0
        self.is_locked = False
        self.x = x
        self.y = y
        self.cell_objects = {number: Cell(number, row_index, i, color, x + (70 * i), y) for i, number in enumerate(range(start_index, end_index, reverse))}
        self.cells = list(self.cell_objects.values())
        
    def display_row(self, screen):
        hit_boxes = []
        pygame.draw.rect(screen, GREY, (self.x - 5, self.y - 5, 850, 70))
        # if self.is_locked:
        pygame.draw.rect(screen, self.color, (self.x + 780, self.y , 60, 40))
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
            "white1": Die(1, "white"),
            "white2": Die(2, "white"),
            "red": Die(3, "red"),
            "blue": Die(4, "blue"),
            "yellow": Die(5, "yellow"),
            "green": Die(6, "green"),
        }
        self.hit_boxes = None
        self.dice_hit_boxes = None
        self.board = self.get_board()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.screen = None
        self.active_dice = list(self.dice.values())
        self.selected_dice = []
        self.selected_hit_box = None
        self.error_message = None
    
    # def reset_game(self):
    #     for row in self.board:
            

    def get_board(self):
        board = []
        row_colors = [RED, YELLOW, GREEN, BLUE]
        for i, color in enumerate(row_colors):
            if (i < 2):
                # color, index, start_index, end_index, x, y, reverse
                board.append(Row(color, i,  2, 13, 100, 100 + i * 50, 1))
            else:
                board.append(Row(color, i, 12, 1, 100, 100 + i * 50, -1))
        return board
    
    def display_board(self):
        hit_boxes = []
        for row in self.board:
            hit_boxes.extend(row.display_row(self.screen))
        return hit_boxes

    def draw_selected_border(self, selected_color, x, y, width, height):
        border_thickness = 4  # Adjust border thickness as needed
        pygame.draw.rect(self.screen, selected_color, (x - border_thickness, y - border_thickness, width + (2*border_thickness) , height + (2*border_thickness)), border_thickness)

        
    def set_selected(self, die_id, remove=False):
        if die_id not in self.selected_dice:
            if len(self.selected_dice) >= 2:
                self.selected_dice.pop(0)
            self.selected_dice.append(die_id)
        elif remove:
            self.selected_dice.remove(die_id)
        

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
    # Define the game board
    def draw_board(self):
        self.screen.fill(WHITE)  # Fill the background with white

        # Define the colors for the rows
        row_colors = [RED, YELLOW, GREEN, BLUE]

        # Store hit boxes for each number and their associated row
        hit_boxes = []
        dice_hit_boxes = []


        hit_boxes = self.display_board()
        if self.selected_hit_box is not None:
            self.draw_selected_border(BLACK, self.selected_hit_box[1], self.selected_hit_box[2], 60, 40)
        
        # press

        #score

        self.display_score()


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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.hit_boxes:
                        x, y = event.pos
                        for hit_box, xcord, ycord, row, column in self.hit_boxes:
                            if hit_box.collidepoint(x, y):
                                self.selected_hit_box = (hit_box, xcord, ycord, row, column)
                                print(f"Clicked on number {row} in row {column}")
                                redraw = True
                    if self.dice_hit_boxes:
                        for hit_box, die_id, value in self.dice_hit_boxes:
                            if hit_box.collidepoint(x, y):
                                print(f"color: {die_id}, value: {value}")

                                if die_id in self.selected_dice:
                                    self.set_selected(die_id, True)
                                else:
                                    self.set_selected(die_id)
        
                                redraw = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        for die in self.active_dice:
                            print("dice roll")
                            die.roll()
                            self.selected_dice = []
                            redraw = True
                    if event.key == pygame.K_RETURN:
                        if self.selected_hit_box:
                            try: 
                                self.deactivate_cells()
                            except InvalidDeactivate as e:
                                print(f"CustomError: {e}")
                                self.error_message = e
                            except InadequateChecks as e:
                                print(f"CustomError: {e}")
                                self.error_message = e
                
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
    
