# Tasks: Part 1 — Physical AI Foundations

**Input**: Design documents from `/specs/003-introduction-physical-ai/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: No automated tests requested. Content validation via manual pedagogy checklist.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions (Aligned with project-index.md)

- **Docs root**: `apps/docs/docs/`
- **Part folder**: `apps/docs/docs/01-Physical-AI-Foundations/`
- **Chapter 1**: `apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/`
- **Chapter 2**: `apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/`
- **Chapter 3**: `apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/`
- **Static images**: `apps/docs/static/img/part1-foundations/`
- **Sidebar config**: `apps/docs/sidebars.ts`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create folder structure and shared assets before content creation

- [x] T001 Create Part folder at apps/docs/docs/01-Physical-AI-Foundations/
- [x] T002 [P] Create Chapter 1 folder at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/
- [x] T003 [P] Create Chapter 2 folder at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/
- [x] T004 [P] Create Chapter 3 folder at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/
- [x] T005 [P] Create images folder at apps/docs/static/img/part1-foundations/
- [x] T006 Create Part index at apps/docs/docs/01-Physical-AI-Foundations/index.md with frontmatter (sidebar_position: 1, title: "Part 1: Physical AI Foundations")

**Checkpoint**: Folder structure ready for content creation ✅ COMPLETE

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create diagrams that multiple lessons depend on

**Note**: Diagrams can be created as placeholders initially and refined later. Content can reference them before final versions exist.

- [x] T007 [P] Create embodied-intelligence diagram (Digital AI vs Physical AI comparison) at apps/docs/static/img/part1-foundations/embodied-intelligence.svg
- [x] T008 [P] Create robot-morphology diagram (humanoid body with labeled parts) at apps/docs/static/img/part1-foundations/robot-morphology.svg
- [x] T009 [P] Create sensor-placement diagram (robot with sensors annotated) at apps/docs/static/img/part1-foundations/sensor-placement.svg
- [x] T010 [P] Create humanoid-body-plan diagram (joints and DOF) at apps/docs/static/img/part1-foundations/humanoid-body-plan.svg

**Checkpoint**: All required diagrams exist (FR-006 satisfied) ✅ COMPLETE

---

## Phase 3: User Story 1 - Learn Physical AI Fundamentals (Priority: P1)

**Goal**: Student can articulate the difference between digital AI and Physical AI, and explain why robots need to understand physical laws.

**Chapter**: Chapter 1 — What Is Physical AI? The Rise of Embodied Intelligence

**Independent Test**: Verify lesson has: introduction hook, core concepts, 2+ analogies, diagram reference, reflection questions, complete "Try With AI" section

### Chapter 1 Setup

- [x] T011 [US1] Create Chapter 1 index at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/index.md with chapter overview

### Lesson 1: Digital AI vs Physical AI

- [x] T012 [US1] Write Lesson 1 introduction (hook about robot struggling with doorway) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/01-lesson-digital-vs-physical-ai.md
- [x] T013 [US1] Write Lesson 1 core concepts (chatbot vs walking robot comparison) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/01-lesson-digital-vs-physical-ai.md
- [x] T014 [US1] Add Lesson 1 analogies (brain-in-jar vs brain-in-body, at least 2 total) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/01-lesson-digital-vs-physical-ai.md
- [x] T015 [US1] Add Lesson 1 diagram reference (embodied-intelligence.svg) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/01-lesson-digital-vs-physical-ai.md
- [x] T016 [US1] Write Lesson 1 reflection questions (2-3 questions) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/01-lesson-digital-vs-physical-ai.md
- [x] T017 [US1] Write Lesson 1 "Try With AI" section (all 5 parts) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/01-lesson-digital-vs-physical-ai.md

### Lesson 2: The Embodiment Hypothesis

- [x] T018 [US1] Write Lesson 2 introduction (hook about how babies learn) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/02-lesson-embodiment-hypothesis.md
- [x] T019 [US1] Write Lesson 2 core concepts (intelligence through interaction, body shapes mind) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/02-lesson-embodiment-hypothesis.md
- [x] T020 [US1] Add Lesson 2 analogies (learning to ride a bike, at least 2 total) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/02-lesson-embodiment-hypothesis.md
- [x] T021 [US1] Write Lesson 2 reflection questions (2-3 questions) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/02-lesson-embodiment-hypothesis.md
- [x] T022 [US1] Write Lesson 2 "Try With AI" section (all 5 parts) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/02-lesson-embodiment-hypothesis.md

### Lesson 3: Real-world Constraints

- [x] T023 [US1] Write Lesson 3 introduction (hook about split-second decisions) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/03-lesson-real-world-constraints.md
- [x] T024 [US1] Write Lesson 3 core concepts (latency, power, safety) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/03-lesson-real-world-constraints.md
- [x] T025 [US1] Add Lesson 3 analogies (at least 2) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/03-lesson-real-world-constraints.md
- [x] T026 [US1] Write Lesson 3 reflection questions (2-3 questions) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/03-lesson-real-world-constraints.md
- [x] T027 [US1] Write Lesson 3 "Try With AI" section (all 5 parts) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/03-lesson-real-world-constraints.md

### Chapter 1 Lab

- [x] T028 [US1] Write Chapter 1 Lab (Try With AI exercises) at apps/docs/docs/01-Physical-AI-Foundations/01-what-is-physical-ai/04-lab.md

**Checkpoint**: User Story 1 complete - Chapter 1 written with all required sections ✅ COMPLETE

---

## Phase 4: User Story 2 - Understand Robot Perception & Body Systems (Priority: P2)

**Goal**: Student can identify which sensor type is appropriate for different tasks and explain the humanoid body plan.

**Chapter**: Chapter 2 — Sensors, Actuators & The Humanoid Body Plan

**Independent Test**: Verify lesson covers 4 sensor types (LIDAR, camera, IMU, force/torque), includes sensor diagrams, has complete "Try With AI" section

### Chapter 2 Setup

- [x] T029 [US2] Create Chapter 2 index at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/index.md with chapter overview

### Lesson 1: How Robots Sense

- [x] T030 [US2] Write Lesson 1 introduction (hook about what robots "see") at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/01-lesson-robot-sensors.md
- [x] T031 [US2] Write LIDAR section with sonar analogy at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/01-lesson-robot-sensors.md
- [x] T032 [US2] Write Camera section (RGB and Depth, human eye analogy) at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/01-lesson-robot-sensors.md
- [x] T033 [US2] Write IMU section (inner ear analogy) at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/01-lesson-robot-sensors.md
- [x] T034 [US2] Write Force/Torque sensor section at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/01-lesson-robot-sensors.md
- [x] T035 [US2] Add diagram references (sensor-placement.svg) at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/01-lesson-robot-sensors.md
- [x] T036 [US2] Write reflection questions and "Try With AI" section at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/01-lesson-robot-sensors.md

### Lesson 2: Actuators and Movement

- [x] T037 [US2] Write Lesson 2 introduction at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/02-lesson-actuators-motors.md
- [x] T038 [US2] Write core concepts (electric motors, hydraulic vs electric, degrees of freedom) at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/02-lesson-actuators-motors.md
- [x] T039 [US2] Add analogies and diagram references at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/02-lesson-actuators-motors.md
- [x] T040 [US2] Write reflection questions and "Try With AI" section at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/02-lesson-actuators-motors.md

### Lesson 3: The Humanoid Body Plan

- [x] T041 [US2] Write Lesson 3 introduction at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/03-lesson-humanoid-body-plan.md
- [x] T042 [US2] Write core concepts (bipedal form, major joints, DOF, balance) at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/03-lesson-humanoid-body-plan.md
- [x] T043 [US2] Add diagram reference (humanoid-body-plan.svg, robot-morphology.svg) at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/03-lesson-humanoid-body-plan.md
- [x] T044 [US2] Write reflection questions and "Try With AI" section at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/03-lesson-humanoid-body-plan.md

### Chapter 2 Lab

- [x] T045 [US2] Write Chapter 2 Lab (sensor matching exercise) at apps/docs/docs/01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/04-lab.md

**Checkpoint**: User Story 2 complete - Chapter 2 covers sensors, actuators, and body plan ✅ COMPLETE

---

## Phase 5: User Story 3 - Survey Humanoid Robotics Landscape (Priority: P3)

**Goal**: Student can describe 3 current humanoid robot platforms and their capabilities/limitations.

**Chapter**: Chapter 3 — The Humanoid Robotics Landscape

**Independent Test**: Verify lesson names at least 4 platforms (Atlas, Figure 01, Optimus, Unitree G1), discusses challenges, has complete "Try With AI" section

### Chapter 3 Setup

- [x] T046 [US3] Create Chapter 3 index at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/index.md with chapter overview

### Lesson 1: Why Humanoid Form?

- [x] T047 [US3] Write Lesson 1 introduction (hook about why humanoid shape) at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/01-lesson-why-humanoid.md
- [x] T048 [US3] Write core concepts (human-centered environments, tool use, social interaction) at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/01-lesson-why-humanoid.md
- [x] T049 [US3] Add analogies and reflection questions at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/01-lesson-why-humanoid.md
- [x] T050 [US3] Write "Try With AI" section at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/01-lesson-why-humanoid.md

### Lesson 2: Current Platforms

- [x] T051 [US3] Write Lesson 2 introduction at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/02-lesson-current-platforms.md
- [x] T052 [US3] Write Boston Dynamics Atlas section at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/02-lesson-current-platforms.md
- [x] T053 [US3] Write Figure 01 section at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/02-lesson-current-platforms.md
- [x] T054 [US3] Write Tesla Optimus section at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/02-lesson-current-platforms.md
- [x] T055 [US3] Write Unitree G1 section at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/02-lesson-current-platforms.md
- [x] T056 [US3] Add hardware note (no special hardware needed for Part 1) at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/02-lesson-current-platforms.md
- [x] T057 [US3] Write reflection questions and "Try With AI" section at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/02-lesson-current-platforms.md

### Lesson 3: Challenges and Future

- [x] T058 [US3] Write Lesson 3 introduction at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/03-lesson-challenges-future.md
- [x] T059 [US3] Write challenges section (balance, locomotion, energy efficiency, dexterous manipulation) at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/03-lesson-challenges-future.md
- [x] T060 [US3] Write future directions section at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/03-lesson-challenges-future.md
- [x] T061 [US3] Write reflection questions and "Try With AI" section at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/03-lesson-challenges-future.md

### Chapter 3 Lab

- [x] T062 [US3] Write Chapter 3 Lab (researching humanoid robots) at apps/docs/docs/01-Physical-AI-Foundations/03-humanoid-robotics-landscape/04-lab.md

**Checkpoint**: User Story 3 complete - Chapter 3 covers humanoid landscape ✅ COMPLETE

---

## Phase 6: User Story 4 - Complete Part 1 Transition Check (Priority: P4)

**Goal**: Student can sketch a robot model and annotate sensors/joints without assistance.

**Independent Test**: Verify transition check has exercise instructions, self-evaluation checklist, "Try With AI" section for AI-assisted review

### Part 1 Summary & Assessment

- [x] T063 [US4] Write Part 1 summary introduction (recap key concepts) at apps/docs/docs/01-Physical-AI-Foundations/04-part-summary.md
- [x] T064 [US4] Write transition check instructions (sketch and annotate robot) at apps/docs/docs/01-Physical-AI-Foundations/04-part-summary.md
- [x] T065 [US4] Write annotation requirements (4+ sensors, 6+ joints) at apps/docs/docs/01-Physical-AI-Foundations/04-part-summary.md
- [x] T066 [US4] Create self-evaluation checklist for students at apps/docs/docs/01-Physical-AI-Foundations/04-part-summary.md
- [x] T067 [US4] Write readiness assessment for Part 2 (ROS 2) at apps/docs/docs/01-Physical-AI-Foundations/04-part-summary.md
- [x] T068 [US4] Write "Try With AI" section (use AI to evaluate sketch) at apps/docs/docs/01-Physical-AI-Foundations/04-part-summary.md

**Checkpoint**: User Story 4 complete - Transition check ready for students ✅ COMPLETE

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final integration, sidebar update, and validation

- [x] T069 Update sidebar configuration to include new Part structure at apps/docs/sidebars.ts
- [x] T070 [P] Update course-overview link to point to Part 1 at apps/docs/docs/course-overview/index.md
- [x] T071 Verify all lessons follow constitution rules (no code, no internal labels, Try With AI ending)
- [x] T072 [P] Verify all diagrams are referenced correctly in lessons
- [ ] T073 Run Docusaurus dev server and verify all pages render correctly
- [x] T074 Verify sidebar navigation shows correct nested Part/Chapter/Lesson order
- [x] T075 Verify success criteria SC-001 through SC-009 are achievable with content

**Checkpoint**: Part 1 complete and integrated into documentation site ✅ COMPLETE (pending T073 manual verification)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on T005 (images folder exists)
- **User Story 1 (Phase 3)**: Depends on T001, T002 (Part and Chapter 1 folders exist), T007 (diagram exists)
- **User Story 2 (Phase 4)**: Depends on T003 (Chapter 2 folder), T008, T009 (sensor diagrams exist)
- **User Story 3 (Phase 5)**: Depends on T004 (Chapter 3 folder); can run in parallel with US2 after US1 complete
- **User Story 4 (Phase 6)**: Depends on all chapters (references content from them)
- **Polish (Phase 7)**: Depends on all user stories complete

### User Story Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Diagrams)
    ↓
Phase 3 (US1: Chapter 1) ← MVP checkpoint
    ↓
Phase 4 (US2: Chapter 2) ─┬─ can parallel
Phase 5 (US3: Chapter 3) ─┘
    ↓
Phase 6 (US4: Part Summary)
    ↓
Phase 7 (Polish)
```

