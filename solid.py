from pyglet.sprite import Sprite

class Solid(Sprite):
    def __init__(self, img, x, y, batch):
        super().__init__(img, x=x, y=y, batch=batch)
