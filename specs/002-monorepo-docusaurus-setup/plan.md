# Implementation Plan: Monorepo with Docusaurus Setup

**Branch**: `002-monorepo-docusaurus-setup` | **Date**: 2025-11-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-monorepo-docusaurus-setup/spec.md`

## Summary

Set up a Turborepo-based monorepo with pnpm workspaces, then add Docusaurus 3.x as the first application in `apps/docs/`. The monorepo will serve as the foundation for the AI-Native Physical AI & Humanoid Robotics Textbook platform.

**Two-Phase Approach**:
1. **Phase 1**: Initialize empty Turborepo monorepo (clean `apps/` and `packages/`)
2. **Phase 2**: Add Docusaurus site in `apps/docs/` with TypeScript, local search, and navigation sidebar

## Technical Context

**Language/Version**: TypeScript 5.3+, Node.js 20+
**Primary Dependencies**: Turborepo 2.6+, pnpm 10+, Docusaurus 3.x, React 18
**Storage**: N/A (static site generation)
**Testing**: TypeScript type-check (tsc), ESLint
**Target Platform**: Web (static site), Node.js development environment
**Project Type**: Monorepo with web application
**Performance Goals**: Build < 60s (initial), < 10s (cached); Dev server hot-reload < 2s
**Constraints**: Node.js 20+ required, pnpm as package manager, constitution-compliant stack
**Scale/Scope**: Single Docusaurus app initially, expandable to multiple apps/packages

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Requirement | Status |
|------|-------------|--------|
| **III. Technical Stack** | Docusaurus 3 (TypeScript + React) | PASS - Using Docusaurus 3.x with TypeScript |
| **III. Technical Stack** | Do NOT use VuePress or other generators | PASS - Using Docusaurus only |
| **X. Spec-First** | spec.md → plan.md → tasks.md → code | PASS - Following sequence |
| **VI. Student-Facing** | Urdu translation support | PASS - i18n configured for en + ur |

**No violations requiring justification.**

## Project Structure

### Documentation (this feature)

```text
specs/002-monorepo-docusaurus-setup/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Research findings (Phase 0)
├── data-model.md        # File structure model (Phase 1)
├── quickstart.md        # Setup instructions (Phase 1)
├── contracts/           # Configuration contracts (Phase 1)
│   ├── turbo.json
│   ├── pnpm-workspace.yaml
│   └── root-package.json
├── checklists/
│   └── requirements.md  # Quality checklist
└── tasks.md             # Implementation tasks (Phase 2 - /sp.tasks)
```

### Source Code (repository root)

```text
ai-native-robotics/                    # Monorepo root
├── apps/                              # Deployable applications
│   └── docs/                          # Docusaurus site (Phase 2)
│       ├── docs/                      # Markdown content
│       │   └── intro.md               # Introduction page
│       ├── src/
│       │   ├── components/            # Custom React components
│       │   ├── css/
│       │   │   └── custom.css         # Custom styles
│       │   └── pages/                 # Custom pages (if needed)
│       ├── static/
│       │   └── img/                   # Static images
│       ├── docusaurus.config.ts       # Docusaurus configuration
│       ├── sidebars.ts                # Navigation sidebar
│       ├── tsconfig.json              # TypeScript config
│       └── package.json               # App manifest
├── packages/                          # Shared packages (empty initially)
├── turbo.json                         # Turborepo pipeline config
├── pnpm-workspace.yaml                # Workspace definition
├── package.json                       # Root manifest
├── .gitignore                         # Updated for monorepo
└── [existing project files...]        # specs/, history/, .specify/, etc.
```

**Structure Decision**: Monorepo with `apps/` for deployable applications and `packages/` for shared libraries. Docusaurus goes in `apps/docs/` as the first application. Existing project structure (specs, history, .specify) remains unchanged at root level.

## Implementation Phases

### Phase 1: Monorepo Foundation

**Tasks**:
1. Create root `package.json` with Turborepo and Node.js 20+ requirement
2. Create `pnpm-workspace.yaml` defining workspace directories
3. Create `turbo.json` with build/dev/lint/type-check pipelines
4. Create empty `apps/` directory
5. Create empty `packages/` directory
6. Update `.gitignore` for monorepo artifacts

**Acceptance Criteria**:
- `pnpm install` runs successfully
- `turbo run build` completes without errors (no apps yet)
- Directory structure matches spec

### Phase 2: Docusaurus App

**Tasks**:
1. Initialize Docusaurus in `apps/docs/` using TypeScript template
2. Configure `docusaurus.config.ts` with TypeScript, MDX, i18n
3. Add local search plugin (`@easyops-cn/docusaurus-search-local`)
4. Configure `sidebars.ts` for documentation navigation
5. Create initial content (`docs/intro.md`)
6. Verify Turborepo integration (root commands work)

**Acceptance Criteria**:
- `cd apps/docs && pnpm dev` starts development server
- `pnpm dev` from root starts Docusaurus via Turborepo
- `pnpm build` from root builds Docusaurus successfully
- Search functionality works
- Navigation sidebar displays

## Complexity Tracking

> **No violations requiring justification** - Implementation follows constitution-approved stack.

## Key Decisions (from research.md)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Turborepo initialization | Manual setup | Repository already exists with project structure |
| Docusaurus template | `classic` with TypeScript | Constitution-compliant, includes all needed features |
| Search plugin | `@easyops-cn/docusaurus-search-local` | Local, offline-capable, multilingual (en+ur) |
| Package naming | `@ai-native-robotics/docs` | Consistent namespace for workspace protocol |

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Execute Phase 1 (monorepo setup)
3. Execute Phase 2 (Docusaurus app)
4. Verify against spec success criteria
