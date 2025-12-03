
# Project Architecture — Physical AI & Humanoid Robotics AI‑Native Textbook Platform

## 1. Introduction

The **Physical AI & Humanoid Robotics AI‑Native Textbook Platform** is a fully integrated, AI‑augmented learning system that combines a static Docusaurus book with dynamic AI agents, personalized content delivery, authentication, and an embedded RAG chatbot. The goal is to create a next‑generation educational platform where textbooks are interactive, intelligent, and user‑adaptive.

This document describes the **complete architectural blueprint** used across the project, covering frontend, backend, storage, authentication, agents, RAG systems, and operational layers.

---

## 2. High‑Level System Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│                 Docusaurus Static Frontend                   │
│   - Chapters, Lessons, Images                                │
│   - Sidebar + Search + Theming                               │
│   - "Personalize Content" + "Translate to Urdu" + Chatbot    │
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│                     FRONTEND INTELLIGENCE                    │
│     (Agents SDK + ChatKit + Client‑Side Query Layer)         │
│   - Streaming AI responses                                    │
│   - Tool calls (search, fetch, summaries)                     │
│   - Chapter‑specific RAG context fetch                        │
└───────────────────────────────┬──────────────────────────────┘
                                │ HTTP / WebSockets
                                ▼
┌──────────────────────────────────────────────────────────────┐
│                        API BACKEND (FastAPI)                  │
│   - RAG Endpoint: embed → store → query                       │
│   - Chatbot Endpoint: orchestrates Agents SDK                 │
│   - Auth Endpoint: BetterAuth signup/signin                   │
│   - Personalization Engine                                    │
│   - User Preference + History Storage                         │
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│                           DATA LAYER                          │
│   Neon Serverless PostgreSQL                                  │
│   - users, profiles, settings                                 │
│   - saved answers, history                                    │
│   - personalization preferences                                │
│                                                                │
│   Qdrant Cloud                                                 │
│   - embeddings for chapters, lessons, images                   │
│   - vector search for RAG                                      │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Frontend Architecture (Docusaurus)

### 3.1 Technology Stack
- **Docusaurus 3+**
- **React Server Components where possible**
- **TypeScript**
- **Tailwind optional**
- **ChatKit / Agents SDK**
- **BetterAuth client**

### 3.2 Folder Structure

```
book-source/
 ├── docs/
 │    ├── 01-Introducing-AI-Driven-Development/
 │    ├── ...
 │    └── 84-physical-ai-humanoid-robotics/
 ├── static/
 │    ├── images/
 │    ├── slides/
 │    └── audio/
 ├── src/
 │    ├── components/
 │    ├── theme/
 │    └── chatbot/
 └── docusaurus.config.js
```

### 3.3 Key Features

#### ✓ **AI‑Powered Chatbot Panel**
A floating chatbot panel where users can:
- Ask questions about the book
- Select text → ask questions → get answers only about that section
- See citations/snippets

#### ✓ **Personalization**
Buttons at the top of each chapter:
- “**Personalize content**” → re‑write chapter for user background  
- “**Translate to Urdu**” → on‑demand chapter rewrite

#### ✓ **Auth‑Aware Rendering**
If user is logged in:
- Show progress tracking
- Save chapter preferences  
- Provide custom difficulty levels

---

## 4. Backend Architecture (FastAPI)

The backend provides four categories of services:

### 4.1 Authentication Service (BetterAuth)

Features:
- Email/password signup/signin
- Collect user background (education, programming level, hardware)
- Issue JWT / session-based tokens
- Middleware for secured endpoints

### 4.2 RAG Service

#### Pipeline:
1. Extract chapter content  
2. Generate embeddings  
3. Store in Qdrant  
4. Query using cosine similarity  
5. Feed retrieved context to Agents SDK

#### Endpoints:
```
POST /embed
POST /query
POST /rag-answer
```

### 4.3 Chatbot Engine (Agents SDK + Orchestrator)

