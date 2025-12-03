# Feature Specification: Part 1 — Physical AI Foundations

**Feature Branch**: `003-introduction-physical-ai`
**Created**: 2025-11-29
**Status**: Draft
**Input**: User description: "Part 1 content - Physical AI Foundations (Chapters 1-3) covering Weeks 1-2"

## Overview

This specification defines **Part 1 — Physical AI Foundations** of the Physical AI & Humanoid Robotics course, comprising **Chapters 1-3**. This maps to **Weeks 1-2** and covers Layer 1 (Conceptual Foundations) of the 5-layer pedagogy model.

**Project Index Reference**: `.specify/memory/project-index.md` - Part 1 — Physical AI Foundations (Chapters 1–3)
**Curriculum Reference**: `.specify/memory/curriculum.md` - Introduction: Foundations of Physical AI (Weeks 1-2)
**Difficulty Tier**: A2 (Beginner–Intermediate)

## Part Structure

Based on `project-index.md`:

| Chapter | Title | Folder |
|---------|-------|--------|
| 1 | What Is Physical AI? The Rise of Embodied Intelligence | `01-what-is-physical-ai/` |
| 2 | Sensors, Actuators & The Humanoid Body Plan | `02-sensors-actuators-humanoid-body/` |
| 3 | The Humanoid Robotics Landscape: Atlas, Figure, Optimus, Unitree | `03-humanoid-robotics-landscape/` |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Learn Physical AI Fundamentals (Priority: P1)

A student with Python and basic AI/ML background wants to understand what Physical AI means and why it matters. They need to build mental models of embodied intelligence before diving into robotics code.

**Why this priority**: This is the gateway to the entire course. Without understanding Physical AI concepts, students cannot contextualize subsequent technical modules. This content enables all future learning.

**Independent Test**: Student can articulate the difference between digital AI and Physical AI, and explain why robots need to understand physical laws. Can be verified through the "Try With AI" reflection exercise.

**Chapter Mapping**: Chapter 1 (What Is Physical AI?)

**Acceptance Scenarios**:

1. **Given** a student new to robotics, **When** they complete Chapter 1, **Then** they can explain embodied intelligence in their own words
2. **Given** a student who completed Chapter 1, **When** asked to compare a chatbot vs. a walking robot, **Then** they identify at least 3 unique challenges physical robots face
3. **Given** a student, **When** they finish each lesson, **Then** they can answer the "Try With AI" prompt and critically evaluate the AI's response

---

### User Story 2 - Understand Robot Perception & Body Systems (Priority: P2)

A student wants to understand how robots perceive the world through sensors and how their body plan enables interaction. They need to learn about LIDAR, cameras, IMUs, force/torque sensors, and actuators at a conceptual level.

**Why this priority**: Sensor and body understanding is fundamental to all robotics work. Students must grasp what data robots receive and how they move before learning to process it in later modules.

**Independent Test**: Student can identify which sensor type is appropriate for different tasks (navigation, manipulation, balance) and explain the humanoid body plan.

**Chapter Mapping**: Chapter 2 (Sensors, Actuators & The Humanoid Body Plan)

**Acceptance Scenarios**:

1. **Given** a student with no sensor knowledge, **When** they complete Chapter 2, **Then** they can name 4 sensor types and their primary purposes
2. **Given** a list of robot tasks, **When** asked which sensors are needed, **Then** student correctly matches sensors to tasks with 80% accuracy
3. **Given** a robot diagram, **When** asked to annotate it, **Then** student can label sensor and actuator locations and explain their roles

---

### User Story 3 - Survey the Humanoid Robotics Landscape (Priority: P3)

A student wants to understand the current state of humanoid robotics, including key players, robot platforms, and real-world applications.

**Why this priority**: Provides context and motivation for the course. Seeing real humanoid robots helps students understand what they're working toward.

**Independent Test**: Student can describe 3 current humanoid robot platforms and their capabilities/limitations.

