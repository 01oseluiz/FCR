#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

def square():
    global v_left
    global v_right
    
    v_left = Float32()
    v_right = Float32()
    
    for i in range(1,6):
        # Mov to Front
        v_left.data = 1.0
        v_right.data = 1.0
        
        rospy.loginfo(v_left)
        rospy.loginfo(v_right)
        pub_left.publish(v_left)
        pub_right.publish(v_right)
        
        rate.sleep()
        stop()
        
        # Rotate
        v_left.data = 3.14
        v_right.data = -3.14
        
        rospy.loginfo(v_left)
        rospy.loginfo(v_right)
        pub_left.publish(v_left)
        pub_right.publish(v_right)
        
        rate.sleep()
        stop()
    
    


def circle():
    global v_left
    global v_right
    
    v_left = Float32()
    v_right = Float32()
    
    v_left.data = 1.0
    v_right.data = 2.0
    
    for i in range(1,11):
        rospy.loginfo(v_left)
        rospy.loginfo(v_right)
        pub_left.publish(v_left)
        pub_right.publish(v_right)
        
        rate.sleep()
        
    stop()
    
    
def stop():
    global v_left
    global v_right
    
    v_left = Float32()
    v_right = Float32()
    v_left.data = 0.0
    v_right.data = 0.0
    
    rospy.loginfo(v_left)
    rospy.loginfo(v_right)
    pub_left.publish(v_left)
    pub_right.publish(v_right)
    rate.sleep()
    

def talker():
    global pub_right
    global pub_left
    global rate
    
    pub_right = rospy.Publisher('v_right', Float32, queue_size=10)
    pub_left = rospy.Publisher('v_left', Float32, queue_size=10)
    
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 1hz
    
    if not rospy.is_shutdown():
        #circle()
        square()
    

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
