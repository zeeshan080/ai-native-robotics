---
sidebar_position: 4
title: "Lab: Sensor Matching Exercise"
---

# Lab: Sensor Matching Exercise

## Overview

In this hands-on lab, you'll apply everything you've learned about sensors, actuators, and humanoid body design. You'll analyze real-world robotics tasks, select appropriate hardware, and justify your design decisions.

**Duration:** 60-90 minutes
**Prerequisites:** Lessons 1-3 of this chapter

---

## Part 1: Sensor Selection Challenge

### Exercise 1.1: Match Sensors to Tasks

For each robotics task below, identify which sensors are **essential**, which are **helpful**, and which are **unnecessary**. Provide a brief justification.

#### Task A: Autonomous Vacuum Robot

**Environment:** Indoor home with furniture, carpets, and pet toys
**Goal:** Navigate rooms, avoid obstacles, return to charging dock

**Sensor Options:**
- LIDAR (360° scanning laser)
- RGB camera (color camera)
- Depth camera (RGB-D)
- IMU (accelerometer + gyroscope)
- Force/torque sensors
- Cliff sensors (detect stairs/drops)

**Your Analysis:**

| Sensor | Essential / Helpful / Unnecessary | Justification |
|--------|-----------------------------------|---------------|
| LIDAR | | |
| RGB camera | | |
| Depth camera | | |
| IMU | | |
| Force/torque | | |
| Cliff sensors | | |

---

#### Task B: Surgical Robot Arm

**Environment:** Operating room, working on human tissue
**Goal:** Follow surgeon's hand movements precisely, apply exact force

**Sensor Options:**
- LIDAR
- RGB camera (high-resolution)
- Depth camera
- IMU
- Force/torque sensors (in tool tip)
- Proximity sensors

**Your Analysis:**

| Sensor | Essential / Helpful / Unnecessary | Justification |
|--------|-----------------------------------|---------------|
| LIDAR | | |
| RGB camera | | |
| Depth camera | | |
| IMU | | |
| Force/torque | | |
| Proximity | | |

---

#### Task C: Warehouse Inventory Robot

**Environment:** Large warehouse with tall shelves, moving forklifts
**Goal:** Navigate aisles, scan barcodes, avoid collisions

**Sensor Options:**
- LIDAR
- RGB camera (for barcode reading)
- Depth camera
- IMU
- Force/torque sensors
- Ultrasonic sensors (for proximity detection)

**Your Analysis:**

| Sensor | Essential / Helpful / Unnecessary | Justification |
|--------|-----------------------------------|---------------|
| LIDAR | | |
| RGB camera | | |
| Depth camera | | |
| IMU | | |
| Force/torque | | |
| Ultrasonic | | |

---

## Part 2: Actuator Selection Challenge

### Exercise 2.1: Choose Actuators for Different Robots

For each robot below, recommend actuator types for specific joints. Consider power requirements, precision needs, energy budget, and safety.

#### Robot A: Home Companion Robot

**Specifications:**
- **Height:** 1.5m (human-scale)
- **Tasks:** Light cleaning, fetch items (max 5 kg), social interaction
- **Battery:** Must run 8 hours on a single charge
- **Environment:** Shared space with children and pets

**Joints to Specify:**

| Joint | Actuator Type | Key Reasoning |
|-------|---------------|---------------|
| Hip (3 DOF) | | |
| Knee (1 DOF) | | |
| Ankle (2 DOF) | | |
| Shoulder (3 DOF) | | |
| Elbow (1 DOF) | | |
| Gripper | | |

---

#### Robot B: Construction Site Robot

**Specifications:**
- **Height:** 2.0m
- **Tasks:** Lift heavy materials (50 kg), operate power tools, work outdoors
- **Power:** Tethered to generator (unlimited power)
- **Environment:** Dusty, uneven terrain, no humans nearby during operation

**Joints to Specify:**

| Joint | Actuator Type | Key Reasoning |
|-------|---------------|---------------|
| Hip (3 DOF) | | |
| Knee (1 DOF) | | |
| Ankle (2 DOF) | | |
| Shoulder (3 DOF) | | |
| Elbow (1 DOF) | | |
| Gripper | | |

---

#### Robot C: Laboratory Research Robot

**Specifications:**
- **Height:** 1.4m
- **Tasks:** Handle delicate equipment, pour liquids, record observations
- **Battery:** 4 hours runtime (frequent recharge acceptable)
- **Environment:** Controlled lab, working alongside human researchers

**Joints to Specify:**

| Joint | Actuator Type | Key Reasoning |
|-------|---------------|---------------|
| Hip (3 DOF) | | |
| Knee (1 DOF) | | |
| Ankle (2 DOF) | | |
| Shoulder (3 DOF) | | |
| Elbow (1 DOF) | | |
| Gripper | | |

---

## Part 3: Humanoid Design Challenge

### Exercise 3.1: Design a Humanoid for a Specific Task

**Scenario:**
You've been hired to design a humanoid robot for **airport passenger assistance**. The robot will:

1. Greet passengers and answer questions
2. Guide passengers to their gates
3. Carry luggage (up to 20 kg)
4. Operate elevators and open doors
5. Navigate crowded terminals safely

