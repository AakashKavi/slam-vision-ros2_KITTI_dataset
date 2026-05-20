import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='orb_slam3_ros2',
            executable='stereo',
            name='orb_slam3_stereo',
            output='screen',
            parameters=[{
                'vocabulary_file': os.path.expanduser('~/ORB_SLAM3/Vocabulary/ORBvoc.txt'),
                'settings_file': os.path.expanduser('~/ORB_SLAM3/Examples/Stereo/KITTI00-02.yaml'),
            }],
            remappings=[
                ('camera/left', '/kitti/camera_gray_left'),
                ('camera/right', '/kitti/camera_gray_right'),
            ]
        )
    ])