**Chapter Mapping**: Chapter 3 (The Humanoid Robotics Landscape)

**Acceptance Scenarios**:

1. **Given** a student unfamiliar with humanoid robots, **When** they complete Chapter 3, **Then** they can name at least 4 humanoid robot platforms (Atlas, Figure, Optimus, Unitree)
2. **Given** descriptions of humanoid robots, **When** asked about their applications, **Then** student can identify appropriate use cases
3. **Given** the "Try With AI" prompt about humanoid robots, **When** student evaluates the response, **Then** they can identify what the AI got right/wrong based on chapter content

---

### User Story 4 - Complete Part 1 Transition Check (Priority: P4)

A student completes all Part 1 content and needs to verify readiness for Part 2 (ROS 2 Fundamentals).

**Why this priority**: Quality gate ensuring students have the conceptual foundation before technical content.

**Independent Test**: Student can sketch a robot model and annotate sensors/joints without assistance.

**Chapter Mapping**: Part 1 Summary/Assessment

**Acceptance Scenarios**:

1. **Given** a blank diagram template, **When** student sketches a humanoid robot, **Then** the sketch includes body, limbs, head, and basic proportions
2. **Given** the sketch, **When** student annotates it, **Then** they label at least 4 sensors and 6 major joints correctly
3. **Given** the annotated sketch, **When** reviewed by instructor/AI, **Then** it demonstrates understanding of sensor placement rationale

---

### Edge Cases

- What happens when a student has extensive robotics background? (Provide advanced "Try With AI" prompts for deeper exploration)
- How does system handle students with no AI/ML background? (Include prerequisite check at Part 1 start, recommend foundational resources)
- What if student skips chapters? (Each chapter builds on previous; sidebar shows completion status and prerequisites)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Content MUST include 3 chapters as defined in project-index.md: (1) What Is Physical AI?, (2) Sensors, Actuators & The Humanoid Body Plan, (3) The Humanoid Robotics Landscape
- **FR-002**: Each chapter MUST contain multiple lessons, each following the structure: Concept explanation, Analogies/diagrams, Reflection questions, "Try With AI" section
- **FR-003**: Content MUST NOT include executable code (Layer 1 is conceptual only)
- **FR-004**: Lessons MUST use student-facing language (no internal scaffolding labels like "L1" or "Layer 1")
- **FR-005**: Each lesson MUST end with a "Try With AI" section following the 5-part pattern (Initial Request, Critical Evaluation, Focused Update, Second Iteration, Reflection)
- **FR-006**: Content MUST include visual diagrams for: robot morphology, sensor placement, embodied intelligence concept, humanoid body plan
- **FR-007**: Lessons MUST be translatable to Urdu format (Urdu preserves technical terms in English)
- **FR-008**: Part 1 MUST include a transition assessment (sketch and annotate robot)
- **FR-009**: Content MUST reference hardware requirements (workstation, edge kit) but clarify that Part 1 requires no special hardware
- **FR-010**: Each lesson MUST include at least 2 analogies to help build mental models
- **FR-011**: Directory structure MUST follow project-index.md conventions: `01-Physical-AI-Foundations/{chapter-folder}/`

### Key Entities

- **Part**: A major section of the book (Part 1 = Physical AI Foundations)
- **Chapter**: A collection of lessons on a focused topic (3 chapters in Part 1)
- **Lesson**: A single learning unit with title, content, diagrams, reflection questions, and "Try With AI" section
- **Transition Check**: Assessment verifying readiness to proceed to the next Part
- **Try With AI Prompt**: Structured AI interaction pattern for active learning

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Students can complete all 3 chapters within 4 hours of study time (2 hours per week)
- **SC-002**: 90% of students correctly identify at least 3 differences between digital AI and Physical AI after completing Chapter 1
- **SC-003**: Students can name and describe the purpose of 4 sensor types (LIDAR, camera, IMU, force/torque) after completing Chapter 2
- **SC-004**: 85% of students pass the transition check (sketch and annotate robot with correct sensor/joint placement)
- **SC-005**: Each lesson includes at least 1 diagram that students rate as "helpful" in understanding the concept
- **SC-006**: Students engage with the "Try With AI" section in at least 80% of lessons (measured by completion tracking)
- **SC-007**: Urdu translations maintain technical accuracy while being readable to Urdu speakers
- **SC-008**: Content passes pedagogy review for appropriate cognitive load (no advanced concepts introduced prematurely)
- **SC-009**: All content passes safety review (no misleading claims about robot capabilities or safety)

