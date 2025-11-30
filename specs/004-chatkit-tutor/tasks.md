# Tasks: ChatKit AI Robotics Tutor

**Input**: Design documents from `/specs/004-chatkit-tutor/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓

**Tests**: Not explicitly requested in spec - tests are OPTIONAL for this hackathon MVP.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `apps/docs/src/` (Docusaurus site)
- **Backend**: `packages/chatkit-backend/src/chatkit_backend/` (Python FastAPI)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for both backend and frontend components

- [x] T001 Create backend package directory structure at packages/chatkit-backend/
- [x] T002 [P] Create pyproject.toml with uv config at packages/chatkit-backend/pyproject.toml
- [x] T003 [P] Create .env.example with environment template at packages/chatkit-backend/.env.example
- [x] T004 [P] Create frontend component directory at apps/docs/src/components/ChatKit/
- [x] T005 Initialize Python package with __init__.py files in packages/chatkit-backend/src/chatkit_backend/

**Checkpoint**: Project structure created - ready for foundational implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [x] T006 [P] Create Pydantic models (MessageContent, PageContext, ChatRequest, ChatEvent) in packages/chatkit-backend/src/chatkit_backend/models/messages.py
- [x] T007 [P] Create models __init__.py with exports at packages/chatkit-backend/src/chatkit_backend/models/__init__.py
- [x] T008 [P] Implement LLM factory function (create_model) in packages/chatkit-backend/src/chatkit_backend/agents/factory.py
- [x] T009 [P] Create agents __init__.py with exports at packages/chatkit-backend/src/chatkit_backend/agents/__init__.py
- [x] T010 Implement FastAPI app with CORS and health endpoint in packages/chatkit-backend/src/chatkit_backend/main.py

### Frontend Foundation

- [x] T011 [P] Create ChatKit CSS styles in apps/docs/src/css/chatkit.css
- [x] T012 [P] Create types and interfaces in apps/docs/src/components/ChatKit/types.ts
- [x] T013 Create ChatKit index.ts with exports at apps/docs/src/components/ChatKit/index.ts

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Ask a Question While Reading (Priority: P1) 🎯 MVP

**Goal**: Enable students to type a question in the floating chat bar and receive a streaming AI response

**Independent Test**: Open any lesson page, type "What is Physical AI?" in chat bar, press Enter, verify streaming response appears within 5 seconds

### Backend Implementation for US1

- [x] T014 [US1] Implement Robotics Tutor Agent with educational instructions in packages/chatkit-backend/src/chatkit_backend/agents/tutor.py
- [x] T015 [US1] Implement event router with SSE streaming response in packages/chatkit-backend/src/chatkit_backend/router.py
- [x] T016 [US1] Wire up /chatkit/api POST endpoint with router in packages/chatkit-backend/src/chatkit_backend/main.py

### Frontend Implementation for US1

- [x] T017 [P] [US1] Create ChatMessage component for displaying messages in apps/docs/src/components/ChatKit/ChatMessage.tsx
- [x] T018 [US1] Create FloatingChatBar component with input field and send button in apps/docs/src/components/ChatKit/FloatingChatBar.tsx
- [x] T019 [US1] Implement SSE streaming handler and state management in FloatingChatBar.tsx
- [x] T020 [US1] Add keyboard shortcut (Ctrl+I / Cmd+I) to focus chat input in FloatingChatBar.tsx
- [x] T021 [US1] Create Root.tsx theme wrapper to inject ChatKit on all pages at apps/docs/src/theme/Root.tsx
- [x] T022 [US1] Update ChatKit index.ts to export FloatingChatBar at apps/docs/src/components/ChatKit/index.ts

### Integration for US1

- [x] T023 [US1] Add CHATKIT_API_URL to docusaurus.config.ts customFields at apps/docs/docusaurus.config.ts
- [x] T024 [US1] Test end-to-end: start backend, start frontend, send message, verify response

**Checkpoint**: User Story 1 complete - Students can ask questions and receive streaming AI responses

---

## Phase 4: User Story 2 - Expand Chat for Full Conversation (Priority: P2)

**Goal**: Enable students to expand the chat bar to see full conversation history

**Independent Test**: Ask 3 questions, click expand button, verify all messages visible and scrollable, click minimize, verify returns to compact bar

### Frontend Implementation for US2

- [x] T025 [P] [US2] Create ChatPanel component with scrollable message history in apps/docs/src/components/ChatKit/ChatPanel.tsx
- [x] T026 [US2] Add expand/minimize toggle state and UI controls to FloatingChatBar.tsx
- [x] T027 [US2] Implement panel positioning and overlay behavior in chatkit.css
- [x] T028 [US2] Wire ChatPanel to FloatingChatBar state for message display
- [x] T029 [US2] Add auto-scroll to latest message when new messages arrive in ChatPanel.tsx

**Checkpoint**: User Story 2 complete - Students can view full conversation history in expanded panel

---

## Phase 5: User Story 3 - Get Context-Aware Help (Priority: P3)

**Goal**: AI tutor is aware of current lesson page and provides contextual answers

**Independent Test**: On "Embodiment Hypothesis" lesson, ask "What is this lesson about?", verify AI mentions embodiment in response

### Backend Enhancement for US3

- [x] T030 [US3] Update Robotics Tutor Agent to use pageUrl/pageTitle context in tutor.py instructions
- [x] T031 [US3] Ensure router passes context to agent in router.py

### Frontend Enhancement for US3

- [x] T032 [US3] Capture current page URL and title in FloatingChatBar.tsx
- [x] T033 [US3] Include context in ChatRequest payload sent to backend
- [x] T034 [US3] Test context-awareness: ask "What am I learning about?" on different pages

**Checkpoint**: User Story 3 complete - AI provides context-aware responses based on current lesson

---

## Phase 6: User Story 4 - Text Selection Actions (Priority: P2)

**Goal**: Enable students to highlight text and choose Explain/Translate/Summarize actions that auto-send to chat

**Independent Test**: Highlight any text on a lesson page, verify tooltip appears with 3 buttons, click "Explain", verify chat opens with "Explain: [selected text]" and receives response

### Frontend Implementation for US4

- [x] T035 [P] [US4] Create useTextSelection hook for detecting text selection in apps/docs/src/components/ChatKit/useTextSelection.ts
- [x] T036 [P] [US4] Create SelectionTooltip component with Explain/Translate/Summarize buttons in apps/docs/src/components/ChatKit/SelectionTooltip.tsx
- [x] T037 [US4] Add tooltip styles (positioning, buttons, animations) to chatkit.css
- [x] T038 [US4] Integrate SelectionTooltip with useTextSelection hook in Root.tsx
- [x] T039 [US4] Wire tooltip actions to FloatingChatBar (open chat + send prefixed message)
- [x] T040 [US4] Add text truncation for selections > 500 chars with "[...truncated]" indicator
- [x] T041 [US4] Update ChatKit index.ts to export SelectionTooltip and useTextSelection

### Backend Enhancement for US4

- [x] T042 [US4] Update Robotics Tutor Agent instructions to recognize and handle action prefixes (Explain:, Translate to Urdu:, Summarize:) in tutor.py

### Integration for US4

- [x] T043 [US4] Test selection actions: highlight text, click each action, verify appropriate AI response

**Checkpoint**: User Story 4 complete - Students can highlight text and get instant explanations, translations, or summaries

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, edge cases, and improvements that affect multiple user stories

### Error Handling

- [ ] T044 [P] Add error message display and retry button in FloatingChatBar.tsx
- [ ] T045 [P] Add backend error handling with user-friendly messages in router.py
- [ ] T046 Add loading indicator during message processing in FloatingChatBar.tsx

### Edge Cases

- [ ] T047 [P] Add character counter and 2000 char limit to chat input
- [ ] T048 [P] Handle rapid message sending (queue or disable send while processing)
- [ ] T049 Add mobile responsive styles for chat bar and panel in chatkit.css

### Documentation

- [ ] T050 [P] Update quickstart.md with actual setup commands at specs/004-chatkit-tutor/quickstart.md
- [ ] T051 Run quickstart.md validation - verify all steps work

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 (Phase 3): Can start after Phase 2
  - US2 (Phase 4): Can start after Phase 2 (independent of US1)
  - US3 (Phase 5): Can start after Phase 2 (builds on US1 features)
  - US4 (Phase 6): Requires US1 complete (needs chat infrastructure to send messages)
- **Polish (Phase 7)**: Depends on desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1
- **User Story 3 (P3)**: Best done after US1 (uses the same chat flow, adds context)
- **User Story 4 (P2)**: Requires US1 complete (tooltip sends messages to FloatingChatBar)

### Within Each User Story

- Backend models/agents before router
- Router before main.py wiring
- Frontend types before components
- Components before Root.tsx integration
- Integration test after all components ready

### Parallel Opportunities

**Phase 1 (all parallel after T001)**:
- T002, T003, T004 can run in parallel

**Phase 2 (parallel groups)**:
- T006, T007, T008, T009 (backend models/agents) can run in parallel
- T011, T012 (frontend foundation) can run in parallel
- T010 depends on models being ready

**Phase 3 (US1)**:
- T017 can run in parallel with backend tasks
- T014, T015, T016 must be sequential (agent → router → main)
- T018-T022 are sequential (build on each other)

**Phase 4 (US2)**:
- T025 can start independently
- T026-T029 are sequential

**Phase 5 (US3)**:
- T030, T031 (backend) in sequence
- T032, T033 (frontend) in sequence
- Backend and frontend tracks can be parallel

**Phase 6 (US4)**:
- T035, T036 (hook and tooltip component) can run in parallel
- T037-T041 are sequential (styling → integration → wiring → exports)
- T042 (backend) can run in parallel with frontend tasks

**Phase 7 (Polish)**:
- T044, T045, T047, T048, T050 can all run in parallel

---

## Parallel Example: Phase 2 Foundation

```bash
# Launch backend foundation tasks together:
Task: "Create Pydantic models in packages/chatkit-backend/src/chatkit_backend/models/messages.py"
Task: "Create models __init__.py at packages/chatkit-backend/src/chatkit_backend/models/__init__.py"
Task: "Implement LLM factory in packages/chatkit-backend/src/chatkit_backend/agents/factory.py"
Task: "Create agents __init__.py at packages/chatkit-backend/src/chatkit_backend/agents/__init__.py"

