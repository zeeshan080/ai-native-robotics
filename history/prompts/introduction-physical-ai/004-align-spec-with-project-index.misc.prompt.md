---
id: 004
title: Align Spec Plan Tasks with Project Index
stage: misc
date: 2025-11-29
surface: agent
model: claude-opus-4-5-20250514
feature: introduction-physical-ai
branch: 003-introduction-physical-ai
user: dell
command: continuation-from-previous-session
labels: ["alignment", "project-index", "spec-update", "plan-update", "tasks-update"]
links:
  spec: /specs/003-introduction-physical-ai/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-introduction-physical-ai/spec.md
  - specs/003-introduction-physical-ai/plan.md
  - specs/003-introduction-physical-ai/tasks.md
  - specs/003-introduction-physical-ai/data-model.md
  - .specify/memory/curriculum.md
  - apps/docs/docs/course-overview/index.md
tests:
  - Manual review of file paths against project-index.md
---

## Prompt

User identified that the spec/plan/tasks created for `003-introduction-physical-ai` did not align with the authoritative structure defined in `.specify/memory/project-index.md`. The original documents used a flat structure (`01-introduction-to-physical-ai/` with 4 lessons) instead of the correct nested Part/Chapter/Lesson hierarchy:

- Part 1 — Physical AI Foundations (folder: `01-Physical-AI-Foundations/`)
  - Chapter 1: `01-what-is-physical-ai/`
  - Chapter 2: `02-sensors-actuators-humanoid-body/`
  - Chapter 3: `03-humanoid-robotics-landscape/`

User requested: "Update spec/plan/tasks to align with project-index.md structure... also update the student facing curriculum"

## Response snapshot

Updated 6 files to align with project-index.md structure:

1. **spec.md** - Changed title to "Part 1 — Physical AI Foundations", added project-index.md reference, restructured to 3 chapters with lessons instead of 4 lessons

2. **plan.md** - Updated directory structure to show `01-Physical-AI-Foundations/` with nested chapter folders, updated file inventory, modified diagram paths to `static/img/part1-foundations/`

3. **tasks.md** - Complete rewrite with 75 tasks organized by:
   - Phase 1: Setup (folder creation)
   - Phase 2: Diagrams
   - Phase 3-5: User Stories 1-3 (Chapters 1-3)
   - Phase 6: Part summary/transition check
   - Phase 7: Polish

   All file paths updated to nested structure.

4. **data-model.md** - Added Part entity, restructured Chapter/Lesson entities, updated content inventory with all 18 files

5. **curriculum.md** - Updated to v2.0.0 with project-index.md reference, restructured from Module-based to Part-based organization, added folder paths for all chapters

6. **course-overview/index.md** - Updated course structure to 6 Parts, added Chapter breakdown for Part 1, changed "Ready to Begin?" to reference Part 1

## Outcome

- ✅ Impact: All spec documents now correctly reference project-index.md Part/Chapter/Lesson hierarchy
- 🧪 Tests: Manual path verification against project-index.md
- 📁 Files: 6 files modified (spec.md, plan.md, tasks.md, data-model.md, curriculum.md, course-overview/index.md)
- 🔁 Next prompts: Begin implementation with `/sp.implement` or manual task execution starting with Phase 1 (folder setup)
- 🧠 Reflection: Always verify spec documents against authoritative sources (project-index.md) before proceeding to implementation

## Evaluation notes (flywheel)

- Failure modes observed: Original spec/plan/tasks were created without referencing project-index.md, leading to structural mismatch
- Graders run and results (PASS/FAIL): Manual review PASS - all paths now match project-index.md
- Prompt variant (if applicable): N/A
- Next experiment: Add automated validation that compares spec file paths against project-index.md structure
