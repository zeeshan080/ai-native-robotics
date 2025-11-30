# Data Model: Part 1 — Physical AI Foundations

**Feature**: 003-introduction-physical-ai
**Date**: 2025-11-29
**Purpose**: Define entities and structures for educational content
**Reference**: `.specify/memory/project-index.md` (authoritative structure)

## Overview

This feature creates **educational content files**, not database entities. The "data model" describes the structure of markdown files and their relationships following the Part → Chapter → Lesson hierarchy defined in project-index.md.

---

## Entity: Part

A collection of related chapters under a common theme.

### Structure

```yaml
# Part Index Frontmatter (apps/docs/docs/01-Physical-AI-Foundations/index.md)
---
sidebar_position: 1
title: "Part 1: Physical AI Foundations"
description: "Embodied Intelligence, Real-World AI, Humanoid Robotics Overview"
---
```

### Contents

| Component | Count | Purpose |
|-----------|-------|---------|
| index.md | 1 | Part overview and navigation |
| Chapters | 3 | Thematic groupings of lessons |
| Part Summary | 1 | Transition check for next part |

### File Structure (per project-index.md)

```
apps/docs/docs/01-Physical-AI-Foundations/
├── index.md                           # Part overview
├── 01-what-is-physical-ai/            # Chapter 1
├── 02-sensors-actuators-humanoid-body/ # Chapter 2
├── 03-humanoid-robotics-landscape/     # Chapter 3
└── 04-part-summary.md                  # Transition check
```

---

## Entity: Chapter

A collection of lessons within a part, focused on a specific topic.

### Structure

```yaml
# Chapter Index Frontmatter (e.g., 01-what-is-physical-ai/index.md)
---
sidebar_position: 1
title: "Chapter 1: What Is Physical AI?"
description: "The Rise of Embodied Intelligence"
---
```

### Contents

| Component | Count | Purpose |
|-----------|-------|---------|
| index.md | 1 | Chapter overview |
| Lessons | 3 | Individual learning units |
| Lab | 1 | Hands-on exercises |

### File Naming Convention (per project-index.md)

```
{chapter-folder}/
├── index.md                              # Chapter overview
├── 01-lesson-{lesson-slug}.md            # Lesson 1
├── 02-lesson-{lesson-slug}.md            # Lesson 2
├── 03-lesson-{lesson-slug}.md            # Lesson 3
└── 04-lab.md                             # Lab exercises
```

---

## Entity: Lesson

A single learning unit within a chapter.

### Structure

```yaml
# Lesson Frontmatter
---
sidebar_position: {number}      # Order in chapter (1-4)
title: {string}                 # Display title
description: {string}           # SEO description
keywords: [{string}]            # Search keywords
---
```

### Content Sections

| Section | Required | Purpose |
|---------|----------|---------|
| H1 Title | Yes | Page title (matches frontmatter title) |
| Introduction | Yes | Hook and context (2-3 paragraphs) |
| Core Concepts | Yes | Main content with H2/H3 headings |
| Analogies | Yes | At least 2 per lesson (FR-010) |
| Diagrams | Yes | At least 1 per lesson (FR-006, SC-005) |
| Reflection Questions | Yes | 2-3 questions for self-assessment |
| Try With AI | Yes | Final section, 5-part pattern (FR-005) |

### Validation Rules

- Must NOT contain executable code blocks (FR-003)
- Must NOT use internal labels like "Layer 1" (FR-004)
- Must NOT end with "Summary", "Key Takeaways", etc. (Constitution VI)
- Final section MUST be "## Try With AI"

---

## Entity: Lab

Hands-on exercises at the end of each chapter.

### Structure

```yaml
---
sidebar_position: 4
title: "Lab: {Chapter Topic}"
description: "Hands-on exercises for {chapter topic}"
---
```

### Content Sections

| Section | Purpose |
|---------|---------|
| Overview | Explain what the lab covers |
| Exercises | 2-3 guided exercises |
| Try With AI | AI-assisted extension activities |

---

## Entity: Part Summary / Transition Check

Assessment verifying readiness for next part.

### Structure

```yaml
---
sidebar_position: 5
title: "Part 1 Check: Ready for ROS 2?"
description: "Verify your understanding before continuing to Part 2"
---
```

### Content Sections

| Section | Purpose |
|---------|---------|
| Key Concepts Review | Recap main ideas from all chapters |
| Exercise | The sketch-and-annotate task |
| Self-Evaluation | Checklist for students |
| What's Next | Preview of Part 2 (ROS 2) |
| Try With AI | Use AI to evaluate their work |

---

## Entity: Try With AI Section

Structured AI interaction pattern (5 parts).

### Structure

```markdown
## Try With AI

### Initial Request
> [Blockquote with copyable prompt]

### Critical Evaluation
[Checklist of things to verify]

### Focused Update
> [Follow-up prompt]

### Second Iteration
> [Iteration prompt template]

### Reflection
[Questions connecting AI interaction to lesson]
```

### Validation Rules

- Must appear as final H2 section
- Must include all 5 parts
- Prompts must be in blockquotes for easy copying
- Critical Evaluation should include checkboxes

