# Research: Claude Code Subagents and Skills System

**Feature**: 001-agents-skills
**Date**: 2025-11-29
**Source**: https://code.claude.com/docs/en/subagents

## Research Summary

Claude Code subagents are **Markdown files with YAML frontmatter** stored in `.claude/agents/`. They are NOT Python code or OpenAI Agents SDK implementations. Claude Code natively discovers and uses these files.

---

## Key Findings from Official Documentation

### 1. What Are Subagents?

Subagents are pre-configured AI personalities that Claude Code can delegate tasks to. Each subagent:
- Has a specific purpose and expertise area
- Uses its **own context window** (separate from main conversation)
- Can be configured with specific tools it's allowed to use
- Includes a custom system prompt that guides its behavior

### 2. File Locations

| Type | Location | Scope | Priority |
|------|----------|-------|----------|
| **Project subagents** | `.claude/agents/` | Current project only | Highest |
| **User subagents** | `~/.claude/agents/` | All projects | Lower |

When subagent names conflict, project-level subagents take precedence.

### 3. File Format

Each subagent is a Markdown file with this structure:

```markdown
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # Optional - inherits all tools if omitted
model: sonnet  # Optional - specify model alias or 'inherit'
permissionMode: default  # Optional
skills: skill1, skill2  # Optional - skills to auto-load
---

Your subagent's system prompt goes here. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.
```

### 4. Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier using lowercase letters and hyphens |
| `description` | Yes | Natural language description of the subagent's purpose |
| `tools` | No | Comma-separated list of tools. Inherits all if omitted |
| `model` | No | Model alias (sonnet, opus, haiku) or 'inherit' |
| `permissionMode` | No | default, acceptEdits, bypassPermissions, plan, ignore |
| `skills` | No | Comma-separated list of skills to auto-load |

### 5. Available Tools

Subagents can use Claude Code's internal tools:
- `Read` - Read files
- `Edit` - Edit existing files
- `Write` - Write new files
- `Glob` - File pattern matching
- `Grep` - Content search with regex
- `Bash` - Execute shell commands
- `WebFetch` - Fetch web content
- `WebSearch` - Search the web
- MCP tools (if configured)

### 6. Model Selection

- **sonnet**: Default for subagents, capable reasoning
- **opus**: Most capable, for complex tasks
- **haiku**: Fast, low-latency, good for reviewers
- **'inherit'**: Use same model as main conversation

### 7. Built-in Subagents

Claude Code includes these built-in subagents:

| Name | Model | Purpose |
|------|-------|---------|
| **general-purpose** | Sonnet | Complex multi-step tasks, can read/write |
| **Plan** | Sonnet | Research during plan mode |
| **Explore** | Haiku | Fast read-only codebase exploration |

### 8. Automatic Delegation

Claude Code proactively delegates based on:
- The task description in your request
- The `description` field in subagent configurations
- Current context and available tools

**Tip**: Include "use PROACTIVELY" or "MUST BE USED" in description field to encourage automatic use.

### 9. Explicit Invocation

Users can request a specific subagent:
```
> Use the test-runner subagent to fix failing tests
> Have the code-reviewer subagent look at my recent changes
```

### 10. Managing Subagents

Use `/agents` command for:
- View all subagents (built-in, user, project)
- Create new subagents with guided setup
- Edit existing subagents
- Delete custom subagents

---

## Skills Research

**Source**: https://code.claude.com/docs/en/skills

### What Are Skills?

Agent Skills package expertise into discoverable capabilities. Each Skill consists of:
- A **folder** containing a `SKILL.md` file with instructions
- Optional supporting files (scripts, templates, reference docs)

**Key Difference from Subagents**:
- Skills are **model-invoked** - Claude autonomously decides when to use them based on description
- Subagents are **delegated** - Claude spawns them to handle specific tasks
- Skills provide domain knowledge; Subagents are specialized AI personas

### Skill Locations

| Type | Location | Scope |
|------|----------|-------|
| **Project skills** | `.claude/skills/skill-name/` | Current project only |
| **Personal skills** | `~/.claude/skills/skill-name/` | All projects |
| **Plugin skills** | Bundled with plugins | Plugin-specific |

### SKILL.md File Format

```yaml
---
name: skill-name
description: Brief description of what this Skill does and when to use it
allowed-tools: Read, Grep, Glob  # Optional - restricts tool access
---

# Skill Name

## Instructions
Step-by-step guidance for Claude when using this skill.

## Examples
Concrete examples of using this skill.
```

### Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase letters, numbers, hyphens (max 64 chars) |
| `description` | Yes | What it does AND when to use it (max 1024 chars) |
| `allowed-tools` | No | Comma-separated list of tools Claude can use when skill is active |

### Skill Structure with Supporting Files

```text
my-skill/
├── SKILL.md (required)
├── reference.md (optional documentation)
├── examples.md (optional examples)
├── scripts/
│   └── helper.py (optional utility)
└── templates/
    └── template.txt (optional template)
```

