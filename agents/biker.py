import random

import pyglet

from utils import CONFIG_DICT
from agents.agent import Agent

WINDOW_WIDTH = CONFIG_DICT.get("window_width")
WINDOW_HEIGHT = CONFIG_DICT.get("window_height")


class Biker(Agent):

    BIKER_IMG_1 = pyglet.image.load('resources/images/bike_1_small.png')
    BIKER_IMG_2 = pyglet.image.load('resources/images/bike_2_small.png')

    def __init__(self, x, y):
        super().__init__()
        self._bot_left_x = x
        self._bot_left_y = y
        self.vx = 0
        self.vy = 0
        self.dx = 0   # distance from current destination
        self.dy = 0   # ''
        self.image = random.choice((Biker.BIKER_IMG_1, Biker.BIKER_IMG_2))
        self.width = self.image.width
        self.height = self.image.height
        self.x = self._bot_left_x + self.image.width // 2
        self.y = self._bot_left_y - self.image.height // 2
        self.sprite = None

    def render(self, batch):
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.x, y=self.y, batch=batch)
        # return self.sprite

    def do_biking(self):
        dx = random.uniform(-1, 1)#(1,5)
        dy = 5 * random.random()#randint(1,5)

        self._bot_left_x += dx
        self._bot_left_y += dy
        self.x += dx
        self.y += dy

        self.do_bounds_check()

        self.sprite.x = self.x
        self.sprite.y = self.y

    def reset_center_coords(self):
        self.x = self._bot_left_x - self.image.width // 2
        self.y = self._bot_left_y - self.image.height // 2

    def do_bounds_check(self):

        if self._bot_left_x >= WINDOW_WIDTH:
            self._bot_left_x = self._bot_left_x % WINDOW_WIDTH
        elif self._bot_left_x <= 0:
            self._bot_left_x = self._bot_left_x + WINDOW_WIDTH

        if self._bot_left_y >= WINDOW_HEIGHT:
            self._bot_left_y = self._bot_left_y % WINDOW_HEIGHT
        elif self._bot_left_y <= 0:
            self._bot_left_y = self._bot_left_y + WINDOW_HEIGHT

        self.reset_center_coords()

    def update(self, dt):
        self.do_biking()
    # def draw(self):
    #     self.sprite.draw()

