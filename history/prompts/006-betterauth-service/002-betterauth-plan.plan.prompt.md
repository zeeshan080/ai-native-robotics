---
id: 002
title: BetterAuth Implementation Plan
stage: plan
date: 2025-11-30
surface: agent
model: claude-opus-4-5-20251101
feature: 006-betterauth-service
branch: 006-betterauth-service
user: dell
command: /sp.plan
labels: ["authentication", "betterauth", "architecture", "planning"]
links:
  spec: specs/006-betterauth-service/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/006-betterauth-service/plan.md
  - specs/006-betterauth-service/research.md
  - specs/006-betterauth-service/data-model.md
  - specs/006-betterauth-service/contracts/auth-api.md
  - specs/006-betterauth-service/quickstart.md
tests:
  - Constitution check passed (all gates)
---

## Prompt

Execute /sp.plan workflow for BetterAuth authentication service feature. Create implementation plan based on the spec and reference SSO project patterns.

## Response snapshot

Created comprehensive implementation plan with:

**Phase 0 - Research (research.md)**:
- RQ-001: Minimal BetterAuth config (no OIDC, JWT plugins, social OAuth)
- RQ-002: Cross-origin session sharing strategy
- RQ-003: Database schema simplification (4 tables instead of 8)
- RQ-004: FastAPI session validation via HTTP forwarding
- RQ-005: Simplified password requirements for MVP

**Phase 1 - Design Artifacts**:
- plan.md: Architecture, structure, key patterns from reference SSO
- data-model.md: Drizzle schema for user, session, account, verification tables
- contracts/auth-api.md: API endpoints for sign-up, sign-in, session, sign-out
- quickstart.md: Setup guide with prerequisites and verification steps

**Key Architecture Decisions**:
- AD-001: Separate NeonDB for auth (clean separation)
- AD-002: Simplified BetterAuth config (MVP focus)
- AD-003: Session-based auth for FastAPI (no JWT complexity)
- AD-004: Cross-origin cookie strategy (sameSite: 'lax')

**Constitution Check**: All gates passed
- Auth Library: BetterAuth (required)
- Database: NeonDB (required)
- Frontend: Docusaurus integration (compliant)
- Backend: FastAPI validation (compliant)

## Outcome

- Impact: Complete plan ready for task generation
- Tests: Constitution validation passed
- Files: 5 plan artifacts created
- Next prompts: Run /sp.tasks to generate implementation tasks
- Reflection: Reference SSO project provided clear patterns to follow, significantly reducing design uncertainty

## Evaluation notes (flywheel)

- Failure modes observed: None - reference project provided complete patterns
- Graders run and results (PASS/FAIL): PASS - all constitution gates passed
- Prompt variant (if applicable): Standard /sp.plan workflow
- Next experiment (smallest change to try): Consider creating ADR for auth architecture decisions
