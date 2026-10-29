import math

import rclpy
from rclpy.node import Node
from rclpy.time import Time,Duration
from tf2_ros import Buffer, TransformException, TransformListener
from tf_transformations import euler_from_quaternion


class TargetListener(Node):
    """持续查询目标点在小车坐标系中的位置、距离和角度。"""

    def __init__(self):
        super().__init__('target_listener')

        self.tf_buffer = Buffer()

        self.tf_listener = TransformListener(
            self.tf_buffer,
            self
        )

        self.timer = self.create_timer(
            1.0,
            self.lookup_target_transform
        )

    def lookup_target_transform(self):
        try:
            # 查询 target_point 相对于 base_link 的坐标变换
            result = self.tf_buffer.lookup_transform(
                'base_link',
                'target_point',
                Time(seconds=0.0), # 获取最新时刻的TF值
                Duration(seconds=0.5)   # 根据实际 TF 频率调整
            )

        except TransformException as error:
            self.get_logger().info(
                f'等待完整 TF 树：{error}'
            )
            return

        # 获取 TF 中的平移信息
        tf_result = result.transform

        # 原来的距离计算保持不变
        distance = math.sqrt(
            tf_result.translation.x ** 2
            + tf_result.translation.y ** 2
            + tf_result.translation.z ** 2
        )

        # 使用坐标变换工具把四元数转换成欧拉角
        roll, pitch, yaw = euler_from_quaternion([
            tf_result.rotation.x,
            tf_result.rotation.y,
            tf_result.rotation.z,
            tf_result.rotation.w,
        ])

        # yaw 默认是弧度，转换成角度方便观察
        yaw_deg = math.degrees(yaw)

        self.get_logger().info(
            'target_point 在 base_link 中的位置：'
            f'x={tf_result.translation.x:.2f} m，'
            f'y={tf_result.translation.y:.2f} m，'
            f'z={tf_result.translation.z:.2f} m；'
            f'小车到目标点的直线距离={distance:.2f} m；'
            f'两个坐标系之间的偏航角={yaw_deg:.2f}°'
        )


def main(args=None):
    rclpy.init(args=args)
    node = TargetListener()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()