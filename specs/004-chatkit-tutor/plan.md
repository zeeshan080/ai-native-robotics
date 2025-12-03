# Implementation Plan: ChatKit AI Robotics Tutor

**Branch**: `004-chatkit-tutor` | **Date**: 2025-11-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-chatkit-tutor/spec.md`

## Summary

Implement a floating chat interface (bottom-center "Ask a question..." bar) integrated into the Docusaurus documentation site. The chat connects to a FastAPI backend using OpenAI Agents SDK to provide an AI robotics tutor that helps students with questions while learning. Backend supports provider switching (OpenAI/Gemini) via factory pattern. No authentication required for hackathon demo.

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.x (React 18, Docusaurus 3)
- Backend: Python 3.11+

**Primary Dependencies**:
- Frontend: `@docusaurus/core`, React 18, custom CSS
- Backend: FastAPI, `openai-agents-sdk`, `openai-chatkit`, uvicorn

**Storage**: N/A (session-based, no persistence for hackathon MVP)

**Testing**:
- Frontend: Jest + React Testing Library
- Backend: pytest + httpx

**Target Platform**:
- Frontend: Modern browsers (Chrome, Firefox, Safari, Edge)
- Backend: Linux server (can run locally or containerized)

**Project Type**: Web application (frontend component + backend service)

**Performance Goals**:
- Chat response within 5 seconds average
- Streaming responses for perceived speed
- Chat input focus within 100ms on keyboard shortcut

**Constraints**:
- Must work alongside existing Docusaurus site
- Must not require user authentication
- Backend API keys must remain server-side only

**Scale/Scope**:
- Single documentation site
- Single AI agent (robotics tutor)
- Session-based conversations (no persistence)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Evidence |
|------|--------|----------|
| **Spec-First Development** | ✅ PASS | spec.md created before plan.md |
| **Technical Stack - Frontend** | ✅ PASS | Using Docusaurus 3 (TypeScript + React) per constitution |
| **Technical Stack - Backend** | ✅ PASS | Using FastAPI (Python 3.10+) per constitution |
| **Technical Stack - Chatbot SDK** | ✅ PASS | Using OpenAI Agents SDK / ChatKit per constitution |
| **Technical Stack - Auth** | ✅ PASS | BetterAuth deferred (not required for hackathon per spec) |
| **Hardware Awareness** | N/A | This feature is web-only, no robotics hardware |
| **Safety Governance** | N/A | Chat interface, not robot control |
| **Student-Facing Language** | ✅ PASS | AI tutor will use appropriate educational language |
| **Context Gathering** | ✅ PASS | Spec defines educational context for AI tutor |

**Gate Result**: ALL GATES PASSED - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/004-chatkit-tutor/
├── spec.md              # Feature specification ✓
├── plan.md              # This file ✓
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── chatkit-api.yaml # OpenAPI spec for backend
├── checklists/          # Validation checklists
│   └── requirements.md  # Spec quality checklist ✓
└── tasks.md             # Phase 2 output (by /sp.tasks)
```

### Source Code (repository root)

```text
# Monorepo structure (existing + new)

apps/
└── docs/                          # Existing Docusaurus site
    ├── src/
    │   ├── components/
    │   │   └── ChatKit/           # NEW: Chat UI components
    │   │       ├── FloatingChatBar.tsx
    │   │       ├── ChatPanel.tsx
    │   │       ├── ChatMessage.tsx
    │   │       ├── SelectionTooltip.tsx  # NEW: Text selection actions tooltip
    │   │       ├── useTextSelection.ts   # NEW: Hook for text selection detection
    │   │       └── index.ts
    │   ├── theme/
    │   │   └── Root.tsx           # NEW: Inject ChatKit globally
    │   └── css/
    │       └── chatkit.css        # NEW: Chat styles (includes tooltip styles)
    └── docusaurus.config.ts       # May need minor updates

packages/
└── chatkit-backend/               # NEW: Python backend package
    ├── pyproject.toml             # uv package config
    ├── src/
    │   └── chatkit_backend/
    │       ├── __init__.py
    │       ├── main.py            # FastAPI app
    │       ├── router.py          # Event handlers
    │       ├── agents/
    │       │   ├── __init__.py
    │       │   ├── tutor.py       # Robotics tutor agent
    │       │   └── factory.py     # LLM provider factory
    │       └── models/
    │           ├── __init__.py
    │           └── messages.py    # Pydantic models
    ├── tests/
    │   ├── test_router.py
    │   └── test_agents.py
    └── .env.example               # Environment template
```

**Structure Decision**: Web application pattern with frontend components in `apps/docs/src/components/` and backend as separate package in `packages/chatkit-backend/`. This follows the existing monorepo structure and keeps concerns separated.

## Complexity Tracking

