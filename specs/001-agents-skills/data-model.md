# Data Model: Claude Code Subagents and Skills System

**Feature**: 001-agents-skills
**Date**: 2025-11-29

## Overview

Claude Code subagents and skills are **file-based configurations**, not database entities or Python classes. This document describes the file structures and their relationships.

## Entity Relationship Overview

```text
┌─────────────────────┐
│   Claude Code CLI   │
│   (Orchestrator)    │
└──────────┬──────────┘
           │ discovers & uses
           ▼
┌──────────────────────────────────────────────────┐
│                 .claude/ directory               │
├──────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────────┐  │
│  │    agents/      │    │      skills/        │  │
│  │                 │    │                     │  │
│  │  *.md files     │───>│  skill-name/        │  │
│  │  (subagents)    │refs│    SKILL.md         │  │
│  │                 │    │    + support files  │  │
│  └─────────────────┘    └─────────────────────┘  │
└──────────────────────────────────────────────────┘
           │
           │ references
           ▼
┌─────────────────────┐
│ .specify/memory/    │
│ constitution.md     │
└─────────────────────┘
```

---

## Subagent File Structure

### Location
`.claude/agents/*.md` (project-level, highest priority)
`~/.claude/agents/*.md` (user-level, lower priority)

### File Format

```yaml
---
name: subagent-name              # Required: lowercase-kebab-case
description: When to use         # Required: natural language
tools: Read, Write, Edit         # Optional: comma-separated, inherits all if omitted
model: sonnet                    # Optional: sonnet | opus | haiku | inherit
permissionMode: default          # Optional: default | acceptEdits | bypassPermissions | plan | ignore
skills: skill1, skill2           # Optional: comma-separated skill names to auto-load
---

# System Prompt Body

Markdown content that defines the subagent's persona, workflow, and constraints.
```

### Field Specifications

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `name` | string | Yes | Lowercase letters, hyphens only. Max 64 chars. Must be unique. |
| `description` | string | Yes | Free text. Should include triggers for auto-delegation. Max 1024 chars. |
| `tools` | string | No | Comma-separated list of tool names. If omitted, inherits all tools. |
| `model` | enum | No | One of: `sonnet`, `opus`, `haiku`, `inherit`. Default: `sonnet`. |
| `permissionMode` | enum | No | One of: `default`, `acceptEdits`, `bypassPermissions`, `plan`, `ignore`. |
| `skills` | string | No | Comma-separated list of skill names to auto-load. |

### Available Tools

| Tool | Description |
|------|-------------|
| `Read` | Read files from filesystem |
| `Edit` | Edit existing files |
| `Write` | Write new files |
| `Glob` | File pattern matching |
| `Grep` | Content search with regex |
| `Bash` | Execute shell commands |
| `WebFetch` | Fetch web content |
| `WebSearch` | Search the web |

---

## Skill Folder Structure

### Location
`.claude/skills/skill-name/SKILL.md` (project-level)
`~/.claude/skills/skill-name/SKILL.md` (user-level)

### Folder Structure

```text
skill-name/
├── SKILL.md           # Required: Main skill definition
├── reference.md       # Optional: Detailed reference docs
├── examples.md        # Optional: Usage examples
├── templates/         # Optional: Template files
│   └── *.template
└── scripts/           # Optional: Helper scripts
    └── *.py
```

### SKILL.md Format

```yaml
---
name: skill-name                      # Required: lowercase-kebab-case
description: What it does and when    # Required: triggers for auto-invocation
allowed-tools: Read, Grep, Glob       # Optional: restricts tool access
---

# Skill Name

## Instructions
Step-by-step guidance for Claude.

## Examples
Concrete examples of using this skill.

## Reference
For detailed information, see [reference.md](reference.md).
```

### Field Specifications

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `name` | string | Yes | Lowercase letters, numbers, hyphens. Max 64 chars. Must be unique. |
| `description` | string | Yes | What it does AND when to use it. Max 1024 chars. |
| `allowed-tools` | string | No | Comma-separated list of tools Claude can use when skill is active. |

---

## Subagent Catalog

### Content Subagents

