# Feature Specification: Claude Code Subagents and Skills System

**Feature Branch**: `001-agents-skills`
**Created**: 2025-11-29
**Updated**: 2025-11-29
**Status**: Draft
**Input**: User description: "we first need to create the agents, and their skills for the project"

## Overview

This specification defines the **Claude Code subagent architecture** for the AI-Native Physical AI & Humanoid Robotics Textbook project. Subagents are Markdown files with YAML frontmatter that Claude Code can delegate tasks to. Each subagent has its own context window, specialized system prompt, and configurable tool access.

**Architecture (per Claude Code documentation):**
- **Claude Code CLI** = Main orchestrator (what the human interacts with)
- **Subagents** = Markdown files in `.claude/agents/` with YAML frontmatter defining persona and tools
- **Skills** = Folders containing `SKILL.md` files in `.claude/skills/` that extend Claude's capabilities

**Key Characteristics - Subagents:**
- Subagents are NOT Python code - they are configuration files
- Each subagent operates in its own context window (prevents context pollution)
- Subagents can use Claude Code's built-in tools (Read, Edit, Write, Glob, Grep, Bash, etc.)
- Model can be specified per subagent (sonnet, opus, haiku, or 'inherit')
- Subagents can reference Skills via `skills` frontmatter field

**Key Characteristics - Skills:**
- Skills are **folders** containing a `SKILL.md` file with YAML frontmatter
- Skills are **model-invoked** - Claude autonomously decides when to use them based on description
- Skills can include supporting files (reference.md, scripts/, templates/)
- Skills can restrict tool access via `allowed-tools` frontmatter field
- Skills provide domain knowledge, templates, and specialized workflows

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Write Book Chapter with Subagent Delegation (Priority: P1)

A human asks Claude Code to write a chapter on "Introduction to ROS 2". Claude Code automatically delegates to the chapter-planner subagent which produces plan.md, then chains to lesson-writer subagent for each lesson.

**Why this priority**: This is the core workflow for book creation.

**Independent Test**: Ask Claude Code to plan a chapter and verify it invokes the chapter-planner subagent.

**Acceptance Scenarios**:

1. **Given** Claude Code receives "Write chapter on ROS 2 basics for Layer 3", **When** it recognizes this as a chapter planning task, **Then** it delegates to chapter-planner subagent which reads the constitution and produces plan.md.

2. **Given** chapter-planner has produced plan.md, **When** Claude Code proceeds to lesson writing, **Then** it delegates to lesson-writer subagent with plan.md as context.

3. **Given** lessons are written, **When** Claude Code validates content, **Then** it delegates to safety-reviewer subagent which checks for robotics safety issues.

---

### User Story 2 - Generate Robotics Code with Specialist Subagent (Priority: P1)

A human asks Claude Code to create a URDF file for a humanoid robot or write ROS 2 nodes. Claude Code delegates to robotics-code-specialist subagent which has specialized prompts for URDF generation, ROS 2 patterns, and safety annotations.

**Why this priority**: Robotics code requires domain expertise embedded in the subagent's system prompt.

**Independent Test**: Ask Claude Code to create a URDF and verify the robotics-code-specialist subagent is invoked.

**Acceptance Scenarios**:

1. **Given** Claude Code receives "Create URDF for two-wheeled robot with IMU sensor", **When** it identifies this as robotics code, **Then** it delegates to robotics-code-specialist subagent.

2. **Given** robotics-code-specialist is working, **When** it generates URDF, **Then** output includes joint limits, mass/inertia validation, and safety comments per the subagent's system prompt.

---

### User Story 3 - Build Platform Components with Software Subagents (Priority: P2)

A human asks Claude Code to set up the Docusaurus book site or create FastAPI RAG endpoints. Claude Code delegates to docusaurus-architect or rag-backend-engineer subagents which have system prompts enforcing the strict technical stack.

**Why this priority**: Platform infrastructure requires adherence to specific tech stack constraints.

**Independent Test**: Ask Claude Code to create a RAG endpoint and verify the rag-backend-engineer subagent produces FastAPI code.

**Acceptance Scenarios**:

1. **Given** Claude Code receives "Create chapter ingestion endpoint for RAG", **When** it identifies this as backend work, **Then** it delegates to rag-backend-engineer subagent.

2. **Given** rag-backend-engineer is working, **When** it generates code, **Then** output follows FastAPI + Qdrant patterns per constitution.

---

### User Story 4 - Translate Lesson with Urdu Translator Subagent (Priority: P3)

A human asks Claude Code to translate a completed English lesson to Urdu. Claude Code delegates to translator-urdu subagent which preserves technical terms in English.

**Why this priority**: Bilingual support follows after core content creation.

