from pyglet.sprite import Sprite

class Spike(Sprite):
    def __init__(self, img, x, y, batch):
        super().__init__(img=img, x=x, y=y, batch=batch)
        self.multiplier = 1
        if y == 0:
            self.multiplier = -1
            self.rotation = 180
