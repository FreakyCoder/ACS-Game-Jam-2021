from pyglet.text import Label

class Score:
    def __init__(self, window):
        self._value = 0
        self.label = Label('Score: 0', x=window.width // 100, y=window.height // 50, font_name='DAGGERSQUARE', font_size=36, color=(0, 0, 0, 255))
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, val):
        self._value = val
        self.label.text = format(f'Score: {val}')
    def draw(self):
        self.label.draw()
