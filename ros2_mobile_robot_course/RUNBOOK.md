# 运行手册

## 1. 准备工作空间

```bash
mkdir -p ~/ros2_ws/src
cp -r ros2_mobile_robot_course/src/my_robot_interfaces ~/ros2_ws/src/
cp -r ros2_mobile_robot_course/src/course_mobile_robot_sim ~/ros2_ws/src/
cp -r ros2_mobile_robot_course/src/course_mobile_robot_apps ~/ros2_ws/src/
```

## 2. 安装依赖

### 2.1 使用 rosdep 自动安装（推荐）

`rosdep` 会读取三个包中的 `package.xml`，自动安装尚未安装的系统依赖：

```bash
sudo apt update
sudo apt install -y python3-rosdep ros-dev-tools liburdfdom-tools
```

如果是第一次使用 `rosdep`，还需要初始化；已经初始化过则跳过 `sudo rosdep init`：

```bash
sudo rosdep init
rosdep update
```

进入工作空间并安装依赖：

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y --rosdistro jazzy
```

其中 `--ignore-src` 表示不安装工作空间中已经存在的 ROS 2 包。

### 2.2 手动安装（备用）

如果暂时无法使用 `rosdep`，也可以手动安装本工程所需的软件包：

```bash
sudo apt update
sudo apt install -y \
  ros-jazzy-ros-gz-sim \
  ros-jazzy-ros-gz-bridge \
  ros-jazzy-xacro \
  ros-jazzy-robot-state-publisher \
  ros-jazzy-rviz2 \
  ros-jazzy-slam-toolbox \
  ros-jazzy-rosidl-default-generators \
  liburdfdom-tools \
  ros-dev-tools
```

## 3. 编译工程

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

每次新开终端后，都需要重新加载 ROS 2 和当前工作空间：

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
```

## 4. 可选：检查机器人模型

下面的命令用于上课前检查 Xacro、URDF 和 Gazebo 插件，不影响工程正常运行：

```bash
COURSE_SIM_SHARE=$(ros2 pkg prefix --share course_mobile_robot_sim)
xacro ${COURSE_SIM_SHARE}/urdf/course_mobile_robot.urdf.xacro \
  > /tmp/course_mobile_robot.urdf
check_urdf /tmp/course_mobile_robot.urdf
gz sdf -p /tmp/course_mobile_robot.urdf \
  > /tmp/course_mobile_robot.sdf
grep -E "DiffDrive|JointStatePublisher|course_lidar" \
  /tmp/course_mobile_robot.sdf
printf 'links=%s joints=%s collision=%s inertial=%s gazebo=%s\n' \
  "$(grep -c '<link name=' /tmp/course_mobile_robot.urdf)" \
  "$(grep -c '<joint name=' /tmp/course_mobile_robot.urdf)" \
  "$(grep -c '<collision' /tmp/course_mobile_robot.urdf)" \
  "$(grep -c '<inertial' /tmp/course_mobile_robot.urdf)" \
  "$(grep -c '<gazebo' /tmp/course_mobile_robot.urdf)"
```

这里生成的 `/tmp/course_mobile_robot.sdf` 只用于检查转换结果，不是需要维护的第二份模型。

预期统计为 `links=7 joints=6 collision=6 inertial=6 gazebo=5`。运行后 TF 主链应为 `odom → base_footprint → base_link`；可用 `ros2 run tf2_ros tf2_echo odom base_footprint` 检查里程计 TF。

## 5. 仿真、传感器与键盘控制功能演示

终端 1：

```bash
ros2 launch course_mobile_robot_sim sim.launch.py \
  model:=course_mobile_robot.urdf.xacro
```

终端 2：

```bash
ros2 run course_mobile_robot_sim keyboard_teleop_node
```

键盘操作：`w` 前进、`s` 后退、`a/d` 左右转、`k` 或空格停车、`q/e` 加速和减速。

终端 3：