**Independent Test**: Provide an English lesson and verify translator-urdu subagent output has technical terms in English with Urdu explanatory text.

**Acceptance Scenarios**:

1. **Given** Claude Code receives "Translate lesson-03-ros-nodes.md to Urdu", **When** it processes the request, **Then** it delegates to translator-urdu subagent.

2. **Given** translator-urdu is working, **When** it encounters "ROS 2 node", "Gazebo", "URDF", **Then** it preserves these terms in English per its system prompt.

---

### User Story 5 - Review and Validate Content Quality (Priority: P2)

A human asks Claude Code to review a chapter for pedagogy quality or RAG answerability. Claude Code delegates to pedagogy-reviewer or rag-answerability subagents.

**Why this priority**: Quality gates ensure content meets educational standards.

**Independent Test**: Provide content with known issues and verify the reviewer subagent identifies them.

**Acceptance Scenarios**:

1. **Given** Claude Code receives "Review chapter for cognitive load", **When** it processes, **Then** it delegates to pedagogy-reviewer subagent.

2. **Given** pedagogy-reviewer analyzes content with too many concepts per lesson, **Then** it recommends splitting lessons per its system prompt.

---

### User Story 6 - Skills Auto-Invocation for Domain Tasks (Priority: P2)

A human asks Claude Code about URDF structure or ROS 2 patterns. Claude autonomously discovers and uses the relevant Skill (e.g., urdf-templates skill) based on the request context.

**Why this priority**: Skills reduce repetitive prompting and provide consistent domain expertise.

**Independent Test**: Ask about URDF structure and verify Claude uses the urdf-templates skill.

**Acceptance Scenarios**:

1. **Given** Claude Code receives "Show me the URDF structure for a mobile robot", **When** it processes, **Then** it autonomously uses the urdf-templates skill based on description match.

2. **Given** the ros2-patterns skill exists, **When** user asks "Create a ROS 2 publisher node", **Then** Claude uses the skill's templates and patterns.

3. **Given** a skill has `allowed-tools: Read, Grep, Glob`, **When** the skill is active, **Then** Claude can only use those tools (read-only mode).

---

### Edge Cases

- What happens when Claude Code cannot determine which subagent to use?
  - Claude Code asks the human for clarification before delegating
- What happens when a subagent's output violates constitution constraints?
  - Claude Code (main thread) validates output and either retries or reports to human
- What happens when multiple subagents need to collaborate?
  - Claude Code chains subagent invocations, passing output from one as context to another

## Requirements *(mandatory)*

### Functional Requirements

**Subagent Files (stored in `.claude/agents/`):**
- **FR-001**: Each subagent MUST be a Markdown file with YAML frontmatter containing: name, description, tools (optional), model (optional), skills (optional)
- **FR-002**: Subagent system prompt MUST be in the Markdown body after frontmatter
- **FR-003**: Subagent names MUST be lowercase with hyphens (e.g., "chapter-planner")
- **FR-004**: Subagents MAY specify tools to limit tool access, or inherit all tools if omitted

**Content Subagents (8 subagents):**
- **FR-005**: super-orchestra - Produces spec.md and chapter index from course description
- **FR-006**: chapter-planner - Produces plan.md with lesson list and layer assignments
- **FR-007**: lesson-writer - Produces lesson markdown with "Try With AI" final section
- **FR-008**: robotics-content-specialist - Produces URDF/launch snippets and ROS 2 code for lessons
- **FR-009**: safety-reviewer - Analyzes content for robotics safety issues
- **FR-010**: pedagogy-reviewer - Assesses cognitive load and layer progression
- **FR-011**: translator-urdu - Produces Urdu translation preserving English technical terms
- **FR-012**: rag-answerability - Suggests heading/definition improvements for RAG retrieval

**Software-Building Subagents (8 subagents):**
- **FR-013**: monorepo-architect - Validates and enforces repository layout
- **FR-014**: docusaurus-architect - Produces sidebar, routing, and ChatKit widget configuration
- **FR-015**: rag-backend-engineer - Produces FastAPI endpoints using Qdrant client
- **FR-016**: betterauth-engineer - Produces auth configuration and signup questionnaire code
- **FR-017**: chatkit-backend-engineer - Produces Python ChatKit backend using OpenAI Agents SDK
- **FR-017a**: chatkit-frontend-engineer - Produces frontend ChatKit UI embedding and configuration
- **FR-018**: robotics-code-specialist - Produces ROS 2 packages, URDF, and launch scripts
- **FR-019**: gpu-constraints-checker - Validates hardware requirements for simulations
- **FR-020**: deployment-infra - Produces GitHub Pages and deployment configuration

