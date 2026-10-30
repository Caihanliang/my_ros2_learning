from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'urdf_rviz_gazebo_intro_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # 安装两个 Python launch 文件。
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py'),
        ),

        # 安装 RViz 配置。
        (
            os.path.join('share', package_name, 'rviz'),
            glob('rviz/*'),
        ),

        # 安装 urdf 根目录下的 01～06 阶段入口。
        (
            os.path.join('share', package_name, 'urdf'),
            glob('urdf/*.urdf') + glob('urdf/*.xacro'),
        ),

        # 子目录必须单独声明，否则组件 include 会在安装后找不到。
        (
            os.path.join('share', package_name, 'urdf', 'components'),
            glob('urdf/components/*.xacro'),
        ),
        # 相对于上节，多了worlds文件夹
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.sdf')),
        
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        # 安装 RViz 配置。
        (
            os.path.join('share', package_name, 'rviz'),
               glob('rviz/*'),
        ),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.sdf')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='holly',
    maintainer_email='3228828366@qq.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
