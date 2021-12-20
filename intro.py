from pyglet.text import Label
from pyglet.window import key
from pyglet.graphics import Batch
from pyglet import clock, shapes

class IntroEventHandler:
    def __init__(self, window):
        self.window = window
        self.multiplier = 1
        self.textDelay = 2
        self.textInd = 0
        self.opacity = 0
        self.texts = ['Thousands of years ago', 'There was a war', 'Between good and evil']
        self.batch = Batch()
        self.label = Label('Thousands of years ago...',
                          font_name='Times New Roman',
                          font_size=36,
                          color=(255, 255, 255, 255),
                          x=self.window.width//2, y=self.window.height//2,
                          anchor_x='center', anchor_y='center', batch=self.batch)
        clock.schedule_interval(self.update, 1/60)
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
    def update(self, dt):
        # text animation
        self.opacity += self.multiplier * dt * 127.5
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
                end()
            self.label.text = self.texts[self.textInd]
        self.label.color = (255, 255, 255, int(self.opacity))
        # skip
        if self.spaceHold:
            self.progress += min(self.progressBar.width / 2 * dt, self.progressBar.width)
        else:
            self.progress = 0
        if self.progress >= self.progressBar.width:
            end()
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

