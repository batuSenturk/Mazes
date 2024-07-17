import pygame
import random
import time
import pickle

# Constants for the display
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20  # Number of rows and columns in the maze
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
DARK_GREY = (75, 75, 75)

# Constants for directions
N, S, E, W = 1, 2, 4, 8
IN = 0x10
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}
OPPOSITE = {E: W, W: E, N: S, S: N}

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Wilson's Algorithm Maze Generation")

    def draw_maze(self, cx=None, cy=None, path=None):
        self.screen.fill(BLACK)
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                cell_x, cell_y = x * CELL_WIDTH, y * CELL_HEIGHT
                color = DARK_GREY
                if cell & IN:
                    color = BLACK
                elif path and (x, y) in path:
                    color = GREEN
                pygame.draw.rect(self.screen, color, (cell_x, cell_y, CELL_WIDTH, CELL_HEIGHT))

                if cell & S == 0:
                    pygame.draw.line(self.screen, GREEN, (cell_x, cell_y + CELL_HEIGHT), (cell_x + CELL_WIDTH, cell_y + CELL_HEIGHT), 3)
                if cell & E == 0:
                    pygame.draw.line(self.screen, GREEN, (cell_x + CELL_WIDTH, cell_y), (cell_x + CELL_WIDTH, cell_y + CELL_HEIGHT), 3)
                if cx == x and cy == y:
                    pygame.draw.rect(self.screen, YELLOW, (cell_x, cell_y, CELL_WIDTH, CELL_HEIGHT))
        pygame.display.flip()

    def walk(self):
        while True:
            cx, cy = random.randint(0, self.cols - 1), random.randint(0, self.rows - 1)
            if self.grid[cy][cx] != 0:
                continue

            visits = {(cx, cy): 0}
            start_x, start_y = cx, cy
            walking = True
            path = []

            while walking:
                if (cx, cy) in path:
                    # Loop detected, remove the looped section
                    loop_start_index = path.index((cx, cy))
                    path = path[:loop_start_index + 1]
                else:
                    path.append((cx, cy))

                self.draw_maze(cx, cy, path)
                time.sleep(0.02)

                walking = False
                for dir in random.sample([N, S, E, W], 4):
                    nx, ny = cx + DX[dir], cy + DY[dir]
                    if 0 <= nx < self.cols and 0 <= ny < self.rows:
                        visits[(cx, cy)] = dir

                        if self.grid[ny][nx] != 0:
                            break
                        else:
                            cx, cy = nx, ny
                            walking = True
                            break

            path = []
            x, y = start_x, start_y
            while (x, y) in visits:
                dir = visits[(x, y)]
                path.append((x, y, dir))
                x, y = x + DX[dir], y + DY[dir]

            return path

    def generate_maze(self):
        self.grid[random.randint(0, self.rows - 1)][random.randint(0, self.cols - 1)] = IN

        remaining = self.rows * self.cols - 1

        while remaining > 0:
            for x, y, dir in self.walk():
                nx, ny = x + DX[dir], y + DY[dir]

                self.grid[y][x] |= dir
                self.grid[ny][nx] |= OPPOSITE[dir]
                self.grid[y][x] |= IN
                self.grid[ny][nx] |= IN

                remaining -= 1

                self.draw_maze()
                time.sleep(0.02)

        self.draw_maze()
        self.save_maze("wilson_maze_data.pkl")
    
    # Save the maze data to a file
    def save_maze(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.grid, f)

class MazeGame:
    def __init__(self):
        self.maze = Maze(ROWS, COLS)

    def run(self):
        running = True
        self.maze.generate_maze()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()

if __name__ == "__main__":
    pygame.init()
    game = MazeGame()
    game.run()
