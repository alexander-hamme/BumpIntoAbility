import random

import pyglet
from pyglet import shapes

from agents import CONFIG_DICT
from agents.biker import Biker
from agents.map import Map
from agents.pedestrian import Pedestrian

WINDOW_WIDTH = CONFIG_DICT.get("window_width")
WINDOW_HEIGHT = CONFIG_DICT.get("window_height")


class City:

    def __init__(self):
        self.map = Map("Test")

        self.bikers = []
        self.biker_batch = pyglet.graphics.Batch()
        self.pedestrians = []
        self.pedestrian_batch = pyglet.graphics.Batch()
        self.render()

    def add_bikers(self):
        for i in range(12):
            biker = Biker(random.randint(20, WINDOW_WIDTH - 20), random.randint(20, WINDOW_HEIGHT - 20))
            biker.render(self.biker_batch)
            self.bikers.append(biker)

    def add_pedestrians(self):
        for i in range(12):
            pedestrian = Pedestrian(random.randint(20, WINDOW_WIDTH - 20), random.randint(20, WINDOW_HEIGHT - 20)) #(i * 53, WINDOW_HEIGHT - (i * 31))
            pedestrian.render(self.pedestrian_batch)
            self.pedestrians.append(pedestrian)

    def render(self):
        self.add_bikers()
        self.add_pedestrians()
        self.map.render()
        self.create_backdrop()

    def create_backdrop(self):
        self.backdrop = pyglet.shapes.Rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, color=(230, 255, 240))
        self.backdrop.opacity = 255

    def draw(self):
        self.backdrop.draw()
        self.map.draw()
        self.biker_batch.draw()
        self.pedestrian_batch.draw()

    def run(self, dt):
        for biker in self.bikers:
            biker.update(dt)
        for pedestrian in self.pedestrians:
            pedestrian.update(dt)
        self.draw()

