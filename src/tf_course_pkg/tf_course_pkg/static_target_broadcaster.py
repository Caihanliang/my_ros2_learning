import math
import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster
from tf_transformations import quaternion_from_euler


class StaticTargetBroadcaster(Node):
    """发布世界坐标系到固定目标点的静态关系。"""

    def __init__(self):
        super().__init__('static_target_broadcaster')

        self.broadcaster = StaticTransformBroadcaster(self)

        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = 'world'
        transform.child_frame_id = 'target_point'

        # 目标点固定在世界坐标系中的 (5, 3, 0)。
        transform.transform.translation.x = 5.0
        transform.transform.translation.y = 3.0
        transform.transform.translation.z = 0.0

        # 角度转为弧度
        roll = math.radians(0.0)
        pitch = math.radians(0.0)
        yaw = math.radians(0.0)

        # 弧度转为四元数
        qx, qy, qz, qw = quaternion_from_euler(roll, pitch, yaw)
        transform.transform.rotation.x = qx
        transform.transform.rotation.y = qy
        transform.transform.rotation.z = qz
        transform.transform.rotation.w = qw

        # 坐标系发布
        self.broadcaster.sendTransform(transform)
        self.get_logger().info(
            '已发布静态 TF: world -> target_point；'
            '位置=(5.0, 3.0, 0.0) m'
        )

def main(args=None):
    rclpy.init(args=args)
    node = StaticTargetBroadcaster()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()