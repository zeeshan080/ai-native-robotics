# Constitution Principles Summary

This document summarizes the key principles from `.specify/memory/constitution.md`.

## Core Principles

### III. Strict Technical Stack

**Allowed Technologies:**
- **Backend**: FastAPI (Python), Qdrant (vector DB)
- **Frontend**: Docusaurus 3.x, React, TypeScript
- **Auth**: BetterAuth
- **Chatbot**: CopilotKit/ChatKit
- **Robotics**: ROS 2 Humble, Gazebo, Isaac Sim, URDF/XACRO

**Prohibited:**
- No alternative frameworks without explicit approval
- No hardcoded secrets or tokens

### IV. Pedagogical Layers

| Layer | Name | Focus |
|-------|------|-------|
| L1 | Manual | Explain concepts without AI |
| L2 | Collaboration | AI-generated extensions after student understanding |
| L3 | Intelligence | Reusable templates, skills, and agents |
| L4 | Spec-Driven | Module integration, plan generation, validation |
| L5 | Full Autonomy | End-to-end AI-driven workflows |

### VII. Content Agents Specification

Content must:
- Include "Try With AI" as the final section
- Assign pedagogical layer
- Follow cognitive load guidelines
- Preserve technical terms in translations

### VIII. Software-Building Agents Specification

Code must:
- Follow strict tech stack
- Include error handling
- Use environment variables for secrets
- Follow spec-first development

### IX. Quality & Verification

All output must:
- Pass constitution compliance check
- Include layer assignments for pedagogical content
- Follow safety guidelines for robotics code
- Be validated before delivery
