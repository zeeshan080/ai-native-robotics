---
id: 001
title: "ChatKit Tutor Spec Creation"
stage: spec
date: 2025-11-29
surface: agent
model: claude-opus-4-5-20250929
feature: chatkit-tutor
branch: 004-chatkit-tutor
user: dell
command: /sp.specify
labels: ["chatkit", "spec", "ai-tutor", "hackathon"]
links:
  spec: specs/004-chatkit-tutor/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-chatkit-tutor/spec.md
  - specs/004-chatkit-tutor/checklists/requirements.md
tests: []
---

# ChatKit Tutor Spec Creation

## Prompt

User requested implementation of ChatKit - a floating chat interface with AI robotics tutor for the documentation site. Key requirements discussed:
- Floating bottom-center design (like Claude Code Docs "Ask a question..." bar)
- OpenAI Agents SDK backend with factory pattern for OpenAI/Gemini switching
- No user authentication for hackathon demo
- Custom backend mode (not Agent Builder)

User emphasized following proper workflow: "we need to make the spec first and then start to work"

## Response

Created feature branch `004-chatkit-tutor` and comprehensive specification including:

**User Stories (3 prioritized)**:
1. P1: Ask a Question While Reading - core Q&A functionality
2. P2: Expand Chat for Full Conversation - conversation history view
3. P3: Context-Aware Help - curriculum-aware responses

**Functional Requirements (15 total)**:
- Chat interface requirements (FR-001 to FR-005)
- AI response handling (FR-006 to FR-009)
- Backend service requirements (FR-010 to FR-013)
- Error handling (FR-014 to FR-015)

**Success Criteria (7 measurable outcomes)**:
- Response time < 5 seconds
- 100% page coverage
- 90% relevance rate
- Error recovery within 2 seconds

**Scope Decisions**:
- Out of scope: auth, persistence, file uploads, voice, multi-language, analytics
- Assumptions documented for session-based conversations, single agent, English only

## Outcome

- Branch created: `004-chatkit-tutor`
- Spec file: `specs/004-chatkit-tutor/spec.md`
- Checklist: `specs/004-chatkit-tutor/checklists/requirements.md`
- All validation checks passed
- Ready for `/sp.plan` phase