- Uses **OpenAI Agents SDK**  
- Server acts as **tool provider**, not LLM host  
- Tools exposed:
  - `search_book_text`
  - `fetch_chapter`
  - `personalize_chapter`
  - `translate_chapter`
  - `get_related_lessons`

### 4.4 Personalization Engine

- Stores user background in Neon  
- Adjusts:
  - Difficulty  
  - Vocabulary  
  - Examples (hardware/software relevant)  
  - Robotics-level (Beginner → Advanced)

---

## 5. Storage Architecture

The platform uses PanaversityFS‑style logical design, simplified for single‑book usage.

### 5.1 Content Storage (Local or Cloud)

```
content/
 ├── parts/
 ├── chapters/
 └── lessons/
```

### 5.2 Static Assets Storage

```
static/
 ├── images/
 ├── diagrams/
 ├── animations/
 └── 3d-models/
```

### 5.3 Database Layout (Neon Postgres)

```
users
profiles
preferences
query_history
chapter_progress
auth_sessions
```

### 5.4 Vector Storage (Qdrant)

Collections:
- `chapters`
- `lessons`
- `summaries`
- `images` (optional multimodal embeddings)

---

## 6. Agents Architecture

### 6.1 Agent Categories

#### **1. Content Agents**
- generate lessons
- rewrite chapters
- convert content to student level

#### **2. Pedagogy Agents**
- enforce teaching methodology  
- check prerequisites  
- verify learning objectives

#### **3. Technical Agents**
- handle RAG tools  
- search, retrieve, embed

#### **4. Monorepo / Code Agents**
- manage project scaffold  
- maintain Docusaurus structure  
- manage FastAPI backend skeleton  
- maintain consistent TS/Python formatting  

### 6.2 Agent Interaction Pattern

```
User → Frontend → Agents SDK → Tools → Backend → Qdrant → Backend → Agents SDK → User
```

---

## 7. RAG Pipeline (Detailed)

### 7.1 Embedding Flow

```
Chapter Markdown → Clean → Chunk → Embed → Qdrant (vector + metadata)
```

### 7.2 Query Flow

```
User Query → Embed → Qdrant similarity search → 
Top-K passages → Agents SDK → Answer with citations
```

### 7.3 Selected Text Flow

```
User selects text → send exact snippet → no RAG search → direct answer
```

---

## 8. Auth + Personalization Flow

### 8.1 Signup Flow

1. User enters email + password  
2. System asks:
   - Education level  
   - Programming experience  
   - Robotics experience  
   - Hardware they own  
3. Store all in Neon  
4. Use for personalization

### 8.2 Personalize Chapter

```
Chapter Markdown + User Profile → AI Personalizer → Rewritten chapter
```

### 8.3 Urdu Translation Flow

```
Chapter Markdown → Urdu Translator Agent → Urdu output
```

---

## 9. Deployment Architecture

### 9.1 Frontend (Docusaurus)

- GitHub Pages  
- Cloudflare Pages optional  
- CI builds static site  

### 9.2 Backend (FastAPI)

- Vercel serverless functions  
- Railway  
- Render  
- Fly.io  

### 9.3 Databases

- Neon (serverless Postgres)
- Qdrant Cloud Free Tier

---

## 10. Non‑Functional Requirements

| Category | Requirement |
|----------|-------------|
| **Scalability** | 10–1000 users |
| **Performance** | RAG < 1.2s average |
| **Security** | JWT + BetterAuth |
| **Cost** | Free-tier + minimal |
| **Consistency** | All chapters follow same pedagogy |
| **Portability** | Local or cloud deployment |

---

## 11. Future Extensions

### □ Add voice-based chatbot  
### □ Add robotics simulations  
### □ Add multimodal RAG (images + diagrams)  
### □ Add motion planning tool examples  
### □ Add AR overlays for robotics content  

---

## 12. Summary

This architecture transforms a static textbook into a **fully agentic, AI-native, interactive learning system** combining:
- AI agents  
- RAG search  
- personalized content  
- translations  
- authentication  
- cloud database  
- vector search  

It is future-proof, modular, and fully aligned with modern AI-native learning platforms.

