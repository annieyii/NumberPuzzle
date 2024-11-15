import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 400, 460  # Adjusted height to add button area
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Puzzle")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (107, 130, 114)
BORDER_GRAY = (169, 169, 169, 25)
BUTTON_COLOR = (200, 180, 220)  
BUTTON_HOVER_COLOR = (50, 50, 50)     

# Fonts
font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 40)

# Create the puzzle grid
def create_grid():
    grid = list(range(1, GRID_SIZE * GRID_SIZE)) + [0]  # 0 represents the empty space
    random.shuffle(grid)
    return [grid[i:i + GRID_SIZE] for i in range(0, len(grid), GRID_SIZE)]

# Find the empty space
def find_empty(grid):
    grid_np = np.array(grid)
    index = np.argwhere(grid_np == 0)
    if index.size > 0:
        return tuple(index[0])
    else:
        raise ValueError("No empty space found")

# Draw the grid
def draw_grid(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            val = grid[i][j]
            rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if val != 0:
                pygame.draw.rect(screen, GRAY, rect)
                text = font.render(str(val), True, WHITE)
                text_rect = text.get_rect(center=(j * TILE_SIZE + TILE_SIZE // 2, i * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, BLACK, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, BORDER_GRAY, rect, 1)

# Button position and size
def draw_restart_button():
    button_rect = pygame.Rect((WIDTH - 150) // 2, HEIGHT - 50, 150, 40)  # Adjust Y-coordinate for button position
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    
    text = button_font.render("Restart", True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    return button_rect

# Move the tile
def move_tile(grid, direction):
    i, j = find_empty(grid)
    if direction == 'up' and i < GRID_SIZE - 1:
        grid[i][j], grid[i + 1][j] = grid[i + 1][j], grid[i][j]
    elif direction == 'down' and i > 0:
        grid[i][j], grid[i - 1][j] = grid[i - 1][j], grid[i][j]
    elif direction == 'left' and j < GRID_SIZE - 1:
        grid[i][j], grid[i][j + 1] = grid[i][j + 1], grid[i][j]
    elif direction == 'right' and j > 0:
        grid[i][j], grid[i][j - 1] = grid[i][j - 1], grid[i][j]

# Check if the puzzle is solved
def is_puzzle_solved(grid):
    flat_list = [tile for row in grid for tile in row]
    return flat_list == list(range(1, GRID_SIZE * GRID_SIZE)) + [0]

# Main loop
def main():
    grid = create_grid()
    running = True

    previous_x, previous_y = None, None
    dragging = False  # Mouse detected
    moved = False 

    while running:
        screen.fill(BLACK)
        draw_grid(grid)
        button_rect = draw_restart_button()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):  # Check if Restart button is clicked
                    grid = create_grid()  # Reset the grid
                else:
                    dragging = True
                    previous_x, previous_y = event.pos
                    moved = False
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                moved = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    x, y = event.pos
                    if previous_x is not None and previous_y is not None:
                        if not moved:
                            if x < previous_x:  
                                move_tile(grid, 'left')
                            elif x > previous_x:  
                                move_tile(grid, 'right')
                            if y < previous_y:  
                                move_tile(grid, 'up')
                            elif y > previous_y:  
                                move_tile(grid, 'down')
                            moved = True
                        previous_x, previous_y = x, y  # Update previous coordinates
                    else:
                        previous_x, previous_y = x, y

    pygame.quit()

if __name__ == "__main__":
    main()