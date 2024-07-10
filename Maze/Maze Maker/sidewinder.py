import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20  # Number of rows and columns in the maze
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sidewinder Maze Generation")

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREY = (75, 75, 75)

class Cell:
    def __init__(self):
        self.down = True
        self.right = True
        self.visited = False

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]

    def draw(self, screen, current_cell=None):
        for row in range(self.rows):
            for col in range(self.cols):
                x, y = col * CELL_WIDTH, row * CELL_HEIGHT
                if self.grid[row][col].visited:
                    color = BLACK
                else:
                    color = DARK_GREY
                pygame.draw.rect(screen, color, (x, y, CELL_WIDTH, CELL_HEIGHT))
                
                if self.grid[row][col].down:
                    pygame.draw.line(screen, GREEN, (x, y + CELL_HEIGHT), (x + CELL_WIDTH, y + CELL_HEIGHT), 3)
                if self.grid[row][col].right:
                    pygame.draw.line(screen, GREEN, (x + CELL_WIDTH, y), (x + CELL_WIDTH, y + CELL_HEIGHT), 3)

        if current_cell:
            x, y = current_cell[1] * CELL_WIDTH, current_cell[0] * CELL_HEIGHT
            pygame.draw.rect(screen, GREEN, (x, y, CELL_WIDTH, CELL_HEIGHT))

    def sidewinder(self, screen):
        for row in range(self.rows):
            run = []
            for col in range(self.cols):
                run.append((row, col))
                self.grid[row][col].visited = True

                at_eastern_boundary = (col == self.cols - 1)
                at_northern_boundary = (row == 0)

                should_close_out = at_eastern_boundary or (not at_northern_boundary and random.choice([True, False]))

                if should_close_out:
                    member = random.choice(run)
                    if member[0] > 0:  # Not at northern boundary
                        self.grid[member[0] - 1][member[1]].down = False
                    run = []
                else:
                    self.grid[row][col].right = False

                # Draw the current state of the maze with the current cell highlighted
                screen.fill(BLACK)
                self.draw(screen, current_cell=(row, col))
                pygame.display.flip()
                time.sleep(0.02)  # Adjust the delay for visualization speed

class MazeGame:
    def __init__(self, width, height, rows, cols):
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.maze = Maze(rows, cols)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sidewinder Maze Generation")

    def run(self):
        running = True
        self.maze.sidewinder(self.screen)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(BLACK)
            self.maze.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

# Main
if __name__ == "__main__":
    game = MazeGame(WIDTH, HEIGHT, ROWS, COLS)
    game.run()