**Your Task:**
Complete the design specification below.

#### Body Plan Design

**Total Height:** _________ meters

**Justification:**

---

**Head Configuration:**

| Component | Specification | Justification |
|-----------|---------------|---------------|
| Sensors | | |
| Neck DOF | | |
| Display/Face | | |

---

**Torso Design:**

| Feature | Choice (Rigid / Articulated) | Justification |
|---------|------------------------------|---------------|
| Spine | | |
| Component Housing | | |
| Balance Strategy | | |

---

**Arm Design:**

| Joint Group | DOF | Actuator Type | Payload Capacity |
|-------------|-----|---------------|------------------|
| Shoulder | | | |
| Elbow | | | |
| Wrist | | | |
| Hand/Gripper | | | |

---

**Leg Design:**

| Joint Group | DOF | Actuator Type | Special Features |
|-------------|-----|---------------|------------------|
| Hip | | | |
| Knee | | | |
| Ankle | | | |
| Foot | | | |

---

**Sensor Suite:**

List all sensors and their placement:

1.
2.
3.
4.
5.

---

**Safety Features:**

How will your robot ensure passenger safety?

1.
2.
3.

---

**Battery and Runtime:**

- **Battery Capacity:** _________ kWh
- **Expected Runtime:** _________ hours
- **Charging Strategy:** _________

---

## Part 4: Comparative Analysis

### Exercise 4.1: Humanoid vs. Alternative Designs

For the airport assistant robot scenario above, compare your humanoid design to two alternatives:

#### Alternative 1: Wheeled Robot (like airport cart)

**Advantages over humanoid:**
1.
2.
3.

**Disadvantages vs. humanoid:**
1.
2.
3.

---

#### Alternative 2: Quadruped Robot (like Boston Dynamics Spot)

**Advantages over humanoid:**
1.
2.
3.

**Disadvantages vs. humanoid:**
1.
2.
3.

---

**Final Recommendation:**
Which design (humanoid, wheeled, or quadruped) would you recommend for the airport assistant role? Why?

---

## Part 5: Reflection and Discussion

### Critical Thinking Questions

1. **Sensor Redundancy:**
   In your airport robot design, which sensors should have backups in case of failure? How would you detect sensor malfunction?

2. **Graceful Degradation:**
   If the robot's depth camera fails, how can it continue operating safely using remaining sensors? What functionality would be lost?

3. **Real-World Constraints:**
   Airport terminals have strict safety regulations. What certifications or safety features would your robot need before deployment? How might this affect your design choices?

4. **Ethical Considerations:**
   Some travelers may be uncomfortable with humanoid robots. How could your design address this? Would a less human-like appearance be better?

---

## Try With AI

Now let's use AI to validate and extend your designs.

### Initial Request

> "I designed a humanoid robot for airport passenger assistance with the following specifications: [paste your design from Part 3]. Review this design and identify: (1) potential safety issues, (2) component cost estimates, (3) any missing sensors or actuators, (4) possible failure modes. Provide specific recommendations for improvements."

### Critical Evaluation

After receiving the AI's response, check:

- [ ] Did the AI identify realistic safety concerns you missed?
- [ ] Are the cost estimates reasonable (compare to commercial robots if possible)?
- [ ] Does the AI suggest any sensors you hadn't considered?
- [ ] Are the failure modes plausible and serious?

### Focused Update

> "The airport wants the robot to also assist passengers with disabilities (wheelchair users, visually impaired, hearing impaired). How should the design change to accommodate these requirements? Focus on sensors, interface design, and safety features."

### Second Iteration

> "Compare my design to real airport robots like LG's CLOi GuideBot or SoftBank's Pepper (used in some airports). What design decisions did they make differently? Which approach is better for the airport assistant task?"

### Reflection

1. What design flaws did the AI identify that you missed? Why do you think you overlooked them?
2. Did adding accessibility requirements significantly change the design? Which changes were most important?
3. After learning about real airport robots, would you change your humanoid/wheeled/quadruped recommendation? Why or why not?

---

## Submission Checklist

Before completing this lab, ensure you've:

- [ ] Completed sensor matching for all 3 tasks (Exercise 1.1)
- [ ] Specified actuators for all 3 robot types (Exercise 2.1)
- [ ] Created a complete humanoid design for the airport scenario (Exercise 3.1)
- [ ] Compared humanoid to alternative morphologies (Exercise 4.1)
- [ ] Answered all reflection questions (Part 5)
- [ ] Completed the "Try With AI" sections with actual AI prompts and reflections

---

## What You've Accomplished

By completing this lab, you've:

✅ **Applied sensor selection** principles to real-world tasks
✅ **Made actuator tradeoffs** based on performance requirements
✅ **Designed a full humanoid robot** from scratch
✅ **Compared morphologies** and justified design choices
✅ **Used AI critically** to validate and improve your designs

These skills form the foundation for the hardware understanding you'll need as you progress to simulation, control, and AI integration in upcoming chapters.

**Next:** Chapter 3 - The Humanoid Robotics Landscape
