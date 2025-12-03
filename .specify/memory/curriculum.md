# Physical AI & Humanoid Robotics Curriculum

> **Canonical Source** - This file is the single source of truth for course structure.
> All content agents MUST reference this file before writing lessons.
> **Authoritative Structure**: See `.specify/memory/project-index.md` for Part/Chapter/Lesson hierarchy.

## Course Identity

**Title:** Physical AI & Humanoid Robotics
**Theme:** AI Systems in the Physical World. Embodied Intelligence.
**Duration:** 13 Weeks (1 Quarter)
**Prerequisites:** Python proficiency, basic AI/ML knowledge

## Course Goal

Bridging the gap between the digital brain and the physical body. Students apply their AI knowledge to control Humanoid Robots in simulated and real-world environments.

## Course Overview

The future of AI extends beyond digital spaces into the physical world. This capstone quarter introduces Physical AI—AI systems that function in reality and comprehend physical laws. Students learn to design, simulate, and deploy humanoid robots capable of natural human interactions using ROS 2, Gazebo, and NVIDIA Isaac.

---

## Course Structure (per project-index.md)

The course is organized into **6 Parts** with **18 Chapters**:

| Part | Title | Chapters | Weeks | Tier |
|------|-------|----------|-------|------|
| Part 1 | Physical AI Foundations | 1-3 | 1-2 | A2 (Beginner-Intermediate) |
| Part 2 | ROS 2 Fundamentals | 4-7 | 3-5 | B1 (Intermediate) |
| Part 3 | Simulation Systems | 8-11 | 6-7 | B2 (Intermediate+) |
| Part 4 | NVIDIA Isaac Robotics AI | 12-14 | 8-10 | C1 (Advanced) |
| Part 5 | Vision-Language-Action | 15-17 | 11-12 | C2 (Expert) |
| Part 6 | Capstone Project | 18 | 13 | C2 (Expert Integration) |

---

## Part 1 — Physical AI Foundations (Weeks 1-2)
**Tier:** A2 (Beginner-Intermediate)
**Layer:** L1 (Conceptual Foundations)
**Focus:** Building mental models before any code
**Folder:** `01-Physical-AI-Foundations/`

### Chapter 1: What Is Physical AI? The Rise of Embodied Intelligence
**Folder:** `01-what-is-physical-ai/`

**Lessons:**
- Digital AI vs Physical AI
- The Embodiment Hypothesis
- Real-world Constraints (latency, power, safety)
- Lab: Try With AI exercises

### Chapter 2: Sensors, Actuators & The Humanoid Body Plan
**Folder:** `02-sensors-actuators-humanoid-body/`

**Lessons:**
- How Robots Sense (LIDAR, cameras, IMUs, force/torque)
- Actuators and Movement
- The Humanoid Body Plan
- Lab: Sensor identification exercises

### Chapter 3: The Humanoid Robotics Landscape
**Folder:** `03-humanoid-robotics-landscape/`

**Lessons:**
- Why Humanoid Form?
- Current Platforms (Atlas, Figure 01, Optimus, Unitree G1)
- Challenges and Future Directions
- Lab: Research humanoid robots

**Transition Check:** Can students sketch a robot model and annotate sensors/joints?

---

## Part 2 — ROS 2 Fundamentals (Weeks 3-5)
**Tier:** B1 (Intermediate)
**Layer:** L2-L3 (Simulation + Control)
**Focus:** Middleware for robot control
**Folder:** `02-ROS2-Fundamentals/`

### Chapter 4: ROS 2 Architecture
**Folder:** `04-ros2-architecture/`
- Nodes, Topics, Services, and Actions

### Chapter 5: Creating ROS 2 Packages with Python
**Folder:** `05-ros2-packages-with-python/`
- Building ROS 2 packages with rclpy

### Chapter 6: URDF for Humanoids
**Folder:** `06-urdf-for-humanoids/`
- Robot Description Fundamentals

### Chapter 7: Bridging AI Agents to ROS 2
**Folder:** `07-ai-agent-ros2-bridge/`
- Connecting Python agents to ROS controllers

