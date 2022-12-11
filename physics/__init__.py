from typing import Tuple

import numpy as np
from numba import njit
from pyglet.math import Vec2

from physics import states
from utils import CONFIG_DICT
from physics.potentials import PedPedPotential

# Todo consider the destination portion of this paper too: https://arxiv.org/pdf/cond-mat/9805244.pdf
force_params = CONFIG_DICT.get("forces")


# For reference:  https://github.com/yuxiang-gao/PySocialForce/blob/master/examples/example.py



def update_forces(agents, agents_matrix):

    # big_matrix = (x, y, v_x, v_y, d_x, d_y, [tau])

    # n_agents = len(list_of_agents)
    # force_matrix = np.zeros(n_agents)
    # for force_function in all_forces:
    ww = CONFIG_DICT["window_width"]
    wh = CONFIG_DICT["window_height"]
    # obstacles = [
    #     [[0, 0], [ww, 0]],
    #     [[0,0], [wh, 0]],
    #     [[ww, 0], [ww, wh]],
    #     [[0, wh], [ww, wh]]
    # ]

    # list of linear obstacles given in the form of
    # (x_min, x_max, y_min, y_max)
    obstacles = [
        [0, ww, 0, 0],
        [0, 0, 0, wh],
        [ww, ww, 0, wh],
        [0, ww, wh, wh]
    ]

    avoid = get_obstacle_avoid_force(agents, obstacles)

    if np.sum(avoid) > 0:
        print(avoid)

    # return avoid + get_agent_repulsion_forces(agents_matrix)
    return avoid




