from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    # 1. 声明 Launch 启动参数
    declare_switch_after = DeclareLaunchArgument(
        'switch_after',
        default_value='5.0',
        description='阶段切换时间，单位为秒',
    )

    declare_stage_b_yaw_deg = DeclareLaunchArgument(
        'stage_b_yaw_deg',
        default_value='90.0',
        description='阶段 B 中小车的偏航角，单位为度',
    )

    # 2. 获取 Launch 启动参数
    switch_after = LaunchConfiguration('switch_after')
    stage_b_yaw_deg = LaunchConfiguration('stage_b_yaw_deg')

    # 3. 创建静态 TF 发布节点
    static_tf_node = Node(
        package='tf_course_pkg',
        executable='static_target_broadcaster',
        name='static_target_broadcaster',
        output='screen',
    )

    # 4. 创建动态 TF 发布节点
    dynamic_tf_node = Node(
        package='tf_course_pkg',
        executable='dynamic_robot_broadcaster',
        name='dynamic_robot_broadcaster_withp',
        output='screen',

        parameters=[
            {
                'switch_after': ParameterValue(
                    switch_after,
                    value_type=float,
                ),

                'stage_b_yaw_deg': ParameterValue(
                    stage_b_yaw_deg,
                    value_type=float,
                ),
            }
        ],
    )

    # 5. 创建 TF 监听节点
    listener_node = Node(
        package='tf_course_pkg',
        executable='target_listener',
        name='target_listener',
        output='screen',
    )

    # 6. 返回 LaunchDescription
    # 注意：声明参数的动作要放在使用参数的节点之前

    return LaunchDescription([
        declare_switch_after,
        declare_stage_b_yaw_deg,
        static_tf_node,
        dynamic_tf_node,
        listener_node,
    ])