### Parallel Opportunities

**Phase 1 (Setup)**:
```bash
# These can run in parallel (different folders):
Task T002-T005: Create chapter and images folders
```

**Phase 2 (Diagrams)**:
```bash
# All diagram tasks can run in parallel:
Task T007: embodied-intelligence.svg
Task T008: robot-morphology.svg
Task T009: sensor-placement.svg
Task T010: humanoid-body-plan.svg
```

**Phase 7 (Polish)**:
```bash
# These can run in parallel:
Task T070: Update course-overview
Task T072: Verify diagram references
```

---

## Implementation Strategy

### MVP First (User Story 1 - Chapter 1)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Diagrams (T007-T010) - can use placeholders
3. Complete Phase 3: User Story 1 (T011-T028) → **MVP Checkpoint**
4. **STOP and VALIDATE**: Can a student learn Physical AI fundamentals?
5. Deploy/demo if ready

### Incremental Delivery

1. Complete MVP (US1 - Chapter 1)
2. Complete Phase 4: User Story 2 (T029-T045) - adds sensor/body knowledge
3. Complete Phase 5: User Story 3 (T046-T062) - adds landscape context
4. Complete Phase 6: User Story 4 (T063-T068) - adds assessment
5. Complete Phase 7: Polish (T069-T075)

