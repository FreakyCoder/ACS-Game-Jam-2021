from pyglet.window import mouse
from pyglet import clock, shapes
from snowball import Snowball
from grid import Grid

class GameEventHandler:
    def __init__(self, window):
        self.window = window
        self.player = shapes.Circle(x=self.window.width // 100, y=self.window.height // 5, radius=self.window.width // 50, color=(200, 10, 10))
        self.player.x += self.window.width // 10
        self.player.y += self.player.radius // 2
        self.grid = Grid(self.window)
        self.worldSpeed = 10
        self.snowballSpeed = 1000
        self.snowball = None
        self.gravity = 1000
    def start(self):
        clock.schedule_interval(self.update, 1/60)
    def end(self):
        clock.unschedule(self.update)
    def update(self, dt):
        # snowball movement and check for collisions
        if self.snowball is not None:
            if self.snowball.collides(self.grid):
                self.snowball = None
            else:
                self.snowball.move(dt)
        # gravity
        #  if self.player.y > self.base.y + self.base.height:
            #  self.player.y = int(max(self.player.y - self.gravity * dt, self.base.y + self.base.height + self.player.height / 2))
        # camera movement
        self.grid.update(dt=dt, worldSpeed=self.worldSpeed)
        self.player.x -= self.window.width / 100 * self.worldSpeed * dt
    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.snowball = Snowball((self.player.x, self.player.y), (x, y), self.snowballSpeed)
        if button == mouse.RIGHT and self.snowball is not None:
            self.player.x = self.snowball.x
            self.player.y = self.snowball.y
            self.snowball = None
    def on_draw(self):
        self.window.clear()
        self.grid.draw()
        if self.snowball is not None:
            self.snowball.draw()
        self.player.draw()
