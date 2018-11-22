import cords_calc as calc
import data
import rospy
from geometry_msgs.msg import Twist
import math

pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)


# Return true when reached the point
def move():
    rel_positions = calc.relative_positions()
    vel = Twist()

    x_min = data.params['cord_x'] - data.params['cord_range']
    x_max = data.params['cord_x'] + data.params['cord_range']
    y_max = data.params['cord_y'] + data.params['cord_range']
    y_min = data.params['cord_y'] - data.params['cord_range']

    # Deal with objects with Sonar
    if data.params['type_sensor'] == "sonar":
        pos_x = rel_positions['sonar_front_x']
        pos_y = rel_positions['sonar_front_y']

    # Deal with objects with Lase
    else:
        pos_x = rel_positions['laser_x']
        pos_y = rel_positions['laser_y']

    # If point is reached
    if (x_min <= data.abs_position_x <= x_max and
            y_min <= data.abs_position_y <= y_max):

        print "CHEGUEEEI !!!!"
        return True

    # Deal with volocity to reach a point(x,y)
    else:

        new_waypoint()

        yaw_range = math.pi / 45

        if data.yaw + yaw_range > calc.waypoint_yaw() > data.yaw - yaw_range:
            vel.linear.x = 1.0
            vel.angular.z = 0
            # print "Na direcao certa"
        elif not calc.in_range_of_collision(pos_x, pos_y, 1.1, 2.1):
            vel.linear.x = 0
            if abs(calc.waypoint_yaw() - data.yaw) >= math.pi:
                vel.angular.z = calc.waypoint_yaw() > data.yaw and -0.5 or 0.5
            else:
                vel.angular.z = calc.waypoint_yaw() > data.yaw and 0.5 or -0.5
            # print "Re direcinando"
        else:
            vel.linear.x = 1
            vel.angular.z = 0
            # print "Em rota de colisao"

        # Evit collisions
        if calc.in_range_of_collision(pos_x, pos_y, 1, 2):
            vel.angular.z = 1 / (pos_x / 2) * 5
            # print "Desviando"

    pub.publish(vel)

    return False


# Calculate the intermediary point based in the quantity of distant points
# EXAMPLE: 10 points side by side with distances similar (bean with ang great enough)
def new_waypoint():
    n_ranges = 10
    min_distance = 3
    potential_ranges = []  # x and y of each range and pontuations of how mutch better is the range

    # Filter ranges search for spaces to go
    for index in range(len(data.hokuyo_ranges) - n_ranges):
        is_potential = True

        for i in range(n_ranges):
            if data.hokuyo_ranges[index + i] < min_distance:
                is_potential = False

        if is_potential:
            distance = data.hokuyo_ranges[index + n_ranges / 2]
            ang = (((index + n_ranges / 2) * data.hokuyo_ang_inc) - (math.pi * 135 / 180)) + data.yaw

            potential_ranges = potential_ranges + [{'p_x': data.abs_position_x + distance * math.cos(ang),
                                                    'p_y': data.abs_position_y + distance * math.sin(ang),
                                                    'distance': distance,
                                                    'ang': ang}]

    if len(potential_ranges) > 0:

        # Calculate the pontuation of the pontential ranges
        for index, value in enumerate(potential_ranges):
            if value['ang'] > math.pi:
                value['ang'] = value['ang'] - 2 * math.pi
            elif value['ang'] < -math.pi:
                value['ang'] = value['ang'] + 2 * math.pi

            potential_ranges[index]['pontuation'] = abs(calc.desired_yaw() - value['ang'])

        # Ordenate and get the better way, based in his pontuation
        better_pontuation = sorted(potential_ranges, key=lambda k: k['pontuation'])

        data.params['waypoint_x'] = better_pontuation[0]['p_x']
        data.params['waypoint_y'] = better_pontuation[0]['p_y']

    else:
        data.params['waypoint_x'] = data.params['cord_x']
        data.params['waypoint_y'] = data.params['cord_y']
