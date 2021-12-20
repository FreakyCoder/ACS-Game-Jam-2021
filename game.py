from pyglet.window import mouse
from pyglet import clock, shapes
from snowball import Snowball

class GameEventHandler:
    def __init__(self, window):
        self.window = window
        self.player = shapes.Rectangle(x=self.window.width // 100, y=self.window.height // 5, width=self.window.width // 20, height=self.window.width // 20, color=(200, 10, 10))
        self.player.anchor_position = self.player.width // 2, self.player.height // 2
        self.player.x += self.window.width // 10
        self.player.y += self.player.height // 2
        self.base = shapes.Rectangle(x=0, y=0, width=self.window.width, height=self.window.height//5, color=(255, 255, 255))
        self.worldSpeed = 1
        self.snowballSpeed = 50
        self.snowball = None
        self.gravity = 1000
    def start(self):
        clock.schedule_interval(self.update, 1/120)
    def end(self):
        clock.unschedule(self.update)
    def update(self, dt):
        # snowball movement
        if self.snowball is not None:
            self.snowball.move(dt)
        # gravity
        if self.player.y > self.base.y + self.base.height:
            self.player.y = int(max(self.player.y - self.gravity * dt, self.base.y + self.base.height + self.player.height / 2))
        # camera movement
        self.player.x -= int(self.window.width / 1000 * self.worldSpeed)
    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.snowball = Snowball((self.player.x, self.player.y), (x, y), self.snowballSpeed)
        if button == mouse.RIGHT and self.snowball is not None:
            self.player.position = (self.snowball.x, self.snowball.y)
            self.snowball = None
    def on_draw(self):
        self.window.clear()
        self.base.draw()
        if self.snowball is not None:
            self.snowball.draw()
        self.player.draw()
