import pyglet

from intro import IntroEventHandler

if __name__ == "__main__":
    window = pyglet.window.Window(caption="Rogue Santa", fullscreen=True)
    intro_handlers = IntroEventHandler(window)
    window.push_handlers(intro_handlers)
    pyglet.app.run()
