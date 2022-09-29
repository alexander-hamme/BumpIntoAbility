import random

import pyglet

from agents import CONFIG_DICT

WINDOW_WIDTH = CONFIG_DICT.get("window_width")
WINDOW_HEIGHT = CONFIG_DICT.get("window_height")


class Pedestrian:

    PEDESTRIAN_IMG = pyglet.image.load('resources/images/pedestrian_1.png')

    def __init__(self, x, y):
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.x = x
        self.y = y
        self.sprite = None

    def render(self, batch):
        self.sprite = pyglet.sprite.Sprite(Pedestrian.PEDESTRIAN_IMG, x=self.x, y=self.y, batch=batch)

    def do_walking(self, dt):

        max_v_mag = 70  # max velocity magnitude

        self.vx += random.uniform(-max_v_mag/2, max_v_mag/2)
        self.vy += random.uniform(-max_v_mag/3, max_v_mag/3)#randint(1,5)

        # threshold to max allowed, keeping sign
        if self.vx < 0:
            self.vx = max(-max_v_mag, self.vx)
        elif self.vx > 0:
            self.vx = min(max_v_mag, self.vx)

        if self.vy < 0:
            self.vy = max(-max_v_mag, self.vy)
        elif self.vy > 0:
            self.vy = min(max_v_mag, self.vy)

        self.x = self.x + self.vx * dt  # x1 = x0 + v0 * dt
        self.y = self.y + self.vy * dt  # x1 = x0 + v0 * dt

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
        self.do_walking(dt)