```bash
ros2 node list
ros2 topic list
ros2 topic echo /cmd_vel_manual
ros2 topic echo /cmd_vel_input
ros2 topic echo /cmd_vel
ros2 topic echo /joint_states
ros2 topic echo /front_distance
```

## 6. 三模式综合控制功能演示

### 6.1 启动应用节点

仿真已经运行时，启动巡航和导航两个应用节点：

```bash
ros2 launch course_mobile_robot_apps applications.launch.py
```

或者一条命令运行全部。完整演示默认进入 `CRUISE` 模式：

```bash
ros2 launch course_mobile_robot_apps full_demo.launch.py \
  model:=course_mobile_robot.urdf.xacro
```

也可以用 `initial_mode:=MANUAL` 或 `initial_mode:=NAVIGATION` 指定初始模式。

### 6.2 观察节点通信话题

```bash
ros2 topic echo /front_distance
ros2 topic echo /control_mode
ros2 topic echo /cmd_vel_manual
ros2 topic echo /cmd_vel_cruise
ros2 topic echo /cmd_vel_navigation
ros2 topic echo /cmd_vel_input
```

### 6.3 参数功能演示

查看巡航节点的参数：

```bash
ros2 param list /simple_cruise_node
ros2 param get /simple_cruise_node safe_distance
```

课堂上可以把巡航安全距离临时改成 `1.0 m`，观察小车更早开始转弯：

```bash
ros2 param set /simple_cruise_node safe_distance 1.0
```

重新启动 Launch 后，参数会恢复为 `application_nodes.yaml` 中的值。要长期修改，应编辑 YAML 后重新启动。

### 6.4 手动控制模式

切换模式：

```bash
ros2 service call /set_control_mode \
  my_robot_interfaces/srv/SetControlMode \
  "{mode: MANUAL}"
```

启动键盘节点：

```bash
ros2 run course_mobile_robot_sim keyboard_teleop_node
```

键盘、巡航和导航节点可以同时运行，但只有手动速度会被仲裁节点转发。

### 6.5 简易自主巡航模式

```bash
ros2 service call /set_control_mode \
  my_robot_interfaces/srv/SetControlMode \
  "{mode: CRUISE}"
```

巡航节点始终计算速度，但只有 `CRUISE` 模式会转发它。要暂停运动，切换到手动模式即可。

### 6.6 简易目标导航模式

```bash
ros2 service call /set_control_mode \
  my_robot_interfaces/srv/SetControlMode \
  "{mode: NAVIGATION}"
```

确认 RViz 的 Fixed Frame 为 `odom`，选择工具栏的 `Publish Point`，然后在空旷位置单击。导航节点会先原地转向，再沿近似直线前往目标。到达目标点附近、前方障碍物小于安全距离或雷达数据中断时都会停车。

切换到其他模式会取消当前目标。该节点没有地图和路径规划能力。如果目标直线路径被障碍物挡住，它只会暂停，不会自动绕路。

## 7. 可选扩展：SLAM 建图功能演示

SLAM 不属于三模式控制主线。先正常启动仿真，再在新终端运行：

```bash
ros2 launch course_mobile_robot_sim slam.launch.py
```

切换到手动模式并启动键盘节点：

```bash
ros2 service call /set_control_mode \
  my_robot_interfaces/srv/SetControlMode \
  "{mode: MANUAL}"
ros2 run course_mobile_robot_sim keyboard_teleop_node
```

在 RViz 中完成两项设置：

1. 将 `Global Options → Fixed Frame` 改为 `map`；
2. 添加 `Map` 显示，并将 Topic 设置为 `/map`。

缓慢控制机器人在环境中行走，即可观察地图逐步生成。演示结束后关闭 SLAM，RViz 固定坐标系改回 `odom`，即可继续三模式实验。

建图时建议使用较低转速，不要连续按 `q` 提速。工程已将雷达设置为 `20 Hz`、SLAM 扫描队列设置为 `1`，并降低了扫描匹配的转角阈值，用于减轻转弯时实时激光相对地图来回跳动。SLAM 仍会持续修正 `map → odom`，因此轻微瞬时抖动属于正常现象。
