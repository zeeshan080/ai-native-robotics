# Tasks: Monorepo with Docusaurus Setup

**Input**: Design documents from `/specs/002-monorepo-docusaurus-setup/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No tests explicitly requested in specification. Tasks focus on implementation and verification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Monorepo root**: Repository root (`/home/dell/ai-native-robotics/`)
- **Apps**: `apps/` directory for deployable applications
- **Packages**: `packages/` directory for shared libraries
- **Contracts**: Configuration templates in `specs/002-monorepo-docusaurus-setup/contracts/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization - create empty monorepo structure

- [x] T001 Create root package.json with Turborepo based on contracts/root-package.json in /package.json
- [x] T002 [P] Create pnpm-workspace.yaml based on contracts/pnpm-workspace.yaml in /pnpm-workspace.yaml
- [x] T003 [P] Create turbo.json based on contracts/turbo.json in /turbo.json
- [x] T004 [P] Create empty apps/ directory at /apps/
- [x] T005 [P] Create empty packages/ directory at /packages/
- [x] T006 Update .gitignore with monorepo entries (.turbo, node_modules, build outputs) in /.gitignore

**Checkpoint**: Setup complete - monorepo skeleton ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Verify monorepo foundation works before adding any applications

**⚠️ CRITICAL**: Docusaurus cannot be added until this phase passes

- [x] T007 Run `pnpm install` from root and verify successful completion
- [x] T008 Run `turbo run build` from root and verify it completes (no apps to build)
- [x] T009 Verify directory structure matches spec (apps/ empty, packages/ empty, config files present)

**Checkpoint**: Foundation ready - Docusaurus can now be added

---

## Phase 3: User Story 1 - Initialize Empty Monorepo Structure (Priority: P1) 🎯 MVP

**Goal**: Clean Turborepo monorepo with empty apps/ and packages/ directories

**Independent Test**: Verify `pnpm install` runs successfully and `turbo run build` completes without errors

### Implementation for User Story 1

> **Note**: Most tasks completed in Phase 1-2. This phase validates and documents completion.

