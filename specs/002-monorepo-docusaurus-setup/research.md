# Research: Monorepo with Docusaurus Setup

**Feature**: 002-monorepo-docusaurus-setup
**Date**: 2025-11-29
**Agents Used**: monorepo-architect, docusaurus-architect

## Phase 1: Turborepo Monorepo Setup

### Decision: Manual Setup vs create-turbo

**Decision**: Manual setup (since repository already exists)

**Rationale**:
- Repository already has `.specify/`, `specs/`, `history/` structure
- Using `create-turbo` would overwrite existing files
- Manual setup gives precise control over what gets added

**Alternatives Considered**:
- `pnpm dlx create-turbo@latest` - Would overwrite existing structure
- Git submodule approach - Unnecessary complexity

### Decision: Turborepo Initialization Commands

**Decision**: Use the following sequence:

```bash
# Install Turborepo at root
pnpm add -D turbo@latest

# Create workspace directories
mkdir -p apps packages

# Turborepo will use existing or new turbo.json
```

### Decision: turbo.json Configuration

**Decision**: Minimal configuration with build, dev, lint, type-check tasks

```json
{
  "$schema": "https://turbo.build/schema.json",
  "ui": "tui",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".docusaurus/**", "build/**"],
      "env": ["NODE_ENV"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^lint"],
      "outputs": []
    },
    "type-check": {
      "dependsOn": ["^type-check"],
      "outputs": []
    },
    "clean": {
      "cache": false
    }
  }
}
```

**Rationale**:
- `$schema` enables IDE IntelliSense
- `ui: "tui"` provides modern terminal UI (Turbo v2+)
- `dependsOn: ["^build"]` ensures dependencies build first
- `outputs` includes Docusaurus artifacts (`.docusaurus/**`, `build/**`)
- `cache: false` for dev/clean tasks (always run fresh)
- `persistent: true` for dev servers

### Decision: pnpm-workspace.yaml

**Decision**: Simple wildcard pattern

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

**Rationale**:
- Covers all current and future apps
- Keeps Python backend (`platform/backend`) outside workspace (not Node.js)
- Standard Turborepo convention

### Decision: Root package.json

**Decision**: Minimal root manifest

```json
{
  "name": "ai-native-robotics",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "build": "turbo build",
    "dev": "turbo dev",
    "lint": "turbo lint",
    "type-check": "turbo type-check",
    "clean": "turbo clean"
  },
  "devDependencies": {
    "turbo": "^2.6.1"
  },
  "packageManager": "pnpm@10.18.3",
  "engines": {
    "node": ">=20.0.0",
    "pnpm": ">=8.0.0"
  }
}
```

**Rationale**:
- `private: true` prevents accidental npm publish
- `packageManager` pins pnpm version for Corepack
- `engines` enforces Node.js 20+ requirement (per spec)
- Scripts delegate to Turborepo for parallel/cached execution

---

## Phase 2: Docusaurus App Setup

### Decision: Installation Method

**Decision**: Use `create-docusaurus` with TypeScript template

```bash
npx create-docusaurus@latest apps/docs classic --typescript
```

**Rationale**:
- Official Docusaurus scaffolding ensures correct structure
- TypeScript is mandatory per constitution (Section III)
- Classic preset includes docs, theme, sitemap, search support

**Alternatives Considered**:
- Manual setup - More error-prone, no benefit
- Non-TypeScript template - Violates constitution

### Decision: Docusaurus Template

**Decision**: `classic` template

**Rationale**:
- Includes Docs plugin (primary use case)
- Includes Theme classic (standard UI)
- Blog can be disabled if not needed
- Easy to customize
- MDX support out of the box

### Decision: Search Plugin

**Decision**: `@easyops-cn/docusaurus-search-local`

```bash
npm install --save @easyops-cn/docusaurus-search-local
```

**Rationale**:
- Fully local (no external API calls)
- Works offline
- Supports multiple languages (English + Urdu per constitution)
- Free and open source
- No Algolia account required

**Alternatives Considered**:
- Algolia DocSearch - Requires external service, more setup
- docusaurus-lunr-search - Less feature-rich
- No search - Violates FR-008/FR-009 in spec

**Configuration**:
```typescript
themes: [
  [
    require.resolve("@easyops-cn/docusaurus-search-local"),
    {
      hashed: true,
      language: ["en", "ur"],
      indexDocs: true,
      indexBlog: false,
      docsRouteBasePath: '/',
    },
  ],
],
```

### Decision: Docusaurus Configuration

**Decision**: TypeScript config with docs-only mode

Key features:
- `routeBasePath: '/'` - Docs as homepage
- `blog: false` - Disabled (not needed for textbook)
- i18n support for English + Urdu (per constitution)
- Prism highlighting for Python, Bash, YAML, XML (robotics stack)
- Mermaid diagrams enabled (for architecture diagrams)

### Decision: Package Name Convention

**Decision**: `@ai-native-robotics/docs`

**Rationale**:
- Follows monorepo naming convention
- Allows workspace protocol references: `"@ai-native-robotics/docs": "workspace:*"`
- Clear namespace for future packages

### Decision: Sidebar Structure

**Decision**: Manual sidebar configuration (not autogenerated)

**Rationale**:
- Textbook has specific 6-part, 18-chapter structure
- Manual control over navigation hierarchy
- Can group chapters into parts
- Better UX for educational content

---

## Key Files Summary

| File | Location | Purpose |
|------|----------|---------|
| turbo.json | Root | Turborepo task pipeline |
| pnpm-workspace.yaml | Root | Workspace package definition |
| package.json | Root | Root manifest with scripts |
| package.json | apps/docs/ | Docusaurus app manifest |
| docusaurus.config.ts | apps/docs/ | Docusaurus configuration |
| sidebars.ts | apps/docs/ | Navigation sidebar |
| tsconfig.json | apps/docs/ | TypeScript configuration |

---

## Constitution Compliance Notes

- **Section III (Technical Stack)**: Docusaurus 3 + TypeScript + React - COMPLIANT
- **Section VI (Student-Facing Language)**: i18n for English + Urdu - CONFIGURED
- **Section X (Spec-First)**: Following spec.md → plan.md → tasks.md - IN PROGRESS
