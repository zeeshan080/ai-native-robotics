# Tasks: Claude Code Subagents and Skills System

**Input**: Design documents from `/specs/001-agents-skills/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md

**Tests**: Not requested - this feature involves markdown configuration files only, no code tests needed.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Subagents**: `.claude/agents/*.md`
- **Skills**: `.claude/skills/skill-name/SKILL.md`
- **Constitution**: `.specify/memory/constitution.md`

---

## Phase 1: Setup (Directory Structure)

**Purpose**: Create the directory structure for subagents and skills

- [x] T001 Create `.claude/agents/content/` directory for content subagents
- [x] T002 [P] Create `.claude/agents/software/` directory for software subagents
- [x] T003 [P] Create `.claude/skills/` directory for all skill folders

**Checkpoint**: Directory structure ready - subagent and skill creation can begin

---

## Phase 2: Foundational Skills (Required by Multiple Subagents)

**Purpose**: Create skills that are referenced by multiple subagents - MUST be complete before subagents that reference them

**⚠️ CRITICAL**: These skills are required by subagents in later phases

### Constitution & Compliance Skills

- [x] T004 [P] Create `.claude/skills/constitution-reader/SKILL.md` with frontmatter (name, description, allowed-tools: Read, Grep)
- [x] T005 [P] Create `.claude/skills/constitution-reader/reference.md` with constitution principles summary
- [x] T006 [P] Create `.claude/skills/tech-stack-constraints/SKILL.md` with frontmatter (name, description, allowed-tools: Read, Grep)
- [x] T007 [P] Create `.claude/skills/tech-stack-constraints/allowed-tech.md` with allowed technologies list from constitution

### Pedagogy Skills

- [x] T008 [P] Create `.claude/skills/layer-definitions/SKILL.md` with frontmatter (name, description, allowed-tools: Read)
- [x] T009 [P] Create `.claude/skills/layer-definitions/layers.md` with L1-L5 pedagogy layer definitions
- [x] T010 [P] Create `.claude/skills/lesson-structure/SKILL.md` with frontmatter (name, description, allowed-tools: Read)
- [x] T011 [P] Create `.claude/skills/lesson-structure/template.md` with lesson markdown template
- [x] T012 [P] Create `.claude/skills/student-language-guide/SKILL.md` with frontmatter (name, description, allowed-tools: Read)
- [x] T013 [P] Create `.claude/skills/student-language-guide/examples.md` with good/bad language examples

### Robotics Skills

- [x] T014 [P] Create `.claude/skills/urdf-templates/SKILL.md` with frontmatter (name, description, allowed-tools: Read, Grep)
- [x] T015 [P] Create `.claude/skills/urdf-templates/validation.md` with URDF validation rules
- [x] T016 [P] Create `.claude/skills/urdf-templates/templates/` directory
- [x] T017 Create `.claude/skills/urdf-templates/templates/mobile-robot.urdf` template (depends on T016)
- [x] T018 [P] Create `.claude/skills/urdf-templates/templates/humanoid-base.urdf` template (depends on T016)
- [x] T019 [P] Create `.claude/skills/ros2-patterns/SKILL.md` with frontmatter (name, description, allowed-tools: Read, Bash)
- [x] T020 [P] Create `.claude/skills/ros2-patterns/messages.md` with common ROS 2 message types
- [x] T021 [P] Create `.claude/skills/ros2-patterns/templates/` directory
- [x] T022 Create `.claude/skills/ros2-patterns/templates/publisher.py` template (depends on T021)
- [x] T023 [P] Create `.claude/skills/ros2-patterns/templates/subscriber.py` template (depends on T021)
- [x] T024 [P] Create `.claude/skills/safety-checklist/SKILL.md` with frontmatter (name, description, allowed-tools: Read, Grep)
- [x] T025 [P] Create `.claude/skills/safety-checklist/checklist.md` with robotics safety validation items

### Translation Skills

- [x] T026 [P] Create `.claude/skills/translation-glossary/SKILL.md` with frontmatter (name, description, allowed-tools: Read)
- [x] T027 [P] Create `.claude/skills/translation-glossary/glossary.md` with technical terms to preserve in Urdu

### Additional Skills (Added Later)

- [x] T027a [P] `.claude/skills/openai-chatkit-backend-python/` - ChatKit custom backend skill with:
  - `SKILL.md` - Main skill definition for Python custom ChatKit backends
  - `reference.md` - Folder structure, env vars, endpoints, Agents SDK integration
  - `examples.md` - 7 examples (minimal backend, streaming, tools, multi-agent, uploads, Gemini, tenant context)
  - `templates/` - Ready-to-use FastAPI templates (fastapi_main.py, llm_factory.py, router.py)
  - `chatkit-backend/python/latest.md` - Latest API patterns
  - `chatkit-backend/changelog.md` - Version tracking

- [x] T027b [P] `.claude/skills/openai-chatkit-frontend-embed-skill/` - ChatKit frontend embedding skill with:
  - `SKILL.md` - Main skill definition for frontend ChatKit integration
  - `reference.md` - Configuration options, auth, domain keys, upload strategies
  - `examples.md` - Frontend integration patterns (Next.js, React, vanilla JS)
  - `templates/` - React components (ChatKitProvider.tsx, ChatKitWidget.tsx, FloatingChatButton.tsx, makeFetch.ts)
  - `chatkit-frontend/js/latest.md` - Latest frontend API patterns
  - `chatkit-frontend/changelog.md` - Version tracking

**Checkpoint**: All 11 skills created - subagent creation can now reference skills

---

## Phase 3: User Story 1 - Write Book Chapter with Subagent Delegation (Priority: P1) 🎯 MVP

**Goal**: Create content subagents for chapter planning, lesson writing, and safety review

**Independent Test**: Ask Claude Code "Plan a chapter on ROS 2 basics" and verify chapter-planner subagent is invoked

### Implementation for User Story 1 - Core Content Subagents

- [x] T028 [P] [US1] Create `.claude/agents/content/super-orchestra.md` with:
  - Frontmatter: name, description (use PROACTIVELY for new courses), tools: Read, Write, Glob, model: sonnet, skills: constitution-reader
  - System prompt for course spec.md and chapter index generation

- [x] T029 [P] [US1] Create `.claude/agents/content/chapter-planner.md` with:
  - Frontmatter: name, description (use PROACTIVELY when starting new chapters), tools: Read, Write, Glob, Grep, model: sonnet, skills: layer-definitions, lesson-structure
  - System prompt for plan.md with lesson breakdown and layer assignments
  - Constitution compliance instructions

- [x] T030 [P] [US1] Create `.claude/agents/content/lesson-writer.md` with:
  - Frontmatter: name, description (use PROACTIVELY when plan.md is ready), tools: Read, Write, Edit, model: sonnet, skills: lesson-structure, student-language-guide
  - System prompt for lesson markdown with "Try With AI" final section
  - Constitution compliance instructions

- [x] T031 [P] [US1] Create `.claude/agents/content/safety-reviewer.md` with:
  - Frontmatter: name, description (use PROACTIVELY after content creation), tools: Read, Grep, model: haiku, skills: safety-checklist
  - System prompt for robotics safety review
  - Read-only analysis focus

**Checkpoint**: User Story 1 subagents ready - can test chapter planning workflow

---

## Phase 4: User Story 2 - Generate Robotics Code with Specialist Subagent (Priority: P1)

**Goal**: Create robotics content specialist subagent for URDF and ROS 2 code generation

**Independent Test**: Ask Claude Code "Create URDF for two-wheeled robot" and verify robotics-code-specialist subagent is invoked

### Implementation for User Story 2 - Robotics Subagents

- [x] T032 [P] [US2] Create `.claude/agents/content/robotics-content-specialist.md` with:
  - Frontmatter: name, description, tools: Read, Write, Bash, model: sonnet, skills: urdf-templates, ros2-patterns
  - System prompt for URDF/launch snippets and ROS 2 code for educational content
  - Safety annotation requirements

- [x] T033 [P] [US2] Create `.claude/agents/software/robotics-code-specialist.md` with:
  - Frontmatter: name, description (Create ROS 2 package), tools: Read, Write, Bash, Edit, model: sonnet, skills: urdf-templates, ros2-patterns, safety-checklist
  - System prompt for ROS 2 packages, URDF, and launch scripts
  - Joint limits and safety validation requirements

**Checkpoint**: User Story 2 subagents ready - can test URDF generation workflow

---

## Phase 5: User Story 3 - Build Platform Components with Software Subagents (Priority: P2)

**Goal**: Create software subagents for platform development (Docusaurus, FastAPI, etc.)

**Independent Test**: Ask Claude Code "Create chapter ingestion endpoint for RAG" and verify rag-backend-engineer subagent produces FastAPI code

### Implementation for User Story 3 - Software Subagents

- [x] T034 [P] [US3] Create `.claude/agents/software/monorepo-architect.md` with:
  - Frontmatter: name, description (Set up monorepo), tools: Read, Write, Bash, Glob, model: sonnet, skills: tech-stack-constraints
  - System prompt for repository structure validation

- [x] T035 [P] [US3] Create `.claude/agents/software/docusaurus-architect.md` with:
  - Frontmatter: name, description (Configure Docusaurus), tools: Read, Write, Edit, model: sonnet, skills: tech-stack-constraints
  - System prompt for sidebar.js and Docusaurus configuration

- [x] T036 [P] [US3] Create `.claude/agents/software/rag-backend-engineer.md` with:
  - Frontmatter: name, description (Create RAG endpoint), tools: Read, Write, Edit, Bash, model: sonnet, skills: tech-stack-constraints
  - System prompt for FastAPI endpoints with Qdrant integration

- [x] T037 [P] [US3] Create `.claude/agents/software/betterauth-engineer.md` with:
  - Frontmatter: name, description (Set up auth), tools: Read, Write, Edit, model: sonnet, skills: tech-stack-constraints
  - System prompt for BetterAuth configuration and signup questionnaire

- [x] T038 [P] [US3] Create `.claude/agents/software/chatkit-backend-engineer.md` with:
  - Frontmatter: name, description (ChatKit Python backend), tools: Read, Write, Edit, Bash, model: sonnet, skills: tech-stack-constraints, openai-chatkit-backend-python
  - System prompt for ChatKitServer implementation using OpenAI Agents SDK
  - **Added skill**: `openai-chatkit-backend-python` for ChatKit custom backend patterns, examples, and templates

- [x] T038a [P] [US3] Create `.claude/agents/software/chatkit-frontend-engineer.md` with:
  - Frontmatter: name, description (ChatKit frontend UI embedding), tools: Read, Write, Edit, Bash, model: sonnet, skills: tech-stack-constraints, openai-chatkit-frontend-embed-skill
  - System prompt for ChatKit widget embedding in Next.js/React/vanilla JS
  - **Added skill**: `openai-chatkit-frontend-embed-skill` for frontend integration patterns and templates

- [x] T039 [P] [US3] Create `.claude/agents/software/gpu-constraints-checker.md` with:
  - Frontmatter: name, description (Check GPU requirements), tools: Read, Bash, model: haiku
  - System prompt for hardware requirements validation for Isaac Sim

- [x] T040 [P] [US3] Create `.claude/agents/software/deployment-infra.md` with:
  - Frontmatter: name, description (Set up CI/CD), tools: Read, Write, Edit, model: sonnet
  - System prompt for GitHub Actions and deployment configuration

**Checkpoint**: User Story 3 subagents ready - can test platform development workflow

---

## Phase 6: User Story 4 - Translate Lesson with Urdu Translator Subagent (Priority: P3)

**Goal**: Create translator subagent for English to Urdu translation preserving technical terms

**Independent Test**: Provide an English lesson and verify translator-urdu subagent output has technical terms in English

### Implementation for User Story 4 - Translation Subagent

- [x] T041 [US4] Create `.claude/agents/content/translator-urdu.md` with:
  - Frontmatter: name, description (Translate to Urdu), tools: Read, Write, model: sonnet, skills: translation-glossary
  - System prompt for Urdu translation preserving English technical terms (ROS 2, URDF, Gazebo, etc.)

**Checkpoint**: User Story 4 subagent ready - can test translation workflow

---

## Phase 7: User Story 5 - Review and Validate Content Quality (Priority: P2)

**Goal**: Create reviewer subagents for pedagogy and RAG answerability

**Independent Test**: Provide content with known issues and verify reviewer subagents identify them

### Implementation for User Story 5 - Review Subagents

- [x] T042 [P] [US5] Create `.claude/agents/content/pedagogy-reviewer.md` with:
  - Frontmatter: name, description (Review cognitive load), tools: Read, Grep, model: haiku, skills: layer-definitions
  - System prompt for cognitive load and layer progression assessment

- [x] T043 [P] [US5] Create `.claude/agents/content/rag-answerability.md` with:
  - Frontmatter: name, description (Improve for RAG), tools: Read, Grep, model: haiku
  - System prompt for heading/definition improvements for RAG retrieval

**Checkpoint**: User Story 5 subagents ready - can test review workflow

---

## Phase 8: User Story 6 - Skills Auto-Invocation for Domain Tasks (Priority: P2)

**Goal**: Verify skills are discovered and auto-invoked by Claude

**Independent Test**: Ask "What Skills are available?" and verify all 9 skills are listed

### Validation for User Story 6

- [ ] T044 [US6] Verify all 9 skill folders have valid SKILL.md with frontmatter (name, description)
- [ ] T045 [US6] Test skill auto-invocation: "Show me URDF structure for a mobile robot" → urdf-templates skill used
- [ ] T046 [US6] Test skill auto-invocation: "Create a ROS 2 publisher node" → ros2-patterns skill used
- [ ] T047 [US6] Test allowed-tools restriction: Verify read-only skills cannot modify files

**Checkpoint**: All skills validated - skill auto-invocation working

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation updates

- [ ] T048 Run `/agents` command to verify all 16 subagents are discovered
- [ ] T049 [P] Test explicit invocation for each subagent type
- [ ] T050 [P] Test automatic delegation triggers for content subagents
- [ ] T051 [P] Test automatic delegation triggers for software subagents
- [ ] T052 Verify subagent chaining works (chapter-planner → lesson-writer → safety-reviewer)
- [ ] T053 [P] Test subagent referencing skills via `skills` frontmatter field
- [ ] T054 Update specs/001-agents-skills/quickstart.md with any learnings from validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational Skills (Phase 2)**: Depends on Setup completion - BLOCKS subagent phases that reference skills
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - US1 and US2 are both P1 - can proceed in parallel
  - US3 and US5 are both P2 - can proceed in parallel
  - US4 is P3 - lower priority, can proceed after P1 and P2
  - US6 validates skills - should run last before Polish
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on layer-definitions, lesson-structure, student-language-guide, safety-checklist skills
- **User Story 2 (P1)**: Depends on urdf-templates, ros2-patterns, safety-checklist skills
- **User Story 3 (P2)**: Depends on tech-stack-constraints skill
- **User Story 4 (P3)**: Depends on translation-glossary skill
- **User Story 5 (P2)**: Depends on layer-definitions skill
- **User Story 6 (P2)**: Depends on all skills being created

### Within Each User Story

- Skills MUST be created before subagents that reference them
- Subagent files are independent - can be created in parallel within a story
- Validation should follow creation

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All skill creation tasks marked [P] can run in parallel (different folders)
- All subagent creation tasks marked [P] can run in parallel (different files)
- US1 and US2 (both P1) can run in parallel after skills are ready
- US3 and US5 (both P2) can run in parallel
- Validation tasks marked [P] can run in parallel

---

## Parallel Example: Phase 2 (Foundational Skills)

```bash
# Launch all skill SKILL.md files together (different folders):
Task: "Create .claude/skills/constitution-reader/SKILL.md"
Task: "Create .claude/skills/tech-stack-constraints/SKILL.md"
Task: "Create .claude/skills/layer-definitions/SKILL.md"
Task: "Create .claude/skills/lesson-structure/SKILL.md"
Task: "Create .claude/skills/urdf-templates/SKILL.md"
Task: "Create .claude/skills/ros2-patterns/SKILL.md"
Task: "Create .claude/skills/safety-checklist/SKILL.md"
Task: "Create .claude/skills/translation-glossary/SKILL.md"
Task: "Create .claude/skills/student-language-guide/SKILL.md"
```

## Parallel Example: User Story 1 (Content Subagents)

```bash
# Launch all content subagents together (different files):
Task: "Create .claude/agents/content/super-orchestra.md"
Task: "Create .claude/agents/content/chapter-planner.md"
Task: "Create .claude/agents/content/lesson-writer.md"
Task: "Create .claude/agents/content/safety-reviewer.md"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup (3 tasks)
2. Complete Phase 2: Foundational Skills (24 tasks)
3. Complete Phase 3: User Story 1 - Core Content Subagents (4 tasks)
4. Complete Phase 4: User Story 2 - Robotics Subagents (2 tasks)
5. **STOP and VALIDATE**: Test chapter planning and URDF generation workflows
6. Can begin using for book content creation

### Incremental Delivery

1. Complete Setup + Foundational → Skills ready
2. Add User Story 1 + 2 → Test independently → Content/Robotics workflows (MVP!)
3. Add User Story 3 → Test independently → Platform development
4. Add User Story 5 → Test independently → Quality review
5. Add User Story 4 → Test independently → Urdu translation
6. Add User Story 6 → Validate all skills

---

## Summary

| Phase | Tasks | Parallel Tasks | Description |
|-------|-------|----------------|-------------|
| 1. Setup | 3 | 2 | Directory structure |
| 2. Foundational Skills | 26 | 24 | All 11 skills with supporting files |
| 3. US1 Content | 4 | 4 | Core content subagents |
| 4. US2 Robotics | 2 | 2 | Robotics subagents |
| 5. US3 Platform | 8 | 8 | Software subagents |
| 6. US4 Translation | 1 | 0 | Translator subagent |
| 7. US5 Review | 2 | 2 | Reviewer subagents |
| 8. US6 Validation | 4 | 0 | Skills validation |
| 9. Polish | 7 | 4 | Final validation |
| **Total** | **57** | **46** | |

**MVP Scope**: Phases 1-4 (33 tasks) delivers core chapter planning and robotics code workflows.

---

## Notes

- [P] tasks = different files/folders, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story can be validated independently
- This feature creates markdown configuration files only - no code tests needed
- Commit after each phase or logical group
- Stop at any checkpoint to validate story independently
