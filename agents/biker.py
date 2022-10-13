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
        self.image = random.choice((Biker.BIKER_IMG_1, Biker.BIKER_IMG_2))
        self.width = self.image.width
        self.height = self.image.height
        self.center_x = self.x + self.image.width//2
        self.center_y = self.y - self.image.height//2
        self.sprite = None

    def render(self, batch):
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.center_x, y=self.center_y, batch=batch)
        # return self.sprite

    def do_biking(self):
        dx = random.uniform(-1, 1)#(1,5)
        dy = 5 * random.random()#randint(1,5)

        self.x += dx
        self.y += dy
        self.center_x += dx
        self.center_y += dy

        self.do_bounds_check()

        self.sprite.x = self.center_x
        self.sprite.y = self.center_y

    def reset_center_coords(self):
        self.center_x = self.x - self.image.width//2
        self.center_y = self.y - self.image.height//2

    def do_bounds_check(self):

        if self.x >= WINDOW_WIDTH:
            self.x = self.x % WINDOW_WIDTH
        elif self.x <= 0:
            self.x = self.x + WINDOW_WIDTH

        if self.y >= WINDOW_HEIGHT:
            self.y = self.y % WINDOW_HEIGHT
        elif self.y <= 0:
            self.y = self.y + WINDOW_HEIGHT

        self.reset_center_coords()

    def update(self, dt):
        self.do_biking()
    # def draw(self):
    #     self.sprite.draw()

