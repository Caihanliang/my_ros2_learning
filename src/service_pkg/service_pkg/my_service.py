import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool  # 引入标准的服务接口 (包含 request.data 和 response.success/message)

class LightServer(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("大灯控制服务已启动，等待指令...")
        
        # 创建服务端：接口类型，服务名称，回调函数
        self.srv = self.create_service(SetBool, 'switch_light', self.light_callback)

    # 当客户端发来请求时，自动调用此函数
    def light_callback(self, request, response):
        if request.data == True:
            self.get_logger().info("收到指令：打开大灯！")
            response.success = True
            response.message = "大灯已成功打开！"
        else:
            self.get_logger().info("收到指令：关闭大灯！")
            response.success = True
            response.message = "大灯已成功关闭！"
            
        return response  # 必须返回response对象给客户端

def main(args=None):
    rclpy.init(args=args)
    node = LightServer('light_server')
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()