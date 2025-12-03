# Agent Index — Physical AI & Humanoid Robotics Book Platform

This document provides a **complete index of all AI agents** used in the Physical AI & Humanoid Robotics Book Platform.  
These agents operate across four domains: **Book Generation, Development Automation, RAG Intelligence, and Personalization**.

---

## 1. Book Intelligence Agents (Spec‑Kit + Claude Code)

### ### 1.1 chapter-planner
Plans chapters based on course structure, learning outcomes, and prerequisite analysis.

### 1.2 content-implementer
Implements lessons, diagrams, exercises, and examples using validated teaching patterns.

### 1.3 pedagogical-designer
Ensures every lesson follows cognitive load rules, scaffolding, examples, and learning psychology.

### 1.4 validation-auditor
Validates clarity, correctness, and cohesion across lessons and chapters.

### 1.5 factual-verifier
Checks all facts using external trusted tools and reference agents.

---

## 2. Repo & Project Automation Agents

### 2.1 monorepo-architect
Creates/maintains the entire Docusaurus + Backend + Auth + Agents folder structure.

### 2.2 docusaurus-integrator
Handles pages, sidebars, docs folder structure, metadata, and build integrity.

### 2.3 betterauth-integrator
Manages BetterAuth configuration, routes, user schemas, and onboarding questions.

### 2.4 rag-backend-builder
Generates FastAPI endpoints, Qdrant schemas, Neon migrations, and tool calling.

### 2.5 deployment-orchestrator
Ensures GitHub Pages + backend deployment + environment setup.

---

## 3. RAG & Interactive Intelligence Agents

### 3.1 semantic-indexer
Indexes book content and user-selected text into Qdrant vectors.

### 3.2 retrieval-router
Routes queries to:
- full-book search  
- chapter search  
- inline-selected-text search  

### 3.3 agentic-chatbot
ChatKit/OpenAI Agents SDK orchestrator — responds using text + tool calls + RAG.

### 3.4 context-compressor
Shrinks context windows intelligently based on importance and recency.

---

## 4. Personalized Learning Agents

### 4.1 persona-builder
Builds student profiles from BetterAuth onboarding (hardware, software, experience).

### 4.2 content-adapter
Modifies chapters per-user:  
- Beginner mode  
- Intermediate mode  
- Advanced mode  
- Hardware‑specific instructions  
- Language switching (English ↔ Urdu)

### 4.3 chapter-translator
Translates chapters into Urdu with scientific accuracy.

---

## 5. Build & QA Agents

### 5.1 asset-validator
Checks diagrams, images, and code assets.

### 5.2 link-checker
Ensures all internal and external links work.

### 5.3 spec-consistency-bot
Ensures all chapters follow the constitution, teaching layers, and directory structure.

---

## End of Agent Index
