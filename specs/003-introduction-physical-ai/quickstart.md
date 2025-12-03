# Quickstart: Introduction to Physical AI Content

**Feature**: 003-introduction-physical-ai
**Date**: 2025-11-29
**Purpose**: Guide for content authors creating Introduction module lessons

## Prerequisites

- Docusaurus dev server running (`pnpm dev` from repo root)
- Understanding of the 5-layer pedagogy model (see constitution)
- Familiarity with Physical AI concepts

## Content Location

All content goes in:
```
apps/docs/docs/01-introduction-to-physical-ai/
```

## Quick Steps

### 1. Create Module Folder

```bash
mkdir -p apps/docs/docs/01-introduction-to-physical-ai
```

### 2. Create Module Index

Create `apps/docs/docs/01-introduction-to-physical-ai/index.md`:

```markdown
---
sidebar_position: 1
title: Introduction to Physical AI
description: Weeks 1-2 - Building mental models of Physical AI and embodied intelligence
---

# Introduction to Physical AI

Welcome to the first module of Physical AI & Humanoid Robotics...
```

### 3. Create a Lesson

Create `apps/docs/docs/01-introduction-to-physical-ai/01-what-is-physical-ai.md`:

```markdown
---
sidebar_position: 1
title: What is Physical AI?
description: Understanding the difference between digital AI and robots that interact with the physical world
keywords: [physical ai, embodied intelligence, robotics]
---

# What is Physical AI?

[Introduction - 2-3 paragraphs with hook]

## Digital AI vs Physical AI

[Core concept with analogy]

## Why Robots Need Physics

[Core concept with analogy]

## Reflection Questions

1. [Question 1]
2. [Question 2]

## Try With AI

### Initial Request
> [Prompt for AI assistant]

### Critical Evaluation
- [ ] Check 1
- [ ] Check 2

### Focused Update
> [Follow-up prompt]

### Second Iteration
> [Iteration prompt]

### Reflection
- [Reflection question 1]
- [Reflection question 2]
```

### 4. Add Diagrams

Create diagrams in:
```
apps/docs/static/img/introduction/
```

Reference in lessons:
```markdown
![Robot morphology diagram](/img/introduction/robot-morphology.svg)
```

### 5. Update Sidebar

Edit `apps/docs/sidebars.ts` to include the new module.

### 6. Preview

```bash
pnpm dev
```

Open http://localhost:3000 and navigate to your new content.

---

## Lesson Checklist

Before marking a lesson complete:

- [ ] Frontmatter complete (title, description, keywords)
- [ ] Introduction hooks the reader
- [ ] At least 2 analogies included (FR-010)
- [ ] At least 1 diagram included (SC-005)
- [ ] NO executable code (FR-003)
- [ ] NO internal labels like "Layer 1" (FR-004)
- [ ] Reflection Questions section present
- [ ] Try With AI section is FINAL section
- [ ] All 5 parts of Try With AI included (FR-005)
- [ ] NO "Summary" or "Key Takeaways" section (Constitution VI)

---

## Content Rules (Quick Reference)

### DO

- Use student-facing language
- Include analogies and diagrams
- End every lesson with "## Try With AI"
- Make reflection questions thought-provoking
- Keep content conceptual (this is Layer 1)

### DON'T

- Include executable code
- Use internal labels ("Layer 1", "VLA pipeline")
- End with "Summary", "What's Next", "Congratulations"
- Mix concepts from later modules (ROS 2, Gazebo, etc.)
- Make claims about robot safety without proper context

---

## File Naming Convention

```
{order}-{slug}.md

Examples:
01-what-is-physical-ai.md
02-embodied-intelligence.md
03-robot-sensors.md
04-humanoid-landscape.md
05-transition-check.md
```

---

## Try With AI Template

Copy this template for the Try With AI section:

```markdown
## Try With AI

### Initial Request

> Copy this prompt to your AI assistant:
>
> "I'm learning about [TOPIC]. Can you explain [SPECIFIC QUESTION]? I want to understand [LEARNING GOAL]."

### Critical Evaluation

Before accepting the response, check:
- [ ] Does the explanation match what we learned about [CONCEPT]?
- [ ] Are there any claims that seem incorrect or oversimplified?
- [ ] What important details might be missing?

### Focused Update

Pick ONE thing to improve. Try this follow-up:

> "Your explanation of [ASPECT] was [good/unclear]. Can you [SPECIFIC REQUEST]?"

### Second Iteration

Tell the AI what happened:

> "I tried [ACTION] and [RESULT]. Based on what I learned in this lesson about [CONCEPT], I think [OBSERVATION]. Can you help me understand [QUESTION]?"

### Reflection

After your AI conversation:
- Which part of the AI's response was most helpful for understanding [TOPIC]?
- What did you learn by questioning the AI's explanation?
- How does this connect to [LESSON CONCEPT]?
```

---

## Need Help?

- **Constitution**: `.specify/memory/constitution.md`
- **Curriculum**: `.specify/memory/curriculum.md`
- **Spec**: `specs/003-introduction-physical-ai/spec.md`
- **Data Model**: `specs/003-introduction-physical-ai/data-model.md`
