from math import sqrt
from pyglet import shapes

class Snowball:
    def __init__(self, src, dest, speed):
        dx = dest[0] - src[0]
        dy = dest[1] - src[1]
        dist = sqrt(dx * dx + dy * dy)
        self.directionX = dx / sqrt(dist)
        self.directionY = dy / sqrt(dist)
        self.speed = speed
        self.shape = shapes.Circle(x=src[0], y=src[1], radius=20)
        self.x = self.shape.x
        self.y = self.shape.y
    def move(self, dt):
        self.x += dt * self.speed * self.directionX
        self.y += dt * self.speed * self.directionY
        self.shape.position = (self.x, self.y)
    def draw(self):
        self.shape.draw()
