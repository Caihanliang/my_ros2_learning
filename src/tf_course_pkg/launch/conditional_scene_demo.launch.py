from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_listener = LaunchConfiguration('use_listener')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_listener',
            default_value='true',
            description='是否启动 TF 监听节点',
        ),
        Node(
            package='tf_course_pkg',
            executable='static_target_broadcaster',
            name='static_target_broadcaster',
            output='screen',
            prefix='gnome-terminal --',
        ),
        Node(
            package='tf_course_pkg',
            executable='dynamic_robot_broadcaster',
            name='dynamic_robot_broadcaster',
            output='screen',
            prefix='gnome-terminal --',
        ),
        Node(
            package='tf_course_pkg',
            executable='target_listener',
            name='target_listener',
            output='screen',
            prefix='gnome-terminal --',
            condition=IfCondition(use_listener),
        ),
    ])