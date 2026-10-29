from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
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
        ),
    ])