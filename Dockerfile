FROM ros:humble-desktop

# Install dependencies
RUN apt-get update && apt-get install -y \
    ros-humble-rtabmap-ros \
    ros-humble-cv-bridge \
    python3-opencv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /slam_ws
COPY . .

# Source ROS2
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

CMD ["bash"]
