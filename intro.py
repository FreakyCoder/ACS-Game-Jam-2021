from pyglet.text import Label
from pyglet import clock

class IntroEventHandler:
    def __init__(self, window):
        self.window = window
        self.multiplier = 1
        self.textDelay = 2
        self.textInd = 0
        self.opacity = 0
        self.texts = ['Thousands of years ago', 'There was a war', 'Between good and evil']
        self.label = Label('Thousands of years ago...',
                          font_name='Times New Roman',
                          font_size=36,
                          color=(255, 255, 255, 255),
                          x=self.window.width//2, y=self.window.height//2,
                          anchor_x='center', anchor_y='center')
        clock.schedule_interval(self.update, 1/60)
    def update(self, dt):
        self.opacity += self.multiplier * dt * 127.5
        if self.multiplier == 1 and self.opacity >= 255:
            self.multiplier = 0
            self.opacity = 255
        if self.multiplier == 0:
            self.textDelay -= dt
            print(self.textDelay)
            if self.textDelay <= 0:
                self.textDelay = 2
                self.multiplier = -1
        if self.multiplier == -1 and self.opacity <= 0:
            self.multiplier = 1
            self.opacity = 0
            self.textInd += 1
            self.label.text = self.texts[self.textInd]
        self.label.color = (255, 255, 255, int(self.opacity))
    def on_key_press(self, symbol, modifiers):
        print(f'Key pressed {symbol}')
        return True
    def on_draw(self):
        self.window.clear()
        self.label.draw()

