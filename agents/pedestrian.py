import random

import pyglet

from utils import CONFIG_DICT
from agents.agent import Agent

WINDOW_WIDTH = CONFIG_DICT.get("window_width")
WINDOW_HEIGHT = CONFIG_DICT.get("window_height")


class Pedestrian(Agent):

    PEDESTRIAN_IMG = pyglet.image.load('resources/images/pedestrian_1.png')

    def __init__(self, x, y):
        super().__init__()
        self._bot_left_x = x
        self._bot_left_y = y
        self.vx = 0
        self.vy = 0
        self.dx = 0   # distance from current destination
        self.dy = 0   # ''

        self.image = Pedestrian.PEDESTRIAN_IMG
        self.width = self.image.width
        self.height = self.image.height

        self.x = self._bot_left_x + self.image.width
        self.y = self._bot_left_y - self.image.height // 2   # sprite starts from bottom left

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

    def render(self, batch):
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.x, y=self.y, batch=batch)

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

        self._bot_left_x = self._bot_left_x + self.vx * dt  # x1 = x0 + v0 * dt
        self._bot_left_y = self._bot_left_y + self.vy * dt  # x1 = x0 + v0 * dt

        self.do_bounds_check()

        self.reset_center_coords()

        self.sprite.x = self.x
        self.sprite.y = self.y

    def do_bounds_check(self):

        ''' Pass to other side version
        if self._bot_left_x >= WINDOW_WIDTH:
            self._bot_left_x = self._bot_left_x % WINDOW_WIDTH
        elif self._bot_left_x <= 0:
            self._bot_left_x = self._bot_left_x + WINDOW_WIDTH

        if self._bot_left_y >= WINDOW_HEIGHT:
            self._bot_left_y = self._bot_left_y % WINDOW_HEIGHT
        elif self._bot_left_y <= 0:
            self._bot_left_y = self._bot_left_y + WINDOW_HEIGHT
        '''
        pass


    def reset_center_coords(self):
        self.x = self._bot_left_x - self.image.width // 2
        self.y = self._bot_left_y - self.image.height // 2

    def update(self, dt):
        self.do_walking(dt)
