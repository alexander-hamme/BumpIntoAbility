import math


def distance_between(obj1, obj2):

    if not hasattr(obj1, "center_x") and hasattr(obj1, "center_y"):
        raise TypeError(f"Object of type <{obj1.__class__}> does not have x and y attributes")

    elif not hasattr(obj2, "center_x") and hasattr(obj2, "center_y"):
        raise TypeError(f"Object of type <{obj1.__class__}> does not have x and y attributes")

    return math.pow(math.pow(obj1.center_x - obj2.center_x, 2) + math.pow(obj1.center_y - obj2.center_y, 2), 0.5)
