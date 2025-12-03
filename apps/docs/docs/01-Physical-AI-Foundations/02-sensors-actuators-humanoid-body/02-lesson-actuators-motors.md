---
sidebar_position: 2
title: "Lesson 2: Actuators and Motors"
---

# Lesson 2: Actuators and Motors - How Robots Move

## Learning Objectives

By the end of this lesson, you will be able to:
- Explain the difference between actuators and motors
- Compare electric motors, hydraulic actuators, and pneumatic systems
- Understand degrees of freedom and their role in robot capability
- Describe the tradeoffs between power, precision, speed, and efficiency in actuator selection

## How Do Robots Move?

Imagine trying to walk with your legs completely stiff, unable to bend your knees or ankles. You'd quickly realize that movement depends on **joints**—points where parts of your body can rotate or extend.

Robots face the same challenge. A robot's "brain" (its AI) can plan the perfect motion, but without **actuators**—devices that convert energy into physical movement—those plans remain trapped in the digital realm.

In this lesson, you'll learn how robots move, the technologies that power their motion, and why actuator choice fundamentally shapes what a robot can and cannot do.

---

## What Is an Actuator?

An **actuator** is any device that produces motion. In robotics, actuators are the "muscles" that move joints, grippers, wheels, or any movable part.

**Analogy: Your Muscles**
When your brain sends a signal to your arm muscles, they contract, pulling on bones and moving your elbow. Similarly, when a robot's controller sends a signal to an actuator, it produces force or torque, moving a joint.

### Actuator vs. Motor: What's the Difference?

- **Motor**: Specifically refers to a device that converts electrical energy into rotational motion (like a spinning shaft).
- **Actuator**: A broader term that includes motors, but also hydraulic pistons, pneumatic cylinders, and other motion-generating devices.

**All motors are actuators, but not all actuators are motors.**

---

## Types of Actuators

Robotics uses three main actuation technologies:

### 1. Electric Motors

Electric motors are the most common actuators in modern robotics. They convert electrical energy into rotational motion.

#### Types of Electric Motors

**Brushed DC Motors**
- Simple and inexpensive
- Require maintenance (brushes wear out)
- Used in hobby robots and low-cost applications

**Brushless DC Motors (BLDC)**
- More efficient and durable (no brushes)
- Require electronic controllers
- Common in drones, high-performance robots

**Servo Motors**
- Electric motors with built-in position feedback
- Allow precise control of angle and speed
- Standard in robotic arms and humanoid joints

**Stepper Motors**
- Move in discrete "steps" (e.g., 1.8° per step)
- Excellent precision without feedback sensors
- Used in 3D printers, CNC machines

**Analogy: Electric vs. Gasoline Engine**
Think of electric motors like electric cars—instant response, efficient, quiet. Hydraulics (discussed next) are like diesel trucks—incredibly powerful but loud and requiring more infrastructure.

#### Advantages of Electric Motors
- **Precise control** - Can regulate speed, torque, and position accurately
- **Clean** - No fluids or compressed air needed
- **Scalable** - Available from tiny (watch motors) to massive (industrial robots)
- **Efficient** - Modern BLDC motors exceed 90% efficiency

#### Limitations
- **Power density** - For the same weight, hydraulics produce more force
- **Torque limits** - Electric motors struggle with extremely high torque demands
- **Heat** - High-current operation generates heat, requiring cooling

---

### 2. Hydraulic Actuators

**Hydraulic actuators** use pressurized fluid (usually oil) to create linear or rotational motion.

#### How Hydraulics Work

A hydraulic system consists of:
1. **Pump** - Pressurizes the hydraulic fluid
2. **Valves** - Control fluid flow direction and rate
3. **Cylinder or motor** - Converts fluid pressure into motion

**Analogy: Water Balloon Squeeze**
Imagine a long, sealed balloon filled with water. Squeeze one end, and the other end expands. Hydraulics work similarly—pressure applied in one location is transmitted through fluid, creating force elsewhere.

#### Advantages of Hydraulics
- **Extremely high power** - Can exert massive forces (used in excavators, Atlas robot)
- **Smooth motion** - Fluid pressure allows controlled, continuous movement
- **Force multiplication** - Small input creates large output force

#### Limitations
- **Complexity** - Requires pumps, reservoirs, seals, and plumbing
- **Leaks** - Seals degrade over time, causing fluid leaks
- **Weight** - Pumps and fluid add significant mass
- **Noise** - Hydraulic pumps are loud

**When Hydraulics Are Used:**
Boston Dynamics' Atlas uses hydraulic actuators because the robot needs explosive power for jumping and dynamic motions. However, newer robots like Unitree G1 use electric motors to reduce complexity.

---

### 3. Pneumatic Actuators

**Pneumatic actuators** use compressed air instead of fluid.

#### Advantages
- **Lightweight** - Air is lighter than hydraulic fluid
- **Safe** - Air leaks are less problematic than oil leaks
- **Fast** - Can achieve very high speeds

#### Limitations
- **Less precise** - Air compresses, making fine control difficult
- **Lower force** - Pneumatics can't match hydraulic power density
- **Requires compressor** - Need an air compressor and tank

**Common Uses:**
Pneumatics are popular in factory automation (pick-and-place tasks) and soft robotics (inflatable grippers). They're less common in humanoid robots.

---

## Degrees of Freedom (DOF)

When designing a robot, one critical question is: **How many ways can each part move?**

### What Is a Degree of Freedom?

A **degree of freedom (DOF)** is an independent direction in which something can move.

**Analogy: Door vs. Shoulder**
- A door hinge has **1 DOF**—it can only swing open or closed.
- Your shoulder has **3 DOF**—you can move your arm forward/back, up/down, and rotate it.

