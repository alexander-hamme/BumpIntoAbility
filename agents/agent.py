from abc import ABC, abstractmethod
from typing import List

import pyglet.sprite
from pyglet.math import Vec2

from utils import CONFIG_DICT


class Agent(ABC):

    TAU = CONFIG_DICT["forces"]["scene"]["tau"]

    # noinspection PyTypeChecker
    def __init__(self):
        self._bot_left_x: int = None
        self._bot_left_y: int = None
        self.vx: float = None
        self.vy: float = None
        self.dx: float = None
        self.dy: float = None

        self.width: int = None
        self.height: int = None

        self.x: int = None  # center x
        self.y: int = None  # center y

        self.tau = Agent.TAU

        self.sprite: pyglet.sprite.Sprite = None

        self.force_vectors: List[Vec2] = None

    @abstractmethod
    def render(self, batch):
        pass

    @abstractmethod
    def update(self, dt):
        pass
