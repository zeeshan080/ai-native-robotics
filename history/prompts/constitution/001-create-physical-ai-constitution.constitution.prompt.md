---
id: 001
title: Create Physical AI Robotics Constitution
stage: constitution
date: 2025-11-29
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: master
user: dell
command: /sp.constitution
labels: ["constitution", "physical-ai", "robotics", "pedagogy", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/001-create-physical-ai-constitution.constitution.prompt.md
tests:
  - N/A (governance document)
---

## Prompt

you need to create constitution for this project for that u need to read the content in the folder /home/dell/ai-native-robotics/physical_ai_constitution_full create it as detailed as possible

## Response snapshot

Created comprehensive constitution v1.0.0 for the AI-Native Physical AI & Humanoid Robotics Textbook project. The constitution consolidates 11 source documents into 10 core principles covering:

1. Educational Robotics Architect Persona
2. 5-Layer Physical AI Pedagogy Model (Conceptual → Simulation → Control → VLA → Capstone)
3. Strict Technical Stack (Docusaurus 3, FastAPI, Qdrant, Neon, BetterAuth, ROS 2)
4. Hardware Awareness Constraints (RTX workstations, Jetson edge, physical robots)
5. Robotics Safety Governance (simulation-first, torque limits, latency warnings)
6. Student-Facing Language Protocol ("Try With AI" 5-part pattern, no meta-commentary)
7. Content Agents Specification (8 agents for book creation)
8. Software-Building Agents Specification (8 agents for platform development)
9. Quality & Verification Framework (code, math, API, RAG grounding)
10. Spec-First Development (spec.md → plan.md → tasks.md → code)

Includes Project Vision, Target Audience, Success Criteria, Non-Goals, and full Governance section with amendment workflow and versioning policy.

## Outcome

- Impact: Created foundational governance document for entire project
- Tests: N/A (governance document)
- Files: .specify/memory/constitution.md (377 lines)
- Next prompts: Create monorepo structure, define first chapter spec, setup Docusaurus book
- Reflection: Consolidated 11 detailed source documents into cohesive constitution with clear non-negotiable rules and decision frameworks

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS (manual validation of all placeholders filled)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test constitution compliance in next spec/plan cycle
