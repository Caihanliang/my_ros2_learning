from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'tf_course_pkg'

# 安装 launch 文件
(
    os.path.join('share', package_name, 'launch'),
    glob(os.path.join('launch', '*.launch.py'))
),

# 安装 config 目录下的 YAML 参数文件
(
    os.path.join('share', package_name, 'config'),
    glob(os.path.join('config', '*.yaml'))
),

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='holly',
    maintainer_email='holly@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'static_target_broadcaster = tf_course_pkg.static_target_broadcaster:main',
            'dynamic_robot_broadcaster = tf_course_pkg.dynamic_robot_broadcaster:main',
            'target_listener = tf_course_pkg.target_listener:main',
        ],
    },
)