**Transition Check:** Can students create a ROS 2 node that publishes and subscribes to topics?

---

## Part 3 — Simulation Systems (Weeks 6-7)
**Tier:** B2 (Intermediate+)
**Layer:** L2 (Simulation)
**Focus:** Physics simulation and environment building
**Folder:** `03-Simulation-Systems/`

### Chapter 8: Digital Twins
**Folder:** `08-digital-twins-simulation/`
- Building simulated robots

### Chapter 9: Gazebo Simulation
**Folder:** `09-gazebo-simulation/`
- Physics, sensors, collisions

### Chapter 10: Unity for Robotics
**Folder:** `10-unity-for-robotics/`
- High-fidelity visualization (optional)

### Chapter 11: Sensor Simulation
**Folder:** `11-sensor-simulation/`
- LiDAR, Depth, IMU, RGB-D

**Transition Check:** Can students modify URDF/SDF and see the effect in simulation?

---

## Part 4 — NVIDIA Isaac Robotics AI (Weeks 8-10)
**Tier:** C1 (Advanced Robotics)
**Layer:** L2-L3 (Simulation + Control)
**Focus:** Advanced perception and training
**Folder:** `04-NVIDIA-Isaac-AI/`

### Chapter 12: Isaac Sim Fundamentals
**Folder:** `12-isaac-sim-fundamentals/`
- Environments, USD, Articulations

### Chapter 13: Isaac ROS Perception
**Folder:** `13-isaac-ros-perception/`
- VSLAM, AprilTags, Depth, Navigation

### Chapter 14: Nav2 for Humanoids
**Folder:** `14-nav2-humanoid-path-planning/`
- Bipedal Path Planning & Control

**Transition Check:** Can students run Isaac Sim and deploy a trained model to Jetson?

---

## Part 5 — Vision-Language-Action (Weeks 11-12)
**Tier:** C2 (Expert)
**Layer:** L4 (VLA Integration)
**Focus:** The convergence of LLMs and Robotics
**Folder:** `05-Vision-Language-Action/`

### Chapter 15: Whisper for Voice-to-Action
**Folder:** `15-whisper-voice-to-action/`
- Voice commands using OpenAI Whisper

### Chapter 16: Cognitive Planning
**Folder:** `16-cognitive-planning-llm-to-ros2/`
- From "Clean the Room" to ROS 2 Actions

### Chapter 17: Multimodal Perception
**Folder:** `17-multimodal-perception-humanoid/`
- Vision + Language + Action for humanoids

**Transition Check:** Can students design test cases for voice commands?

---

## Part 6 — Capstone Project (Week 13)
**Tier:** C2 (Expert Integration)
**Layer:** L5 (Capstone Integration)
**Focus:** Full pipeline integration
**Folder:** `06-Capstone/`

### Chapter 18: Build an Autonomous Humanoid Robot
**Folder:** `18-capstone-autonomous-humanoid/`

**Capstone Project: The Autonomous Humanoid**
A final project where a simulated robot:
1. Receives a voice command
2. Plans a path using LLM
3. Navigates obstacles
4. Identifies an object using computer vision
5. Manipulates the object

**Transition Check:** Did student design reasonable specification respecting safety constraints?

---

## Learning Outcomes

Upon completion, students will be able to:

1. **Explain** Physical AI principles and embodied intelligence
2. **Master** ROS 2 (Robot Operating System) for robotic control
3. **Simulate** robots with Gazebo and Unity
4. **Develop** with NVIDIA Isaac AI robot platform
5. **Design** humanoid robots for natural interactions
6. **Integrate** GPT models for conversational robotics
7. **Build** voice → text → plan → ROS 2 → safe behavior pipelines

---

## Assessments

| Assessment | Part | Weight |
|------------|------|--------|
| ROS 2 package development project | Part 2 | 20% |
| Gazebo simulation implementation | Part 3 | 20% |
| Isaac-based perception pipeline | Part 4 | 25% |
| Capstone: Simulated humanoid with conversational AI | Parts 5-6 | 35% |

---

