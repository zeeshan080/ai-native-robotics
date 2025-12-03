# Quickstart: Claude Code Subagents and Skills System

**Feature**: 001-agents-skills
**Date**: 2025-11-29

## Overview

This guide explains how to use Claude Code subagents and skills for the AI-Native Physical AI & Humanoid Robotics Textbook project. Both are **file-based configurations** - no Python code required.

## Architecture

```text
Human ──► Claude Code CLI
              │
              ├──► Discovers .claude/agents/*.md (subagents)
              │         └── Delegated for specialized tasks
              │
              └──► Discovers .claude/skills/*/SKILL.md (skills)
                        └── Auto-invoked for domain knowledge
```

---

## Using Subagents

### Automatic Delegation

Claude Code automatically delegates to subagents based on your request:

```
Human: Plan a chapter on ROS 2 basics for Layer 3

Claude Code: [Automatically delegates to chapter-planner subagent]
             [Subagent produces plan.md with lesson structure]
```

### Explicit Invocation

You can also explicitly request a subagent:

```
Human: Use the safety-reviewer subagent to check my URDF file

Claude Code: [Invokes safety-reviewer subagent]
             [Subagent analyzes URDF for safety issues]
```

### Viewing Available Subagents

Run the `/agents` command to see all available subagents:

```
/agents
```

This shows built-in subagents plus your custom project subagents.

---

## Using Skills

### Automatic Discovery

Skills are **model-invoked** - Claude automatically uses them when relevant:

```
Human: Show me the URDF structure for a mobile robot

Claude Code: [Automatically discovers and uses urdf-templates skill]
             [Provides URDF structure based on skill's templates]
```

### Viewing Available Skills

Ask Claude directly:

```
Human: What Skills are available?

Claude Code: [Lists all discovered skills from .claude/skills/]
```

---

## Creating a Subagent

### Step 1: Create the File

Create a markdown file in `.claude/agents/`:

```bash
mkdir -p .claude/agents
touch .claude/agents/my-subagent.md
```

### Step 2: Add Frontmatter and Prompt

```markdown
---
name: my-subagent
description: Description of when to use this subagent. Use PROACTIVELY for X tasks.
tools: Read, Write, Edit, Glob, Grep
model: sonnet
skills: skill1, skill2
---

# My Subagent

You are a specialized assistant for [purpose].

## Your Role
[What this subagent does]

## Constitution Compliance
Before producing output, read `.specify/memory/constitution.md`.

## Workflow
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Output Format
[Expected structure]

## Constraints
- [Rule 1]
- [Rule 2]
```

### Step 3: Test

```
Human: Use the my-subagent subagent to do X
```

---

## Creating a Skill

### Step 1: Create the Folder

```bash
mkdir -p .claude/skills/my-skill
touch .claude/skills/my-skill/SKILL.md
```

### Step 2: Add SKILL.md

```markdown
---
name: my-skill
description: What this skill does. Use when [specific trigger].
allowed-tools: Read, Grep, Glob
---

# My Skill

## Instructions
Step-by-step guidance for Claude when using this skill.

## Examples
Concrete examples of using this skill.

## Reference
For details, see [reference.md](reference.md).
```

### Step 3: Add Supporting Files (Optional)

```bash
touch .claude/skills/my-skill/reference.md
mkdir -p .claude/skills/my-skill/templates
```

### Step 4: Test

```
Human: [Ask something that matches the skill description]

Claude Code: [Automatically uses the skill]
```

---

## Project Subagents

### Content Subagents (8)

| Name | Trigger | Output |
|------|---------|--------|
| super-orchestra | "Plan entire course" | spec.md, chapter index |
| chapter-planner | "Plan chapter on X" | plan.md |
| lesson-writer | "Write lesson on X" | lesson.md |
| robotics-content-specialist | "Create URDF/ROS 2 example" | Code snippets |
| safety-reviewer | "Review for safety" | Safety report |
| pedagogy-reviewer | "Check cognitive load" | Pedagogy report |
| translator-urdu | "Translate to Urdu" | Urdu content |
| rag-answerability | "Optimize for RAG" | Suggestions |

### Software Subagents (8)

| Name | Trigger | Output |
|------|---------|--------|
| monorepo-architect | "Set up project structure" | Directory structure |
| docusaurus-architect | "Configure book site" | Config files |
| rag-backend-engineer | "Create API endpoint" | FastAPI code |
| betterauth-engineer | "Set up authentication" | Auth config |
| chatkit-engineer | "Integrate chatbot" | Frontend code |
| robotics-code-specialist | "Create ROS 2 package" | ROS 2 packages |
| gpu-constraints-checker | "Check GPU requirements" | Constraints report |
| deployment-infra | "Set up deployment" | Deploy config |

---

## Project Skills

### Constitution & Compliance (2)

| Name | Trigger |
|------|---------|
| constitution-reader | "Check constitution rules" |
| tech-stack-constraints | "Validate tech stack" |

### Pedagogy (3)

| Name | Trigger |
|------|---------|
| layer-definitions | "What is Layer 3?" |
| lesson-structure | "Lesson template" |
| student-language-guide | "Student-friendly language" |

### Robotics (3)

| Name | Trigger |
|------|---------|
| urdf-templates | "URDF structure" |
| ros2-patterns | "ROS 2 node pattern" |
| safety-checklist | "Safety review" |

### Translation (1)

| Name | Trigger |
|------|---------|
| translation-glossary | "Translate to Urdu" |

---

## Example Workflows

### Write a Chapter

```
Human: Write a chapter on Gazebo simulation for Layer 2

Claude Code:
1. Delegates to chapter-planner subagent
2. chapter-planner uses layer-definitions skill
3. Produces plan.md with 4 lessons
4. Delegates to lesson-writer for each lesson
5. Delegates to safety-reviewer on output
6. Returns complete chapter
```

### Create URDF

```
Human: Create a URDF for a two-wheeled robot

Claude Code:
1. Delegates to robotics-code-specialist subagent
2. Subagent uses urdf-templates skill
3. Produces URDF with joint limits
4. Delegates to safety-reviewer
5. Returns validated URDF
```

### Check Constitution

```
Human: What does the constitution say about tech stack?

Claude Code:
1. Uses constitution-reader skill (auto-invoked)
2. Uses tech-stack-constraints skill
3. Returns relevant principles
```

---

## File Locations

| Type | Location | Scope |
|------|----------|-------|
| Project subagents | `.claude/agents/*.md` | This project |
| User subagents | `~/.claude/agents/*.md` | All projects |
| Project skills | `.claude/skills/skill-name/` | This project |
| User skills | `~/.claude/skills/skill-name/` | All projects |

---

## Troubleshooting

### Subagent Not Being Used

- Check if `description` matches your request
- Add "Use PROACTIVELY" to description
- Try explicit invocation: "Use the X subagent"

### Skill Not Being Discovered

- Check folder structure: `.claude/skills/skill-name/SKILL.md`
- Verify YAML frontmatter has `name` and `description`
- Ask "What Skills are available?" to confirm discovery

### Subagent Output Issues

- Verify `tools` field includes needed tools
- Check `model` setting (haiku is fast but less capable)
- Review system prompt in the subagent file

---

## Best Practices

1. **Focused subagents** - One responsibility per subagent
2. **Specific descriptions** - Include trigger phrases
3. **Limit tools** - Only grant necessary tools
4. **Read-only skills** - Use `allowed-tools: Read, Grep, Glob` for reference skills
5. **Constitution compliance** - Include constitution check in all content subagents
6. **Version control** - Check `.claude/agents/` and `.claude/skills/` into git
