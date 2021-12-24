from math import ceil
from random import random
from pyglet.graphics import Batch
from solid import Solid
from present import Present

class Grid:
    def __init__(self, window, present, ice):
        self.window = window
        self.batch = Batch()
        self.chunkSizeX = 50
        self.cellSize = self.window.width // self.chunkSizeX
        self.present = present
        present.width, present.height = self.cellSize, self.cellSize
        self.ice = ice
        ice.width, ice.height = self.cellSize, self.cellSize
        self.chunkSizeY = ceil(self.window.height / self.cellSize)
        self.startIndex = 0
        self.maxChunks = 3
        self.chunks = self.maxChunks * [[]]
        # generate initial chunks
        for ch in range(0, self.maxChunks):
            if ch != 1:
                self.generateChunk((self.startIndex + ch) % self.maxChunks, ((self.startIndex + ch) % self.maxChunks - 1) * self.chunkSizeX * self.cellSize)
            else:
                # generate the chunk that the player spawns in so that the game doesn't immediately end
                for i in range(0, self.chunkSizeX):
                    self.chunks[ch].append([])
                    for j in range(0, self.chunkSizeY):
                        if j == 0 or j == 1 or j == self.chunkSizeY - 1:
                            self.chunks[ch][i].append(Solid(self.ice, x=i * self.cellSize, y=j * self.cellSize, batch=self.batch))
                            continue
                        self.chunks[ch][i].append(None)
        # the distance between the camera's left border and the start of the chunk at startIndex
        self.x = self.chunkSizeX * self.cellSize
    def generateChunk(self, index, startX):
        self.chunks[index] = []
        for i in range (0, self.chunkSizeX):
            self.chunks[index].append([])
            for j in range(0, self.chunkSizeY):
                # add ceiling and floor
                if j == 0 or j == 1 or j == self.chunkSizeY - 1:
                    self.chunks[index][i].append(Solid(self.ice, x=startX + i * self.cellSize, y=j * self.cellSize, batch=self.batch))
                    continue
                if self.chunks[index][i][j - 1] is None and self.chunks[index][i][j - 2] is None and i < self.chunkSizeX - 1 and j + 1 < self.chunkSizeY - 1 and random() > 0.992:
                    # platform
                    self.chunks[index][i].append(Solid(self.ice, x=startX + i * self.cellSize, y=j * self.cellSize, batch=self.batch))
                elif random() > 0.995:
                    self.chunks[index][i].append(Present(self.present, x=startX + i * self.cellSize, y=j * self.cellSize, batch=self.batch))
                else:
                    self.chunks[index][i].append(None)
        for i in range (self.chunkSizeX - 1, -1, -1):
            for j in range(2, self.chunkSizeY - 1):
                if isinstance(self.chunks[index][i][j], Solid):
                    self.dfs(i, j, index, startX, 1)
    def dfs(self, x, y, index, startX, chance):
        if x + 1 < self.chunkSizeX - 1 and not isinstance(self.chunks[index][x + 1][y - 1], Solid) and not isinstance(self.chunks[index][x + 1][y + 1], Solid) and not isinstance(self.chunks[index][x + 1][y], Solid) and not isinstance(self.chunks[index][x + 1][y], Present) and random() < chance / 2:
            self.chunks[index][x + 1][y] = Solid(self.ice, x=startX + (x + 1) * self.cellSize, y=y * self.cellSize, batch=self.batch)
            self.dfs(x + 1, y, index, startX, chance / 1000)
        elif y + 1 < self.chunkSizeY - 2 and not isinstance(self.chunks[index][x][y + 1], Present) and not isinstance(self.chunks[index][x][y + 2], Solid) and random() < chance:
            self.chunks[index][x][y + 1] = Solid(self.ice, x=startX + x * self.cellSize, y=(y + 1) * self.cellSize, batch=self.batch)
            self.dfs(x, y + 1, index, startX, chance / 1000)
    def destroyCell(self, chunk, x, y):
        self.chunks[chunk][x][y] = None
    def update(self, dt, worldSpeed):
        # camera movement
        for chunk in self.chunks:
            for row in chunk:
                for cell in row:
                    if cell is not None:
                        cell.x -= self.window.width / 100 * worldSpeed * dt
        self.x += self.window.width / 100 * worldSpeed * dt
        # delete last chunk and generate a new one
        if self.x >= 1.5 * self.cellSize * self.chunkSizeX:
            self.x -= self.cellSize * self.chunkSizeX
            self.generateChunk(self.startIndex, (self.maxChunks - 1) * self.chunkSizeX * self.cellSize - self.x)
            self.startIndex = (self.startIndex + 1) % self.maxChunks
    def draw(self):
        self.batch.draw()