# Launch frontend foundation tasks together:
Task: "Create ChatKit CSS styles in apps/docs/src/css/chatkit.css"
Task: "Create types and interfaces in apps/docs/src/components/ChatKit/types.ts"
```

---

## Parallel Example: User Story 1

```bash
# After foundation is complete, launch US1 tasks:

# Backend sequence (must be in order):
Task: "Implement Robotics Tutor Agent in packages/chatkit-backend/src/chatkit_backend/agents/tutor.py"
# Then:
Task: "Implement event router in packages/chatkit-backend/src/chatkit_backend/router.py"
# Then:
Task: "Wire up /chatkit/api endpoint in packages/chatkit-backend/src/chatkit_backend/main.py"

# Frontend (can start in parallel with backend after T017):
Task: "Create ChatMessage component in apps/docs/src/components/ChatKit/ChatMessage.tsx"
# Then sequential:
Task: "Create FloatingChatBar component in apps/docs/src/components/ChatKit/FloatingChatBar.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only) 🎯 RECOMMENDED FOR HACKATHON

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T013)
3. Complete Phase 3: User Story 1 (T014-T024)
4. **STOP and VALIDATE**: Test that Q&A works end-to-end
5. **Deploy/demo** - You have a working MVP!

**Estimated MVP tasks**: 24 tasks for fully functional chat

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test → Deploy (MVP!)
3. Add User Story 2 → Test → Deploy (expanded view)
4. Add User Story 3 → Test → Deploy (context-aware)
5. Add User Story 4 → Test → Deploy (text selection actions) ⭐ HIGH IMPACT
6. Add Polish tasks as time permits

### Time Estimate per Phase

| Phase | Task Count | Parallel Opportunities |
|-------|------------|----------------------|
| Setup | 5 | 3 parallel |
| Foundational | 8 | 6 parallel |
| US1 (MVP) | 11 | 2 parallel groups |
| US2 | 5 | 1 parallel |
| US3 | 5 | 2 parallel groups |
| US4 (Selection) | 9 | 3 parallel |
| Polish | 8 | 5 parallel |
| **Total** | **51** | |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- For hackathon: Focus on MVP (US1) first, then US4 (text selection) for high demo impact
- US4 is especially impressive for demos - highlight text → instant AI action
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
