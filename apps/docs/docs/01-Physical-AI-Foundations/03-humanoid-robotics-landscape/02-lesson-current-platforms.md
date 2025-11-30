---
sidebar_position: 2
title: "Lesson 2: Current Platforms"
---

# Lesson 2: Current Platforms

## Learning Objectives

By the end of this lesson, you will be able to:
- Identify the major humanoid robot platforms and their key characteristics
- Compare different design philosophies in humanoid robotics
- Understand the relationship between robot capabilities and intended applications
- Evaluate trade-offs between performance, cost, and accessibility

## Introduction

The year is 2024, and humanoid robots have moved from science fiction to engineering reality. In labs and facilities around the world, robots are learning to walk, manipulate objects, and navigate complex environments. But these robots aren't all the same—each platform represents different design philosophies, capabilities, and visions for the future.

In this lesson, you'll meet four pioneering humanoid platforms. Think of this as meeting the "class of 2024" in humanoid robotics—each with its own personality, strengths, and approach to the challenge of embodied intelligence.

**Important Note**: Throughout this course, you'll be working primarily in simulation. You don't need any special hardware to learn the concepts and skills covered in Part 1. We'll explore simulation environments in later chapters, but for now, focus on understanding the capabilities and design principles of these remarkable machines.

## Boston Dynamics Atlas: The Athletic Pioneer

### Overview

If humanoid robots had an Olympics, Atlas would dominate the gymnastics competition. Developed by Boston Dynamics over more than a decade, Atlas represents the cutting edge of dynamic locomotion and acrobatic capability.

**Key Specifications**:
- Height: 1.5 meters (5 feet)
- Weight: 89 kg (196 lbs)
- Actuation: Hydraulic (fluid-powered muscles)
- Degrees of Freedom: 28
- Development Start: 2013

### What Makes Atlas Special

**Hydraulic Power**: Unlike most robots that use electric motors, Atlas uses hydraulic actuators—think of them as artificial muscles powered by pressurized fluid. This gives Atlas:

- **Explosive power**: Ability to jump, backflip, and perform parkour
- **High force output**: Can lift and manipulate heavy objects
- **Dynamic balance**: Rapid corrections during challenging movements

**Analogy**: If electric motors are like bicycle gears—precise and efficient—hydraulic actuators are like a powerful engine. You sacrifice some efficiency for raw power and responsiveness.

**State-of-the-Art Mobility**: Atlas has demonstrated capabilities that seemed impossible a decade ago:

- Backflips and parkour movements
- Running across uneven terrain
- Recovering from pushes and slips
- Jumping between platforms at different heights

### The Trade-offs

Atlas is a research platform, not a commercial product. Its hydraulic system requires:

- Large, loud power units
- Regular maintenance
- Significant energy consumption
- Specialized expertise to operate

**Intended Purpose**: Atlas exists to push the boundaries of what's possible. It's a testbed for advanced control algorithms and a demonstration of state-of-the-art robotics research.

## Figure 01: The AI-First Approach

### Overview

Figure AI represents a new generation of robotics companies: AI-native from the ground up. Founded in 2022, Figure's approach integrates large language models (LLMs) and vision-language models directly into robot control.

