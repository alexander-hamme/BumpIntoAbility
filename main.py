import pyglet
import yaml

from environment.city import City
from utils import CONFIG_DICT

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


    @window.event
    def on_mouse_release(x, y, button, modifiers):

        print(x, y)

        # # key "C" get press
        # if symbol == key.:
        #     # printing the message
        #     print("Key : C is pressed")

    pyglet.clock.schedule_interval(city.run, interval=1 / float(CONFIG_DICT["target_fps"]))
    pyglet.app.run()

