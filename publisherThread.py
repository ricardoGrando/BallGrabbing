import sys
import rospy
import roslib
import time
from std_msgs.msg import Float64
from control_msgs.msg import JointControllerState
import random
import threading

"""
    Description:    Thread that publish a value to a ros topic
                    Receives a publisher and a mutex that is used to sincronize with all others publishers threads and the main thread
                    With the mutex, a publisher thread does not run at same time with the main thread or other publisher thread
                    The main thread allow a publisher thread to run by setting the run flag
                    This sincronization is used for correctly pose generation
"""

class publisherThread(threading.Thread):
    def __init__ (self, name, pub, mutex, flag, startValue=0):
        threading.Thread.__init__(self)   
        self.name = name     
        self.pub = pub
        self.mutex = mutex
        self.value = None
        self.flag = flag

    # set the angle value for this topic
    def setValue(self, value):
        self.value = value
    
    # Sincronization Flag, True it runs
    def setFlag(self):
        self.flag = True
    
    def run(self):
        while not rospy.is_shutdown():            
            self.mutex.acquire()
            print self.name+" aquired value"
            if self.flag == True:
                # publish the value 
                self.pub.publish(self.value)
                
                self.flag = False

                #print self.name+" is notifying all"
                self.mutex.notify_all()              
            else:
                #print self.name+" wainting"
                self.mutex.wait()
            
            #print self.name+" is releasing"
            self.mutex.release()
