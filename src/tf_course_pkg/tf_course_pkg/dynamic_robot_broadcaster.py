import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
import math
from tf_transformations import quaternion_from_euler


class DynamicRobotBroadcaster(Node):
    """持续发布小车在世界坐标系中的固定初始位姿。"""

    def __init__(self):
        super().__init__('dynamic_robot_broadcaster')

        self.broadcaster = TransformBroadcaster(self)

        # 动态 TF 需要持续发布，并使用当前时间戳。
        self.timer = self.create_timer(0.1, self.publish_robot_transform)

        self.get_logger().info(
            '开始发布动态 TF: world -> base_link, '
            '固定位置=(1.0, 0.0, 0.0) m, yaw=0.0°'
        )

        self.start_time = self.get_clock().now()
        self.last_stage = None

    def publish_robot_transform(self):
        # 过了5s之后变换一下小车的位置，模拟小车相对于世界坐标系在进行动态变化
        current_time = self.get_clock().now()

        elapsed = (
            current_time - self.start_time
        ).nanoseconds / 1e9

        if elapsed < 5.0:
            stage = 'A'
            x = 1.0
            y = 0.0
            z = 0.0
            yaw_deg = 0.0
        else:
            stage = 'B'
            x = 2.0
            y = 2.0
            z = 0.0
            yaw_deg = 90.0

        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = 'world'
        transform.child_frame_id = 'base_link'

        transform.transform.translation.x = x
        transform.transform.translation.y = y
        transform.transform.translation.z = z

        # 角度转为弧度
        roll = math.radians(0.0)
        pitch = math.radians(0.0)
        yaw = math.radians(yaw_deg)
        # 弧度转为四元数
        qx, qy, qz, qw = quaternion_from_euler(roll, pitch, yaw)

        transform.transform.rotation.x = qx
        transform.transform.rotation.y = qy
        transform.transform.rotation.z = qz
        transform.transform.rotation.w = qw

        self.broadcaster.sendTransform(transform)

        if stage != self.last_stage:
            self.get_logger().info(
                f'小车进入阶段 {stage}：位置=({x:.1f}, {y:.1f}, 0.0) m；'
                f'yaw={yaw_deg:.1f}°'
            )
            self.last_stage = stage


def main(args=None):
    rclpy.init(args=args)
    node = DynamicRobotBroadcaster()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()