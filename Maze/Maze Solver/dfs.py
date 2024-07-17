import pygame
import pickle

# Constants for the display
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20  # Number of rows and columns in the maze
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREY = (75, 75, 75)
RED = (255, 0, 0)

# Constants for directions
N, S, E, W = 1, 2, 4, 8
IN = 0x10

class MazeLoader:
    def __init__(self, filename):
        self.filename = filename
        self.grid = self.load_maze()
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows > 0 else 0
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Depth-First Search Maze Solver")

    def load_maze(self):
        with open(self.filename, 'rb') as f:
            return pickle.load(f)

    def draw_maze(self, path=None, current=None):
        self.screen.fill(BLACK)
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                cell_x, cell_y = x * CELL_WIDTH, y * CELL_HEIGHT
                color = DARK_GREY
                if cell & IN:
                    color = BLACK
                pygame.draw.rect(self.screen, color, (cell_x, cell_y, CELL_WIDTH, CELL_HEIGHT))

                if cell & S == 0:
                    pygame.draw.line(self.screen, GREEN, (cell_x, cell_y + CELL_HEIGHT), (cell_x + CELL_WIDTH, cell_y + CELL_HEIGHT), 3)
                if cell & E == 0:
                    pygame.draw.line(self.screen, GREEN, (cell_x + CELL_WIDTH, cell_y), (cell_x + CELL_WIDTH, cell_y + CELL_HEIGHT), 3)
        
        if path:
            for i in range(1, len(path)):
                start_x, start_y = path[i-1]
                end_x, end_y = path[i]
                start_pos = (start_x * CELL_WIDTH + CELL_WIDTH // 2, start_y * CELL_HEIGHT + CELL_HEIGHT // 2)
                end_pos = (end_x * CELL_WIDTH + CELL_WIDTH // 2, end_y * CELL_HEIGHT + CELL_HEIGHT // 2)
                pygame.draw.line(self.screen, RED, start_pos, end_pos, 3)

        if current:
            current_x, current_y = current
            current_pos = (current_x * CELL_WIDTH + CELL_WIDTH // 2, current_y * CELL_HEIGHT + CELL_HEIGHT // 2)
            pygame.draw.circle(self.screen, RED, current_pos, 5)

        pygame.display.flip()

    def dfs(self, start, end):
        stack = [start]
        visited = set()
        path = []
        backtrack = []

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            path.append(current)

            self.draw_maze(path=path, current=current)
            pygame.time.wait(50)  # Delay to visualize the search

            if current == end:
                return path

            x, y = current
            neighbors = []
            if self.grid[y][x] & N and (x, y-1) not in visited:
                neighbors.append((x, y-1))
            if self.grid[y][x] & S and (x, y+1) not in visited:
                neighbors.append((x, y+1))
            if self.grid[y][x] & E and (x+1, y) not in visited:
                neighbors.append((x+1, y))
            if self.grid[y][x] & W and (x-1, y) not in visited:
                neighbors.append((x-1, y))

            if not neighbors:
                # If no unvisited neighbors, backtrack
                while path and not neighbors:
                    backtrack.append(path.pop())
                    if path:
                        x, y = path[-1]
                        neighbors = []
                        if self.grid[y][x] & N and (x, y-1) not in visited:
                            neighbors.append((x, y-1))
                        if self.grid[y][x] & S and (x, y+1) not in visited:
                            neighbors.append((x, y+1))
                        if self.grid[y][x] & E and (x+1, y) not in visited:
                            neighbors.append((x+1, y))
                        if self.grid[y][x] & W and (x-1, y) not in visited:
                            neighbors.append((x-1, y))
            else:
                backtrack = []

            stack.extend(neighbors)

    def run(self):
        running = True
        start = (0, 0)
        end = (self.cols - 1, self.rows - 1)
        path = self.dfs(start, end)
        self.draw_maze(path=path)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()

if __name__ == "__main__":
    pygame.init()
    maze_loader = MazeLoader("wilson_maze_data.pkl")
    maze_loader.run()