@njit
def desired_directions(state: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:

    # state is pedestrian info:
    # (x, y, v_x, v_y, d_x, d_y, [tau])   tau is relaxation time

    """Given the current state and destination, compute desired direction."""
    destination_vectors = state[:, 4:6] - state[:, 0:2]
    directions, dist = normalize(destination_vectors)
    return directions, dist

@njit
def normalize(vectors: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Normalize nx2 array along the second axis
    input: [n,2] ndarray
    output: (normalized vectors, norm factors)
    """
    norm_factors = []
    for line in vectors:
        norm_factors.append(np.linalg.norm(line))
    norm_factors = np.array(norm_factors)
    normalized = vectors / np.expand_dims(norm_factors, -1)
    # get rid of nans
    for i in range(norm_factors.shape[0]):
        if norm_factors[i] == 0:
            normalized[i] = np.zeros(vectors.shape[1])
    return normalized, norm_factors


def get_agent_repulsion_forces(big_matrix):
    potential_func = PedPedPotential(
        force_params["scene"]["step_width"],
        v0=force_params["ped_repulsive_force"]["v0"],
        sigma=force_params["ped_repulsive_force"]["sigma"]
    )
    f_ab = -1.0 * potential_func.grad_r_ab(big_matrix)

    fov = FieldOfView(phi=force_params["ped_repulsive_force"]["fov_phi"],
                      out_of_view_factor=force_params["ped_repulsive_force"]["fov_factor"])
    w = np.expand_dims(fov(desired_directions(big_matrix), -f_ab), -1)
    F_ab = w * f_ab
    return np.sum(F_ab, axis=1) * force_params["ped_repulsive_force"]["factor"]



all_forces = [
    get_agent_repulsion_forces,
    # get_wall_avoid_force,
]





class FieldOfView(object):
    """Compute field of view prefactors.

    The field of view angle twophi is given in degrees.
    out_of_view_factor is C in the paper.
    """

    def __init__(self, phi=None, out_of_view_factor=None):
        phi = phi or 100.0
        out_of_view_factor = out_of_view_factor or 0.5
        self.cosphi = np.cos(phi / 180.0 * np.pi)
        self.out_of_view_factor = out_of_view_factor

    def __call__(self, desired_direction, forces_direction):
        """Weighting factor for field of view.

        desired_direction : e, rank 2 and normalized in the last index.
        forces_direction : f, rank 3 tensor.
        """
        in_sight = (
            np.einsum("aj,abj->ab", desired_direction, forces_direction)
            > np.linalg.norm(forces_direction, axis=-1) * self.cosphi
        )
        out = self.out_of_view_factor * np.ones_like(in_sight)
        out[in_sight] = 1.0
        np.fill_diagonal(out, 0.0)
        return out


def get_obstacle_avoid_force(agents, obstacles):
    sigma = CONFIG_DICT["forces"]["obstacle_force"]["sigma"]
    threshold = CONFIG_DICT["forces"]["obstacle_force"]["threshold"]
    force = np.zeros((len(agents), 2))
    if len(obstacles) == 0:
        return force
    # obstacles = np.vstack(obstacles)   # todo can this happen earlier
    pos = np.asarray([[a.x, a.y] for a in agents])


    # Obstacles is turned into a flattened array of all line points,
    # with no differentiation between obstacles

    # is this a good approach? maybe...


    # obstacles can be put back to a list of discrete points?


    # TODO    Window bounds should be a separate calculation, not part of obstacles

    for i, a in enumerate(agents):
        ww = CONFIG_DICT["window_width"]
        wh = CONFIG_DICT["window_height"]
        a_width_thresh = a.width / 2
        a_height_thresh = a.height / 2

        # get distance away, including agent dimensions
        # normalize the values
        # multiple by np.exp(reverse sign of values)

        bounds_distances = np.asarray([
            [a.x - a_width_thresh - 0, a.y - a_height_thresh],
            [(a.x + a_width_thresh) - ww, (a.y + a_height_thresh) - wh]
            # [a.x - a_width_thresh - 0, wh - (a.y + a_height_thresh)],
            # [ww - (a.x + a_width_thresh), a.y - a_height_thresh]
        ], dtype=float)

        # bounds_distances[bounds_distances < 0] = 0

        print(f"bd = {bounds_distances}")

        directions, dist = states.normalize(bounds_distances)

        print(directions, dist)

        _thresh = 2 * (threshold + ((a.width + a.height) / 2))

        print(threshold, _thresh, a.width, a.height)

        # if np.all(dist >= _thresh):
        #     continue

        dist_mask = dist < _thresh
        print(dist_mask)
        print(directions[dist_mask])
        directions[dist_mask] *= np.exp(-dist[dist_mask].reshape(-1, 1) / sigma)

        print(directions[dist_mask])

        force[i] = np.sum(directions[dist_mask], axis=0)
        a.fx, a.fy = np.sum(directions[dist_mask], axis=0)

        print(force[i])

    # print(f"pos={pos}")

    return force * CONFIG_DICT["forces"]["obstacle_force"]["factor"]


    # force is calculated by summing the vectors from all the nearest points to get a vector pointing away

    # you could repeat this and filter the points ahead of time to only include close ones, PLUS subsample the points for fewer calculations

    # Do you need to pick 3 closest points (with some min dist between them?)


    for i, (p, a) in enumerate(zip(pos, agents)):

        print(p)

        _thresh = threshold + (a.width + a.height) / 2   # todo handle individually
        diff = p - obstacles
        directions, dist = states.normalize(diff)
        dist = dist - (a.width + a.height) / 2
        if np.all(dist >= _thresh):
            continue

        '''
        np.asarray([[1,2],[3,4]]) * np.asarray([10,100])
        array([[ 10, 200],
               [ 30, 400]])
        np.asarray([[1,2],[3,4]]) * np.asarray([10,100]).reshape(-1,1)
        array([[ 10,  20],
               [300, 400]])
        '''

        dist_mask = dist < _thresh
        directions[dist_mask] *= np.exp(-dist[dist_mask].reshape(-1, 1) / sigma)
        force[i] = np.sum(directions[dist_mask], axis=0)

    return force * CONFIG_DICT["forces"]["obstacle_force"]["factor"]




def _get_wall_avoid_force(agent, x1_bound, y1_bound, x2_bound, y2_bound) -> Vec2:
    """
    Can be used for avoiding both game window bounds and stationary objects such as buildings
    :param agent:
    :param x1_bound:
    :param y1_bound:
    :param x2_bound:
    :param y2_bound:
    :return:
    """

    required_attributes = {"center_x", "center_y", "width", "height"}

    if not all(hasattr(agent, a) for a in required_attributes):
        missing_attributes = required_attributes - set(agent.__dir__())
        raise AttributeError(f"{agent.__class__.__name__} object missing "
                             f"attribute{'s' if len(missing_attributes) > 1 else ''} "
                             f"{missing_attributes}")

    if agent.x < x1_bound + (agent.width / 2.0):   # agent edge has passed the x1_bound
        x_multiplier = 1
    elif agent.x > x2_bound - (agent.width / 2.0):
        x_multiplier = -1
    else:
        x_multiplier = 0

    # Pyglet y-axis increases up not down!
    if agent.y < y1_bound + (agent.height / 2.0):   # agent edge has passed the x1_bound
        y_multiplier = 1
    elif agent.y > y2_bound - (agent.height / 2.0):
        y_multiplier = -1
    else:
        y_multiplier = 0

    if x_multiplier == y_multiplier == 0:
        return Vec2(0, 0)

    x_component = 0

    """

        // x component of Force increases as Gnat gets closer to obstacle
        double x_component = (x_multiplier == 1) ? prox_x - centerx : (x_multiplier == -1) ?
                (prox_x - (WINDOW_BOUNDS_X - centerx))
                : 0.0;

        // same with y component
        double y_component = (y_multiplier == 1) ? prox_y - centery : (y_multiplier == -1) ?
                (prox_y - (WINDOW_BOUNDS_Y - centery))
                : 0.0;

        x_component *= 0.5 * x_multiplier;
        y_component *= 0.5 * y_multiplier;"""