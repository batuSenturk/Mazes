import pygame
import random
import pickle
import time

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

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Kruskal's Algorithm Maze Generation")

    def draw_maze(self, remaining_walls):
        self.screen.fill(BLACK)
        for y in range(self.rows):
            for x in range(self.cols):
                cell_x, cell_y = x * CELL_WIDTH, y * CELL_HEIGHT
                color = DARK_GREY if self.grid[y][x] & IN == 0 else BLACK
                pygame.draw.rect(self.screen, color, (cell_x, cell_y, CELL_WIDTH, CELL_HEIGHT))

                if self.grid[y][x] & S == 0:
                    pygame.draw.line(self.screen, GREEN, (cell_x, cell_y + CELL_HEIGHT), (cell_x + CELL_WIDTH, cell_y + CELL_HEIGHT), 2)
                if self.grid[y][x] & E == 0:
                    pygame.draw.line(self.screen, GREEN, (cell_x + CELL_WIDTH, cell_y), (cell_x + CELL_WIDTH, cell_y + CELL_HEIGHT), 2)

        for wall in remaining_walls:
            x, y, direction = wall
            if direction == S:
                pygame.draw.line(self.screen, GREEN, (x * CELL_WIDTH, (y + 1) * CELL_HEIGHT), ((x + 1) * CELL_WIDTH, (y + 1) * CELL_HEIGHT), 2)
            elif direction == E:
                pygame.draw.line(self.screen, GREEN, ((x + 1) * CELL_WIDTH, y * CELL_HEIGHT), ((x + 1) * CELL_WIDTH, (y + 1) * CELL_HEIGHT), 2)

        pygame.display.flip()

    def generate_maze(self):
        dset = DisjointSet(self.rows * self.cols)
        walls = [(x, y, S) for y in range(self.rows) for x in range(self.cols) if y < self.rows - 1] + [(x, y, E) for y in range(self.rows) for x in range(self.cols) if x < self.cols - 1]
        random.shuffle(walls)
        remaining_walls = set(walls)

        while walls:
            self.draw_maze(remaining_walls)
            pygame.time.delay(50)

            x, y, direction = walls.pop()
            nx, ny = x + DX[direction], y + DY[direction]

            if dset.find(y * self.cols + x) != dset.find(ny * self.cols + nx):
                dset.union(y * self.cols + x, ny * self.cols + nx)
                self.grid[y][x] |= direction
                self.grid[ny][nx] |= OPPOSITE[direction]
                self.grid[y][x] |= IN
                self.grid[ny][nx] |= IN
                remaining_walls.remove((x, y, direction))

        self.draw_maze(remaining_walls)
        self.save_maze("kruskal_maze_data.pkl")

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
