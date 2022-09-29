import random

import pyglet

from agents import CONFIG_DICT

WINDOW_WIDTH = CONFIG_DICT.get("window_width")
WINDOW_HEIGHT = CONFIG_DICT.get("window_height")


class Biker:

    BIKER_IMG_1 = pyglet.image.load('resources/images/bike_1_small.png')
    BIKER_IMG_2 = pyglet.image.load('resources/images/bike_2_small.png')

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = None

    def render(self, batch):
        self.sprite = pyglet.sprite.Sprite(random.choice((Biker.BIKER_IMG_1, Biker.BIKER_IMG_2)),
                                           x=self.x, y=self.y, batch=batch)
        # return self.sprite

    def do_biking(self):
        self.x += random.uniform(-1, 1)#(1,5)
        self.y += 5 * random.random()#randint(1,5)

        self.do_bounds_check()

        self.sprite.x = self.x
        self.sprite.y = self.y

    def do_bounds_check(self):

        if self.x >= WINDOW_WIDTH:
            self.x = self.x % WINDOW_WIDTH
        elif self.x <= 0:
            self.x = self.x + WINDOW_WIDTH

        if self.y >= WINDOW_HEIGHT:
            self.y = self.y % WINDOW_HEIGHT
        elif self.y <= 0:
            self.y = self.y + WINDOW_HEIGHT

    def update(self, dt):
        self.do_biking()
    # def draw(self):
    #     self.sprite.draw()

