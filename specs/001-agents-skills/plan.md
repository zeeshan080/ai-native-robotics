# Implementation Plan: Claude Code Subagents and Skills System

**Branch**: `001-agents-skills` | **Date**: 2025-11-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-agents-skills/spec.md`

## Summary

Implement a subagent architecture for Claude Code CLI using **Markdown files with YAML frontmatter**. Each subagent is a `.md` file stored in `.claude/agents/` that defines specialized AI assistants for domain-specific tasks (content creation, robotics code, platform development, reviews). No Python code required - subagents are configuration files that Claude Code reads natively.

## Technical Context

**Implementation Type**: Markdown configuration files (no code)
**Subagent Location**: `.claude/agents/` (project-level subagents)
**Skills Location**: `.claude/skills/skill-name/SKILL.md` (project-level skills)
**File Format**: Markdown with YAML frontmatter
**Available Tools**: Claude Code built-in tools (Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch)
**Model Options**: sonnet, opus, haiku, or 'inherit'
**Target Platform**: Claude Code CLI
**Scope**: 17 subagents (8 content, 9 software), 11 skills

## Constitution Check

*GATE: Must pass before implementation. All subagent prompts must reference constitution.*

| Principle | Status | Notes |
|-----------|--------|-------|
| III. Strict Technical Stack | ✅ PASS | Subagents are markdown files, not code |
| VII. Content Agents Specification | ✅ PASS | All 8 content agents defined with prompts |
| VIII. Software-Building Agents Specification | ✅ PASS | All 8 software agents defined with prompts |
| IX. Quality & Verification | ✅ PASS | Reviewer subagents include validation guidance |
| X. Spec-First Development | ✅ PASS | Following spec → plan → implementation sequence |

**All gates pass. Proceeding to implementation.**

## Project Structure

### Subagent Files (to be created)

```text
.claude/agents/
├── content/
│   ├── super-orchestra.md
│   ├── chapter-planner.md
│   ├── lesson-writer.md
│   ├── robotics-content-specialist.md
│   ├── safety-reviewer.md
│   ├── pedagogy-reviewer.md
│   ├── translator-urdu.md
│   └── rag-answerability.md
└── software/
    ├── monorepo-architect.md
    ├── docusaurus-architect.md
    ├── rag-backend-engineer.md
    ├── betterauth-engineer.md
    ├── chatkit-backend-engineer.md
    ├── chatkit-frontend-engineer.md
    ├── robotics-code-specialist.md
    ├── gpu-constraints-checker.md
    └── deployment-infra.md
```

Note: Claude Code reads subagents from `.claude/agents/` directory. Subdirectories are organizational only - all `.md` files are discovered.

### Skills (folders with SKILL.md files)

```text
.claude/skills/
├── constitution-reader/
│   ├── SKILL.md                 # Main skill definition
│   └── reference.md             # Constitution principles summary
├── layer-definitions/
│   ├── SKILL.md
│   └── layers.md                # L1-L5 definitions
├── urdf-templates/
│   ├── SKILL.md
│   ├── templates/               # URDF template files
│   │   ├── mobile-robot.urdf
│   │   └── humanoid-base.urdf
│   └── validation.md            # Validation rules
├── ros2-patterns/
│   ├── SKILL.md
│   ├── templates/               # Node template files
│   │   ├── publisher.py
│   │   └── subscriber.py
│   └── messages.md              # Common message types
├── tech-stack-constraints/
│   ├── SKILL.md
│   └── allowed-tech.md          # Allowed technologies list
├── student-language-guide/
│   ├── SKILL.md
│   └── examples.md              # Good/bad examples
├── lesson-structure/
│   ├── SKILL.md
│   └── template.md              # Lesson template
├── safety-checklist/
│   ├── SKILL.md
│   └── checklist.md             # Safety validation items
├── translation-glossary/
│   ├── SKILL.md
│   └── glossary.md              # Technical terms list
├── openai-chatkit-backend-python/
│   ├── SKILL.md
│   ├── reference.md             # Backend patterns
│   ├── examples.md              # Code examples
│   └── templates/               # FastAPI templates
└── openai-chatkit-frontend-embed-skill/
    ├── SKILL.md
    ├── reference.md             # Frontend config
    ├── examples.md              # Integration examples
    └── templates/               # React components
```

Note: Skills are **folders** containing a `SKILL.md` file. Claude autonomously discovers and uses skills based on the description in SKILL.md frontmatter (model-invoked).

## Subagent File Format

Each subagent file follows this structure:

```markdown
---
name: subagent-name
description: Description of when to use this subagent. Use PROACTIVELY for X tasks.
tools: Read, Write, Edit, Glob, Grep, Bash
model: sonnet
skills: skill1, skill2
---

