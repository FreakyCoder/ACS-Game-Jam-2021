from pyglet.window import mouse
from pyglet import clock
from snowball import Snowball
from grid import Grid
from player import Player
from score import Score

class GameEventHandler:
    def __init__(self, window, end_game, mediaPlayer, santa, present, ice, music):
        self.window = window
        self.end_game = end_game
        self.mediaPlayer = mediaPlayer
        self.santa = santa
        self.present = present
        self.ice = ice
        self.music = music
    def start(self):
        self.worldSpeed = 10
        self.snowballSpeed = 1000
        self.player = Player(self.santa, x=self.window.width // 2, y=self.window.height // 5, radius=self.window.width // 25)
        self.player.x += self.window.width // 10
        self.player.y += self.player.radius // 2
        self.grid = Grid(self.window, self.present, self.ice)
        self.snowball = None
        self.gravity = 1000
        self.score = Score(self.window)
        self.mediaPlayer.queue(self.music)
        self.mediaPlayer.play()
        self.mediaPlayer.loop = True
        clock.schedule_interval(self.update, 1/60)
    def end(self):
        self.mediaPlayer.next_source()
        clock.unschedule(self.update)
    def update(self, dt):
        # snowball movement and check for collisions
        if self.snowball is not None:
            if self.snowball.collides(self.grid):
                self.snowball = None
            else:
                self.snowball.move(dt)
       # camera movement
        self.grid.update(dt=dt, worldSpeed=self.worldSpeed)
        self.player.x -= self.window.width / 100 * self.worldSpeed * dt
        playerCollides = self.player.collides(self.grid)
        self.score.value += playerCollides[1]
        if playerCollides[0] or self.player.x + self.player.radius < 0:
            # end game
            self.end_game(self.score.value)
            return
        self.worldSpeed += 0.1 * dt
        self.snowballSpeed += 0.01 * dt
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
        self.score.draw()
        if self.snowball is not None:
            self.snowball.draw()
        self.player.draw()
