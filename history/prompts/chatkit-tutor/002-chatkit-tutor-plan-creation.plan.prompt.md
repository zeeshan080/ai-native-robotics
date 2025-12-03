---
id: 002
title: "ChatKit Tutor Plan Creation"
stage: plan
date: 2025-11-29
surface: agent
model: claude-opus-4-5-20250929
feature: chatkit-tutor
branch: 004-chatkit-tutor
user: dell
command: /sp.plan
labels: ["chatkit", "plan", "architecture", "hackathon"]
links:
  spec: specs/004-chatkit-tutor/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-chatkit-tutor/plan.md
  - specs/004-chatkit-tutor/research.md
  - specs/004-chatkit-tutor/data-model.md
  - specs/004-chatkit-tutor/contracts/chatkit-api.yaml
  - specs/004-chatkit-tutor/quickstart.md
tests: []
---

# ChatKit Tutor Plan Creation

## Prompt

User ran `/sp.plan` with argument "make it for me" to create the implementation plan for the ChatKit AI Robotics Tutor feature.

## Response

Created comprehensive implementation plan with all Phase 0 and Phase 1 artifacts:

**plan.md** - Main implementation plan with:
- Technical context (TypeScript/React frontend, Python/FastAPI backend)
- Constitution check (all gates passed)
- Project structure (monorepo with apps/docs and packages/chatkit-backend)
- Architecture diagram (floating chat → FastAPI → Agents SDK → LLM)
- 5 key design decisions documented (chat position, SSE streaming, factory pattern, no persistence, theme integration)
- Dependencies and environment configuration
- Risk assessment

**research.md** - Phase 0 research with 6 resolved topics:
- R1: OpenAI Agents SDK integration (run_streamed + stream_agent_response)
- R2: LLM provider factory pattern (env-based switching)
- R3: Docusaurus injection (Root component swizzling)
- R4: SSE streaming implementation (sse-starlette)
- R5: Robotics tutor instructions (educational focus)
- R6: Error handling strategy (layered, user-friendly)

**data-model.md** - Phase 1 data model with:
- Message entity (id, role, content, timestamp, status)
- Conversation entity (messages, timestamps)
- ChatEvent (streaming events: text_delta, message_complete, error)
- ChatRequest (frontend → backend payload)
- Frontend React state model
- Backend Pydantic models

**contracts/chatkit-api.yaml** - OpenAPI 3.1 spec with:
- POST /chatkit/api (SSE streaming endpoint)
- GET /health (health check)
- All request/response schemas
- Example payloads

**quickstart.md** - Developer setup guide with:
- Prerequisites
- Backend setup (uv, dependencies, .env)
- Frontend setup (pnpm, env.local)
- Integration testing steps
- Troubleshooting guide
- Environment variables reference

## Outcome

All planning artifacts created:
- `specs/004-chatkit-tutor/plan.md`
- `specs/004-chatkit-tutor/research.md`
- `specs/004-chatkit-tutor/data-model.md`
- `specs/004-chatkit-tutor/contracts/chatkit-api.yaml`
- `specs/004-chatkit-tutor/quickstart.md`

Agent context updated in CLAUDE.md.

Ready for `/sp.tasks` to generate implementation tasks.
