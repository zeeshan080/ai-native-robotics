# Agent & Skill Update Checklist

> **Branch**: `001-agents-skills`
> **Purpose**: All agent and skill definitions live here. Update this branch when issues are found.

---

## Quick Start

```bash
# 1. Switch to the agents branch
git checkout 001-agents-skills
git pull origin 001-agents-skills  # if remote exists

# 2. Make your changes (see sections below)

# 3. Commit and push
git add .claude/agents/ .claude/skills/
git commit -m "fix(agents): <description>"
git push origin 001-agents-skills

# 4. Merge back to your feature branch
git checkout your-feature-branch
git merge 001-agents-skills
```

---

## File Locations

### Agents
```
.claude/agents/
├── content/                    # Educational content agents
│   ├── chapter-planner.md
│   ├── lesson-writer.md
│   ├── pedagogy-reviewer.md
│   ├── rag-answerability.md
│   ├── robotics-content-specialist.md
│   ├── safety-reviewer.md
│   ├── super-orchestra.md
│   └── translator-urdu.md
└── software/                   # Engineering agents
    ├── betterauth-engineer.md
    ├── chatkit-backend-engineer.md
    ├── chatkit-frontend-engineer.md
    ├── deployment-infra.md
    ├── docusaurus-architect.md
    ├── gpu-constraints-checker.md
    ├── monorepo-architect.md
    ├── rag-backend-engineer.md
    └── robotics-code-specialist.md
```

### Skills
```
.claude/skills/
├── constitution-reader/
├── layer-definitions/
├── lesson-structure/
├── openai-chatkit-backend-python/
├── openai-chatkit-frontend-embed-skill/
├── ros2-patterns/
├── safety-checklist/
├── student-language-guide/
├── tech-stack-constraints/
├── translation-glossary/
└── urdf-templates/
```

---

## Agent File Format

```markdown
---
name: agent-name
description: Short description shown in Task tool. Use PROACTIVELY when...
tools: Read, Write, Glob, Grep    # Allowed tools
model: sonnet                      # sonnet | haiku | opus
skills: skill1, skill2             # Skills this agent can invoke
---

# Agent Title

[System prompt content...]
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (kebab-case) |
| `description` | Yes | Shown in Task tool; include "Use PROACTIVELY when..." |
| `tools` | Yes | Comma-separated: Read, Write, Edit, Glob, Grep, Bash |
| `model` | No | `haiku` (fast/cheap), `sonnet` (balanced), `opus` (powerful) |
| `skills` | No | Skills the agent can invoke |

---

## Skill Folder Structure

```
.claude/skills/<skill-name>/
├── SKILL.md          # Main skill definition (required)
├── reference.md      # Reference documentation
├── examples.md       # Usage examples
└── templates/        # Code templates (optional)
    └── *.py, *.tsx, etc.
```

### SKILL.md Format

```markdown
# Skill Name

## Instructions

[When to use this skill and how...]

## Quick Reference

[Key information...]

## Reference

See [reference.md](reference.md) for details.
```

---

## Common Issues & Fixes

### Agent Issues

| Issue | Solution |
|-------|----------|
| Agent lacks context | Add details to system prompt body |
| Wrong tools available | Update `tools:` frontmatter |
| Agent needs a skill | Add to `skills:` frontmatter |
| Too slow/expensive | Change `model:` to `haiku` |
| Missing validation steps | Add checklist to prompt body |
| Incorrect delegation | Update "Delegation Pattern" section |

### Skill Issues

| Issue | Solution |
|-------|----------|
| Skill content outdated | Update reference files |
| Missing examples | Add `examples.md` |
| Template errors | Fix files in `templates/` folder |
| Instructions unclear | Revise `SKILL.md` |

---

## Update Checklist

### Before Making Changes

- [ ] Switched to `001-agents-skills` branch
- [ ] Pulled latest changes from remote
- [ ] Identified the specific agent/skill to update
- [ ] Documented the issue being fixed

### Agent Updates

- [ ] Updated frontmatter if needed (tools, model, skills)
- [ ] Updated system prompt content
- [ ] Verified markdown formatting is correct
- [ ] Tested agent with Task tool

### Skill Updates

- [ ] Updated SKILL.md instructions
- [ ] Updated reference files if needed
- [ ] Updated templates if applicable
- [ ] Tested skill invocation

### After Changes

- [ ] Committed with descriptive message
- [ ] Pushed to `001-agents-skills` branch
- [ ] Merged to feature branch if needed
- [ ] Verified agents/skills work in feature branch

---

## Testing Agents & Skills

### Test an Agent
```
Use Task tool with:
- subagent_type: "<agent-name>"
- prompt: "Describe your capabilities briefly"
- model: "haiku"
```

### Test a Skill
```
Use Skill tool with:
- skill: "<skill-name>"
```

---

## Adding New Agents

1. Create `.claude/agents/<category>/<agent-name>.md`
2. Add frontmatter with name, description, tools, model
3. Write system prompt with:
   - Role definition
   - Primary responsibilities
   - Workflow steps
   - Output format
   - Delegation patterns (if applicable)
4. Test with Task tool

## Adding New Skills

1. Create `.claude/skills/<skill-name>/` folder
2. Create `SKILL.md` with instructions
3. Add reference files as needed
4. Add templates if applicable
5. Test with Skill tool

---

## Commit Message Convention

```
feat(agents): add new <agent-name> agent
fix(agents): correct <agent-name> tool permissions
fix(skills): update <skill-name> reference content
docs(agents): improve <agent-name> system prompt
refactor(skills): reorganize <skill-name> templates
```
