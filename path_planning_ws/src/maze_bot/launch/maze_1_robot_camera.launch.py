import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    package_share_dir = get_package_share_directory("maze_bot")
    urdf_file = os.path.join(package_share_dir, "urdf", "maze_bot.urdf")
    world_file = os.path.join(package_share_dir, "worlds", "maze_1.world")

    with open(urdf_file, "r") as f:
        robot_description = f.read()

    gz_model_path = os.path.join(package_share_dir, "..")

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py",
            )
        ),
        launch_arguments={"gz_args": f"-r {world_file}"}.items(),
    )

    spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name", "maze_bot",
            "-topic", "robot_description",
        ],
        output="screen",
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description}],
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
            "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
            "/Botcamera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image",
            "/rrbot/camera1/image_raw@sensor_msgs/msg/Image[gz.msgs.Image",
            "/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V",
        ],
        output="screen",
    )

    return LaunchDescription([
        SetEnvironmentVariable("GZ_SIM_RESOURCE_PATH", gz_model_path),
        gz_sim,
        robot_state_publisher,
        spawn_entity,
        bridge,
    ])