### DOF in Robotics

Each joint in a robot adds degrees of freedom:
- **1-DOF joint**: Rotates around one axis (like an elbow)
- **2-DOF joint**: Rotates around two axes (like a wrist)
- **3-DOF joint**: Rotates around three axes (like a shoulder)

#### Example: Human Arm
- **Shoulder**: 3 DOF (ball-and-socket joint)
- **Elbow**: 1 DOF (hinge joint)
- **Wrist**: 2 DOF (can bend and rotate)
- **Fingers**: Multiple 1-DOF joints

**Total**: A human arm has approximately **7 DOF** from shoulder to fingertips (excluding individual finger joints).

### Why DOF Matters

More degrees of freedom = more flexibility, but also:
- More actuators (higher cost, weight, power consumption)
- More complex control (harder to coordinate many joints)
- Increased failure points (more things that can break)

**Design Tradeoff:**
A simple gripper might have 1 DOF (open/close). A dexterous robotic hand might have 20+ DOF. The right choice depends on the task.

![Robot Morphology](/img/part1-foundations/robot-morphology.svg)
*Figure 1: Comparison of joint configurations and DOF in different robot designs*

---

## Power, Precision, Speed, and Efficiency: The Four Tradeoffs

When selecting actuators, engineers must balance competing priorities:

### 1. Power (Force/Torque)

**Question:** How much weight can the robot lift or move?

- **Hydraulics**: Highest power density
- **Electric motors**: Moderate power, improving with better materials
- **Pneumatics**: Lower than hydraulics

**Example:** A humanoid robot lifting a heavy box needs high torque in shoulder and elbow joints.

### 2. Precision (Positioning Accuracy)

**Question:** How accurately can the robot position its joints?

- **Electric servos**: Excellent precision (sub-millimeter)
- **Stepper motors**: Extremely precise (discrete steps)
- **Hydraulics**: Good, but fluid compressibility limits precision
- **Pneumatics**: Poorest precision

**Example:** A robotic surgeon needs electric servos for precise tissue manipulation.

### 3. Speed (Response Time)

**Question:** How quickly can the actuator move?

- **Pneumatics**: Fastest (air accelerates quickly)
- **Electric motors**: Fast, especially with low inertia
- **Hydraulics**: Moderate (fluid flow limits speed)

**Example:** A robot catching a thrown ball needs fast actuators.

### 4. Efficiency (Energy Consumption)

**Question:** How much energy is wasted as heat or friction?

- **Electric motors**: Most efficient (80-95%)
- **Hydraulics**: Moderate efficiency (~60%)
- **Pneumatics**: Least efficient (~20-30%, due to air compression losses)

**Example:** A battery-powered mobile robot prioritizes electric motors to extend runtime.

---

## Real-World Example: Humanoid Robot Arms

Let's compare actuator choices for a humanoid robot arm:

### Scenario 1: Industrial Assembly Line

**Task:** Pick up 10 kg metal parts and place them precisely on a conveyor.

**Actuator Choice:** Electric servo motors
- **Reasoning:** Need precision, moderate force, and energy efficiency for continuous operation.

### Scenario 2: Disaster Response Robot

**Task:** Lift heavy debris (50+ kg) in unpredictable environments.

**Actuator Choice:** Hydraulic actuators
- **Reasoning:** Need maximum power-to-weight ratio, even if it adds complexity.

### Scenario 3: Personal Home Robot

**Task:** Hand objects to users, open doors, carry lightweight items.

**Actuator Choice:** Small electric BLDC motors with harmonic drives
- **Reasoning:** Quiet, safe, efficient, and precise—critical for human environments.

---

## Reflection Questions

1. **Design Choice**: You're building a robot to compete in a high-jump competition. Would you choose hydraulic or electric actuators? Justify your answer considering power, weight, and control requirements.

2. **Degrees of Freedom**: A humanoid robot needs to reach objects on high shelves. Which joints (shoulder, elbow, wrist) need the most DOF? Which could have fewer DOF to save cost?

3. **Energy Budget**: A battery-powered humanoid robot needs to operate for 4 hours between charges. How would this constraint influence your actuator selection?

---

## Try With AI

Now that you understand actuator types and tradeoffs, let's use AI to explore actuator selection for a specific robot design.

### Initial Request

> "I'm designing a humanoid robot for warehouse logistics. It needs to walk at human speed, lift 20 kg boxes from floor to shoulder height, and operate for 8-hour shifts. Recommend actuator types for: (1) leg joints (hip, knee, ankle), (2) arm joints (shoulder, elbow, wrist), and (3) gripper. Explain your reasoning including power, precision, and efficiency considerations."

### Critical Evaluation

After receiving the AI's response, check:

- [ ] Does the AI differentiate between leg and arm actuator requirements?
- [ ] Are battery life and energy efficiency mentioned?
- [ ] Does the AI consider the weight of actuators themselves?
- [ ] Are there any safety considerations (e.g., torque limiting near humans)?

### Focused Update

> "The robot will work alongside human warehouse workers. Revise the actuator selection to prioritize safety and quiet operation, even if it reduces maximum lifting capacity. What specific actuator features or technologies would you add?"

### Second Iteration

> "Compare the actuator suite you recommended to the actuators used in real warehouse robots like Boston Dynamics' Stretch or Agility Robotics' Digit. What design choices did commercial robots make differently?"

### Reflection

1. How did the AI's recommendations change when you emphasized safety over performance?
2. What actuator technologies used in commercial robots surprised you?
3. If you had to choose between a robot that lifts 30 kg but operates for 4 hours vs. one that lifts 15 kg but operates for 10 hours, which tradeoff would you make? Why?
