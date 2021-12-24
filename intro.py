from pyglet.text import Label
from pyglet.window import key
from pyglet.graphics import Batch
from pyglet import clock, shapes

class IntroEventHandler:
    def __init__(self, window, start_game, mediaPlayer, music):
        self.window = window
        self.start_game = start_game
        self.mediaPlayer = mediaPlayer
        self.multiplier = 1
        self.textDelay = 1
        self.textInd = 0
        self.opacity = 0
        self.music = music
        self.texts = ['Thousands of years ago...', 'There was a war...', 'Between good and evil...', 'Red Santa won and threw you in an abyss...', 'For an eternity you waited in that prison...', 'For the perfect opportunity to escape...', 'And get your revenge', 'Now it\'s time to escape', 'It\'s time for SANTASCAPE', 'In this prison, the laws of physics are abandoned', 'You can only move by teleportation', 'Use the left mouse button to throw a snowball', 'And the right mouse button to teleport to it', 'Stay in view', 'Or lose yourself in darkness forever...', 'Don\'t teleport into blocks',  'Unless you desire to be embedded in ice', 'Steal presents to ruin Christmas', 'Go have your revenge!']
        self.batch = Batch()
        self.label = Label('Thousands of years ago...',
                          font_name='DAGGERSQUARE',
                          font_size=self.window.width // 100,
                          color=(255, 255, 255, 255),
                          x=self.window.width//2, y=self.window.height//2,
                          anchor_x='center', anchor_y='center', batch=self.batch)
        self.spaceHold = False
        self.skip = Label('Hold space to skip.',
                font_name='Times New Roman',
                font_size = 16,
                color=(255, 255, 255, 255),
                x=self.window.width - 20, y=self.window.height - 20,
                anchor_x='right', anchor_y='top', batch=self.batch) 
        self.progressBar = shapes.BorderedRectangle(x=self.window.width - 20 - self.skip.content_width, y=self.window.height - 20 - self.skip.content_height * 2, width = self.skip.content_width, height=self.skip.content_height // 2, border=1, color=(0, 0, 0), border_color=(255, 255, 255), batch=self.batch)
        self.progress = 0
        self.progressRect = shapes.Rectangle(x=self.progressBar.x, y = self.progressBar.y, width = 0, height = self.progressBar.height, color=(255, 255, 255), batch=self.batch)
    def start(self):
        self.mediaPlayer.queue(self.music)
        self.mediaPlayer.play()
        clock.schedule_interval(self.update, 1/60)
    def end(self):
        self.mediaPlayer.next_source()
        clock.unschedule(self.update)
    def update(self, dt):
        # text animation
        self.opacity += self.multiplier * dt * 255
        if self.multiplier == 1 and self.opacity >= 255:
            self.multiplier = 0
            self.opacity = 255
        if self.multiplier == 0:
            self.textDelay -= dt
            if self.textDelay <= 0:
                self.textDelay = 2
                self.multiplier = -1
        if self.multiplier == -1 and self.opacity <= 0:
            self.multiplier = 1
            self.opacity = 0
            self.textInd += 1
            if self.textInd >= len(self.texts):
                self.start_game()
                return
            self.label.text = self.texts[self.textInd]
        self.label.color = (255, 255, 255, int(self.opacity))
        # skip
        if self.spaceHold:
            self.progress += min(self.progressBar.width / 2 * dt, self.progressBar.width)
        else:
            self.progress = 0
        if self.progress >= self.progressBar.width:
            self.start_game()
        self.progressRect.width = int(self.progress)
    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.spaceHold = True
        return True
    def on_key_release(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.spaceHold = False
        return True
    def on_draw(self):
        self.window.clear()
        self.label.draw()
        self.skip.draw()
        self.progressBar.draw()
        self.progressRect.draw()

