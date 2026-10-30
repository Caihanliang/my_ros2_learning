from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    package_share = FindPackageShare('urdf_rviz_gazebo_intro_py')

    declare_model = DeclareLaunchArgument(
        'model',
        default_value='06_physics_robot.urdf.xacro',
        description='Model filename inside the package urdf directory.',
    )
    declare_world = DeclareLaunchArgument(
        'world',
        default_value='my_world.sdf',
        description='World filename inside the package worlds directory.',
    )

    model = LaunchConfiguration('model')
    world = LaunchConfiguration('world')

    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                package_share,
                'launch',
                'gazebo_demo.launch.py',
            ])
        ),
        launch_arguments={
            'model': model,
            'world': world,
            'use_sim_time': 'True',
        }.items(),
    )

    bridge_config = PathJoinSubstitution([
        package_share,
        'config',
        'bridge.yaml',
    ])

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        parameters=[{'config_file': bridge_config}],
        output='screen',
    )

    return LaunchDescription([
        declare_model,
        declare_world,
        simulation,
        bridge,
    ])