**Skills (Folders with SKILL.md in `.claude/skills/`):**
- **FR-021**: Each Skill MUST be a folder containing a `SKILL.md` file with YAML frontmatter
- **FR-022**: Skill folders MUST be stored in `.claude/skills/skill-name/` (project) or `~/.claude/skills/skill-name/` (personal)
- **FR-023**: Skill frontmatter MUST contain: `name` (lowercase-hyphen, max 64 chars) and `description` (max 1024 chars)
- **FR-024**: Skills MAY specify `allowed-tools` to restrict tool access when skill is active
- **FR-025**: Skills MAY include supporting files: reference.md, examples.md, scripts/, templates/
- **FR-026**: Skills are model-invoked - Claude autonomously discovers and uses them based on description match
- **FR-027**: Skills can be referenced by subagents via `skills: skill1, skill2` frontmatter

**Skills Catalog (11 skills for this project):**
- **FR-028**: constitution-reader - Read and summarize constitution principles
- **FR-029**: layer-definitions - L1-L5 pedagogy layer reference
- **FR-030**: urdf-templates - URDF structure templates and validation patterns
- **FR-031**: ros2-patterns - ROS 2 node templates and message types
- **FR-032**: tech-stack-constraints - Allowed technologies per constitution
- **FR-033**: student-language-guide - Student-facing language rules
- **FR-034**: lesson-structure - Lesson markdown structure templates
- **FR-035**: safety-checklist - Robotics safety validation checklist
- **FR-036**: translation-glossary - Technical terms to preserve in translation
- **FR-037a**: openai-chatkit-backend-python - Python custom ChatKit backend patterns with Agents SDK
- **FR-037b**: openai-chatkit-frontend-embed-skill - Frontend ChatKit embedding patterns for Next.js/React

**Constitution Compliance:**
- **FR-037**: All subagent system prompts MUST include constitution compliance instructions
- **FR-038**: Subagents MUST be instructed to read constitution before producing output
- **FR-039**: Content subagents MUST include layer assignment guidance in their prompts

### Key Entities

- **Subagent File**: A Markdown file in `.claude/agents/` with YAML frontmatter (name, description, tools, model, skills) and system prompt body.

- **Skill Folder**: A folder in `.claude/skills/skill-name/` containing:
  - `SKILL.md` (required) - YAML frontmatter + instructions
  - Supporting files (optional) - reference.md, examples.md, scripts/, templates/

- **SKILL.md Structure**:
  ```yaml
  ---
  name: skill-name
  description: What this skill does and when to use it
  allowed-tools: Read, Grep, Glob  # Optional - restricts tool access
  ---

  # Skill Name

  ## Instructions
  Step-by-step guidance for Claude.

  ## Examples
  Concrete examples of using this skill.
  ```

- **Subagent Context**: Claude Code passes context by describing the task in the prompt when invoking the Task tool with `subagent_type` parameter.

### Claude Code Built-in Tools (Available to Subagents)

Per Claude Code documentation, subagents can use these tools:
- `Read` - Read files from filesystem
- `Edit` - Edit existing files
- `Write` - Write new files
- `Glob` - File pattern matching
- `Grep` - Content search with regex
- `Bash` - Execute shell commands
- `WebFetch` - Fetch web content
- `WebSearch` - Search the web
- MCP tools if configured

## Subagent Catalog (Detailed)

### Content Subagents

| Name | Description | Model | Tools |
|------|-------------|-------|-------|
| super-orchestra | Produces spec.md and chapter index from course description. Use PROACTIVELY for new courses. | sonnet | Read, Write, Glob |
| chapter-planner | Produces plan.md with lesson list and layer assignments. Use PROACTIVELY when starting new chapters. | sonnet | Read, Write, Glob, Grep |
| lesson-writer | Writes lesson markdown with required sections. Use PROACTIVELY when plan.md is ready. | sonnet | Read, Write, Edit |
| robotics-content-specialist | Generates URDF/launch snippets and ROS 2 code for lessons. | sonnet | Read, Write, Bash |
| safety-reviewer | Reviews content for robotics safety issues. Use PROACTIVELY after content creation. | haiku | Read, Grep |
| pedagogy-reviewer | Assesses cognitive load and layer progression. | haiku | Read, Grep |
| translator-urdu | Translates lessons to Urdu preserving technical terms. | sonnet | Read, Write |
| rag-answerability | Suggests improvements for RAG retrieval quality. | haiku | Read, Grep |

### Software Subagents

