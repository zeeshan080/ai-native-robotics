#!/usr/bin/env python3
"""
ROS 2 Publisher Node Template

This template demonstrates how to create a publisher node that sends
messages to a topic at a regular interval.

Usage:
    ros2 run <package_name> <node_name>

Topics Published:
    /topic_name (std_msgs/String): Example string messages
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PublisherNode(Node):
    """A simple ROS 2 publisher node."""

    def __init__(self):
        """Initialize the publisher node."""
        super().__init__('publisher_node')

        # Create publisher
        # Parameters: message type, topic name, queue size
        self.publisher = self.create_publisher(
            String,
            'topic_name',
            10  # Queue size
        )

        # Create timer for periodic publishing
        # Parameters: period in seconds, callback function
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Initialize counter for demonstration
        self.counter = 0

        self.get_logger().info('Publisher node started')

    def timer_callback(self):
        """Timer callback - publishes a message."""
        # Create message
        msg = String()
        msg.data = f'Hello, ROS 2! Count: {self.counter}'

        # Publish message
        self.publisher.publish(msg)

        # Log the published message
        self.get_logger().info(f'Publishing: "{msg.data}"')

        # Increment counter
        self.counter += 1


def main(args=None):
    """Main entry point."""
    # Initialize ROS 2
    rclpy.init(args=args)

    # Create node
    node = PublisherNode()

    try:
        # Spin (process callbacks)
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
