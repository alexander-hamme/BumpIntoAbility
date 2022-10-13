import pyglet

from agents import CONFIG_DICT
from agents.city import City

if __name__ == "__main__":

    city = City("Amsterdam")

    window = pyglet.window.Window(
        width=CONFIG_DICT.get("window_width"),
        height=CONFIG_DICT.get("window_height"),
        caption="Amsterdam"
    )

    @window.event()
    def on_draw():

        window.clear()
        city.draw()

    pyglet.clock.schedule_interval(city.run, interval=1 / 120.0)
    pyglet.app.run()