# System Prompt

You are the [Subagent Name] for the AI-Native Physical AI & Humanoid Robotics Textbook.

## Your Role
[Detailed description of what this subagent does]

## Constitution Compliance
Before producing any output, you MUST:
1. Read the constitution at `.specify/memory/constitution.md`
2. Validate your output against relevant principles
3. Include layer assignments for pedagogical content

## Your Workflow
[Step-by-step instructions for the subagent]

## Output Format
[Expected output structure]

## Constraints
[Specific rules and limitations]
```

## Skills File Format

Each skill is a **folder** containing a `SKILL.md` file:

```markdown
---
name: skill-name
description: What this skill does and when to use it. Use when [specific trigger].
allowed-tools: Read, Grep, Glob  # Optional - restricts tool access
---

# Skill Name

## Instructions
Step-by-step guidance for Claude when using this skill.

## Examples
Concrete examples of using this skill.

## Reference
For detailed information, see [reference.md](reference.md).
```

**Key differences from subagents:**
- Skills are **folders** with SKILL.md, subagents are single .md files
- Skills are **model-invoked** (Claude decides when to use), subagents are **delegated** (Claude spawns them)
- Skills use `allowed-tools` to restrict access, subagents use `tools` to specify available tools
- Skills provide domain knowledge, subagents are specialized AI personas

---

## Implementation Phases

### Phase 1: Create Directory Structure

Create `.claude/agents/` and `.claude/skills/` directories.

**Directories to create:**
- `.claude/agents/content/` - Content subagents
- `.claude/agents/software/` - Software subagents
- `.claude/skills/` - All skill folders

### Phase 2: Content Subagents (8 files)

Create the 8 content subagent markdown files:

1. **super-orchestra.md** - Course spec and chapter index generation
2. **chapter-planner.md** - Chapter planning with layer assignments
3. **lesson-writer.md** - Lesson content with "Try With AI" sections
4. **robotics-content-specialist.md** - URDF/ROS 2 content for lessons
5. **safety-reviewer.md** - Robotics safety review
6. **pedagogy-reviewer.md** - Cognitive load and layer review
7. **translator-urdu.md** - English to Urdu translation
8. **rag-answerability.md** - RAG retrieval optimization

### Phase 3: Software Subagents (9 files)

Create the 9 software subagent markdown files:

1. **monorepo-architect.md** - Repository structure
2. **docusaurus-architect.md** - Docusaurus configuration
3. **rag-backend-engineer.md** - FastAPI + Qdrant endpoints
4. **betterauth-engineer.md** - Authentication flows
5. **chatkit-backend-engineer.md** - Python ChatKit backend (Agents SDK)
6. **chatkit-frontend-engineer.md** - Frontend ChatKit embedding
7. **robotics-code-specialist.md** - ROS 2 packages
8. **gpu-constraints-checker.md** - Hardware validation
9. **deployment-infra.md** - CI/CD and deployment

### Phase 4: Skills (11 skill folders)

Create skill folders with SKILL.md files:

**Constitution & Compliance Skills:**
1. **constitution-reader/** - Read and summarize constitution principles
2. **tech-stack-constraints/** - Validate code against allowed technologies

**Pedagogy Skills:**
3. **layer-definitions/** - L1-L5 pedagogy layer reference
4. **lesson-structure/** - Lesson markdown templates
5. **student-language-guide/** - Student-facing language rules

**Robotics Skills:**
6. **urdf-templates/** - URDF structure templates and validation
7. **ros2-patterns/** - ROS 2 node templates and message types
8. **safety-checklist/** - Robotics safety validation checklist

**Translation Skills:**
9. **translation-glossary/** - Technical terms to preserve in translation

**ChatKit Skills (Added):**
10. **openai-chatkit-backend-python/** - Python ChatKit backend patterns
11. **openai-chatkit-frontend-embed-skill/** - Frontend ChatKit embedding

Each skill folder contains:
- `SKILL.md` (required) - Frontmatter + instructions
- Supporting files (optional) - reference.md, templates/, scripts/

### Phase 5: Validation

**Subagent Validation:**
1. Run `/agents` in Claude Code to verify all subagents are discovered
2. Test explicit invocation: "Use the chapter-planner subagent"
3. Test automatic delegation: "Plan a chapter on ROS 2 basics"
4. Verify subagent output follows constitution constraints

**Skills Validation:**
5. Ask Claude "What Skills are available?" to verify skills are discovered
6. Test skill auto-invocation: "Show me URDF structure for a mobile robot"
7. Verify skills with `allowed-tools` correctly restrict Claude's tools
8. Test subagent referencing skills: Verify lesson-writer can use lesson-structure skill

---

## Subagent Specifications

### Content Subagents

#### 1. super-orchestra
- **Purpose**: Generate course spec.md and chapter index from high-level description
- **Model**: sonnet
- **Tools**: Read, Write, Glob
- **Trigger**: "Create course structure", "Plan new textbook"

#### 2. chapter-planner
- **Purpose**: Create plan.md with lesson breakdown and layer assignments
- **Model**: sonnet
- **Tools**: Read, Write, Glob, Grep
- **Trigger**: "Plan chapter on X", "Create chapter structure"

#### 3. lesson-writer
- **Purpose**: Write lesson content with required sections
- **Model**: sonnet
- **Tools**: Read, Write, Edit
- **Trigger**: "Write lesson on X", "Create lesson content"

#### 4. robotics-content-specialist
- **Purpose**: Generate URDF, ROS 2 code snippets for educational content
- **Model**: sonnet
- **Tools**: Read, Write, Bash
- **Trigger**: "Create URDF for lesson", "Add ROS 2 example"

#### 5. safety-reviewer
- **Purpose**: Review content for robotics safety issues
- **Model**: haiku (fast, focused)
- **Tools**: Read, Grep
- **Trigger**: "Review for safety", "Check safety compliance"

#### 6. pedagogy-reviewer
- **Purpose**: Assess cognitive load and layer progression
- **Model**: haiku
- **Tools**: Read, Grep
- **Trigger**: "Review cognitive load", "Check pedagogy"

#### 7. translator-urdu
- **Purpose**: Translate English lessons to Urdu, preserving technical terms
- **Model**: sonnet
- **Tools**: Read, Write
- **Trigger**: "Translate to Urdu", "Create Urdu version"

#### 8. rag-answerability
- **Purpose**: Improve content for RAG retrieval quality
- **Model**: haiku
- **Tools**: Read, Grep
- **Trigger**: "Improve for RAG", "Check answerability"

### Software Subagents

#### 9. monorepo-architect
- **Purpose**: Validate and create repository structure
- **Model**: sonnet
- **Tools**: Read, Write, Bash, Glob
- **Trigger**: "Set up monorepo", "Validate structure"

#### 10. docusaurus-architect
- **Purpose**: Create Docusaurus configuration and sidebar
- **Model**: sonnet
- **Tools**: Read, Write, Edit
- **Trigger**: "Configure Docusaurus", "Create sidebar"

#### 11. rag-backend-engineer
- **Purpose**: Create FastAPI endpoints with Qdrant
- **Model**: sonnet
- **Tools**: Read, Write, Edit, Bash
- **Trigger**: "Create RAG endpoint", "Build API"

#### 12. betterauth-engineer
- **Purpose**: Implement BetterAuth authentication
- **Model**: sonnet
- **Tools**: Read, Write, Edit
- **Trigger**: "Set up auth", "Configure BetterAuth"

#### 13. chatkit-backend-engineer
- **Purpose**: Create Python ChatKit backends using OpenAI Agents SDK
- **Model**: sonnet
- **Tools**: Read, Write, Edit, Bash
- **Trigger**: "Create ChatKit backend", "ChatKitServer implementation"
- **Skills**: tech-stack-constraints, openai-chatkit-backend-python

#### 13a. chatkit-frontend-engineer
- **Purpose**: Embed ChatKit UI in web frontends
- **Model**: sonnet
- **Tools**: Read, Write, Edit, Bash
- **Trigger**: "Embed ChatKit", "ChatKit widget", "Frontend chat integration"
- **Skills**: tech-stack-constraints, openai-chatkit-frontend-embed-skill

#### 14. robotics-code-specialist
- **Purpose**: Create ROS 2 packages, URDF, launch files
- **Model**: sonnet
- **Tools**: Read, Write, Bash, Edit
- **Trigger**: "Create ROS 2 package", "Build robot code"

#### 15. gpu-constraints-checker
- **Purpose**: Validate hardware requirements for Isaac Sim
- **Model**: haiku
- **Tools**: Read, Bash
- **Trigger**: "Check GPU requirements", "Validate hardware"

#### 16. deployment-infra
- **Purpose**: Create GitHub Actions, deployment configs
- **Model**: sonnet
- **Tools**: Read, Write, Edit
- **Trigger**: "Set up CI/CD", "Configure deployment"

---

## Skills Specifications

### Constitution & Compliance Skills

#### 1. constitution-reader
- **Purpose**: Read and summarize constitution principles
- **Trigger**: "Check constitution rules", "What does the constitution say about X"
- **Allowed Tools**: Read, Grep
- **Supporting Files**: reference.md (constitution summary)

#### 2. tech-stack-constraints
- **Purpose**: Validate code against allowed technologies per constitution
- **Trigger**: "Check if X technology is allowed", "Validate tech stack"
- **Allowed Tools**: Read, Grep
- **Supporting Files**: allowed-tech.md (technology list)

### Pedagogy Skills

#### 3. layer-definitions
- **Purpose**: Provide L1-L5 pedagogy layer reference
- **Trigger**: "What is Layer 3?", "Assign layer to content"
- **Allowed Tools**: Read
- **Supporting Files**: layers.md (layer definitions)

#### 4. lesson-structure
- **Purpose**: Provide lesson markdown templates
- **Trigger**: "Create lesson structure", "Lesson template"
- **Allowed Tools**: Read
- **Supporting Files**: template.md (lesson structure)

#### 5. student-language-guide
- **Purpose**: Student-facing language rules
- **Trigger**: "Check student language", "Is this student-friendly"
- **Allowed Tools**: Read
- **Supporting Files**: examples.md (good/bad examples)

### Robotics Skills

#### 6. urdf-templates
- **Purpose**: URDF structure templates and validation patterns
- **Trigger**: "Create URDF", "URDF structure", "Robot description"
- **Allowed Tools**: Read, Grep
- **Supporting Files**: templates/ (URDF files), validation.md

#### 7. ros2-patterns
- **Purpose**: ROS 2 node templates and message types
- **Trigger**: "Create ROS 2 node", "Publisher pattern", "ROS 2 message types"
- **Allowed Tools**: Read, Bash
- **Supporting Files**: templates/ (Python files), messages.md

#### 8. safety-checklist
- **Purpose**: Robotics safety validation checklist
- **Trigger**: "Check safety", "Safety review", "Validate robot code"
- **Allowed Tools**: Read, Grep
- **Supporting Files**: checklist.md (safety items)

### Translation Skills

#### 9. translation-glossary
- **Purpose**: Technical terms to preserve in Urdu translation
- **Trigger**: "Translate to Urdu", "Preserve technical terms"
- **Allowed Tools**: Read
- **Supporting Files**: glossary.md (term list)

---

## Key Design Decisions

### D1: Markdown Files Over Python Code
**Decision**: Implement subagents as Markdown files, not Python classes
**Rationale**: Claude Code natively reads `.claude/agents/*.md` files. No custom code needed.
**Trade-off**: Less programmatic control, but simpler maintenance and version control.

### D2: Constitution in Every Prompt
**Decision**: Every subagent system prompt includes constitution reference
**Rationale**: Ensures all output complies with project principles
**Trade-off**: Slightly longer prompts, but guaranteed compliance.

### D3: Model Selection Per Subagent
**Decision**: Use haiku for reviewers (fast), sonnet for creators (capable)
**Rationale**: Reviewers do read-only analysis; creators need more reasoning
**Trade-off**: Mixed models may have slight inconsistency, but optimizes cost/speed.

### D4: Tools Specified Per Subagent
**Decision**: Explicitly list tools for each subagent
**Rationale**: Limits blast radius - reviewers can't edit, builders can
**Trade-off**: More configuration, but better security.

### D5: Skills as Folders with Supporting Files
**Decision**: Skills are folders containing SKILL.md plus optional supporting files
**Rationale**: Allows bundling templates, scripts, and reference docs with skill
**Trade-off**: Slightly more complex structure, but enables progressive disclosure.

### D6: Skills are Model-Invoked, Not User-Invoked
**Decision**: Claude autonomously decides when to use skills based on description
**Rationale**: Reduces cognitive load on users; skills activate when relevant
**Trade-off**: Less explicit control, but more seamless experience.

---

## Validation Checklist

### Subagents
- [ ] All 17 subagent files created in `.claude/agents/`
- [ ] Each file has valid YAML frontmatter (name, description, tools, model)
- [ ] Each file has comprehensive system prompt
- [ ] `/agents` command shows all custom subagents
- [ ] Explicit invocation works for each subagent
- [ ] Automatic delegation triggers correctly
- [ ] Subagent output follows constitution constraints

### Skills
- [ ] All 11 skill folders created in `.claude/skills/`
- [ ] Each folder has valid SKILL.md with frontmatter (name, description)
- [ ] Skills with allowed-tools correctly restrict Claude's access
- [ ] Supporting files (reference.md, templates/) present where needed
- [ ] "What Skills are available?" lists all skills
- [ ] Skills auto-invoke when relevant queries are asked
- [ ] Subagents can reference skills via `skills` frontmatter
