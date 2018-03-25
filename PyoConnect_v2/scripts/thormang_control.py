import time
import sys
import rospy
import roslib
from std_msgs.msg import Float64
from std_msgs.msg import String
import random

"""
    Description:    Functions to read from Myo and publish to a topic: MyoInterface.
                    This is readed by PyoConnect and runs in background after gazebo's thormang initialization
                    Values readed from are: Roll, Pitch, Yaw, Gyro and Wavein WaveOut
                    Wave in and out are used to control the thormang's gripper
                    Only GyroX is used in thormang

"""

"""Mainly Myo functions
myo.getArm()
myo.getXDirection()
myo.getTimeMilliseconds()
myo.getRoll()
myo.getPitch()
myo.getYaw()
myo.getGyro()
myo.getAccel()
"""

#Global variables used in the myo functions
FLAG = True
pub = None
FINGERSPREAD = False
WAVEOUT = False
WAVEIN = False
gripper = 0

def onUnlock():
	myo.rotSetCenter()
	myo.unlock("hold")
	
def onPeriodic():
    global FLAG
    global pub
    global FINGERSPREAD
    global WAVEOUT
    global WAVEIN
    global gripper

    # Init Myo Interface Node
    if FLAG == True:
        print "test"
        pub = rospy.Publisher("MyoInterface", String, queue_size=10)
        rospy.init_node('MyoInterface', anonymous = True)    
        FLAG = False
    else:
        pass
	
    counter = 0    
    while not rospy.is_shutdown():
        # makes a string off desired myo outputs readed
        value = str(Float64(myo.getRoll())) + "," + str(Float64(myo.getPitch())) + "," + str(Float64(myo.getYaw())) + "," + str(myo.getGyro()) + "," + str(gripper)
        # publish once
        pub.publish(value)
        if counter == 1:
            break
        counter += 1        

    	
def onPoseEdge(pose, edge):
    global FINGERSPREAD
    global WAVEOUT
    global WAVEIN
    global gripper

    if pose == "fingersSpread" and edge == 'on':
       	FINGERSPREAD = True
        print "fingerspred"
    # Using waveout to grab in to the angle limit
    elif pose == "waveOut":        
        if edge == 'on':
            WAVEOUT = False
        else:
            gripper += 0.1
            if gripper > 1.2:
                gripper = 1.2
            WAVEOUT = True
    #Using wavein to grab out to the angle limit           
    elif pose == "waveIn":       
        if edge == 'on': 
			WAVEIN = False
        else:
            gripper -= 0.1
            if gripper < 0:
                gripper = 0
            WAVEIN = True
    # fingerspred not used
    elif pose == "rest":
        print "rest"
        FINGERSPREAD = False
        
        

    


    
		