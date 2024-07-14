import pygame
import random
import time
import pickle

pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20  # Number of rows and columns in the maze
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Iterative Backtracking Maze Generation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
DARK_GREY = (75, 75, 75)

class Cell:
    def __init__(self):
        self.down = True
        self.right = True
        self.visited = False
        self.in_stack = False

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]

    def draw(self, screen, current_cell=None):
        for row in range(self.rows):
            for col in range(self.cols):
                x, y = col * CELL_WIDTH, row * CELL_HEIGHT
                if self.grid[row][col].in_stack:
                    color = DARK_GREY
                elif self.grid[row][col].visited:
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
            pygame.draw.rect(screen, YELLOW, (x, y, CELL_WIDTH, CELL_HEIGHT))
        
    def get_neighbours(self, cell):
        neighbours = []
        row, col = cell
        if row > 0 and not self.grid[row - 1][col].visited:
            neighbours.append((row - 1, col))
        if row < self.rows - 1 and not self.grid[row + 1][col].visited:
            neighbours.append((row + 1, col))
        if col > 0 and not self.grid[row][col - 1].visited:
            neighbours.append((row, col - 1))
        if col < self.cols - 1 and not self.grid[row][col + 1].visited:
            neighbours.append((row, col + 1))
        return neighbours
    
    def remove_wall(self, current_cell, next_cell):
        row, col = current_cell
        next_row, next_col = next_cell
        if row == next_row:
            if col < next_col:
                self.grid[row][col].right = False
            else:
                self.grid[row][next_col].right = False
        else:
            if row < next_row:
                self.grid[row][col].down = False
            else:
                self.grid[next_row][col].down = False
        
    def generate_maze(self, screen):
        stack = []
        current_cell = (0, 0)
        self.grid[current_cell[0]][current_cell[1]].visited = True
        stack.append(current_cell)
        self.grid[current_cell[0]][current_cell[1]].in_stack = True
        
        while stack:
            screen.fill(BLACK)
            self.draw(screen, current_cell)
            pygame.display.flip()
            time.sleep(0.05)  # Adjust the delay for visualization speed

            current_cell = stack[-1]
            neighbours = self.get_neighbours(current_cell)
            if neighbours:
                next_cell = random.choice(neighbours)
                self.remove_wall(current_cell, next_cell)
                self.grid[next_cell[0]][next_cell[1]].visited = True
                stack.append(next_cell)
                self.grid[next_cell[0]][next_cell[1]].in_stack = True
            else:
                cell = stack.pop()
                self.grid[cell[0]][cell[1]].in_stack = False

        self.save_maze("irb_maze_data.pkl")
    
    def save_maze(self, filename):
        grid_data = [[(cell.down, cell.right, cell.visited) for cell in row] for row in self.grid]
        with open(filename, 'wb') as f:
            pickle.dump(grid_data, f)

            
class MazeGame():
    def __init__(self, width, height, rows, cols):
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.maze = Maze(rows, cols)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Iterative Backtracking Maze Generation")
    
    def run(self):
        running = True
        self.maze.generate_maze(self.screen)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.screen.fill(BLACK)
            self.maze.draw(self.screen)
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    game = MazeGame(WIDTH, HEIGHT, ROWS, COLS)
    game.run()