---

## Entity: Diagram

Visual aid supporting conceptual understanding.

### Required Diagrams (FR-006)

| Diagram | Chapter | Description |
|---------|---------|-------------|
| embodied-intelligence.svg | Chapter 1 | Digital AI vs Physical AI comparison |
| robot-morphology.svg | Chapter 2 | Humanoid body with labeled parts |
| sensor-placement.svg | Chapter 2 | Robot with sensors annotated |
| humanoid-body-plan.svg | Chapter 2 | Joints and degrees of freedom |

### File Structure

```
apps/docs/static/img/part1-foundations/
├── embodied-intelligence.svg
├── robot-morphology.svg
├── sensor-placement.svg
├── humanoid-body-plan.svg
└── [additional diagrams as needed]
```

### Diagram Requirements

- Format: SVG preferred, PNG acceptable
- Alt text: Descriptive for accessibility
- Size: Responsive, max-width 800px
- Style: Clean, educational, consistent

---

## Relationships

```
Part 1: Physical AI Foundations (1)
├── index.md (1)
├── Chapter 1: What Is Physical AI? (1)
│   ├── index.md (1)
│   ├── Lessons (3)
│   │   └── Try With AI Section (1 per lesson)
│   └── Lab (1)
│       └── Try With AI Section (1)
├── Chapter 2: Sensors, Actuators & Body Plan (1)
│   ├── index.md (1)
│   ├── Lessons (3)
│   │   └── Try With AI Section (1 per lesson)
│   └── Lab (1)
├── Chapter 3: Humanoid Robotics Landscape (1)
│   ├── index.md (1)
│   ├── Lessons (3)
│   │   └── Try With AI Section (1 per lesson)
│   └── Lab (1)
├── Part Summary (1)
│   └── Try With AI Section (1)
└── Diagrams (4+)
```

---

## Content Inventory

### Part 1: Physical AI Foundations

| File | Type | Status |
|------|------|--------|
| `01-Physical-AI-Foundations/index.md` | Part Index | To Create |

### Chapter 1: What Is Physical AI?

| File | Type | Status |
|------|------|--------|
| `01-Physical-AI-Foundations/01-what-is-physical-ai/index.md` | Chapter Index | To Create |
| `01-Physical-AI-Foundations/01-what-is-physical-ai/01-lesson-digital-vs-physical-ai.md` | Lesson | To Create |
| `01-Physical-AI-Foundations/01-what-is-physical-ai/02-lesson-embodiment-hypothesis.md` | Lesson | To Create |
| `01-Physical-AI-Foundations/01-what-is-physical-ai/03-lesson-real-world-constraints.md` | Lesson | To Create |
| `01-Physical-AI-Foundations/01-what-is-physical-ai/04-lab.md` | Lab | To Create |

### Chapter 2: Sensors, Actuators & Humanoid Body Plan

| File | Type | Status |
|------|------|--------|
| `01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/index.md` | Chapter Index | To Create |
| `01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/01-lesson-robot-sensors.md` | Lesson | To Create |
| `01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/02-lesson-actuators-motors.md` | Lesson | To Create |
| `01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/03-lesson-humanoid-body-plan.md` | Lesson | To Create |
| `01-Physical-AI-Foundations/02-sensors-actuators-humanoid-body/04-lab.md` | Lab | To Create |

### Chapter 3: Humanoid Robotics Landscape

| File | Type | Status |
|------|------|--------|
| `01-Physical-AI-Foundations/03-humanoid-robotics-landscape/index.md` | Chapter Index | To Create |
| `01-Physical-AI-Foundations/03-humanoid-robotics-landscape/01-lesson-why-humanoid.md` | Lesson | To Create |
| `01-Physical-AI-Foundations/03-humanoid-robotics-landscape/02-lesson-current-platforms.md` | Lesson | To Create |
| `01-Physical-AI-Foundations/03-humanoid-robotics-landscape/03-lesson-challenges-future.md` | Lesson | To Create |
| `01-Physical-AI-Foundations/03-humanoid-robotics-landscape/04-lab.md` | Lab | To Create |

### Part Summary

| File | Type | Status |
|------|------|--------|
| `01-Physical-AI-Foundations/04-part-summary.md` | Transition Check | To Create |

### Diagrams

| File | Status |
|------|--------|
| `static/img/part1-foundations/embodied-intelligence.svg` | To Create |
| `static/img/part1-foundations/robot-morphology.svg` | To Create |
| `static/img/part1-foundations/sensor-placement.svg` | To Create |
| `static/img/part1-foundations/humanoid-body-plan.svg` | To Create |

---

## State Transitions

### Content States (for tracking)

```
Draft → Review → Published
```

### Part States

```
Planning → Content Creation → Review → Published
```

---

## Notes

- All paths relative to `apps/docs/docs/` unless noted
- Structure follows project-index.md Part/Chapter/Lesson hierarchy
- No database entities - all content is file-based
- Docusaurus handles rendering, search, and navigation
- Sidebar auto-generated from folder structure
- Frontmatter provides metadata for SEO and organization