### Single Developer Execution

Execute tasks in order: T001 → T002 → ... → T075
- Respect dependencies between phases
- Parallel tasks ([P]) can be batched if comfortable
- Commit after each phase completion

---

## Summary

| Phase | Tasks | User Story | Files |
|-------|-------|------------|-------|
| Phase 1: Setup | T001-T006 | - | 5 folders + 1 index |
| Phase 2: Diagrams | T007-T010 | - | 4 SVG diagrams |
| Phase 3: US1 | T011-T028 | Physical AI Fundamentals (P1) | Chapter 1 (4 lessons + index) |
| Phase 4: US2 | T029-T045 | Robot Perception (P2) | Chapter 2 (4 lessons + index) |
| Phase 5: US3 | T046-T062 | Humanoid Landscape (P3) | Chapter 3 (4 lessons + index) |
| Phase 6: US4 | T063-T068 | Transition Check (P4) | Part summary |
| Phase 7: Polish | T069-T075 | - | Sidebar + validation |

**Total Tasks**: 75
**Tasks per User Story**: US1=18, US2=17, US3=17, US4=6
**Parallel Opportunities**: 12 tasks marked [P]
**MVP Scope**: Chapter 1 (through T028) = 28 tasks

---

## Notes

- [P] tasks = different files, no dependencies - can run simultaneously
- [Story] label maps task to specific user story for traceability
- Each lesson must end with "## Try With AI" section (FR-005)
- No executable code allowed in any lesson (FR-003)
- Verify each checkpoint before proceeding to next phase
- Commit after each phase completion
- Success criteria (SC-001 through SC-009) should be verified in Phase 7
- Structure follows project-index.md Part/Chapter/Lesson hierarchy