| Name | Description | Model | Tools |
|------|-------------|-------|-------|
| monorepo-architect | Validates and creates repository structure. | sonnet | Read, Write, Bash, Glob |
| docusaurus-architect | Produces sidebar.js and Docusaurus configuration. | sonnet | Read, Write, Edit |
| rag-backend-engineer | Creates FastAPI endpoints with Qdrant integration. | sonnet | Read, Write, Edit, Bash |
| betterauth-engineer | Creates BetterAuth configuration and auth flows. | sonnet | Read, Write, Edit |
| chatkit-backend-engineer | Creates Python ChatKit backends using Agents SDK. | sonnet | Read, Write, Edit, Bash |
| chatkit-frontend-engineer | Creates frontend ChatKit UI embedding. | sonnet | Read, Write, Edit, Bash |
| robotics-code-specialist | Produces ROS 2 packages, URDF, launch scripts. | sonnet | Read, Write, Bash, Edit |
| gpu-constraints-checker | Validates hardware requirements for Isaac Sim. | haiku | Read, Bash |
| deployment-infra | Creates GitHub Actions and deployment configs. | sonnet | Read, Write, Edit |

## Skills Catalog (Detailed)

### Constitution & Compliance Skills

| Name | Description | Allowed Tools | Supporting Files |
|------|-------------|---------------|------------------|
| constitution-reader | Read and summarize constitution principles. Use when checking project rules. | Read, Grep | reference.md |
| tech-stack-constraints | Validate code against allowed technologies. Use when writing platform code. | Read, Grep | allowed-tech.md |

### Pedagogy Skills

| Name | Description | Allowed Tools | Supporting Files |
|------|-------------|---------------|------------------|
| layer-definitions | L1-L5 pedagogy layer reference. Use when assigning layers to content. | Read | layers.md |
| lesson-structure | Lesson markdown templates. Use when writing lessons. | Read | template.md |
| student-language-guide | Student-facing language rules. Use when writing educational content. | Read | examples.md |

### Robotics Skills

| Name | Description | Allowed Tools | Supporting Files |
|------|-------------|---------------|------------------|
| urdf-templates | URDF structure templates and validation. Use when creating robot descriptions. | Read, Grep | templates/, validation.md |
| ros2-patterns | ROS 2 node templates and message types. Use when writing ROS 2 code. | Read, Bash | templates/, messages.md |
| safety-checklist | Robotics safety validation checklist. Use when reviewing robot code. | Read, Grep | checklist.md |

### Translation Skills

| Name | Description | Allowed Tools | Supporting Files |
|------|-------------|---------------|------------------|
| translation-glossary | Technical terms to preserve in translation. Use when translating to Urdu. | Read | glossary.md |

### ChatKit Skills (Added)

| Name | Description | Allowed Tools | Supporting Files |
|------|-------------|---------------|------------------|
| openai-chatkit-backend-python | Python custom ChatKit backend patterns. Use when building ChatKitServer backends. | Read, Grep | reference.md, examples.md, templates/ |
| openai-chatkit-frontend-embed-skill | Frontend ChatKit embedding. Use when embedding ChatKit widgets. | Read | reference.md, examples.md, templates/ |

## Assumptions

- Claude Code's `/agents` command can manage subagents
- Subagents are stored in `.claude/agents/` directory
- Skills are stored in `.claude/skills/skill-name/` directories with SKILL.md files
- Claude Code automatically delegates to subagents based on task description and subagent `description` field
- Claude autonomously discovers and uses Skills based on Skill `description` field (model-invoked)
- Skills can be referenced by subagents via `skills` frontmatter field
- Asking Claude "What Skills are available?" lists all discovered skills

## Success Criteria *(mandatory)*

### Measurable Outcomes - Subagents

- **SC-001**: All 17 subagent files created in `.claude/agents/` with valid frontmatter
- **SC-002**: Claude Code `/agents` command lists all custom subagents
- **SC-003**: Claude Code automatically delegates to chapter-planner when asked to plan a chapter
- **SC-004**: Content subagents produce output following constitution constraints
- **SC-005**: Software subagents produce code following tech stack constraints
- **SC-006**: Human can explicitly invoke any subagent by name (e.g., "Use the safety-reviewer subagent")
- **SC-007**: Subagent chaining works (output from one used as input to another)

### Measurable Outcomes - Skills

- **SC-008**: All 11 skill folders created in `.claude/skills/` with valid SKILL.md files
- **SC-009**: Claude responds correctly to "What Skills are available?" listing all skills
- **SC-010**: Claude autonomously uses urdf-templates skill when asked about URDF structure
- **SC-011**: Claude autonomously uses ros2-patterns skill when asked to create ROS 2 code
- **SC-012**: Skills with `allowed-tools` correctly restrict Claude's tool access
- **SC-013**: Subagents can reference skills via `skills` frontmatter field
- **SC-014**: Skills with supporting files (reference.md, scripts/) are read correctly by Claude
