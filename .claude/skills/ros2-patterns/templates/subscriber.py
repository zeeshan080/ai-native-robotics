#!/usr/bin/env python3
"""
ROS 2 Subscriber Node Template

This template demonstrates how to create a subscriber node that receives
messages from a topic and processes them.

Usage:
    ros2 run <package_name> <node_name>

Topics Subscribed:
    /topic_name (std_msgs/String): Incoming string messages
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SubscriberNode(Node):
    """A simple ROS 2 subscriber node."""

    def __init__(self):
        """Initialize the subscriber node."""
        super().__init__('subscriber_node')

        # Create subscription
        # Parameters: message type, topic name, callback, queue size
        self.subscription = self.create_subscription(
            String,
            'topic_name',
            self.listener_callback,
            10  # Queue size
        )

        # Prevent unused variable warning
        self.subscription

        self.get_logger().info('Subscriber node started')

    def listener_callback(self, msg):
        """
        Callback function for incoming messages.

        Args:
            msg: The received String message
        """
        # Log the received message
        self.get_logger().info(f'Received: "{msg.data}"')

        # Process the message here
        self.process_message(msg)

    def process_message(self, msg):
        """
        Process the received message.

        Override this method to add custom processing logic.

        Args:
            msg: The received message
        """
        # Example: Check message content
        if 'error' in msg.data.lower():
            self.get_logger().warning('Error detected in message!')


def main(args=None):
    """Main entry point."""
    # Initialize ROS 2
    rclpy.init(args=args)

    # Create node
    node = SubscriberNode()

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
