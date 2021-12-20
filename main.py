import pyglet

from intro import IntroEventHandler
from game import GameEventHandler

if __name__ == "__main__":
    window = pyglet.window.Window(caption="Rogue Santa", fullscreen=True)
    scenes = {}
    def change_scene(next_scene):
        scenes[current_scene].end()
        window.pop_handlers()
        scenes[next_scene].start()
        window.push_handlers(scenes[next_scene])
    scenes = {
        'intro': IntroEventHandler(window, change_scene),
        'game': GameEventHandler(window)
    }
    current_scene = 'intro'
    window.push_handlers(scenes[current_scene])
    scenes[current_scene].start()
    pyglet.app.run()
