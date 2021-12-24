from pyglet.sprite import Sprite
from math import sqrt
from solid import Solid
from present import Present

class Player(Sprite):
    def __init__(self, img, x, y, radius):
        self.radius = radius
        img.width, img.height = radius, radius
        img.anchor_x, img.anchor_y = radius // 2, radius // 2
        super().__init__(img=img, x=x, y=y)
    def collides(self, grid, spikes):
        presents = 0
        solid = False
        chunk = int(((self.x + grid.x) // (grid.chunkSizeX * grid.cellSize) + grid.startIndex) % grid.maxChunks)
        cellX = int(((self.x + grid.x) // grid.cellSize) % grid.chunkSizeX)
        cellY = int(self.y // grid.cellSize)
        if isinstance(grid.chunks[chunk][cellX][cellY], Solid):
            solid |= True
        elif isinstance(grid.chunks[chunk][cellX][cellY], Present):
            presents += 1
            grid.destroyCell(chunk, cellX, cellY)
        cellsToCheck = []
        cell = None
        # top
        if cellY + 1 <= grid.chunkSizeY - 1:
            # top left
            if cellX - 1 >= 0:
                cell = (grid.chunks[chunk][cellX - 1][cellY + 1], chunk, cellX - 1, cellY + 1)
            else:
                cell = (grid.chunks[(chunk - 1) % grid.maxChunks][grid.chunkSizeX - 1][cellY + 1], (chunk - 1) % grid.maxChunks, grid.chunkSizeX - 1, cellY + 1)
            if isinstance(cell[0], Sprite):
                cellsToCheck.append((cell, cell[0].x + cell[0].width, cell[0].y))
            # top right
            if cellX + 1 <= grid.chunkSizeX - 1:
                cell = (grid.chunks[chunk][cellX + 1][cellY + 1], chunk, cellX + 1, cellY + 1)
            else:
                cell = (grid.chunks[(chunk + 1) % grid.maxChunks][0][cellY + 1], (chunk + 1) % grid.maxChunks, 0, cellY + 1)
            if isinstance(cell[0], Sprite):
                cellsToCheck.append((cell, cell[0].x, cell[0].y))
            # top
            cell = (grid.chunks[chunk][cellX][cellY + 1], chunk, cellX, cellY + 1)
            if isinstance(cell[0], Sprite):
                cellsToCheck.append((cell, self.x, cell[0].y))
        # bottom
        if cellY - 1 >= 0:
            # bottom left
            if cellX - 1 >= 0:
                cell = (grid.chunks[chunk][cellX - 1][cellY - 1], chunk, cellX - 1, cellY - 1)
            else:
                cell = (grid.chunks[(chunk - 1) % grid.maxChunks][grid.chunkSizeX - 1][cellY - 1], (chunk - 1) % grid.maxChunks, grid.chunkSizeX - 1, cellY - 1)
            if isinstance(cell[0], Sprite):
                cellsToCheck.append((cell, cell[0].x + cell[0].width, cell[0].y))
            # bottom right
            if cellX + 1 <= grid.chunkSizeX - 1:
                cell = (grid.chunks[chunk][cellX + 1][cellY - 1], chunk, cellX + 1, cellY - 1)
            else:
                cell = (grid.chunks[(chunk + 1) % grid.maxChunks][0][cellY - 1], (chunk + 1) % grid.maxChunks, 0, cellY - 1)
            if isinstance(cell[0], Sprite):
                cellsToCheck.append((cell, cell[0].x, cell[0].y))
            # bottom
            cell = (grid.chunks[chunk][cellX][cellY - 1], chunk, cellX, cellY - 1)
            if isinstance(cell[0], Sprite):
                cellsToCheck.append((cell, self.x, cell[0].y + cell[0].height))
        # left
        if cellX - 1 >= 0:
            cell = (grid.chunks[chunk][cellX - 1][cellY], chunk, cellX - 1, cellY)
        else:
            cell = (grid.chunks[(chunk - 1) % grid.maxChunks][grid.chunkSizeX - 1][cellY], (chunk - 1) % grid.maxChunks, grid.chunkSizeX - 1, cellY)
        if isinstance(cell[0], Sprite):
            cellsToCheck.append((cell, cell[0].x + cell[0].width, self.y))
        # right
        if cellX + 1 <= grid.chunkSizeX - 1:
            cell = (grid.chunks[chunk][cellX + 1][cellY], chunk, cellX + 1, cellY)
        else:
            cell = (grid.chunks[(chunk + 1) % grid.maxChunks][0][cellY], (chunk + 1) % grid.maxChunks, 0, cellY)
        if isinstance(cell[0], Sprite):
            cellsToCheck.append((cell, cell[0].x, self.y))
        for cell in cellsToCheck:
            dx = cell[1] - self.x
            dy = cell[2] - self.y
            if sqrt(dx * dx + dy * dy) < self.radius:
                if isinstance(cell[0][0], Solid):
                    solid |= True
                else:
                    presents += 1
                    grid.destroyCell(cell[0][1], cell[0][2], cell[0][3])
        # spikes
        for spike in spikes:
            x1, y1 = spike.x, spike.y
            x2, y2 = spike.x - spike.width // 2, spike.y + spike.height
            x3, y3 = spike.x + spike.width // 2, spike.y + spike.height
            dx = x1 - self.x
            dy = y1 - self.y
            if sqrt(dx * dx + dy * dy) < self.radius:
                return (True, presents)
            dx = x2 - self.x
            dy = y2 - self.y
            if sqrt(dx * dx + dy * dy) < self.radius:
                return (True, presents)
            dx = x3 - self.x
            dy = y3 - self.y
            if sqrt(dx * dx + dy * dy) < self.radius:
                return (True, presents)
             
        return (solid, presents)
