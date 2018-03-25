# Ball Grabbing Experiment on Thormang3 Simulator
A first experiment using [Thormang3 Simulator in Gazebo](http://wiki.ros.org/ROBOTIS-THORMANG3). The experiment idea is make Thormang3 grab a ball and put it in a bowl. This action was reproduced by two different ways: by Teleoperation and by Fixed Sequenced Pose. To achieve it, a few modifications and implementations on Thormang3 files were made.


## Thormang3's world modifications
The Thormang3's world is empty after installation. Then three gazebo default objects were added to the [world](https://github.com/ROBOTIS-GIT/ROBOTIS-THORMANG-Common/blob/master/thormang3_gazebo/worlds/empty.world): A ball, a bowl and a table. The objects position were manually set in the [created world](/world/pimped.world). For this experiment, Thormang3 was also fixed in the world.

![Gripper modification](/world.png)

## Gripper Implementation
By default, Thormang3 simulator in gazebo does not have the gripper collision implemented, which is necessary for the experiment.
For that, the [thormang3.structure.arm.xacro description](https://github.com/ROBOTIS-GIT/ROBOTIS-THORMANG-Common/blob/master/thormang3_description/urdf/thormang3.structure.arm.xacro) was modified and the collision implemented. The change effect can be see in the image below.


![Gripper modification](/gripper.png)


## Fixed Sequenced Pose mode
This way of movement generation uses a manually defined sequence of angles to publish in each topic. Every 1.5 secs an angle value is published in each topic. For this grab ball movement, a sequence of seven angles were sent to each topic. This hand-defined angles in topics.py is defined as a matrix, where the columns are for the arm pose in every time step. The result of this experiment can be seen in the image below.


![Fixed Sequenced Pose experiment](/fixed.gif)


## Teleoperation mode
The idea is to control Thormang3 arm with your arm. For this was used the Myo armband. The [Myo armband interface](http://www.fernandocosentino.net/pyoconnect/) for linux was used to read the angles from. The values of Roll, Pitch, Yaw, GyroX and WaveIn/Waveout were read and published to a ROS topic MyoInterface and sent to Thormang3's arm topics. The image below show to result. 


![Fixed Sequenced Pose experiment](/fixed.gif)


**Obs: Only the absolute read Myo angles were used. It may not work properly since no cinematic description was used. Also, be aware that Myo adapts differently in each person arm.**


## How to run
Open the Thormang3 gazebo in a terminal by executing the following command:

***roslaunch thormang3_gazebo robotis_world.launch*** 


In a new terminal window, execute the Thormang3 Manager:

***roslaunch thormang3_manager thormang3_manager.launch*** 


After Thormang3 is running, go to the PyoConnect folder and execute the PyoManager if you want to teleoperate the arm. Be assure Myo is plugged in and adjusted to your arm.

***python PyoManager.pyc***


For the last, execute the code by invoking python **main.py** in a new terminal window.
