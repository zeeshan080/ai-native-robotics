# Student Language Examples

## Good vs Bad Examples

### Internal Labels

**BAD** (exposes internal labels):
> "This is an L2 lesson that builds on L1 concepts."

**GOOD** (student-friendly):
> "This lesson builds on what you learned in the previous chapter. Now we'll explore how AI can help extend your understanding."

---

### Technical Jargon

**BAD** (unexplained jargon):
> "The URDF defines the kinematic chain through joint-link relationships."

**GOOD** (with analogy):
> "A URDF file describes how a robot is built, like a blueprint. It shows how each part (link) connects to other parts through joints - similar to how your arm bone connects to your shoulder through a joint that lets it rotate."

---

### Instructions

**BAD** (passive, formal):
> "The following procedure should be executed to configure the environment."

**GOOD** (active, friendly):
> "Let's set up your workspace! Follow these steps to get your environment ready."

---

### Encouragement

**BAD** (condescending):
> "Even beginners can understand this simple concept."

**GOOD** (encouraging):
> "This concept might seem complex at first, but by the end of this section, you'll have a clear understanding."

---

### Error Messages

**BAD** (technical, unhelpful):
> "RuntimeError: Node initialization failed due to parameter mismatch."

**GOOD** (student-friendly):
> "Oops! The robot node couldn't start because some settings don't match. Let's check that your configuration file has the correct values."

---

## Language by Layer

### L1 (Manual) Language
- Simple, foundational terms
- Lots of analogies
- Step-by-step instructions
- No AI terminology yet

### L2 (Collaboration) Language
- Introduce AI as a helper
- Compare manual vs AI approaches
- Explain when AI helps and when it doesn't

### L3 (Intelligence) Language
- Templates and patterns terminology
- Reusability concepts
- Building blocks metaphors

### L4 (Spec-Driven) Language
- Specifications and requirements
- Generation and validation terms
- Integration vocabulary

### L5 (Autonomy) Language
- Orchestration and automation
- Agent terminology (with explanation)
- Professional workflow language

---

## Checklist for Content Review

- [ ] No internal labels (L1, L2, etc.) visible to students
- [ ] Technical terms are explained on first use
- [ ] At least one analogy for abstract concepts
- [ ] Active voice for instructions
- [ ] Encouraging tone throughout
- [ ] Error scenarios have helpful guidance