## Chapter Outline

Based on project-index.md, Part 1 includes these chapters:

### Chapter 1: What Is Physical AI? The Rise of Embodied Intelligence

**Folder**: `01-what-is-physical-ai/`

**Lessons**:
- 01-lesson-digital-vs-physical-ai.md - Digital AI vs Physical AI
- 02-lesson-embodiment-hypothesis.md - The Embodiment Hypothesis
- 03-lesson-real-world-constraints.md - Real-world Constraints (latency, power, safety)
- 04-lab.md - Try With AI: Exploring Physical AI concepts

### Chapter 2: Sensors, Actuators & The Humanoid Body Plan

**Folder**: `02-sensors-actuators-humanoid-body/`

**Lessons**:
- 01-lesson-robot-sensors.md - How Robots Sense (LIDAR, cameras, IMU, force/torque)
- 02-lesson-actuators-motors.md - Actuators and Movement
- 03-lesson-humanoid-body-plan.md - The Humanoid Body Plan (joints, degrees of freedom)
- 04-lab.md - Try With AI: Sensor matching exercise

### Chapter 3: The Humanoid Robotics Landscape

**Folder**: `03-humanoid-robotics-landscape/`

**Lessons**:
- 01-lesson-why-humanoid.md - Why Humanoid Form?
- 02-lesson-current-platforms.md - Current Platforms (Atlas, Figure 01, Optimus, Unitree G1)
- 03-lesson-challenges-future.md - Challenges and Future Directions
- 04-lab.md - Try With AI: Researching humanoid robots

### Part 1 Summary

**File**: `04-part-summary.md` (in Part 1 root)
- Part 1 recap
- Transition Check: Sketch and annotate a humanoid robot
- Readiness assessment for Part 2 (ROS 2)

## Assumptions

- Students have Python proficiency and basic AI/ML knowledge (course prerequisites)
- Students have access to a web browser to view Docusaurus content
- No special hardware required for Part 1 (conceptual content only)
- Diagrams will be created as static images or simple interactive components
- "Try With AI" sections assume students have access to an AI assistant (ChatGPT, Claude, etc.)

## Out of Scope

- Executable code examples (deferred to Part 2: ROS 2 Fundamentals)
- Simulation setup or installation (deferred to Part 3: Simulation Systems)
- Hardware-specific instructions (conceptual overview only)
- Assessment grading system (platform feature, not content)
- Video content (text and diagrams only for initial release)

## Dependencies

- **Docusaurus site**: `apps/docs/` must be running (completed in spec 002)
- **Project Index**: `.specify/memory/project-index.md` for chapter structure (completed)
- **Curriculum file**: `.specify/memory/curriculum.md` (to be updated)
- **Constitution**: `.specify/memory/constitution.md` for pedagogy rules (completed)

## Risks

- **Content quality**: Conceptual lessons may be too abstract without hands-on elements
  - *Mitigation*: Strong analogies, diagrams, and "Try With AI" interactive sections
- **Urdu translation accuracy**: Technical concepts may lose meaning in translation
  - *Mitigation*: Technical terms stay in English; translation reviewed by native speakers
- **Scope creep**: Temptation to add code examples in a "conceptual" part
  - *Mitigation*: Strict Layer 1 enforcement per constitution