| Name | Description | Model | Tools | Skills |
|------|-------------|-------|-------|--------|
| super-orchestra | Course spec and chapter index | sonnet | Read, Write, Glob | constitution-reader |
| chapter-planner | Chapter planning with layers | sonnet | Read, Write, Glob, Grep | layer-definitions, lesson-structure |
| lesson-writer | Lesson content creation | sonnet | Read, Write, Edit | lesson-structure, student-language-guide |
| robotics-content-specialist | URDF/ROS 2 for lessons | sonnet | Read, Write, Bash | urdf-templates, ros2-patterns |
| safety-reviewer | Safety review | haiku | Read, Grep | safety-checklist |
| pedagogy-reviewer | Cognitive load review | haiku | Read, Grep | layer-definitions |
| translator-urdu | Urdu translation | sonnet | Read, Write | translation-glossary |
| rag-answerability | RAG optimization | haiku | Read, Grep | - |

### Software Subagents

| Name | Description | Model | Tools | Skills |
|------|-------------|-------|-------|--------|
| monorepo-architect | Repository structure | sonnet | Read, Write, Bash, Glob | tech-stack-constraints |
| docusaurus-architect | Docusaurus config | sonnet | Read, Write, Edit | tech-stack-constraints |
| rag-backend-engineer | FastAPI endpoints | sonnet | Read, Write, Edit, Bash | tech-stack-constraints |
| betterauth-engineer | Auth configuration | sonnet | Read, Write, Edit | tech-stack-constraints |
| chatkit-engineer | Chatbot integration | sonnet | Read, Write, Edit | tech-stack-constraints |
| robotics-code-specialist | ROS 2 packages | sonnet | Read, Write, Bash, Edit | urdf-templates, ros2-patterns, safety-checklist |
| gpu-constraints-checker | Hardware validation | haiku | Read, Bash | - |
| deployment-infra | CI/CD and deployment | sonnet | Read, Write, Edit | - |

---

## Skills Catalog

### Constitution & Compliance

| Name | Description | Allowed Tools | Supporting Files |
|------|-------------|---------------|------------------|
| constitution-reader | Read constitution principles | Read, Grep | reference.md |
| tech-stack-constraints | Validate tech stack | Read, Grep | allowed-tech.md |

### Pedagogy

| Name | Description | Allowed Tools | Supporting Files |
|------|-------------|---------------|------------------|
| layer-definitions | L1-L5 layer reference | Read | layers.md |
| lesson-structure | Lesson templates | Read | template.md |
| student-language-guide | Student language rules | Read | examples.md |

### Robotics

| Name | Description | Allowed Tools | Supporting Files |
|------|-------------|---------------|------------------|
| urdf-templates | URDF templates | Read, Grep | templates/, validation.md |
| ros2-patterns | ROS 2 patterns | Read, Bash | templates/, messages.md |
| safety-checklist | Safety validation | Read, Grep | checklist.md |

### Translation

| Name | Description | Allowed Tools | Supporting Files |
|------|-------------|---------------|------------------|
| translation-glossary | Technical terms | Read | glossary.md |

---

## Key Differences: Subagents vs Skills

| Aspect | Subagents | Skills |
|--------|-----------|--------|
| **Format** | Single .md file | Folder with SKILL.md + files |
| **Location** | `.claude/agents/*.md` | `.claude/skills/skill-name/` |
| **Invocation** | Delegated by Claude | Model-invoked (auto-detected) |
| **Purpose** | Specialized AI persona | Domain knowledge/templates |
| **Tool Field** | `tools` (what to use) | `allowed-tools` (restriction) |
| **Context** | Separate context window | Loaded into current context |
| **Model** | Can specify model | Uses main conversation model |

---

## Validation Rules

### Subagent Validation
1. File must have `.md` extension
2. YAML frontmatter must have `name` and `description`
3. `name` must be unique across all subagents
4. `name` must be lowercase-kebab-case
5. `tools` must reference valid Claude Code tools
6. `model` must be sonnet, opus, haiku, or inherit
7. `skills` must reference existing skill folders

### Skill Validation
1. Must be a folder with `SKILL.md` inside
2. SKILL.md must have YAML frontmatter with `name` and `description`
3. `name` must be unique across all skills
4. `name` must be lowercase with hyphens/numbers
5. `allowed-tools` must reference valid Claude Code tools
6. Supporting files must exist if referenced in SKILL.md
