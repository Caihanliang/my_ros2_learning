from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    params_file = PathJoinSubstitution([
        FindPackageShare('tf_course_pkg'),
        'config',
        'tf_params.yaml',
    ])

    return LaunchDescription([
        Node(
            package='tf_course_pkg',
            executable='static_target_broadcaster',
            name='static_target_broadcaster',
            output='screen',
        ),
        Node(
            package='tf_course_pkg',
            executable='dynamic_robot_broadcaster',
            name='dynamic_robot_broadcaster',
            parameters=[params_file],
            output='screen',
        ),
        Node(
            package='tf_course_pkg',
            executable='target_listener',
            name='target_listener',
            output='screen',
        ),
    ])