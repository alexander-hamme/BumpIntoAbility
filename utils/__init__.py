import math

import yaml

with open("resources/config.yaml", "r") as f:
    CONFIG_DICT = yaml.load(f, Loader=yaml.Loader)

def distance_between(obj1, obj2):

    if not hasattr(obj1, "center_x") and hasattr(obj1, "center_y"):
        raise TypeError(f"Object of type <{obj1.__class__}> does not have x and y attributes")

    elif not hasattr(obj2, "center_x") and hasattr(obj2, "center_y"):
        raise TypeError(f"Object of type <{obj1.__class__}> does not have x and y attributes")

    return math.pow(math.pow(obj1.x - obj2.x, 2) + math.pow(obj1.y - obj2.y, 2), 0.5)
