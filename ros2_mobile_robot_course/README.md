# ROS 2 移动机器人综合实战工程

环境：Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic。

工程包含三个 ROS 2 包：自定义接口包 `my_robot_interfaces`、仿真与基础节点包 `course_mobile_robot_sim`、应用节点包 `course_mobile_robot_apps`。

机器人采用组件化单一模型源：`course_mobile_robot.urdf.xacro` 是顶层装配入口，`urdf/components/` 分别维护参数、材质、`base_footprint`、车体、车轮、支撑球、雷达支撑与 Gazebo 扩展。RViz 和 Gazebo 使用同一份展开结果，Gazebo 在生成实体时自动转换为内部 SDF；`classroom_world.sdf` 只负责描述仿真场景。

统一坐标树为：

```text
odom → base_footprint（地面投影）→ base_link（车体中心）
                                      └→ lidar_support_link → lidar_link
```

模型展开统计为 7 个 link、6 个 joint、6 个 collision、6 个 inertial 和 5 个顶层 gazebo 扩展块。`base_footprint` 不参与物理计算；两个驱动轮与万向轮最低点同为模型 `Z=0`。

速度控制采用三个独立来源和一个模式仲裁节点：

```text
/cmd_vel_manual ─────┐
/cmd_vel_cruise ─────┼→ control_mode_node → /cmd_vel_input
/cmd_vel_navigation ─┘                         ↓
                                      cmd_vel_safety_node → /cmd_vel
```

模式为 `MANUAL`、`CRUISE` 和 `NAVIGATION`。仲裁节点只选择速度来源，最终速度的限速和超时停车统一由 `cmd_vel_safety_node` 完成。

本版本以“一个节点只讲一个主要功能”为原则，只保留 6 个节点。参数也只保留最常调的三类：运动速度、距离阈值和安全超时；话题名、服务名、控制频率固定在代码中，避免初学阶段同时追踪过多配置。

两份短参数文件分别是：

- `course_mobile_robot_sim/config/sim_nodes.yaml`：最终限速和指令超时；
- `course_mobile_robot_apps/config/application_nodes.yaml`：巡航速度、避障距离和导航容差。

另外提供独立的 `slam.launch.py` 作为课后扩展。它不会随主工程自动启动，也不参与三模式速度控制；启用后 TF 会在原有主链前增加 `map → odom`。

## 仿真与基础节点包 course_mobile_robot_sim

自编节点：

1. `keyboard_teleop_node.py`
2. `control_mode_node.py`
3. `cmd_vel_safety_node.py`
4. `front_distance_node.py`

模式切换使用接口包中的 `SetControlMode.srv`，通过一个 `/set_control_mode` 服务接收三种模式。

## 上层应用节点包 course_mobile_robot_apps

自编节点：

1. `simple_cruise_node.py`
2. `simple_goal_navigation_node.py`
详细命令看 `RUNBOOK.md`。
