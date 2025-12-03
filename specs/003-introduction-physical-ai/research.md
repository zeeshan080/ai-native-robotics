# Research: Introduction to Physical AI

**Feature**: 003-introduction-physical-ai
**Date**: 2025-11-29
**Purpose**: Resolve unknowns and document research for Phase 0

## Research Summary

This feature is **educational content creation**, not software development. The research focuses on:
1. Lesson structure patterns for Layer 1 conceptual content
2. "Try With AI" pattern implementation
3. Diagram requirements and creation approach
4. Docusaurus MDX file structure for lessons

---

## Research Item 1: Lesson Structure for Layer 1 Content

### Question
What is the optimal structure for conceptual lessons that build mental models without code?

### Decision
Each lesson follows this structure:
1. **Introduction** - Hook with real-world relevance
2. **Core Concepts** - 2-3 main ideas with analogies
3. **Visual Aids** - Diagrams, illustrations, comparisons
4. **Reflection Questions** - 2-3 questions for self-assessment
5. **Try With AI** - 5-part interactive pattern

### Rationale
- Constitution mandates "Try With AI" as final section
- FR-002 requires: Concept explanation → Analogies/diagrams → Reflection questions → Try With AI
- Layer 1 prohibits heavy code, so emphasis on visual/conceptual learning

### Alternatives Considered
- **Video-first approach**: Rejected (out of scope for initial release)
- **Interactive simulations**: Rejected (requires Layer 2+ complexity)
- **Quiz-based assessment**: Partially included via Reflection Questions

---

## Research Item 2: "Try With AI" Pattern Implementation

### Question
How should the 5-part "Try With AI" pattern be structured in lesson markdown?

### Decision
Use a consistent MDX component or markdown structure:

```markdown
## Try With AI

### Initial Request
> Copy this prompt to your AI assistant:
> "[Specific prompt related to lesson topic]"

### Critical Evaluation
Before accepting the AI's response, check:
- [ ] Does it match what we learned about [concept]?
- [ ] Are there any claims that seem incorrect?
- [ ] What's missing from the explanation?

### Focused Update
Pick ONE thing to improve. Try this follow-up:
> "[Specific follow-up prompt]"

### Second Iteration
Tell the AI what happened:
> "The explanation was [good/confusing] because [reason]. Can you [specific request]?"

### Reflection
- Which part of the AI's response was most helpful?
- What did you learn by questioning the AI?
- How does this connect to [lesson concept]?
```

### Rationale
- Constitution Section VI defines the 5-part pattern explicitly
- Consistent structure allows students to build the habit
- Checkboxes enable self-assessment

### Alternatives Considered
- **Single prompt only**: Rejected (misses learning iteration)
- **Free-form AI chat**: Rejected (no structure for critical evaluation)

---

## Research Item 3: Diagram Requirements

### Question
What diagrams are needed and how should they be created?

### Decision
Required diagrams per spec FR-006:
1. **Robot morphology diagram** - Humanoid body with labeled parts
2. **Sensor placement diagram** - Robot with sensors annotated
3. **Embodied intelligence concept** - Comparison of digital vs physical AI

Creation approach:
- Static SVG or PNG images
- Placed in `/apps/docs/static/img/introduction/`
- Referenced in MDX with standard image syntax
- Alt text for accessibility

### Rationale
- FR-006 mandates visual diagrams for these three concepts
- SVG preferred for scalability and accessibility
- Static images work without additional dependencies

### Alternatives Considered
- **Mermaid diagrams**: Good for flowcharts but limited for robot illustrations
- **Interactive 3D models**: Too complex for Layer 1
- **ASCII art**: Not suitable for complex robot diagrams

---

## Research Item 4: Docusaurus File Structure

### Question
How should lessons be organized in the Docusaurus docs folder?

### Decision
```
apps/docs/docs/
├── course-overview/
│   └── index.md
├── 01-introduction-to-physical-ai/       # Module folder
│   ├── index.md                          # Module overview
│   ├── 01-what-is-physical-ai.md         # Lesson 1
│   ├── 02-embodied-intelligence.md       # Lesson 2
│   ├── 03-robot-sensors.md               # Lesson 3
│   ├── 04-humanoid-landscape.md          # Lesson 4
│   └── 05-transition-check.md            # Module assessment
└── 02-ros2-fundamentals/                 # Next module (future)
```

### Rationale
- Numbered prefixes ensure consistent ordering
- Module folder groups related lessons
- index.md provides module overview and navigation
- Matches Docusaurus sidebar auto-generation patterns

### Alternatives Considered
- **Flat structure**: Rejected (doesn't scale as modules grow)
- **Deep nesting (part/chapter/lesson)**: Rejected (too complex for 4 lessons)

---

## Research Item 5: Urdu Translation Approach

### Question
How should Urdu translations be structured in the codebase?

### Decision
For initial release, Urdu translations will be:
- Separate files with `-ur` suffix: `01-what-is-physical-ai-ur.md`
- OR use Docusaurus i18n plugin with `/ur/` locale folder
- Technical terms (ROS 2, LIDAR, IMU, etc.) remain in English per constitution

Implementation deferred to post-MVP. English-only for initial content creation.

### Rationale
- FR-007 requires Urdu translatability, not immediate translation
- Constitution Section VI specifies "technical terms in English"
- i18n plugin is standard Docusaurus approach

### Alternatives Considered
- **Inline bilingual content**: Rejected (clutters reading experience)
- **Auto-translation**: Rejected (loses technical accuracy)

---

## Research Item 6: Hardware Requirements Presentation

### Question
How should hardware requirements be presented in Layer 1 content?

### Decision
- Mention hardware requirements in course-overview (already done)
- In Lesson 4 (Humanoid Landscape), briefly reference hardware tiers
- Explicitly state: "Weeks 1-2 require only a web browser"
- Link to full hardware guide for interested students

### Rationale
- FR-009 requires hardware mention but clarification that none needed for Weeks 1-2
- Constitution Section IV defines hardware constraints
- Don't overwhelm students with hardware before they understand concepts

### Alternatives Considered
- **Detailed hardware section per lesson**: Rejected (irrelevant for conceptual content)
- **No hardware mention**: Rejected (violates FR-009)

---

## Unknowns Resolved

| Unknown | Resolution |
|---------|------------|
| Lesson structure | 5-part structure with Try With AI ending |
| Diagram creation | Static SVG/PNG in `/static/img/` |
| File organization | Numbered module folder with numbered lessons |
| Urdu translation | Deferred; use i18n plugin when ready |
| Hardware presentation | Brief mention, clarify not needed for Weeks 1-2 |

---

## Dependencies Confirmed

| Dependency | Status | Notes |
|------------|--------|-------|
| Docusaurus site | Ready | `apps/docs/` running |
| Static images folder | Ready | `apps/docs/static/img/` exists |
| Sidebar configuration | Ready | `sidebars.ts` can be updated |
| Constitution | Ready | Layer 1 rules clear |
| Curriculum | Ready | Weeks 1-2 topics defined |

---

## Next Steps

1. Create `data-model.md` defining lesson/module entities
2. Create `quickstart.md` for content authors
3. Update `plan.md` with technical decisions
4. Proceed to `/sp.tasks` for implementation tasks
