import data
import math
import graph


# Calculates the desired yaw to reach the point
def desired_yaw():
    co = data.params['coord_y'] - data.abs_position_y
    ca = data.params['coord_x'] - data.abs_position_x

    return math.atan2(co, ca)


# Calculates the necessary yaw to reach the waypoint
def waypoint_yaw():
    co = data.params['waypoint_y'] - data.abs_position_y
    ca = data.params['waypoint_x'] - data.abs_position_x

    return math.atan2(co, ca)


# Calculates the necessary yaw to reach any point x,y
def yaw_to_point(x, y):
    co = y - data.abs_position_y
    ca = x - data.abs_position_x

    return math.atan2(co, ca)


# Calculates if the point (x,y) is in range of collision with a rectangular object formed by range(x,y)
def in_range_of_collision(p_x, p_y, range_x=1, range_y=3):
    if p_y > 0:
        return abs(p_x) < range_x and p_y < range_y

    return False


# Calculates the distance between two points
def distance_between_points((p1_x, p1_y), (p2_x, p2_y)):
    ca = p1_x - p2_x
    co = p1_y - p2_y

    return math.sqrt(pow(ca, 2) + pow(co, 2))


# ------------------ Calc Position ------------------
# RETURN:
# rel_positions:
#   - sonar_front_x
#   - sonar_front_y
#   - laser_x
#   - laser_y

def relative_positions():
    rel_positions = {}
    rel_positions['sonar_front_x'] = math.cos(data.front_min_ang) * data.front_min
    rel_positions['sonar_front_y'] = math.sin(data.front_min_ang) * data.front_min
    rel_positions['laser_x'] = math.sin(data.hokuyo_min_ang) * data.hokuyo_min
    rel_positions['laser_y'] = math.cos(data.hokuyo_min_ang) * data.hokuyo_min

    return rel_positions

# ------------------ End Calc Position ------------------
