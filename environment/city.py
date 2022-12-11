import math
import random

import numpy as np
import pyglet

import utils
from utils import CONFIG_DICT
from agents.biker import Biker
from environment.map import Map
from agents.pedestrian import Pedestrian
from physics import update_forces

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
        self.force_vectors = []

        self.agents = []  # all agents

        self.agents_matrix = None  # x, y, vx, vy, dx, dy, tau

        self.render()

    def add_bikers(self):
        for i in range(0):
            biker = Biker(random.randint(20, WINDOW_WIDTH - 20), random.randint(20, WINDOW_HEIGHT - 20))
            biker.render(self.biker_batch)
            self.bikers.append(biker)
            self.agents.append(biker)

    def add_pedestrians(self):
        for i in range(1):
            pedestrian = Pedestrian(random.randint(20, WINDOW_WIDTH - 20), random.randint(20, WINDOW_HEIGHT - 20)) #(i * 53, WINDOW_HEIGHT - (i * 31))
            pedestrian.render(self.pedestrian_batch)
            self.pedestrians.append(pedestrian)
            self.agents.append(pedestrian)

    def render(self):
        self.add_bikers()
        self.add_pedestrians()
        self.map.render()
        self.create_backdrop()
        self.init_matrix()

    def init_matrix(self):
        self.agents_matrix = np.zeros((len(self.agents), 7))    # x, y, vx, vy, dx, dy, tau
        self.update_matrix()

    def update_matrix(self):
        self.agents_matrix = np.asarray([[a.x, a.y, a.vx, a.vy, a.dx, a.dy, a.TAU] for a in self.agents])

    def apply_matrix(self):
        for agent_list, agent in zip(self.agents_matrix.tolist(), self.agents):
            agent.vx = agent_list[2]
            agent.vy = agent_list[3]

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
            pyglet.shapes.Circle(pedestrian._bot_left_x, pedestrian._bot_left_y, 3, color=(0, 255, 0)).draw()
        for biker in self.bikers:
            pyglet.shapes.Circle(biker._bot_left_x, biker._bot_left_y, 3, color=(0, 255, 0)).draw()

        for v_line in self.force_vectors:
            v_line.draw()

        if len(self.collision_stars) > 0:
            pass


    def run(self, dt):

        self.collision_stars.clear()
        self.force_vectors.clear()

        self.update_matrix()

        update_forces(self.agents, self.agents_matrix)

        self.apply_matrix()

        for agent in self.agents:

            for pedestrian in self.pedestrians:
                if pedestrian is agent:
                    continue

                if utils.distance_between(agent, pedestrian) <= (agent.width):
                    # print("collision!")

                    collision_star = pyglet.shapes.Star((agent.x + pedestrian.x) // 2,
                                                        (agent.y + pedestrian.y) // 2,
                                                        outer_radius=5, inner_radius=7, num_spikes=7,
                                                        rotation=15, color=(255, 0, 50))
                    self.collision_stars.append(collision_star)

            for biker in self.bikers:
                if biker is agent:
                    continue

                if utils.distance_between(agent, biker) <= (agent.width < 2):
                    print("collision!")
                    collision_star = pyglet.shapes.Star((agent._bot_left_x + biker._bot_left_x) // 2, (agent._bot_left_y + biker._bot_left_y) // 2,
                                                        outer_radius=6, inner_radius=10, num_spikes=7,
                                                        rotation=15, color=(255, 0, 50))
                    self.collision_stars.append(collision_star)

            if agent.fx is not None and agent.fy is not None:
                angle = math.atan2(agent.fy, agent.fx)

                x = 5 * math.cos(angle)
                y = 5 * math.sin(angle)

                self.force_vectors.append(
                    pyglet.shapes.Line(agent.x, agent.y, agent.x + x, agent.y + y, width=3, color=(255,0,0), batch=None)
                )
            agent.update(dt)

        # for pedestrian in self.pedestrians:
        #     pedestrian.update(dt)
        self.draw()

