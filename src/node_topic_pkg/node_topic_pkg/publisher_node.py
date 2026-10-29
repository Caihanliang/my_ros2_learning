import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class RobotNode(Node):
    """模拟机器人本体，并周期发布运行状态。"""

    def __init__(self):
        super().__init__('publisher_node')

        # 创建发布者：
        # 消息类型为 String
        # 话题名称为 robot_status
        # 队列深度为 10
        self.status_publisher = self.create_publisher(
            String,
            'robot_status',
            10
        )
        # 每隔 1 秒执行一次 publish_status
        self.timer = self.create_timer(
            1.0,
            self.publish_status
        )

        self.count = 0
        self.get_logger().info('机器人发布节点已启动。')

    def publish_status(self):
        """定时发布机器人状态。"""
        # 第一步：创建消息
        msg = String()
        # 第二步：填写消息内容
        msg.data = f'机器人运行正常，心跳次数：{self.count}'
        # 第三步：发布消息
        self.status_publisher.publish(msg)
        self.get_logger().info(
            f'已发布：{msg.data}'
        )
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    node = RobotNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()