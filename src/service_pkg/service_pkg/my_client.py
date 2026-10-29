import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
import sys

class LightClient(Node):
    def __init__(self, name):
        super().__init__(name)
        # 创建客户端：接口类型，服务名称
        self.client = self.create_client(SetBool, 'switch_light')
        
        # 等待服务端上线 (每1秒检查一次)
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('服务未上线，请先启动服务器...')
            
        self.request = SetBool.Request()  # 创建一个请求对象

    # 发送请求的函数
    def send_request(self, value):
        self.request.data = value
        # 异步发送请求，并返回一个未来对象(Future)
        self.future = self.client.call_async(self.request)
        rclpy.spin_until_future_complete(self, self.future) # 阻塞等待结果
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
      # 使用命令行参数来控制
    # value = bool(int(sys.argv[1])) 
    
    node = LightClient('light_client')
    
    # 为了演示简单，我们直接在代码里请求“打开大灯”
    node.get_logger().info("正在发送开灯请求...")
    response = node.send_request(True)
    # 打印服务端返回的结果
    node.get_logger().info(f"收到服务器回复: success={response.success}, message='{response.message}'")
    
    node.destroy_node()
    rclpy.shutdown()