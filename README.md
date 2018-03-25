# Ball Grabbing Experiment with Thormang
A first experiment using [Thormang Simulator in Gazebo](http://wiki.ros.org/ROBOTIS-THORMANG3). The experiment idea is make thormang grab a ball and put it in a bowl. This action was reproduced by two diferrent ways: by teleoperation and by fixed sequenced pose. But first, a few modifications and implementations were made.

## Gripper Implementation:
By default, thormang simulator in gazebo does not has the gripper collision properly implemented, whitch is necessary for the experiment.
For that the thormang3.structure.arm.xacro description was modified and the collision implemented. The effect of the change can be saw in the image below.

![Gripper modification](/gripper.png)

## Thormang world modifications:
The thormang's world is empty after installation. Then three gazebo default obajects were added to the world: A ball, a bowl and a table. The objects position were manually setted. For this experiment, thormang was also fixed in the world.

## Fixed Sequenced Pose mode

## Teleoperation mode


