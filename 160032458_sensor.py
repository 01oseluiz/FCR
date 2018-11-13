#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan #To /sonar_front, /sonar_back, /hokuyo_scan
from nav_msgs.msg import Odometry #To /pose
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist


#------------------ CallBacks ------------------
def callback_sonar_front(scan):
    global sensor_hash
    
    sensor_hash['front_min'] = min(scan.ranges)
    sensor_hash['front_min_ang'] = scan.ranges.index(min(scan.ranges)) * scan.angle_increment
    
    
    
def callback_sonar_back(scan):
    global sensor_hash
    
    sensor_hash['back_min'] = min(scan.ranges)
    sensor_hash['back_min_ang'] = scan.ranges.index(min(scan.ranges)) * scan.angle_increment
    
def callback_hokuyo_scan(scan):
    global sensor_hash
    
    sensor_hash['hokuyo_min'] = min(scan.ranges)
    sensor_hash['hokuyo_min_ang'] = (math.pi * 135/180) - scan.ranges.index(min(scan.ranges)) * scan.angle_increment
    
    
def callback_pose(odometry):
    global sensor_hash
    
    x = odometry.pose.pose.position.x
    y = odometry.pose.pose.position.y
    
    quaternion =  (odometry.pose.pose.orientation.x,
                   odometry.pose.pose.orientation.y,
                   odometry.pose.pose.orientation.z,
                   odometry.pose.pose.orientation.w)
    
    (roll,pitch,yaw) = euler_from_quaternion(quaternion)
    
    sensor_hash['roll'] = roll
    sensor_hash['pitch'] = pitch
    sensor_hash['yaw'] = yaw

#------------------ End CallBacks ------------------
    
#------------------ Calc Position ------------------
def relative_positions():   
    if len(sensor_hash) < 9:
        return {}
        
    rel_positions = {}
    rel_positions['sonar_front_x'] = math.cos(sensor_hash['front_min_ang']) * sensor_hash['front_min']
    rel_positions['sonar_front_y'] = math.sin(sensor_hash['front_min_ang']) * sensor_hash['front_min']
    rel_positions['laser_x'] = math.sin(sensor_hash['hokuyo_min_ang']) * sensor_hash['hokuyo_min']
    rel_positions['laser_y'] = math.cos(sensor_hash['hokuyo_min_ang']) * sensor_hash['hokuyo_min']
    
    #print "----------------SENSOR HASH-----------------"
    #for key,value in sensor_hash.iteritems():
        #print key, value
        
    print "----------------ABS POSITIONS-----------------"
    for key,value in rel_positions.iteritems():
        print key, value
    
    return rel_positions 

#------------------ End Calc Position ------------------

#----------------- Move ----------------------

def move(pub, type_sensor):
    rel_positions = relative_positions()
    
    if len(rel_positions) < 1:
        return
    
    vel = Twist()
    
    vel.linear.x = 1.0
    vel.angular.z = 0
    
    # Position with Sonar
    if type_sensor == "sonar":
        pos_x = rel_positions['sonar_front_x']
        pos_y = rel_positions['sonar_front_y']
    
    # Position with Lase
    else:
        pos_x = rel_positions['laser_x']
        pos_y = rel_positions['laser_y']
    
    if abs(pos_x) < 1 and pos_y < 3 and pos_y > 0:
        vel.angular.z =  1 / (pos_x / 2) * 5 
        
    pub.publish(vel)
    
    
#----------------- End Move --------------------
    
    
def listener_talker():
    global sensor_hash
    sensor_hash = {}
    
    rospy.init_node('listener_talker', anonymous = True)
    rate = rospy.Rate(10)
    
    rospy.Subscriber("sonar_front", LaserScan, callback_sonar_front)
    rospy.Subscriber("sonar_back", LaserScan, callback_sonar_back)
    rospy.Subscriber("hokuyo_scan", LaserScan, callback_hokuyo_scan)
    rospy.Subscriber("pose", Odometry, callback_pose)
    
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    
    while not rospy.is_shutdown():
        move(pub, "laser")
        rate.sleep()
        
    
    
    

if __name__ == '__main__':
    try:
        listener_talker()
    except rospy.ROSInterruptException:
        pass
