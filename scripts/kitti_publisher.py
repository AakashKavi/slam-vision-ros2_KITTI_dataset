import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import TransformStamped
from tf2_ros import StaticTransformBroadcaster
from cv_bridge import CvBridge
import cv2
import os

class KittiPublisher(Node):
    def __init__(self):
        super().__init__('kitti_publisher')
        self.publisher_left = self.create_publisher(Image, '/stereo_camera/left/image_raw', 10)
        self.publisher_right = self.create_publisher(Image, '/stereo_camera/right/image_raw', 10)
        self.publisher_left_info = self.create_publisher(CameraInfo, '/stereo_camera/left/camera_info', 10)
        self.publisher_right_info = self.create_publisher(CameraInfo, '/stereo_camera/right/camera_info', 10)
        self.bridge = CvBridge()
        self.sequence_path = os.path.expanduser(
            '~/datasets/kitti/2011_09_26/2011_09_26_drive_0002_sync'
        )
        self.left_path = os.path.join(self.sequence_path, 'image_00/data')
        self.right_path = os.path.join(self.sequence_path, 'image_01/data')
        self.images = sorted(os.listdir(self.left_path))
        self.index = 0

        # Publish static TF between left and right camera
        self.tf_broadcaster = StaticTransformBroadcaster(self)
        self.publish_static_tf()

        self.timer = self.create_timer(0.5, self.publish_images)
        self.get_logger().info(f'Found {len(self.images)} image pairs')

    def publish_static_tf(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'left_camera'
        t.child_frame_id = 'right_camera'
        # KITTI stereo baseline is 0.54 meters
        t.transform.translation.x = 0.54
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0
        self.tf_broadcaster.sendTransform(t)
        self.get_logger().info('Published static TF left_camera -> right_camera')

    def make_camera_info_left(self, stamp):
        info = CameraInfo()
        info.header.stamp = stamp
        info.header.frame_id = 'left_camera'
        info.width = 1242
        info.height = 375
        info.k = [7.215377e+02, 0.0, 6.095593e+02,
                  0.0, 7.215377e+02, 1.728540e+02,
                  0.0, 0.0, 1.0]
        info.d = [0.0, 0.0, 0.0, 0.0, 0.0]
        info.distortion_model = 'plumb_bob'
        info.r = [1.0, 0.0, 0.0,
                  0.0, 1.0, 0.0,
                  0.0, 0.0, 1.0]
        # Left camera - Tx is 0
        info.p = [7.215377e+02, 0.0, 6.095593e+02, 0.0,
                  0.0, 7.215377e+02, 1.728540e+02, 0.0,
                  0.0, 0.0, 1.0, 0.0]
        return info

    def make_camera_info_right(self, stamp):
        info = CameraInfo()
        info.header.stamp = stamp
        info.header.frame_id = 'right_camera'
        info.width = 1242
        info.height = 375
        info.k = [7.215377e+02, 0.0, 6.095593e+02,
                  0.0, 7.215377e+02, 1.728540e+02,
                  0.0, 0.0, 1.0]
        info.d = [0.0, 0.0, 0.0, 0.0, 0.0]
        info.distortion_model = 'plumb_bob'
        info.r = [1.0, 0.0, 0.0,
                  0.0, 1.0, 0.0,
                  0.0, 0.0, 1.0]
        # Right camera - Tx = -fx * baseline = -721.5377 * 0.54 = -389.63
        info.p = [7.215377e+02, 0.0, 6.095593e+02, -3.896448e+02,
                  0.0, 7.215377e+02, 1.728540e+02, 0.0,
                  0.0, 0.0, 1.0, 0.0]
        return info

    def publish_images(self):
        if self.index >= len(self.images):
            self.get_logger().info('Sequence finished! Restarting...')
            self.index = 0
            return
        img_name = self.images[self.index]
        left_img = cv2.imread(os.path.join(self.left_path, img_name), cv2.IMREAD_GRAYSCALE)
        right_img = cv2.imread(os.path.join(self.right_path, img_name), cv2.IMREAD_GRAYSCALE)
        if left_img is None or right_img is None:
            self.get_logger().warn(f'Could not read image {img_name}')
            self.index += 1
            return
        stamp = self.get_clock().now().to_msg()
        left_msg = self.bridge.cv2_to_imgmsg(left_img, encoding='mono8')
        right_msg = self.bridge.cv2_to_imgmsg(right_img, encoding='mono8')
        left_msg.header.stamp = stamp
        left_msg.header.frame_id = 'left_camera'
        right_msg.header.stamp = stamp
        right_msg.header.frame_id = 'right_camera'
        self.publisher_left.publish(left_msg)
        self.publisher_right.publish(right_msg)
        self.publisher_left_info.publish(self.make_camera_info_left(stamp))
        self.publisher_right_info.publish(self.make_camera_info_right(stamp))
        self.get_logger().info(f'Published image {self.index + 1}/{len(self.images)}')
        self.index += 1

def main(args=None):
    rclpy.init(args=args)
    node = KittiPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
