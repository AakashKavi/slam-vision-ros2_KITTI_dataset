#!/bin/bash
echo "Setting up Visual SLAM environment..."

# Install ROS2 Humble
sudo apt update && sudo apt install locales -y
sudo locale-gen en_US en_US.UTF-8
sudo apt install software-properties-common curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list
sudo apt update
sudo apt install ros-humble-desktop python3-colcon-common-extensions -y

# Install RTAB-Map
sudo apt install ros-humble-rtabmap-ros -y

# Install dependencies
sudo apt install libopencv-dev python3-cv-bridge -y

echo "Source ROS2:"
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

echo "Setup complete!"
