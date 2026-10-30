from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    package_share = FindPackageShare(
        'urdf_rviz_gazebo_intro_py'
    )

    # 设置默认打开的模型文件名
    declare_model = DeclareLaunchArgument(
        'model',
        default_value='06_physics_robot.urdf.xacro',
        description=(
            'Model filename inside the package urdf directory.'
        ),
    )

    # 获取启动参数
    model = LaunchConfiguration('model')

    # 自动拼接：功能包共享目录/urdf/模型文件名
    model_path = PathJoinSubstitution([
        package_share,
        'urdf',
        model,
    ])

    # xacro 可以展开 Xacro，也可以直接读取普通 URDF
    robot_description = ParameterValue(
        Command([
            FindExecutable(name='xacro'),
            ' ',
            model_path,
        ]),
        value_type=str,
    )

    rviz_config = PathJoinSubstitution([
        package_share,
        'rviz',
        'urdf_intro.rviz',
    ])

    return LaunchDescription([
        declare_model,

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
                'robot_description': robot_description,
            }],
            output='screen',
        ),

        Node(
            # package='joint_state_publisher_gui',
            # executable='joint_state_publisher_gui',
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher_gui',
            parameters=[{
                'robot_description': robot_description,
            }],
            output='screen',
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config],
            output='screen',
        ),
    ])