# URDF Validation Rules

## Required Elements Checklist

### Every Link Must Have

- [ ] `<visual>` - How the link looks
- [ ] `<collision>` - Collision boundary (can differ from visual)
- [ ] `<inertial>` - Mass and inertia properties
  - [ ] `<mass value="X"/>` - Realistic mass in kg
  - [ ] `<inertia>` - Inertia tensor (ixx, ixy, ixz, iyy, iyz, izz)

### Every Joint Must Have

- [ ] `type` attribute - continuous, revolute, prismatic, fixed
- [ ] `<parent link="..."/>` - Parent link name
- [ ] `<child link="..."/>` - Child link name
- [ ] `<origin>` - Position and orientation relative to parent

### Revolute/Prismatic Joints Must Have

- [ ] `<limit>` element with:
  - [ ] `lower` - Minimum position (rad or m)
  - [ ] `upper` - Maximum position (rad or m)
  - [ ] `effort` - Maximum force/torque (N or Nm)
  - [ ] `velocity` - Maximum velocity (rad/s or m/s)

## Safety Validation

### Joint Limits

| Joint Type | Typical Range | Max Effort | Max Velocity |
|------------|---------------|------------|--------------|
| Shoulder | ±180° | 50-100 Nm | 2.0 rad/s |
| Elbow | 0-150° | 30-50 Nm | 2.5 rad/s |
| Wrist | ±90° | 10-20 Nm | 3.0 rad/s |
| Wheel | continuous | 5-20 Nm | 10 rad/s |

### Mass Guidelines

| Component | Typical Mass |
|-----------|--------------|
| Mobile base | 5-50 kg |
| Arm link | 0.5-5 kg |
| Gripper | 0.2-1 kg |
| Sensor | 0.1-0.5 kg |

## Common Errors

### Error: Missing Inertial

```xml
<!-- BAD: No inertial -->
<link name="arm">
  <visual>...</visual>
</link>

<!-- GOOD: Complete link -->
<link name="arm">
  <visual>...</visual>
  <collision>...</collision>
  <inertial>
    <mass value="1.0"/>
    <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
  </inertial>
</link>
```

### Error: Missing Joint Limits

```xml
<!-- BAD: No limits on revolute joint -->
<joint name="shoulder" type="revolute">
  <parent link="base"/>
  <child link="arm"/>
</joint>

<!-- GOOD: Complete joint with limits -->
<joint name="shoulder" type="revolute">
  <parent link="base"/>
  <child link="arm"/>
  <origin xyz="0 0 0.1" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-3.14" upper="3.14" effort="50" velocity="2.0"/>
</joint>
```

## Validation Command

```bash
# Check URDF syntax
check_urdf robot.urdf

# Visualize in RViz
ros2 launch urdf_tutorial display.launch.py model:=robot.urdf
```
