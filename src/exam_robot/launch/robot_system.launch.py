from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='exam_robot',
            executable='battery_node',
            name='battery_node',
            output='screen'
        ),
        Node(
            package='exam_robot',
            executable='distance_sensor',
            name='distance_sensor',
            output='screen'
        ),
        Node(
            package='exam_robot',
            executable='robot_controller',
            name='robot_controller',
            output='screen'
        ),
        Node(
            package='exam_robot',
            executable='status_display',
            name='status_display',
            output='screen'
        ),
    ])