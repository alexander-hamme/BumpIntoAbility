from abc import ABC, abstractmethod
from typing import List

import pyglet.sprite
from pyglet.math import Vec2


class Agent(ABC):

    # noinspection PyTypeChecker
    def __init__(self):
        self.x: int = None
        self.y: int = None
        self.width: int = None
        self.height: int = None

        self.center_x: int = None
        self.center_y: int = None

        self.sprite: pyglet.sprite.Sprite = None

        self.force_vectors: List[Vec2] = None

    @abstractmethod
    def render(self, batch):
        pass

    @abstractmethod
    def update(self, dt):
        pass
