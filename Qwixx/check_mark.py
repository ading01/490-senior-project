import pygame
import sys

pygame.init()

# Set up the main game window
width, height = 400, 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Checkbox Example")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font for text
font = pygame.font.Font(None, 36)

# Checkbox properties
checkbox_x = 50
checkbox_y = 50
checkbox_size = 30
checkbox_checked = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                # Check if the mouse click is inside the checkbox
                if checkbox_x < mouse_x < checkbox_x + checkbox_size and checkbox_y < mouse_y < checkbox_y + checkbox_size:
                    checkbox_checked = not checkbox_checked

    # Clear the screen
    screen.fill(WHITE)

    # Draw the checkbox outline
    pygame.draw.rect(screen, BLACK, (checkbox_x, checkbox_y, checkbox_size, checkbox_size), 2)

    # If the checkbox is checked, draw an "X" inside
    if checkbox_checked:
        pygame.draw.line(screen, BLACK, (checkbox_x, checkbox_y), (checkbox_x + checkbox_size, checkbox_y + checkbox_size), 2)
        pygame.draw.line(screen, BLACK, (checkbox_x + checkbox_size, checkbox_y), (checkbox_x, checkbox_y + checkbox_size), 2)

    # Display text next to the checkbox
    text = font.render("Checkbox", True, BLACK)
    screen.blit(text, (checkbox_x + checkbox_size + 10, checkbox_y))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