## Hardware Requirements

### Tier 1: The "Digital Twin" Workstation (Required)

> **Critical:** NVIDIA Isaac Sim requires RTX capabilities. Standard laptops will NOT work.

| Component | Specification | Notes |
|-----------|--------------|-------|
| **GPU** | NVIDIA RTX 4070 Ti (12GB) minimum | Ideal: RTX 3090/4090 (24GB) |
| **CPU** | Intel Core i7 (13th Gen+) or AMD Ryzen 9 | Physics calculations are CPU-intensive |
| **RAM** | 64 GB DDR5 | 32 GB absolute minimum |
| **OS** | Ubuntu 22.04 LTS | ROS 2 Humble/Iron native to Linux |

### Tier 2: The "Physical AI" Edge Kit

> For deploying to real hardware and understanding resource constraints.

| Component | Model | Price | Purpose |
|-----------|-------|-------|---------|
| **Brain** | NVIDIA Jetson Orin Nano Super (8GB) | ~$249 | Industry standard for embodied AI |
| **Eyes** | Intel RealSense D435i | ~$349 | RGB + Depth + IMU for SLAM |
| **Ears** | ReSpeaker USB Mic Array v2.0 | ~$69 | Voice commands (Part 5) |
| **Storage** | 128GB High-endurance SD Card | ~$30 | OS and models |
| **Total** | | **~$700** | |

### Tier 3: The Robot Lab (Optional Tiers)

**Option A: Proxy Approach (Budget)**
- Robot: Unitree Go2 Edu (~$1,800-$3,000)
- Pros: Durable, excellent ROS 2 support
- Cons: Not bipedal (quadruped)

**Option B: Miniature Humanoid**
- Robot: Unitree G1 (~$16k) or Hiwonder TonyPi Pro (~$600)
- Note: Budget kits run on Raspberry Pi (no Isaac ROS)

**Option C: Premium Lab**
- Robot: Unitree G1 Humanoid
- Full sim-to-real deployment capability

### Cloud Alternative (High OpEx)

| Resource | Specification | Cost |
|----------|--------------|------|
| Instance | AWS g5.2xlarge (A10G, 24GB VRAM) | ~$1.50/hour |
| Usage | 10 hours/week × 12 weeks | 120 hours |
| Storage | EBS volumes | ~$25/quarter |
| **Total** | | **~$205/quarter** |

> **Warning:** Cloud simulation works for training, but controlling real robots requires local deployment due to latency.

---

## Why Physical AI Matters

Humanoid robots are poised to excel in our human-centered world because they share our physical form and can be trained with abundant data from interacting in human environments. This represents a significant transition from AI models confined to digital environments to **embodied intelligence** that operates in physical space.

---

## Layer Mapping Reference

| Part | Weeks | Content | Constitution Layer |
|------|-------|---------|-------------------|
| Part 1 | 1-2 | Physical AI Foundations | L1 - Conceptual Foundations |
| Part 2 | 3-5 | ROS 2 Fundamentals | L2-L3 - Simulation + Control |
| Part 3 | 6-7 | Simulation Systems | L2 - Simulation |
| Part 4 | 8-10 | NVIDIA Isaac Platform | L2-L3 - Simulation + Control |
| Part 5 | 11-12 | Vision-Language-Action | L4 - VLA Integration |
| Part 6 | 13 | Capstone Project | L5 - Capstone Integration |

---

## Content Creation Rules

When writing lessons for this curriculum:

1. **Always reference this file AND project-index.md** before writing any content
2. **Check the layer** - don't introduce L3 concepts in L1 lessons
3. **Respect prerequisites** - Part 2 assumes Part 1 knowledge
4. **Use "Try With AI" pattern** for all lessons (see constitution)
5. **Hardware awareness** - warn when content requires specific hardware
6. **Safety first** - all robot examples are simulation-first
7. **Follow folder structure** - use exact folder names from project-index.md

---

**Version:** 2.0.0
**Created:** 2025-11-29
**Last Updated:** 2025-11-29
**Aligned with:** project-index.md v2025-02-27
