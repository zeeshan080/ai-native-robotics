# Implementation Plan: Part 1 — Physical AI Foundations

**Branch**: `003-introduction-physical-ai` | **Date**: 2025-11-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-introduction-physical-ai/spec.md`

## Summary

Create **Part 1 — Physical AI Foundations** for the Physical AI & Humanoid Robotics course, comprising **Chapters 1-3**. This covers **Weeks 1-2** and **Layer 1 (Conceptual Foundations)** of the 5-layer pedagogy model. Each chapter contains multiple lessons following the constitution's "Try With AI" pattern for active learning.

## Technical Context

**Language/Version**: Markdown/MDX (Docusaurus 3.x compatible)
**Primary Dependencies**: Docusaurus 3, React 18, TypeScript 5.3+
**Storage**: File-based (no database for content)
**Testing**: Manual review + pedagogy checklist
**Target Platform**: Web browser (Docusaurus static site)
**Project Type**: Content creation (educational materials)
**Performance Goals**: Pages load under 2 seconds, search indexable
**Constraints**: Layer 1 only (no code), student-facing language, "Try With AI" ending
**Scale/Scope**: 3 chapters with ~4 lessons each + Part summary, ~4 hours study time

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| Layer 1 Conceptual Only | PASS | No executable code in lessons (FR-003) |
| 5-Layer Pedagogy Model | PASS | This is Layer 1 content with clear transition check |
| Student-Facing Language | PASS | No internal labels (FR-004) |
| "Try With AI" Pattern | PASS | 5-part pattern required for all lessons (FR-005) |
| Prohibited End Sections | PASS | No "Summary", "Key Takeaways" - ends with Try With AI |
| Technical Stack | PASS | Using Docusaurus 3, MDX, TypeScript |
| Safety Governance | PASS | Conceptual content, no physical execution claims |
| Spec-First Development | PASS | spec.md → plan.md → tasks.md sequence followed |
| Project Index Alignment | PASS | Follows structure from project-index.md (FR-011) |

**Gate Result**: PASS - All constitution principles satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/003-introduction-physical-ai/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file
├── research.md          # Phase 0 output (complete)
├── data-model.md        # Phase 1 output (to update)
├── quickstart.md        # Phase 1 output (to update)
├── checklists/
│   └── requirements.md  # Quality checklist (complete)
└── tasks.md             # Phase 2 output (to update)
```

### Source Code (content files)

Per `project-index.md` conventions:

```text
apps/docs/docs/
├── course-overview/
│   └── index.md                                    # Existing (to update)
├── 01-Physical-AI-Foundations/                     # NEW PART FOLDER
│   ├── index.md                                    # Part overview
│   ├── 01-what-is-physical-ai/                     # Chapter 1
│   │   ├── index.md                                # Chapter overview
│   │   ├── 01-lesson-digital-vs-physical-ai.md
│   │   ├── 02-lesson-embodiment-hypothesis.md
│   │   ├── 03-lesson-real-world-constraints.md
│   │   └── 04-lab.md
│   ├── 02-sensors-actuators-humanoid-body/         # Chapter 2
│   │   ├── index.md
│   │   ├── 01-lesson-robot-sensors.md
│   │   ├── 02-lesson-actuators-motors.md
│   │   ├── 03-lesson-humanoid-body-plan.md
│   │   └── 04-lab.md
│   ├── 03-humanoid-robotics-landscape/             # Chapter 3
│   │   ├── index.md
│   │   ├── 01-lesson-why-humanoid.md
│   │   ├── 02-lesson-current-platforms.md
│   │   ├── 03-lesson-challenges-future.md
│   │   └── 04-lab.md
│   └── 04-part-summary.md                          # Part 1 summary & transition check
└── intro.md                                        # Existing

apps/docs/static/img/
└── part1-foundations/                              # NEW FOLDER
    ├── embodied-intelligence.svg
    ├── robot-morphology.svg
    ├── sensor-placement.svg
    └── humanoid-body-plan.svg

apps/docs/sidebars.ts                               # UPDATE for new structure
```

**Structure Decision**: Nested Part/Chapter/Lesson structure per project-index.md. Static images in `/static/img/part1-foundations/` for diagrams.

## Design Decisions

### Decision 1: Directory Structure

**Choice**: Nested folders matching project-index.md

```
01-Physical-AI-Foundations/
├── 01-what-is-physical-ai/
│   ├── 01-lesson-*.md
│   └── ...
```

**Rationale**: Follows authoritative project-index.md structure. Enables consistent navigation across all Parts.

### Decision 2: Chapter Structure

**Choice**: Each chapter has 3-4 lessons + 1 lab

