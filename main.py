#!/usr/bin/env python

import sys
import rospy
import roslib
import time
from std_msgs.msg import Float64
from control_msgs.msg import JointControllerState
import random
import keyboard
import threading

from publisherThread import *
from subscriberThread import *
from topics import *    
from myoThread import *

"""
    Description:    Create the publishers and subscribers threads. Synchronise all of them with a mutex to avoid have two of them running
                    at same time. It can work by two mods: Fixed posed mode or Myo Mode. The fixed pose mod set a hand-defined
                    sequence for the angles. The sequence is the movement1 in topics.py. The Myo mode uses Myo Armband to control
                    the arm. 
                    For any topic listed in topics.py a publisher and a subscriber thread is created. The main thread receives values
                    from Myo Thread. Those values are sent to the correctly publisher. A time delay of 1.5 secs is used 
                    for the fixed sequence mod.
"""

class main(object):
    def __init__(self, Myo, nsamples):    
        # create an object with all the topics name
        self.topic_list = topics()
        # mutex used to soncronize the main and others publishers threads
        self.mutex = threading.Condition()
        # list of all publishers
        self.publishers = []
        # list of the publishers/subscribers threads
        self.publishersThreads = []
        self.subscribersThreads = []
        # Run with or without Myo
        self.Myo = Myo
        # init and run        
        self.__initAndStart__(nsamples)
        self.__run__()

        
    # init all the variables 
    def __initAndStart__(self, nsamples):
        # set the threads of all the publishers/subscriber of the list
        for i in range(0, len(self.topic_list.pubList)):
            # init the ros publishers
            self.publishers.append(rospy.Publisher(self.topic_list.pubList[i], Float64, queue_size=10))
            #init the publishers thread passing the mutex and a start value for the topic
            self.publishersThreads.append(publisherThread(self.topic_list.pubList[i], self.publishers[i], self.mutex, False, 0))
            # init all the subscribers with the number of samples to subscribe
            self.subscribersThreads.append(subscriberThread(self.topic_list.subList[i], self.topic_list.names[i], self.mutex, False, nsamples))

        # Init myo thread
        if self.Myo == True:
            self.myoSubscriber = myoThread("MyoInterface")
        else: 
            pass
        
        # init node
        rospy.init_node('pup_and_sub', anonymous = True)      
        # start all subscribers/publishers threads
        for i in range(0, len(self.topic_list.pubList)):
            self.publishersThreads[i].start()
            self.subscribersThreads[i].start()
        
        # Start myo thread
        if self.Myo == True:
            self.myoSubscriber.start()
        else: 
            pass
        
    def __run__(self):
        # variables used inn the while true
        value = 0 
        index = 0
        gyroX = 0
        gripper = 0
        while True:
            self.mutex.acquire()
            #print "Main aquired"

            # flag used to  to avoid havinnng a thread running at same time of main thread
            publishersFlag = True
            for i in range(0, len(self.publishersThreads)):
                if self.publishersThreads[i].flag == True:
                    publishersFlag = False
                    break
            for i in range(0, len(self.subscribersThreads)):
                if self.subscribersThreads[i].flag == True:
                    publishersFlag = False
                    break

            # onnnly enters when all publisher threads wainting
            if publishersFlag == True:
                #print "Main setting value"
                # for each publisher            
                for i in range(0, len(self.topic_list.pubList)): 
                    # Running with Myo?
                    if self.Myo == True:                             
                        # for roll topic
                        if i == 5: #5
                            # verify if is reading correctly
                            if self.myoSubscriber.rollRead != None:
                                #set the read value plus bias                  
                                self.publishersThreads[i].setValue(Float64(float(self.myoSubscriber.rollRead) + 0.2))   
                            else:
                                # otherwise make nothing 
                                pass 
                        # for pitch topic
                        elif i == 3: #3
                            # verify if is reading correctly
                            if self.myoSubscriber.pitchRead != None:
                                #set the read value plus bias   
                                self.publishersThreads[i].setValue(Float64(float(self.myoSubscriber.pitchRead)))   
                            else:
                                # otherwise make nothing 
                                pass
                        # for yaw topic
                        elif i == 0: #0
                            # verify if is reading correctly
                            if self.myoSubscriber.yawRead != None:
                                #set the read value plus bias 
                                self.publishersThreads[i].setValue(Float64(float(self.myoSubscriber.yawRead)+1.5))   
                            else:
                                # otherwise make nothing 
                                pass
                        # for gyroX topic
                        elif i == 7: #7
                            # verify if is reading correctly
                            if self.myoSubscriber.gyroXRead != None:
                                #set the read value divided by a bias 
                                self.publishersThreads[i].setValue(Float64(float(self.myoSubscriber.gyroXRead)/2880))   
                            else:
                                # otherwise make nothing 
                                pass
                        # for gripper topics
                        elif i == 1 or i == 2:
                            # set the read value
                            self.publishersThreads[i].setValue(Float64(self.myoSubscriber.gripper))  
                        else:
                            # otherwise makes nothing 
                            pass
                    else:
                        # if not using myo, makes a projected movement
                        self.publishersThreads[i].setValue(Float64(self.topic_list.movement1[i][index]))
                    # set the flag, allowing thread to run
                    self.publishersThreads[i].setFlag()
                
                # used for fixed movement
                index += 1
                if index >= len(self.topic_list.movement1[i]):
                    index = 0                            
                #print "Main notifying"
                self.mutex.notify_all()  

                # For fixed Movement
                if self.Myo == False:
                    time.sleep(1.5)
                
                # activate all subscribers thread
                for i in range(0, len(self.topic_list.subList)):
                    self.subscribersThreads[i].setFlag()
                                
                #print "Main notifying"
                self.mutex.notify_all()
            else:
                #print "Main wainting"
                self.mutex.wait()            
            #print "Main releasing"
            self.mutex.release()
 
        # wait for all threadss
        for i in range(0, len(self.topic_list.pubList)):
            self.publishersThreads[i].join()
            self.subscribersThreads[i].join()        
        self.myoSubscriber.join()
   
m = main(False, 1000000)


