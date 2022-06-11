#Installation of ros and its requirements
#Setup your computer to accept software from packages.ros.org.
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
	
sudo apt install curl
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

sudo apt update
sudo apt install ros-noetic-desktop-full

sudo apt-get install ros-noetic-joy ros-noetic-teleop-twist-joy ros-noetic-teleop-twist-keyboard ros-noetic-laser-proc ros-noetic-rgbd-launch ros-noetic-depthimage-to-laserscan ros-noetic-rosserial-arduino ros-noetic-rosserial-python ros-noetic-rosserial-server ros-noetic-rosserial-client ros-noetic-rosserial-msgs ros-noetic-amcl ros-noetic-map-server ros-noetic-move-base ros-noetic-urdf ros-noetic-xacro ros-noetic-compressed-image-transport ros-noetic-rqt-image-view ros-noetic-gmapping ros-noetic-navigation ros-noetic-interactive-markers


echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
echo "export TURTLEBOT3_MODEL=waffle_pi" >> ~/.bashrc

source ~/.bashrc

sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential


sudo rosdep init
rosdep update

sudo apt-get install ros-noetic-pointgrey-camera-driver
sudo apt-get install ros-noetic-lms1xx

mkdir -p ../src

cd ..

source /opt/ros/noetic/setup.bash


catkin_make -DPYTHON_EXECUTABLE=/usr/bin/python3

source /opt/ros/noetic/setup.bash

. devel/setup.bash

catkin_make

#sudo mkdir /usr/share/gazebo-11
#sudo cp -r src/robomaster_sim/media  /usr/share/gazebo-11 
#sudo cp -r src/robomaster_sim/models  /usr/share/gazebo-11
#sudo cp -r src/robomaster_sim/worlds  /usr/share/gazebo-11
