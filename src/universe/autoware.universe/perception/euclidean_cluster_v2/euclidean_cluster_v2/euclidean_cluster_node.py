import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import PointCloud2
from tier4_perception_msgs.msg import DetectedObjectsWithFeature
from rosgraph_msgs.msg import Clock

class EuclideanClusterNode(Node):
    def __init__(self):
        super().__init__('euclidean_cluster')

        # Define QoS profile to handle incompatible QoS settings
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            depth=10
        )

        # Subscribers
        self.subscription_clock = self.create_subscription(
            Clock,
            '/clock',
            self.clock_callback,
            qos_profile
        )
        
        self.subscription_pointcloud = self.create_subscription(
            PointCloud2,
            '/perception/object_recognition/detection/pointcloud_map_filtered/pointcloud',
            self.pointcloud_callback,
            qos_profile
        )

        # Publishers
        self.publisher_clusters = self.create_publisher(
            DetectedObjectsWithFeature,
            '/perception/object_recognition/detection/clustering/clusters',
            10
        )

        # Timer to publish at 20Hz
        self.timer = self.create_timer(1.0 / 20.0, self.publish_clusters)

        # Placeholder for the most recent point cloud
        self.recent_pointcloud = None
        self.current_time = None

    def clock_callback(self, msg):
        # Update the current time from the /clock topic
        self.current_time = msg.clock

    def pointcloud_callback(self, msg):
        # Save the most recent point cloud
        self.recent_pointcloud = msg
        # self.get_logger().info(f'Received a new PointCloud2 message with frame_id: {msg.header.frame_id}, width: {msg.width}, height: {msg.height}')

    def publish_clusters(self):
        if self.current_time is None:
            # self.get_logger().warn('No /clock message received yet.')
            return

        if self.recent_pointcloud is not None:
            clusters_msg = DetectedObjectsWithFeature()

            # Populate clusters_msg with data (currently empty as placeholder)
            clusters_msg.header.stamp = self.current_time
            clusters_msg.header.frame_id = 'base_link'  # Example frame ID

            # Log and publish
            # self.get_logger().info('Publishing clusters')
            self.publisher_clusters.publish(clusters_msg)
        # else:
        #     self.get_logger().warn('No PointCloud2 data available to process. Ensure the publisher is active.')

def main(args=None):
    rclpy.init(args=args)
    node = EuclideanClusterNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down node')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
