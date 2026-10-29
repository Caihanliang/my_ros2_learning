import rclpy
from rclpy.node import Node

class RobotNode(Node):
    def __init__(self):
        super().__init__('robot_node')
        self.get_logger().info('机器人节点已启动')

def main(args=None):
    #初始化ros@python客户端
    rclpy.init(args=args)
    #创建节点对象
    node = RobotNode()
    rclpy.spin(node)   #保持运行
    node.destroy_node() #销毁节点对象
    rclpy.shutdown()

if __name__ == '__main__':
    main()

        
                
                