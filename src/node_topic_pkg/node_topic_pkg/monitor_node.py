import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MonitorNode(Node):
    """订阅并显示机器人运行状态。"""

    def __init__(self):
        super().__init__('monitor_node')

        # 创建订阅者
        self.status_subscription = self.create_subscription(
            String,
            'robot_status',
            self.status_callback,
            10
        )

        self.get_logger().info(
            '机器人监控节点已启动。'
        )

    def status_callback(self, msg):
        """每收到一条状态消息，就执行一次。"""
        self.get_logger().info(
            f'收到机器人状态：{msg.data}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = MonitorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()