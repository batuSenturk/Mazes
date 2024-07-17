import pygame
import pickle
from collections import deque

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
DARK_GREEN = (0, 150, 0)

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
        pygame.display.set_caption("Dead-End Filling Maze Solver")
        self.visited = set()  # Track visited cells

    def load_maze(self):
        with open(self.filename, 'rb') as f:
            return pickle.load(f)

    def draw_maze(self, path=None, final=False):
        self.screen.fill(BLACK)
        wall_color = GREEN  # Default wall color
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                cell_x, cell_y = x * CELL_WIDTH, y * CELL_HEIGHT
                color = GREEN if (x, y) in self.visited else DARK_GREY
                if cell & IN:
                    color = BLACK
                pygame.draw.rect(self.screen, color, (cell_x, cell_y, CELL_WIDTH, CELL_HEIGHT))


                # Check if the current cell is visited for wall color decision
                if (x, y) in self.visited:
                    wall_color = GREEN  # Keep original wall color if visited

                if cell & S == 0:
                    pygame.draw.line(self.screen, wall_color, (cell_x, cell_y + CELL_HEIGHT), (cell_x + CELL_WIDTH, cell_y + CELL_HEIGHT), 3)
                if cell & E == 0:
                    pygame.draw.line(self.screen, wall_color, (cell_x + CELL_WIDTH, cell_y), (cell_x + CELL_WIDTH, cell_y + CELL_HEIGHT), 3)
                if cell & N == 0:
                    pygame.draw.line(self.screen, wall_color, (cell_x, cell_y), (cell_x + CELL_WIDTH, cell_y), 3)
                if cell & W == 0:
                    pygame.draw.line(self.screen, wall_color, (cell_x, cell_y), (cell_x, cell_y + CELL_HEIGHT), 3)

        if path:
            for i in range(len(path) - 1):
                start = path[i]
                end = path[i + 1]
                start_pos = (start[0] * CELL_WIDTH + CELL_WIDTH // 2, start[1] * CELL_HEIGHT + CELL_HEIGHT // 2)
                end_pos = (end[0] * CELL_WIDTH + CELL_WIDTH // 2, end[1] * CELL_HEIGHT + CELL_HEIGHT // 2)
                pygame.draw.line(self.screen, RED, start_pos, end_pos, 3)

        pygame.display.flip()

    def dead_end_filling(self):
        changes = True
        while changes:
            changes = False
            for y in range(self.rows):
                for x in range(self.cols):
                    if (x, y) != (0, 0) and (x, y) != (self.cols - 1, self.rows - 1) and self.is_dead_end((x, y)):  # Skip the start and end nodes
                        self.visited.add((x, y))  # Mark cell as visited
                        self.fill_dead_end((x, y))
                        changes = True
                        self.draw_maze()
                        pygame.time.wait(50)  # Delay to visualize the process

    def is_dead_end(self, cell):
        x, y = cell
        if not (0 <= x < self.cols and 0 <= y < self.rows):
            return False
        directions = [N, S, E, W]
        open_paths = sum([self.grid[y][x] & d > 0 for d in directions])
        return open_paths == 1

    def fill_dead_end(self, cell):
        x, y = cell
        if self.grid[y][x] & N:
            self.grid[y-1][x] &= ~S
        if self.grid[y][x] & S:
            self.grid[y+1][x] &= ~N
        if self.grid[y][x] & E:
            self.grid[y][x+1] &= ~W
        if self.grid[y][x] & W:
            self.grid[y][x-1] &= ~E
        self.grid[y][x] = 0  # Mark the cell as visited by setting it to 0

    def bfs(self, start, end):
        queue = deque([start])
        visited = {start: None}
        while queue:
            current = queue.popleft()
            if current == end:
                break
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited[neighbor] = current
        path = []
        step = end
        while step:
            path.append(step)
            step = visited[step]
        path.reverse()
        return path

    def get_neighbors(self, cell):
        x, y = cell
        neighbors = []
        if self.grid[y][x] & N:
            neighbors.append((x, y-1))
        if self.grid[y][x] & S:
            neighbors.append((x, y+1))
        if self.grid[y][x] & E:
            neighbors.append((x+1, y))
        if self.grid[y][x] & W:
            neighbors.append((x-1, y))
        return neighbors

    def run(self):
        running = True
        self.draw_maze()  # Draw initial maze
        self.dead_end_filling()

        start = (0, 0)
        end = (self.cols - 1, self.rows - 1)
        path = self.bfs(start, end)
        self.draw_maze(path=path, final=True)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()

if __name__ == "__main__":
    pygame.init()
    maze_loader = MazeLoader("wilson_maze_data.pkl")
    maze_loader.run()
