import random

import pyglet

from agents import CONFIG_DICT
from agents.agent import Agent

WINDOW_WIDTH = CONFIG_DICT.get("window_width")
WINDOW_HEIGHT = CONFIG_DICT.get("window_height")


class Pedestrian(Agent):

    PEDESTRIAN_IMG = pyglet.image.load('resources/images/pedestrian_1.png')

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = Pedestrian.PEDESTRIAN_IMG
        self.width = self.image.width
        self.height = self.image.height

        self.center_x = self.x + self.image.width
        self.center_y = self.y - self.image.height//2   # sprite starts from bottom left

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

    def render(self, batch):
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.center_x, y=self.center_y, batch=batch)

    def do_walking(self, dt):

        max_v_mag = 70  # max velocity magnitude

        self.vx += random.uniform(-max_v_mag/5, max_v_mag/5)
        self.vy += random.uniform(-max_v_mag/7, max_v_mag/7)#randint(1,5)

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

        self.reset_center_coords()

        self.sprite.x = self.center_x
        self.sprite.y = self.center_y

    def do_bounds_check(self):

        if self.x >= WINDOW_WIDTH:
            self.x = self.x % WINDOW_WIDTH
        elif self.x <= 0:
            self.x = self.x + WINDOW_WIDTH

        if self.y >= WINDOW_HEIGHT:
            self.y = self.y % WINDOW_HEIGHT
        elif self.y <= 0:
            self.y = self.y + WINDOW_HEIGHT

    def reset_center_coords(self):
        self.center_x = self.x - self.image.width//2
        self.center_y = self.y - self.image.height//2

    def update(self, dt):
        self.do_walking(dt)
