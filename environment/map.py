import random

from pyglet import shapes
import pyglet

from agents import CONFIG_DICT

WINDOW_WIDTH = CONFIG_DICT.get("window_width")
WINDOW_HEIGHT = CONFIG_DICT.get("window_height")


class Map:

    def __init__(self, name):
        self.name = name
        self.buildings_batch = pyglet.graphics.Batch()
        self.buildings = []
        self.render()

    def render(self):
        for i in range(12):
            square = shapes.Rectangle((x := random.uniform(20,WINDOW_WIDTH)),
                                       (y := random.uniform(20,WINDOW_HEIGHT)), x + 100, y + 100,
                                        color=(55, 55, 255), batch=self.buildings_batch)
            rectangle = shapes.Rectangle(i*30, i*20, 400, 200, color=(30, 255, 20), batch=self.buildings_batch)
            rectangle.opacity = 128
            rectangle.rotation = 10
            self.buildings.append(rectangle)

    def draw(self):

        self.buildings_batch.draw()

        label = pyglet.text.Label(self.name,
                                  font_name='Times New Roman',
                                  font_size=36,
                                  x=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT // 2,
                                  anchor_x='center', anchor_y='center')

        label.draw()