Claude reads supporting files only when needed (progressive disclosure).

### allowed-tools Field

Use `allowed-tools` to restrict Claude's tool access when a skill is active:

```yaml
---
name: safe-file-reader
description: Read files without making changes. Use when you need read-only file access.
allowed-tools: Read, Grep, Glob
---
```

When this skill is active, Claude can only use Read, Grep, Glob without asking permission.

### Skill Discovery

Skills are automatically discovered by Claude. To view available skills:
- Ask Claude: "What Skills are available?"
- Check filesystem: `ls ~/.claude/skills/` or `ls .claude/skills/`

### Testing Skills

Test skills by asking questions that match the description:
```
# If description mentions "PDF files":
> Can you help me extract text from this PDF?

# If description mentions "URDF":
> Show me the URDF structure for a mobile robot
```

Claude autonomously uses the skill if it matches the request.

### Skills vs. Slash Commands

| Feature | Skills | Slash Commands |
|---------|--------|----------------|
| Invocation | **Model-invoked** (Claude decides) | **User-invoked** (/command) |
| Discovery | Claude reads SKILL.md | User types /command |
| Format | Folder with SKILL.md | Single .md file |
| Location | `.claude/skills/` | `.claude/commands/` |

### Skill Best Practices

1. **Keep skills focused** - One capability per skill
2. **Write specific descriptions** - Include triggers and use cases
3. **Use progressive disclosure** - Put details in supporting files
4. **Limit tool access** - Use `allowed-tools` for read-only skills
5. **Version control** - Check project skills into git

### Example Skill (from documentation)

```yaml
---
name: pdf-processing
description: Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction. Requires pypdf and pdfplumber packages.
---

# PDF Processing

## Quick start

Extract text:
python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    text = pdf.pages[0].extract_text()

For form filling, see [FORMS.md](FORMS.md).
For detailed API reference, see [REFERENCE.md](REFERENCE.md).

## Requirements

Packages must be installed in your environment:
bash
pip install pypdf pdfplumber
```

---

## Implementation Decisions

### D1: Use Project-Level Subagents
**Decision**: Store subagents in `.claude/agents/` (project-level)
**Rationale**: Keeps agents versioned with the project, shareable via git
**Alternative Rejected**: User-level (~/.claude/agents/) - not project-specific

### D2: No Python/SDK Code
**Decision**: Implement as pure Markdown files
**Rationale**: Claude Code natively reads these files, no custom runtime needed
**Alternative Rejected**: OpenAI Agents SDK - wrong platform, Claude Code has built-in support

### D3: Explicit Tool Lists
**Decision**: Specify tools per subagent rather than inheriting all
**Rationale**: Reviewers shouldn't have Edit access; builders need Bash
**Trade-off**: More configuration, but better security/focus

### D4: Model Optimization
**Decision**: Use haiku for reviewers, sonnet for creators
**Rationale**: Reviewers do fast read-only analysis; creators need reasoning
**Trade-off**: Slight model inconsistency, but better cost/latency

### D5: Constitution in Prompts
**Decision**: Include constitution reading instruction in every subagent
**Rationale**: Ensures compliance without external validation
**Trade-off**: Longer prompts, but guaranteed alignment

### D6: Skills as Folders
**Decision**: Implement skills as folders with SKILL.md, not single files
**Rationale**: Allows bundling templates, scripts, and reference docs
**Alternative Rejected**: Single markdown files - can't include supporting files

### D7: Model-Invoked Skills
**Decision**: Let Claude autonomously decide when to use skills
**Rationale**: More seamless UX than requiring explicit invocation
**Trade-off**: Less user control, but reduces cognitive load

### D8: allowed-tools for Read-Only Skills
**Decision**: Use `allowed-tools: Read, Grep, Glob` for reference skills
**Rationale**: Prevents accidental modifications when using reference materials
**Trade-off**: Requires configuration per skill, but improves safety

---

## Example Subagent (from documentation)

```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is simple and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

---

## Resumable Subagents (Advanced)

Subagents can be resumed to continue previous conversations:
- Each execution gets unique `agentId`
- Transcript stored in `agent-{agentId}.jsonl`
- Resume with `resume` parameter

---

## Best Practices (from documentation)

1. **Start with Claude-generated agents** - Generate initial subagent with Claude, then customize
2. **Design focused subagents** - Single, clear responsibilities
3. **Write detailed prompts** - Specific instructions, examples, constraints
4. **Limit tool access** - Only grant necessary tools
5. **Version control** - Check project subagents into git

---

## References

- Claude Code Subagents Documentation: https://code.claude.com/docs/en/subagents
- Claude Code Skills Documentation: https://code.claude.com/docs/en/skills
- Agent Skills Overview: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- Agent Skills Best Practices: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
- Claude Code Settings: https://code.claude.com/docs/en/settings
- Claude Code Hooks: https://code.claude.com/docs/en/hooks
