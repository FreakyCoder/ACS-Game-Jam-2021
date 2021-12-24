from pyglet.sprite import Sprite

class Present(Sprite):
    def __init__(self, img, x, y, batch):
        super().__init__(img=img, x=x, y=y, batch=batch)
