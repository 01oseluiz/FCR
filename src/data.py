import rospy
import math
from sensor_msgs.msg import LaserScan  # To /sonar_front, /sonar_back, /hokuyo_scan
from nav_msgs.msg import Odometry  # To /pose
from tf.transformations import euler_from_quaternion, quaternion_from_euler

# --- Class Variables - DATA ----

front_min = None
front_min_ang = None
back_min = None
back_min_ang = None
hokuyo_min = None
hokuyo_min_ang = None
hokuyo_ranges = None
hokuyo_ang_inc = None
abs_position_x = None
abs_position_y = None
abs_position_z = None
roll = None
pitch = None
yaw = None

params = {'type_sensor': 'lase',
          'cord_x': 0,
          'cord_y': 0,
          'cord_range': 0.1,
          'waypoint_x': 0,
          'waypoint_y': 0}


def initialize():
    rospy.Subscriber("sonar_front", LaserScan, callback_sonar_front)
    rospy.Subscriber("sonar_back", LaserScan, callback_sonar_back)
    rospy.Subscriber("hokuyo_scan", LaserScan, callback_hokuyo_scan)
    rospy.Subscriber("pose", Odometry, callback_pose)


def is_data_initialized():
    return (front_min is not None and
            front_min_ang is not None and
            back_min is not None and
            back_min_ang is not None and
            hokuyo_min is not None and
            hokuyo_min_ang is not None and
            hokuyo_ranges is not None and
            hokuyo_ang_inc is not None and
            abs_position_x is not None and
            abs_position_y is not None and
            abs_position_z is not None and
            roll is not None and
            pitch is not None and
            yaw is not None)


def print_all_data():
    print "front_min: " + str(front_min)
    print "front_min_ang: " + str(front_min_ang)
    print "back_min: " + str(back_min)
    print "back_min_ang: " + str(back_min_ang)
    print "hokuyo_min: " + str(hokuyo_min)
    print "hokuyo_min_ang: " + str(hokuyo_min_ang)
    print "hokuyo_ranges: " + str(hokuyo_ranges)
    print "hokuyo_ang_inc: " + str(hokuyo_ang_inc)
    print "abs_position_x: " + str(abs_position_x)
    print "abs_position_y: " + str(abs_position_y)
    print "abs_position_z: " + str(abs_position_z)
    print "roll: " + str(roll)
    print "pitch: " + str(pitch)
    print "yaw: " + str(yaw)
    print "Params: " + str(params)


def set_params(key, value):
    params[key] = value


# ------------------ CallBacks ------------------
def callback_sonar_front(scan):
    global front_min, front_min_ang

    front_min = min(scan.ranges)
    front_min_ang = scan.ranges.index(min(scan.ranges)) * scan.angle_increment


def callback_sonar_back(scan):
    global back_min, back_min_ang

    back_min = min(scan.ranges)
    back_min_ang = scan.ranges.index(min(scan.ranges)) * scan.angle_increment


def callback_hokuyo_scan(scan):
    # TODO calculo de cordenadas errado - Fazer como no move.new_waypoint()
    global hokuyo_min, hokuyo_min_ang, hokuyo_ranges, hokuyo_ang_inc

    hokuyo_min = min(scan.ranges)
    hokuyo_min_ang = (math.pi * 135 / 180) - scan.ranges.index(
        min(scan.ranges)) * scan.angle_increment
    hokuyo_ranges = scan.ranges
    hokuyo_ang_inc = scan.angle_increment


def callback_pose(odometry):
    global abs_position_x, abs_position_y, abs_position_z, roll, pitch, yaw

    abs_position_x = odometry.pose.pose.position.x
    abs_position_y = odometry.pose.pose.position.y
    abs_position_z = odometry.pose.pose.position.z

    quaternion = (odometry.pose.pose.orientation.x,
                  odometry.pose.pose.orientation.y,
                  odometry.pose.pose.orientation.z,
                  odometry.pose.pose.orientation.w)

    (roll, pitch, yaw) = euler_from_quaternion(quaternion)

    roll = roll
    pitch = pitch
    yaw = yaw

# ------------------ End CallBacks ------------------
