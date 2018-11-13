#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

def square():
    global msg
    msg = Twist()
    
    for i in range(1,11):
        msg.linear.x = 20.0
        msg.angular.z = 0.0
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()
    
    for i in range(1,11):
        msg.linear.x = 0.0
        msg.angular.z = 3.14
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()
    

def circle():
    global msg
    msg = Twist()
    
    msg.linear.x = 2.0
    msg.angular.z = 1.57
    rospy.loginfo(msg)
    pub.publish(msg)
    rate.sleep()
    

def talker():
    global pub
    global rate
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=110)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 1hz
    
    while not rospy.is_shutdown():
        circle()
        #square()
        
        
        
    

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
