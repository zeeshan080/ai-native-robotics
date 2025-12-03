---
id: 001
title: Create Subagents Skills Specification
stage: spec
date: 2025-11-29
surface: agent
model: claude-opus-4-5-20251101
feature: 001-agents-skills
branch: 001-agents-skills
user: dell
command: /sp.specify
labels: ["subagents", "skills", "specification", "claude-code", "orchestration"]
links:
  spec: specs/001-agents-skills/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-agents-skills/spec.md
  - specs/001-agents-skills/checklists/requirements.md
  - history/prompts/001-agents-skills/001-create-agents-skills-spec.spec.prompt.md
tests:
  - N/A (specification document)
---

## Prompt

we first need to create the agents, and their skills for the project

## Response snapshot

Created specification for **Claude Code Subagents and Skills System** (`001-agents-skills`).

**Architecture** (corrected after user feedback):
- Claude Code CLI = Main orchestrator (human interacts with this)
- Subagents = Specialized AI agents spawned by Claude Code for domain tasks
- Skills = Reusable tools/capabilities that subagents use

**User Stories (5 total)**:
1. P1: Write book chapter with subagent delegation (Chapter-Planner → Lesson-Writer → Safety Reviewer)
2. P1: Generate robotics code with specialist subagent (URDF, ROS 2 nodes)
3. P2: Build platform components with software subagents (Docusaurus, FastAPI, etc.)
4. P3: Translate lesson with Urdu Translator subagent
5. P2: Review and validate content quality (Pedagogy, RAG Answerability)

**Key Entities**:
- Subagent (16 total: 8 content + 8 software)
- Skill (18 initial skills across 5 categories)
- Subagent Context (what Claude Code passes when spawning)
- Skill Invocation (execution record)

**Skills Catalog** (initial 18 skills):
- Shared: read-constitution, validate-compliance, read-chapter-index, determine-layer, check-prerequisites
- Content: generate-lesson-structure, generate-try-with-ai, assess-cognitive-load, validate-student-language
- Robotics: generate-urdf, generate-ros2-node, validate-joint-limits, check-hardware-constraints, annotate-simulation-only
- Translation: preserve-technical-terms, translate-to-urdu
- Platform: validate-tech-stack, generate-fastapi-endpoint, generate-docusaurus-config

**Functional Requirements**: 27 requirements covering orchestration (4), content subagents (8), software subagents (8), skills system (4), constitution compliance (3).

## Outcome

- Impact: Created foundational specification for Claude Code's subagent delegation system
- Tests: N/A (specification document)
- Files: spec.md (219 lines), requirements.md checklist
- Next prompts: Run `/sp.clarify` or `/sp.plan` to proceed with implementation planning
- Reflection: Initial spec had wrong perspective (user-facing agents vs Claude Code subagents). Corrected after user feedback.

## Evaluation notes (flywheel)

- Failure modes observed: Initial spec written from wrong perspective (user invoking agents directly instead of Claude Code spawning subagents)
- Graders run and results (PASS/FAIL): PASS after revision (all checklist items validated)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate subagent spawning flow during plan phase
