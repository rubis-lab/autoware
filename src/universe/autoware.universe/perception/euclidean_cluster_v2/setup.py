from setuptools import find_packages, setup

package_name = 'euclidean_cluster_v2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    py_modules=[
        'euclidean_cluster_v2.euclidean_cluster_node',
    ],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rubis',
    maintainer_email='rubis@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'euclidean_cluster_node = euclidean_cluster_v2.euclidean_cluster_node:main',
        ],
    },
)
