# Physical AI & Humanoid Robotics — Chapter Index
**18 Chapters Across 6 Parts**
**Version: 2025-02-27**

This index defines the official structure, naming conventions, and folder layout for the **Physical AI & Humanoid Robotics** book.  
Claude Code agents, Spec-Kit Plus, and RAG pipelines rely on THIS FILE as the authoritative mapping of:

- Parts  
- Chapters  
- Learning objectives  
- Difficulty tiers  
- Folder names  
- Sidebar ordering  

Use this document BEFORE creating any chapter or lesson.

---

# **Part 1 — Physical AI Foundations (Chapters 1–3)**  
**Theme:** Embodied Intelligence, Real-World AI, Humanoid Robotics Overview  
**Tier:** A2 (Beginner–Intermediate)

| # | Chapter Title | File Name | Status |
|---|---------------|-----------|--------|
| 1 | What Is Physical AI? The Rise of Embodied Intelligence | `01-what-is-physical-ai/` | Planned |
| 2 | Sensors, Actuators & The Humanoid Body Plan | `02-sensors-actuators-humanoid-body/` | Planned |
| 3 | The Humanoid Robotics Landscape: Atlas, Figure, Optimus, Unitree | `03-humanoid-robotics-landscape/` | Planned |

---

# **Part 2 — ROS 2 Fundamentals (Chapters 4–7)**  
**Theme:** Robotic Nervous System, Middleware, OS for Robots  
**Tier:** B1 (Intermediate)

| # | Chapter Title | File Name | Status |
|---|---------------|-----------|--------|
| 4 | ROS 2 Architecture: Nodes, Topics, Services, Actions | `04-ros2-architecture/` | Planned |
| 5 | Creating ROS 2 Packages with Python (rclpy) | `05-ros2-packages-with-python/` | Planned |
| 6 | URDF for Humanoids: Robot Description Fundamentals | `06-urdf-for-humanoids/` | Planned |
| 7 | Bridging AI Agents to ROS 2 Controllers | `07-ai-agent-ros2-bridge/` | Planned |

---

# **Part 3 — Simulation Systems (Chapters 8–11)**  
**Theme:** Digital Twins, Physics Simulation, Human-Robot Interaction  
**Tier:** B2 (Intermediate+)

| # | Chapter Title | File Name | Status |
|---|---------------|-----------|--------|
| 8  | Digital Twins: Building Simulated Robots | `08-digital-twins-simulation/` | Planned |
| 9  | Gazebo Simulation: Physics, Sensors, Collisions | `09-gazebo-simulation/` | Planned |
| 10 | Unity for Robotics: High-Fidelity Visualization | `10-unity-for-robotics/` | Planned |
| 11 | Sensor Simulation: LiDAR, Depth, IMU, RGB-D | `11-sensor-simulation/` | Planned |

---

# **Part 4 — NVIDIA Isaac Robotics AI (Chapters 12–14)**  
**Theme:** GPU-Accelerated Perception, VSLAM, Nav2, Synthetic Data  
**Tier:** C1 (Advanced Robotics)

| # | Chapter Title | File Name | Status |
|---|---------------|-----------|--------|
| 12 | Isaac Sim Fundamentals: Environments, USD, Articulations | `12-isaac-sim-fundamentals/` | Planned |
| 13 | Isaac ROS Perception: VSLAM, AprilTags, Depth, Navigation | `13-isaac-ros-perception/` | Planned |
| 14 | Nav2 for Humanoids: Bipedal Path Planning & Control | `14-nav2-humanoid-path-planning/` | Planned |

---

# **Part 5 — Vision-Language-Action (Chapters 15–17)**  
**Theme:** LLM + Robotics Fusion, Cognitive Planning, Multimodal AI  
**Tier:** C2 (Expert)

| # | Chapter Title | File Name | Status |
|---|---------------|-----------|--------|
| 15 | Whisper for Voice-to-Action Control | `15-whisper-voice-to-action/` | Planned |
| 16 | Cognitive Planning: From “Clean the Room” to ROS 2 Actions | `16-cognitive-planning-llm-to-ros2/` | Planned |
| 17 | Multimodal Perception for Humanoids: Vision + Language + Action | `17-multimodal-perception-humanoid/` | Planned |

---

# **Part 6 — Capstone Project (Chapter 18)**  
**Theme:** Fully Autonomous Humanoid  
**Tier:** C2 (Expert Integration)

| # | Chapter Title | File Name | Status |
|---|---------------|-----------|--------|
| 18 | Capstone: Build an Autonomous Humanoid Robot (Simulated) | `18-capstone-autonomous-humanoid/` | Planned |

---

# Directory Structure Rules

Follow the same conventions used by Panaversity:

```
book-source/
└── docs/
    ├── 01-Physical-AI-Foundations/
    │   └── 01-what-is-physical-ai/
    ├── 02-ROS2-Fundamentals/
    │   └── 04-ros2-architecture/
    ├── 03-Simulation-Systems/
    ├── 04-NVIDIA-Isaac-AI/
    ├── 05-Vision-Language-Action/
    └── 06-Capstone/
```

Each chapter folder contains:

```
01-lesson-1.md
02-lesson-2.md
03-lab.md
04-summary.md
```

---

# Usage

Before generating ANY chapter or lesson, Claude Code must:

1. Read **this project-index.md**  
2. Read the part folder structure  
3. Determine the Pedagogical Layer  
4. Match chapter difficulty (A2/B1/B2/C1/C2)  
5. Apply Spec-Driven Development (Section 0 in every chapter)  

---

