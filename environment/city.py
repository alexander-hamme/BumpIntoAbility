import random

import pyglet

import utils
from agents import CONFIG_DICT
from agents.biker import Biker
from environment.map import Map
from agents.pedestrian import Pedestrian

WINDOW_WIDTH = CONFIG_DICT.get("window_width")
WINDOW_HEIGHT = CONFIG_DICT.get("window_height")


class City:

    def __init__(self, name):
        self.map = Map(name)

        self.bikers = []
        self.biker_batch = pyglet.graphics.Batch()
        self.pedestrians = []
        self.pedestrian_batch = pyglet.graphics.Batch()
        self.collision_stars = []

        self.agents = []  # all agents

        self.render()

    def add_bikers(self):
        for i in range(12):
            biker = Biker(random.randint(20, WINDOW_WIDTH - 20), random.randint(20, WINDOW_HEIGHT - 20))
            biker.render(self.biker_batch)
            self.bikers.append(biker)
            self.agents.append(biker)

    def add_pedestrians(self):
        for i in range(12):
            pedestrian = Pedestrian(random.randint(20, WINDOW_WIDTH - 20), random.randint(20, WINDOW_HEIGHT - 20)) #(i * 53, WINDOW_HEIGHT - (i * 31))
            pedestrian.render(self.pedestrian_batch)
            self.pedestrians.append(pedestrian)
            self.agents.append(pedestrian)

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
        for star in self.collision_stars:
            star.draw()

        for pedestrian in self.pedestrians:
            pyglet.shapes.Circle(pedestrian.x, pedestrian.y, 3, color=(0, 255, 0)).draw()
        for biker in self.bikers:
            pyglet.shapes.Circle(biker.x, biker.y, 3, color=(0, 255, 0)).draw()

        if len(self.collision_stars) > 0:
            pass

    def run(self, dt):

        self.collision_stars.clear()

        for agent in self.agents:

            for pedestrian in self.pedestrians:
                if pedestrian is agent:
                    continue

                if utils.distance_between(agent, pedestrian) <= (agent.width):
                    # print("collision!")

                    collision_star = pyglet.shapes.Star((agent.center_x + pedestrian.center_x)//2,
                                                        (agent.center_y + pedestrian.center_y)//2,
                                                        outer_radius=5, inner_radius=7, num_spikes=7,
                                                        rotation=15, color=(255, 0, 50))
                    self.collision_stars.append(collision_star)

            for biker in self.bikers:
                if biker is agent:
                    continue

                if utils.distance_between(agent, biker) <= (agent.width < 2):
                    print("collision!")
                    collision_star = pyglet.shapes.Star((agent.x + biker.x)//2, (agent.y + biker.y)//2,
                                                        outer_radius=6, inner_radius=10, num_spikes=7,
                                                        rotation=15, color=(255, 0, 50))
                    self.collision_stars.append(collision_star)

            agent.update(dt)

        # for pedestrian in self.pedestrians:
        #     pedestrian.update(dt)
        self.draw()

