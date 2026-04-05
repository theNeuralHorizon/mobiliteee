import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    package_share_dir = get_package_share_directory("maze_bot")
    urdf_file = os.path.join(package_share_dir, "urdf", "maze_bot.urdf")
    world_file = os.path.join(package_share_dir, "worlds", "maze_2.world")

    gazebo_ros_share = get_package_share_directory("gazebo_ros")
    gazebo_model_path = os.path.join(package_share_dir, "..")

    env = {
        "GAZEBO_MODEL_PATH": gazebo_model_path,
    }

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_share, "launch", "gazebo.launch.py")
        ),
        launch_arguments={
            "verbose": "true",
            "world": world_file,
        }.items(),
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        arguments=[urdf_file],
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
    ])