**Key Specifications**:
- Height: 1.68 meters (5'6")
- Weight: ~60 kg (132 lbs)
- Actuation: Electric motors
- Focus: Manipulation and human-robot interaction
- Notable Partnership: OpenAI collaboration

### What Makes Figure 01 Special

**Vision-Language-Action (VLA) Integration**: Figure 01 can:

- Understand voice commands in natural language
- Reason about objects in its environment using vision
- Plan and execute multi-step tasks
- Explain its actions and decisions

**Example interaction**:
- Human: "Please put the blue block in the box"
- Figure 01: *Identifies blue block, plans grasp, executes pickup, places in box*
- Human: "Why did you pick that one?"
- Figure 01: "It was the only blue block within reach on the table"

**Analogy**: If Atlas is a trained athlete who can execute complex movements, Figure 01 is more like a capable assistant who understands what you want and figures out how to do it. The emphasis shifts from raw physical capability to intelligent decision-making.

**Electric Actuation**: Unlike Atlas, Figure 01 uses electric motors, which provide:

- Quieter operation
- Lower maintenance requirements
- More predictable power consumption
- Easier integration with standard facilities

### The Trade-offs

Figure 01 prioritizes cognitive capability over athletic performance:

- Less dynamic movement than Atlas
- Slower, more deliberate motions
- Focus on manipulation over locomotion
- Still in early development stages

**Intended Purpose**: Figure's goal is deployment in real-world work environments—warehouses, manufacturing facilities, eventually homes and offices. The question they're answering: "Can AI make robots useful enough to justify their complexity?"

## Tesla Optimus: The Mass Production Vision

### Overview

When Tesla announced Optimus (also called Tesla Bot), the robotics community took notice—not because Tesla invented new robotics technology, but because of their manufacturing expertise. Optimus represents a bet on making humanoid robots economically viable through mass production.

**Key Specifications**:
- Height: 1.73 meters (5'8")
- Weight: ~56 kg (123 lbs)
- Actuation: Electric motors
- Production Goal: Millions of units
- Target Price: Eventually under $20,000

### What Makes Optimus Special

**Manufacturing-First Philosophy**: Tesla approaches Optimus the way they approach cars:

- Design for manufacturability
- Vertical integration (making components in-house)
- Iterative improvement through versions
- Economies of scale

**Analogy**: Think about the difference between a hand-crafted luxury car and a mass-produced Tesla Model 3. Optimus aims to be the "Model 3" of humanoid robots—not the most advanced in any single capability, but affordable and reliable enough for widespread deployment.

**Tesla Ecosystem Integration**:

- Computer vision from Full Self-Driving (FSD) development
- Battery technology from electric vehicles
- Motor and actuator manufacturing expertise
- Massive training data infrastructure

**Current Capabilities** (rapidly evolving):

- Walking and basic locomotion
- Object sorting and manipulation
- Autonomous navigation
- Operating in structured environments (like factories)

### The Trade-offs

Optimus is optimizing for different metrics than research platforms:

- Prioritizes reliability over peak performance
- Conservative movement to avoid falls and damage
- Cost constraints influence design choices
- Still proving capabilities compared to established platforms

**Intended Purpose**: Tesla envisions Optimus as a general-purpose robot that could:

- Work in Tesla factories (initial deployment)
- Perform repetitive or dangerous tasks
- Eventually assist in homes and businesses
- Become affordable through volume production ($20k-$30k target)

## Unitree G1: The Accessible Humanoid

### Overview

Unitree Robotics, known for their affordable quadruped robots, entered the humanoid space with G1. This platform represents a different approach: making advanced humanoid robotics accessible to researchers, universities, and developers.

**Key Specifications**:
- Height: 1.27 meters (4'2")
- Weight: ~35 kg (77 lbs)
- Actuation: Electric motors
- Price: ~$16,000
- Degrees of Freedom: 23-43 (depending on configuration)

### What Makes Unitree G1 Special

**Accessibility Focus**: G1 is designed to be:

- Affordable enough for university labs
- Modular and hackable for research
- Well-documented with ROS 2 support
- Available for purchase (not vaporware)

**Analogy**: If Atlas is a Formula 1 race car and Optimus is a production sedan, Unitree G1 is like a hobbyist kit car—smaller, more accessible, and designed for tinkering and learning rather than ultimate performance.

**Impressive Capabilities for Size**:

- Walking speeds up to 2 m/s
- 360-degree vision system
- 3D LiDAR for environment mapping
- Demonstrated object manipulation
- Surprisingly robust for its weight class

**ROS 2 Native Design**: Unlike some commercial platforms, G1 is designed with the robotics research community in mind:

- Full ROS 2 support out of the box
- Open interfaces for custom development
- Simulation models available (Gazebo, Isaac Sim)
- Active developer community

### The Trade-offs

G1's accessibility comes with limitations:

- Smaller size limits payload capacity
- Less powerful actuators than larger platforms
- Reduced runtime compared to larger battery capacity platforms
- Focus on development/research over deployment

**Intended Purpose**: Unitree G1 aims to democratize humanoid robotics research. It's the platform you might actually use in a university robotics lab or for personal research projects.

## Comparing the Platforms

| Platform | Philosophy | Key Strength | Primary Trade-off | Availability |
|----------|-----------|--------------|-------------------|--------------|
| **Atlas** | Push boundaries | Athletic capability | Complexity, cost | Research only |
| **Figure 01** | AI-first | Cognitive ability | Early stage | Limited deployment |
| **Optimus** | Mass production | Scalability | Proving capabilities | Internal Tesla use |
| **Unitree G1** | Accessibility | Price, openness | Size, payload | Purchasable now |

## Beyond These Four

These aren't the only humanoid robots being developed. Other notable platforms include:

- **Agility Robotics Digit**: Optimized for logistics and package handling
- **Sanctuary AI Phoenix**: Focus on teleoperation and learning from demonstration
- **Apptronik Apollo**: Modular design for various applications
- **1X Technologies NEO**: Human-like appearance for service roles

Each platform represents different bets about what capabilities matter most and what markets will emerge first.

## Reflection Questions

1. **Design Philosophy**: If you were designing a humanoid robot for use in a hospital, which platform's approach (Atlas's athleticism, Figure's AI-first design, Optimus's manufacturability, or G1's accessibility) would you prioritize? Why?

2. **Capability vs. Cost**: Unitree G1 costs about $16,000 while Atlas is likely millions of dollars. For a university robotics program with a $50,000 budget, would you buy three G1 robots or pool resources with other universities for one Atlas? What factors influence this decision?

3. **Evolution Prediction**: These platforms are all evolving rapidly. In five years, which capabilities do you think will have improved most: locomotion, manipulation, cognitive reasoning, or energy efficiency? What might drive those improvements?

## Try With AI

Now that you've learned about different humanoid platforms, let's use AI to deepen your understanding and explore these robots from different perspectives.

### Initial Request

> "I'm studying four major humanoid robot platforms: Boston Dynamics Atlas, Figure 01, Tesla Optimus, and Unitree G1. Can you create a comparison table that shows which platform would be best suited for three different scenarios: (1) warehouse package sorting, (2) assisting elderly people in a home, and (3) conducting research on bipedal locomotion algorithms. For each scenario, explain your reasoning."

### Critical Evaluation

Review the AI's response using these criteria:

- [ ] **Does the AI correctly match capabilities to requirements?** (For example, Atlas is overkill for most practical tasks)
- [ ] **Does it consider availability and cost?** (You can't deploy what you can't buy)
- [ ] **Are safety considerations mentioned?** (Home use has very different requirements than lab use)
- [ ] **Does it acknowledge what's realistic now vs. future capabilities?** (Some platforms are more proven than others)

### Focused Update

Choose one scenario from the AI's response and dig deeper:

> "For the [warehouse/home/research] scenario, you suggested [platform name]. Can you detail the specific technical requirements this application demands—like runtime duration, payload capacity, navigation precision, and safety features—and explain how [platform]'s specifications match these needs?"

### Second Iteration

After reviewing the detailed technical breakdown:

> "Now identify the three biggest technical challenges or limitations that [platform] would face in the [scenario] application. What would need to improve for this to be a reliable, deployable solution?"

### Reflection

Think about your interaction with the AI:

1. **Information Quality**: Did the AI provide information consistent with what you learned in the lesson? If there were discrepancies, which source seems more reliable and why?

2. **Depth of Reasoning**: When you asked for specific technical requirements, did the AI demonstrate understanding of trade-offs between different specifications (e.g., runtime vs. payload capacity), or did it just list features?

3. **Practical vs. Aspirational**: Did the AI distinguish between what these robots can do now versus their potential future capabilities? This distinction is crucial in Physical AI—the gap between demonstration and deployment is often years.

**Key Learning**: AI can help you analyze and compare complex systems, but your understanding of the fundamentals (sensor requirements, actuation trade-offs, energy constraints) is what allows you to evaluate whether the AI's analysis is grounded in physical reality or just plausible-sounding text.

As you continue in this course, you'll develop the technical knowledge to not just use AI as an information source, but as a reasoning partner that helps you explore the design space of robotic systems.
