import sys
import rospy
import roslib
import time
from std_msgs.msg import Float64
from control_msgs.msg import JointControllerState
import random
import keyboard #Using module keyboard
import threading

"""
    Description:    Subscribe the thormang topic value and store in disk as txt numberSamples times
                    Receives a mutex that is used to sincronize with all others publishers and subscribers threads and the main thread
                    With the mutex, a subscriber thread does not run at same time with the main thread or other subscriber and publisher thread
                    The main thread allow a subscriber thread to run by setting the run flag                    
"""

class subscriberThread(threading.Thread):
    def __init__ (self, topic, name, mutex, flag, numberSamples):
        threading.Thread.__init__(self)   
        self.topic = topic
        self.JointController = None
        self.name = name
        self.file = open("dataset/"+self.name+".txt","a") 
        self.num_samples = numberSamples
        self.count = 0
        self.mutex = mutex
        self.flag = flag
        
    # Sincronization Flag, True it subscribe
    def setFlag(self):
        self.flag = True

    # write data to disk
    def __writeData__(self, data):
        self.JointController = data
        self.file = open("dataset/"+self.name+".txt","a") 
        self.file.write(str(self.JointController.process_value)+'\n')              
        self.count += 1
        self.file.close() 
        
    # the callback function
    def callback(self, data):
        self.mutex.acquire()
        print self.name+" aquired value"        
        if self.flag == True:
            # if has already achieved the samples number desired
            if (self.num_samples >= self.count):
                self.__writeData__(data)
            else:
                print "Finished Subscribing"
            
            self.flag = False

            #print self.name+" is notifying all"
            self.mutex.notify_all()              
        else:
            #print self.name+" wainting"
            self.mutex.wait()
                
        #print self.name+" is releasing"
        self.mutex.release()
 
    def run(self):
        rospy.Subscriber(self.topic, JointControllerState, self.callback)
        rospy.spin()

