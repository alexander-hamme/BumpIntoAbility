import math

# from pyglet.math import Vec2

# class Force2DVector:
#
#     def __init__(self):
#         self.fx = None
#         self.fy = None
#
#     def set_components(self, x, y):
#         self.fx = x
#         self.fy = y
#
#     def set_vector(self, magnitude, theta_deg):
#         theta = math.radians(theta_deg)
#         self.fx = magnitude * math.cos(theta)
#         self.fy = magnitude * math.sin(theta)


def calculate_forces(list_of_agents):

    array = []

    for agent in list_of_agents:
        required_attributes = {"center_x", "center_y", "width", "height"}

        if not all(hasattr(agent, a) for a in required_attributes):
            missing_attributes = required_attributes - set(agent.__dir__())
            raise AttributeError(f"{agent.__class__.__name__} object missing "
                                 f"attribute{'s' if len(missing_attributes) > 1 else ''} "
                                 f"{missing_attributes}")