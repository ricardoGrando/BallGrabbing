import sys
import rospy
import roslib
from std_msgs.msg import String
import threading

"""
    Description:    Myo thread read string msg from ros topic started in thormang_control
"""

class myoThread(threading.Thread):
    def __init__ (self, topic):
        print "Init myo thread"
        threading.Thread.__init__(self)   
        self.topic = topic
        self.value = None
        self.name = topic
        
        # variables
        self.rollRead = None
        self.pitchRead = None
        self.yawRead = None
        self.gyroXRead = None
        self.gripper = None

    def __treatString__(self):
        # get the values from msg string to float
        tmp = self.value.split(",")
        self.rollRead = float(tmp[0][13:])
        self.pitchRead = float(tmp[1][6:])
        self.yawRead = float(tmp[2][6:])
        self.gyroXRead = float(tmp[3][1:])
        self.gripper = float(tmp[6][:-1])

    def callback(self, data):
        self.value = data
        self.__treatString__()
        
    def run(self):
        rospy.Subscriber(self.topic, String, self.callback)
        rospy.spin()

