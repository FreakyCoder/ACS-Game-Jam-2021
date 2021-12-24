from math import sqrt
from pyglet import shapes
from present import Present
from solid import Solid

class Snowball:
    def __init__(self, src, dest, speed):
        dx = dest[0] - src[0]
        dy = dest[1] - src[1]
        dist = sqrt(dx * dx + dy * dy)
        self.directionX = dx / dist
        self.directionY = dy / dist
        self.speed = speed
        self.shape = shapes.Circle(x=src[0], y=src[1], radius=20)
        self.x = self.shape.x
        self.y = self.shape.y
    def collides(self, grid):
        chunk = int(((self.x + grid.x) // (grid.chunkSizeX * grid.cellSize) + grid.startIndex) % grid.maxChunks)
        cellX = int(((self.x + grid.x) // grid.cellSize) % grid.chunkSizeX)
        cellY = int(self.y // grid.cellSize)
        if isinstance(grid.chunks[chunk][cellX][cellY], Solid):
           return True
        cellsToCheck = []
        cell = None
        # top
        if cellY + 1 <= grid.chunkSizeY - 1:
            # top left
            if cellX - 1 >= 0:
                cell = grid.chunks[chunk][cellX - 1][cellY + 1]
            else:
                cell = grid.chunks[chunk][grid.chunkSizeX - 1][cellY + 1]
            if isinstance(cell, Solid):
                cellsToCheck.append((cell, cell.x + cell.width, cell.y))
            # top right
            if cellX + 1 <= grid.chunkSizeX - 1:
                cell = grid.chunks[chunk][cellX + 1][cellY + 1]
            else:
                cell = grid.chunks[(chunk + 1) % grid.maxChunks][0][cellY + 1]
            if isinstance(cell, Solid):
                cellsToCheck.append((cell, cell.x, cell.y))
            # top
            cell = grid.chunks[chunk][cellX][cellY + 1]
            if isinstance(cell, Solid):
                cellsToCheck.append((cell, self.x, cell.y))
        # bottom
        if cellY - 1 >= 0:
            # bottom left
            if cellX - 1 >= 0:
                cell = grid.chunks[chunk][cellX - 1][cellY - 1]
            else:
                cell = grid.chunks[(chunk - 1) % grid.maxChunks][grid.chunkSizeX - 1][cellY - 1]
            if isinstance(cell, Solid):
                cellsToCheck.append((cell, cell.x + cell.width, cell.y))
            # bottom right
            if cellX + 1 <= grid.chunkSizeX - 1:
                cell = grid.chunks[chunk][cellX + 1][cellY - 1]
            else:
                cell = grid.chunks[(chunk + 1) % grid.maxChunks][0][cellY - 1]
            if isinstance(cell, Solid):
                cellsToCheck.append((cell, cell.x, cell.y))
            # bottom
            cell = grid.chunks[chunk][cellX][cellY - 1]
            if isinstance(cell, Solid):
                cellsToCheck.append((cell, self.x, cell.y + cell.height))
        # left
        if cellX - 1 >= 0:
            cell = grid.chunks[chunk][cellX - 1][cellY]
        else:
            cell = grid.chunks[(chunk - 1) % grid.maxChunks][grid.chunkSizeX - 1][cellY]
        if isinstance(cell, Solid):
            cellsToCheck.append((cell, cell.x + cell.width, self.y))
        # right
        if cellX + 1 <= grid.chunkSizeX - 1:
            cell = grid.chunks[chunk][cellX + 1][cellY]
        else:
            cell = grid.chunks[(chunk + 1) % grid.maxChunks][0][cellY]
        if isinstance(cell, Solid):
            cellsToCheck.append((cell, cell.x, self.y))
        for cell in cellsToCheck:
            dx = cell[1] - self.x
            dy = cell[2] - self.y
            if sqrt(dx * dx + dy * dy) < self.shape.radius:
                return True
        return False
    def move(self, dt):
        self.x += dt * self.speed * self.directionX
        self.y += dt * self.speed * self.directionY
        self.shape.position = (self.x, self.y)
    def draw(self):
        self.shape.draw()
