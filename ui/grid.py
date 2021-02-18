from globals import SCREEN_WIDTH, SCREEN_HEIGHT
from ui.components import Node


class Grid:
    def __init__(self):
        self.dim = 25
        self.size_x = SCREEN_WIDTH // self.dim
        self.size_y = ((SCREEN_HEIGHT-30) // self.dim)
        self.grid = self.grid_init()
        self.start = (0, 0)
        self.target = (24, 24)
        self.shortest_path = []

    def grid_init(self):
        grid = [[] for _ in range(self.dim)]
        for r in range(self.dim):
            for c in range(self.dim):
                nd = Node(self.size_x * r, (self.size_y * c)+30, (r, c), self.size_x, self.size_y)
                grid[r].append(nd)
        return grid

    def draw(self, win):
        for r in range(self.dim):
            for c in range(self.dim):
                node = self.grid[r][c]
                ip = node.pos in self.shortest_path
                node.draw(win, self, ip)

    def get_row_col_clicked(self, pos):
        row = pos[0] // self.size_x
        col = (pos[1]-30) // self.size_y
        return row, col