- [x] T010 [US1] Verify turbo.json has correct task pipelines (build, dev, lint, type-check) in /turbo.json
- [x] T011 [US1] Verify pnpm-workspace.yaml defines apps/* and packages/* in /pnpm-workspace.yaml
- [x] T012 [US1] Verify root package.json has correct scripts and engines (Node 20+) in /package.json
- [x] T013 [US1] Document completion by updating spec status to "Phase 1 Complete"

**Checkpoint**: User Story 1 complete - empty monorepo is fully functional

---

## Phase 4: User Story 2 - Add Docusaurus App to Monorepo (Priority: P2)

**Goal**: Docusaurus-based documentation website in apps/docs/ with local search and sidebar

**Independent Test**: Navigate to apps/docs/ and run `pnpm dev` to start development server at localhost:3000

### Implementation for User Story 2

- [x] T014 [US2] Initialize Docusaurus 3.x with TypeScript template using `npx create-docusaurus@latest apps/docs classic --typescript`
- [x] T015 [US2] Update apps/docs/package.json to use name `@ai-native-robotics/docs` in /apps/docs/package.json
- [x] T016 [US2] Install local search plugin `@easyops-cn/docusaurus-search-local` in /apps/docs/
- [x] T017 [US2] Configure docusaurus.config.ts with TypeScript, docs-only mode, and search plugin in /apps/docs/docusaurus.config.ts
- [x] T018 [US2] Configure sidebars.ts with mainSidebar for documentation in /apps/docs/sidebars.ts
- [x] T019 [US2] Create initial intro.md content with frontmatter and welcome text in /apps/docs/docs/intro.md
- [x] T020 [US2] Run `pnpm install` from root to install Docusaurus dependencies
- [x] T021 [US2] Verify `cd apps/docs && pnpm dev` starts server at localhost:3000
- [x] T022 [US2] Verify `turbo run build` from root builds Docusaurus successfully
- [x] T023 [US2] Verify search functionality appears in navbar
- [x] T024 [US2] Verify sidebar navigation displays correctly

**Checkpoint**: User Story 2 complete - Docusaurus app is functional with search and navigation

---

## Phase 5: User Story 3 - Root-Level Development Commands (Priority: P3)

**Goal**: Run development commands from monorepo root to manage all apps

**Independent Test**: Run `pnpm dev` and `pnpm build` from root and verify they work via Turborepo

### Implementation for User Story 3

- [x] T025 [US3] Verify `pnpm dev` from root starts Docusaurus via Turborepo
- [x] T026 [US3] Verify `pnpm build` from root builds all apps with caching
- [x] T027 [US3] Verify `pnpm lint` from root runs lint across workspaces (if lint configured in Docusaurus)
- [x] T028 [US3] Test hot-reload by modifying /apps/docs/docs/intro.md and observing dev server update
- [x] T029 [US3] Verify Turborepo caching by running `pnpm build` twice and checking cache hit

**Checkpoint**: User Story 3 complete - root commands work via Turborepo

---

## Phase 6: User Story 4 - Shared Configuration Packages (Priority: P4) ⏸️ DEFERRED

**Goal**: Shared ESLint and TypeScript configs in packages/

**Status**: OUT OF SCOPE for initial implementation (marked in spec.md Out of Scope section)

**Independent Test**: Would verify apps can extend shared configs from packages/

> **Note**: This user story is deferred to a future feature. The packages/ directory remains empty.

**Checkpoint**: Skipped - deferred to future enhancement

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and documentation

- [x] T030 [P] Verify all success criteria from spec.md are met (SC-001 through SC-009)
- [x] T031 [P] Update README.md with monorepo setup instructions (if README exists)
- [x] T032 Run quickstart.md validation steps to verify setup works end-to-end
- [ ] T033 Commit all changes with descriptive message

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - validates monorepo foundation
- **User Story 2 (Phase 4)**: Depends on US1 - adds Docusaurus app
- **User Story 3 (Phase 5)**: Depends on US2 - validates root commands with app present
- **User Story 4 (Phase 6)**: DEFERRED - out of scope
- **Polish (Phase 7)**: Depends on US1, US2, US3 completion

### User Story Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational)
    ↓
Phase 3 (US1: Empty Monorepo) ← MVP checkpoint
    ↓
Phase 4 (US2: Docusaurus App) ← Primary deliverable
    ↓
Phase 5 (US3: Root Commands) ← Convenience layer
    ↓
Phase 7 (Polish) ← Final verification
```

### Parallel Opportunities

**Phase 1 (Setup)**:
```bash
# These can run in parallel (different files):
Task T002: Create pnpm-workspace.yaml
Task T003: Create turbo.json
Task T004: Create empty apps/ directory
Task T005: Create empty packages/ directory
```

**Phase 7 (Polish)**:
```bash
# These can run in parallel:
Task T030: Verify success criteria
Task T031: Update README.md
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T009)
3. Complete Phase 3: User Story 1 (T010-T013) → **MVP Checkpoint 1**
4. Complete Phase 4: User Story 2 (T014-T024) → **MVP Checkpoint 2**
5. **STOP and VALIDATE**: Test Docusaurus runs independently
6. Deploy/demo if ready

### Full Delivery

1. Complete MVP (US1 + US2)
2. Complete Phase 5: User Story 3 (T025-T029)
3. Complete Phase 7: Polish (T030-T033)
4. Skip Phase 6 (US4 deferred)

### Sequential Execution (Single Developer)

Execute tasks in order: T001 → T002 → ... → T033
- Respect dependencies
- Parallel tasks ([P]) can be batched if comfortable
- Commit after each phase completion

---

## Summary

| Phase | Tasks | User Story | Status |
|-------|-------|------------|--------|
| Phase 1: Setup | T001-T006 | - | Ready |
| Phase 2: Foundational | T007-T009 | - | Ready |
| Phase 3: US1 | T010-T013 | Empty Monorepo (P1) | Ready |
| Phase 4: US2 | T014-T024 | Docusaurus App (P2) | Ready |
| Phase 5: US3 | T025-T029 | Root Commands (P3) | Ready |
| Phase 6: US4 | - | Shared Configs (P4) | DEFERRED |
| Phase 7: Polish | T030-T033 | - | Ready |

**Total Tasks**: 33
**Tasks per User Story**: US1=4, US2=11, US3=5, US4=0 (deferred)
**Parallel Opportunities**: 6 tasks marked [P]
**MVP Scope**: US1 + US2 (15 tasks through T024)

---

## Notes

- [P] tasks = different files, no dependencies - can run simultaneously
- [Story] label maps task to specific user story for traceability
- User Story 4 (shared configs) is explicitly deferred per spec.md Out of Scope
- Verify each checkpoint before proceeding to next phase
- Commit after each phase completion
- Success criteria (SC-001 through SC-009) should be verified in Phase 7
