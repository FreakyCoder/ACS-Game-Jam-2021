from pyglet.text import Label
from pyglet.window.key import SPACE as Space
from pyglet import clock, shapes

class EndEventHandler:
    def __init__(self, window, start_game):
        self.window = window
        self.start_game = start_game
        self.score = Label('Your Score: 0', x=window.width // 2, y=window.height // 2, anchor_x='center', anchor_y='center', font_name='DAGGERSQUARE', font_size=36)
        self.retry = Label('Hold space to retry.', x=window.width // 2, y=window.height // 2 - self.score.content_height, anchor_x='center', anchor_y='top', font_name='DAGGERSQUARE', font_size=16)
        self.progressBar = shapes.BorderedRectangle(x=self.window.width // 2, y=self.retry.y - self.retry.content_height * 2, width=self.retry.content_width, height=self.retry.content_height // 2, border=1, color=(0, 0, 0), border_color=(255, 255, 255))
        self.progressBar.anchor_position = (self.progressBar.width // 2, self.progressBar.height)
        self.progressRect = shapes.Rectangle(x=self.progressBar.x, y=self.progressBar.y, width=0, height=self.progressBar.height, color=(255, 255, 255))
        self.progressRect.anchor_position = (self.progressBar.width // 2, self.progressBar.height)
    
    def update(self, dt):
        if self.space:
            self.progress += min(self.progressBar.width / 2 * dt, self.progressBar.width)
        else:
            self.progress = 0
        if self.progress >= self.progressBar.width:
            self.start_game()
        self.progressRect.width = int(self.progress)
    def start(self, points):
        self.space = False
        self.progress = 0
        self.progressRect.width = 0
        self.score.text = format(f'Your Score: {points}')
        clock.schedule_interval(self.update, 1/60) 
    def end(self):
        clock.unschedule(self.update)
    def on_key_press(self, symbol, modifiers):
        if symbol == Space:
           self.space = True
    def on_key_release(self, symbol, modifiers):
        if symbol == Space:
            self.space = False
    def on_draw(self):
        self.window.clear()
        self.score.draw()
        self.retry.draw()
        self.progressBar.draw()
        self.progressRect.draw()
