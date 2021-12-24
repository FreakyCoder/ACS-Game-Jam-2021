import pyglet
from pyglet.resource import Loader
from pyglet import font, media

from intro import IntroEventHandler
from game import GameEventHandler
from end import EndEventHandler

class All:
    def __init__(self):
        self.loader = Loader('assets')
        self.loader.add_font('daggersquare.otf')
        self.ds = font.load('DAGGERSQUARE Regular')
        self.window = pyglet.window.Window(caption="Santascape", fullscreen=True)
        self.mediaPlayer = media.Player()
        self.scenes = {}
        self.current_scene = 'intro'
        self.scenes = {
            'intro': IntroEventHandler(self.window, self.start_game, self.mediaPlayer, music=self.loader.media('epic.wav', streaming=False)),
            'game': GameEventHandler(self.window, self.end_game, self.mediaPlayer, self.loader.image('santa.png'), self.loader.image('present.png'), self.loader.image('ice.png'), self.loader.media('music.wav', streaming=False)),
            'end': EndEventHandler(self.window, self.start_game)
        }
        self.window.push_handlers(self.scenes[self.current_scene])
        self.scenes[self.current_scene].start()
        pyglet.app.run()
    def start_game(self):
        self.scenes[self.current_scene].end()
        self.window.pop_handlers()
        self.current_scene = 'game'
        self.scenes[self.current_scene].start()
        self.window.push_handlers(self.scenes[self.current_scene])
    def end_game(self, points):
        self.scenes[self.current_scene].end()
        self.window.pop_handlers()
        self.current_scene = 'end'
        self.scenes[self.current_scene].start(points)
        self.window.push_handlers(self.scenes[self.current_scene])

if __name__ == "__main__":
    all = All()