> No violations to justify - design follows constitution constraints.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     BROWSER (Student)                        │
├─────────────────────────────────────────────────────────────┤
│  Docusaurus Site (apps/docs)                                │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Lesson Content                                     │    │
│  │  "The embodiment hypothesis proposes that..."       │    │
│  │            ▲                                        │    │
│  │            │ (text selected)                        │    │
│  │  ┌────────────────────────────┐                     │    │
│  │  │ [Explain] [Translate] [Summarize] │ ← Tooltip   │    │
│  │  └────────────────────────────┘                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                              │ (click action)               │
│                              ▼                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  FloatingChatBar (bottom-center)                    │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │  [Ask a question...]           [↑] [Ctrl+I] │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │                      ↓ expand                       │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │  ChatPanel (expanded view)                  │    │    │
│  │  │  - Message history                          │    │    │
│  │  │  - Streaming responses                      │    │    │
│  │  │  - Error states                             │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ POST /chatkit/api
                              │ (SSE streaming)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│             FastAPI Backend (packages/chatkit-backend)       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────────────────┐     │
│  │  /chatkit/api   │───▶│  Router (event handling)    │     │
│  │  (CORS enabled) │    │  - user_message             │     │
│  └─────────────────┘    │  - error handling           │     │
│                         └─────────────────────────────┘     │
│                                      │                       │
│                                      ▼                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Robotics Tutor Agent                               │    │
│  │  - Educational instructions                         │    │
│  │  - Curriculum-aware context                         │    │
│  │  - Streaming response via Runner.run_streamed()     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                      │                       │
│                                      ▼                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  LLM Factory                                        │    │
│  │  - LLM_PROVIDER=openai → OpenAI GPT-4              │    │
│  │  - LLM_PROVIDER=gemini → Gemini via OpenAI compat  │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

### D1: Floating Chat Bar Position
**Decision**: Bottom-center fixed position, similar to Claude Code Docs
**Rationale**: Non-intrusive, always accessible, doesn't obscure content
**Alternatives**: Corner bubble (rejected - less discoverable), sidebar (rejected - takes content space)

### D2: Backend Communication Protocol
**Decision**: Server-Sent Events (SSE) for streaming responses
**Rationale**: Enables word-by-word streaming for better UX, simpler than WebSockets
**Alternatives**: WebSockets (rejected - overkill for unidirectional streaming), polling (rejected - poor UX)

### D3: Provider Factory Pattern
**Decision**: Factory function that reads `LLM_PROVIDER` env var to select OpenAI or Gemini
**Rationale**: Easy switching between providers without code changes
**Alternatives**: Hardcoded provider (rejected - inflexible), runtime selection via API (rejected - complexity)

### D4: No Persistence for MVP
**Decision**: Session-based conversations cleared on page refresh
**Rationale**: Faster implementation for hackathon, avoids database setup
**Alternatives**: SQLite/PostgreSQL storage (deferred - post-hackathon enhancement)

### D5: Docusaurus Theme Integration
**Decision**: Inject chat via custom Root wrapper component
**Rationale**: Ensures chat appears on all pages without modifying each page
**Alternatives**: Plugin (rejected - more complex), manual import per page (rejected - maintenance burden)

### D6: Text Selection Detection
**Decision**: Custom React hook (`useTextSelection`) that listens to `selectionchange` and `mouseup` events
**Rationale**: Allows centralized selection state management with position tracking for tooltip placement
**Alternatives**: Global event listener (rejected - harder to integrate with React state), third-party library (rejected - unnecessary dependency)

### D7: Selection Action Prefixes
**Decision**: Use simple text prefixes ("Explain:", "Translate to Urdu:", "Summarize:") in user messages
**Rationale**: Simple to implement, AI tutor instructions can easily recognize and act on prefixes
**Alternatives**: Separate API endpoint per action (rejected - over-engineering), metadata field (rejected - adds complexity)

## Dependencies

### Frontend Dependencies (apps/docs)
```json
{
  "dependencies": {
    "@docusaurus/core": "^3.x",
    "react": "^18.x"
  }
}
```
No additional dependencies needed - using native fetch and React state.

### Backend Dependencies (packages/chatkit-backend)
```toml
[project.dependencies]
fastapi = ">=0.109.0"
uvicorn = ">=0.27.0"
openai = ">=1.0.0"
openai-agents = ">=0.1.0"
pydantic = ">=2.0.0"
python-dotenv = ">=1.0.0"
sse-starlette = ">=2.0.0"
```

## Environment Configuration

### Backend (.env)
```bash
# Required
LLM_PROVIDER=openai  # or "gemini"

# For OpenAI
OPENAI_API_KEY=sk-...
OPENAI_DEFAULT_MODEL=gpt-4o-mini

# For Gemini (alternative)
GEMINI_API_KEY=...
GEMINI_DEFAULT_MODEL=gemini-2.0-flash
```

### Frontend (docusaurus.config.ts)
```ts
customFields: {
  chatkitApiUrl: process.env.CHATKIT_API_URL || 'http://localhost:8000'
}
```

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| API rate limiting | Medium | High | Use streaming, cache common responses |
| CORS issues | High | Medium | Proper CORS config, test locally first |
| Streaming breaks in some browsers | Low | Medium | Fallback to non-streaming response |
| Provider API changes | Low | High | Pin versions, test regularly |
| Long response times | Medium | Medium | Loading indicators, timeout handling |
