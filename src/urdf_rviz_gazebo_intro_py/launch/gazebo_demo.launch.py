from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
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
    model_path = PathJoinSubstitution([package_share, 'urdf', model])
    world_path = PathJoinSubstitution([package_share, 'worlds', world])

    robot_description = ParameterValue(
        Command([FindExecutable(name='xacro'), ' ', model_path]),
        value_type=str,
    )
    rviz_config = PathJoinSubstitution([
        package_share,
        'rviz',
        'urdf_intro.rviz',
    ])

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py',
            ])
        ),
        launch_arguments={
            'gz_args': ['-r -v 3 ', world_path],
            'on_exit_shutdown': 'true',
        }.items(),
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        output='screen',
    )

    # 本节还没有Gazebo关节状态插件和ros_gz_bridge，
    # 暂时使用GUI给RViz中的连续关节提供角度。
    joint_state_publisher_gui = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher_gui',
        parameters=[{'robot_description': robot_description}],
        output='screen',
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen',
    )

    spawn_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_spawn_model.launch.py',
            ])
        ),
        launch_arguments={
            'world': 'my_world',
            'topic': 'robot_description',
            'entity_name': 'course_mobile_robot',
            'allow_renaming': 'False',
            'x': '0.0',
            'y': '0.0',
            'z': '0.02',
        }.items(),
    )

    return LaunchDescription([
        declare_model,
        declare_world,
        gazebo,
        robot_state_publisher,
        joint_state_publisher_gui,
        rviz,
        spawn_robot,
    ])


'''
# 代码2
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
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
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='False',
        description='Use the Gazebo simulation clock for ROS 2 nodes.',
    )

    model = LaunchConfiguration('model')
    world = LaunchConfiguration('world')
    use_sim_time = LaunchConfiguration('use_sim_time')
    model_path = PathJoinSubstitution([package_share, 'urdf', model])
    world_path = PathJoinSubstitution([package_share, 'worlds', world])

    robot_description = ParameterValue(
        Command([FindExecutable(name='xacro'), ' ', model_path]),
        value_type=str,
    )
    rviz_config = PathJoinSubstitution([
        package_share,
        'rviz',
        'urdf_intro.rviz',
    ])

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py',
            ])
        ),
        launch_arguments={
            'gz_args': ['-r -v 3 ', world_path],
            'on_exit_shutdown': 'true',
        }.items(),
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': use_sim_time,
        }],
        output='screen',
    )

    # 本节还没有Gazebo关节状态插件和ros_gz_bridge，
    # 暂时使用GUI给RViz中的连续关节提供角度。
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': use_sim_time,
        }],
        output='screen',
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen',
    )

    spawn_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_spawn_model.launch.py',
            ])
        ),
        launch_arguments={
            'world': 'my_world',
            'topic': 'robot_description',
            'entity_name': 'course_mobile_robot',
            'allow_renaming': 'False',
            'x': '0.0',
            'y': '0.0',
            'z': '0.02',
        }.items(),
    )

    return LaunchDescription([
        declare_model,
        declare_world,
        declare_use_sim_time,
        robot_state_publisher,
        joint_state_publisher,
        rviz,
        gazebo,
        spawn_robot,
    ])
'''