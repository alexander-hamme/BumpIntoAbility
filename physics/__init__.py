from pyglet.math import Vec2

def get_wall_avoid_force(agent, x1_bound, y1_bound, x2_bound, y2_bound):
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

    if agent.center_x < x1_bound + (agent.width / 2.0):   # agent edge has passed the x1_bound
        x_multiplier = 1
    elif agent.center_x > x2_bound - (agent.width / 2.0):
        x_multiplier = -1
    else:
        x_multiplier = 0

    # Pyglet y-axis increases up not down!
    if agent.center_y < y1_bound + (agent.height / 2.0):   # agent edge has passed the x1_bound
        y_multiplier = 1
    elif agent.center_y > y2_bound - (agent.height / 2.0):
        y_multiplier = -1
    else:
        y_multiplier = 0

    if x_multiplier == y_multiplier == 0:


    """
            double prox_x = img_width / 2.0;
        double prox_y = img_height / 2.0;

        int centerx = this.x + (int) Math.round(prox_x);
        int centery = this.y + (int) Math.round(prox_y);

        int x_multiplier = (centerx < prox_x) ? 1 : (centerx > WINDOW_BOUNDS_X - prox_x) ? -1 : 0;
        int y_multiplier = (centery < prox_y) ? 1 : (centery > WINDOW_BOUNDS_Y - prox_y) ? -1 : 0;


        if (x_multiplier == 0 && y_multiplier == 0) {
            obstacle_avoidance.setMagnitude(0.0);
            return;
        }

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