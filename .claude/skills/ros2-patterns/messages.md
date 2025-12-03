# ROS 2 Common Message Types

## Standard Messages (std_msgs)

| Message | Fields | Use Case |
|---------|--------|----------|
| `String` | `data: string` | Text data |
| `Int32` | `data: int32` | Integer values |
| `Float64` | `data: float64` | Decimal values |
| `Bool` | `data: bool` | True/False |
| `Header` | `stamp, frame_id` | Timestamp and frame |

## Geometry Messages (geometry_msgs)

| Message | Fields | Use Case |
|---------|--------|----------|
| `Point` | `x, y, z` | 3D position |
| `Vector3` | `x, y, z` | 3D vector |
| `Quaternion` | `x, y, z, w` | Rotation |
| `Pose` | `position, orientation` | Position + rotation |
| `Twist` | `linear, angular` | Velocity command |
| `Transform` | `translation, rotation` | Coordinate transform |

## Sensor Messages (sensor_msgs)

| Message | Fields | Use Case |
|---------|--------|----------|
| `Image` | `header, data, encoding` | Camera images |
| `LaserScan` | `ranges, intensities` | Lidar data |
| `Imu` | `orientation, angular_velocity, linear_acceleration` | IMU sensor |
| `JointState` | `name, position, velocity, effort` | Joint positions |
| `PointCloud2` | `header, data, fields` | 3D point cloud |

## Navigation Messages (nav_msgs)

| Message | Fields | Use Case |
|---------|--------|----------|
| `Odometry` | `pose, twist` | Robot odometry |
| `Path` | `poses[]` | Planned path |
| `OccupancyGrid` | `data, resolution` | Map data |

## Import Examples

```python
# Standard messages
from std_msgs.msg import String, Int32, Float64, Bool

# Geometry messages
from geometry_msgs.msg import Twist, Pose, Point, Vector3

# Sensor messages
from sensor_msgs.msg import Image, LaserScan, Imu, JointState

# Navigation messages
from nav_msgs.msg import Odometry, Path
```

## Quality of Service (QoS)

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

# Sensor data QoS (best effort, keep last)
sensor_qos = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    depth=10
)

# Reliable QoS (for commands)
reliable_qos = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    history=HistoryPolicy.KEEP_LAST,
    depth=10
)
```