**Structure**:
- index.md (chapter overview)
- 01-lesson-*.md through 03-lesson-*.md (content)
- 04-lab.md (Try With AI exercise)

**Rationale**: Separates conceptual content from interactive exercises. Lab files focus on Try With AI pattern.

### Decision 3: Lesson Structure

**Choice**: 5-section structure ending with "Try With AI"

**Sections**:
1. Introduction (hook + context)
2. Core Concepts (with H2/H3 headings)
3. Visual Aids (diagrams)
4. Reflection Questions
5. Try With AI (5-part pattern)

**Rationale**: Matches constitution requirements and FR-002.

### Decision 4: Diagram Organization

**Choice**: Images in `/static/img/part1-foundations/`

**Rationale**: Part-specific folder keeps images organized as course grows. SVG for scalability.

### Decision 5: Sidebar Integration

**Choice**: Nested category structure in sidebars.ts

```typescript
{
  type: 'category',
  label: 'Part 1: Physical AI Foundations',
  items: [
    '01-Physical-AI-Foundations/index',
    {
      type: 'category',
      label: 'Chapter 1: What Is Physical AI?',
      items: [...lessons],
    },
    // ... more chapters
  ],
}
```

**Rationale**: Reflects book structure with Parts containing Chapters.

## Content Outline

Based on project-index.md, Part 1 includes:

### Chapter 1: What Is Physical AI? The Rise of Embodied Intelligence

**Theme**: Embodied Intelligence, Real-World AI

- **Lesson 1**: Digital AI vs Physical AI
  - Hook: The robot that can't cross a doorway
  - Key comparison: chatbot vs walking robot
  - Analogies: Brain-in-jar vs brain-in-body

- **Lesson 2**: The Embodiment Hypothesis
  - Intelligence through interaction
  - The body shapes the mind
  - Learning from physical experience

- **Lesson 3**: Real-world Constraints
  - Latency: decisions in milliseconds
  - Power: battery life matters
  - Safety: humans and robots share space

- **Lab**: Try With AI - Exploring Physical AI concepts

### Chapter 2: Sensors, Actuators & The Humanoid Body Plan

**Theme**: How robots sense and move

- **Lesson 1**: How Robots Sense
  - LIDAR (sonar analogy)
  - Cameras: RGB and Depth
  - IMU (inner ear analogy)
  - Force/Torque sensors

- **Lesson 2**: Actuators and Movement
  - Electric motors
  - Hydraulic vs electric
  - Degrees of freedom

- **Lesson 3**: The Humanoid Body Plan
  - Why bipedal form?
  - Major joints and DOF
  - Balance and stability

- **Lab**: Try With AI - Sensor matching exercise

### Chapter 3: The Humanoid Robotics Landscape

**Theme**: Current state of the field

- **Lesson 1**: Why Humanoid Form?
  - Human-centered environments
  - Tool use and manipulation
  - Social interaction

- **Lesson 2**: Current Platforms
  - Boston Dynamics Atlas
  - Figure 01
  - Tesla Optimus
  - Unitree G1

- **Lesson 3**: Challenges and Future
  - Balance and locomotion
  - Energy efficiency
  - Dexterous manipulation
  - Where the field is heading

- **Lab**: Try With AI - Researching humanoid robots

### Part 1 Summary

- Recap of key concepts
- Transition Check: Sketch and annotate a humanoid robot
- Readiness self-assessment for Part 2 (ROS 2)

## Complexity Tracking

> No constitution violations requiring justification. All design choices align with Layer 1 requirements.

| Aspect | Complexity | Justification |
|--------|------------|---------------|
| Chapter count | 3 chapters | Per project-index.md |
| Lessons per chapter | 3-4 | Balanced content depth |
| Diagram count | 4 minimum | Per FR-006 requirements |
| Try With AI | Labs for each chapter | Per constitution pattern |

## Dependencies

| Dependency | Status | Impact |
|------------|--------|--------|
| Docusaurus site | Ready | Can render content |
| Project Index | Ready | Structure defined |
| Static img folder | Needs creation | For diagrams |
| Sidebar config | Needs update | For navigation |
| Constitution | Ready | Rules defined |
| Curriculum | Needs update | To match project-index |

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Content too abstract | Medium | High | Strong analogies, diagrams, Try With AI |
| Scope creep to code | Low | High | Strict Layer 1 enforcement |
| Diagram creation delay | Medium | Medium | Can proceed with placeholder images |
| Structure mismatch | Low | Medium | Verified against project-index.md |

## Next Steps

1. Update tasks.md with new file paths
2. Update curriculum.md to reference project-index structure
3. Update course-overview/index.md for students
4. Create Part 1 folder structure
5. Write content following quickstart guide
6. Create diagrams
7. Update sidebar
8. Review against constitution checklist
