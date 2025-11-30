# Research: ChatKit AI Robotics Tutor

**Feature**: 004-chatkit-tutor
**Date**: 2025-11-29
**Status**: Complete

## Research Tasks

This document consolidates research findings for technical decisions in the ChatKit implementation.

---

## R1: OpenAI Agents SDK Integration with ChatKit

**Question**: How to properly integrate OpenAI Agents SDK with ChatKit for streaming responses?

**Decision**: Use `Runner.run_streamed()` with `stream_agent_response()` helper

**Rationale**:
- `run_streamed()` returns an async generator, perfect for SSE
- `stream_agent_response()` converts agent events to ChatKit-compatible format
- Avoid `Runner.run_sync()` which blocks and can't stream

**Implementation Pattern**:
```python
from agents import Agent, Runner
from openai_chatkit.streaming import stream_agent_response

async def respond(self, input_text: str):
    result = Runner.run_streamed(self.agent, input=input_text)
    async for event in stream_agent_response(context, result):
        yield event
```

**Alternatives Considered**:
- `Runner.run_sync()` - rejected, can't stream
- Direct OpenAI `stream=True` - rejected, doesn't use Agents SDK features

---

## R2: LLM Provider Factory Pattern

**Question**: Best approach for switching between OpenAI and Gemini?

**Decision**: Factory function reading environment variable at startup

**Rationale**:
- Gemini supports OpenAI-compatible API via `generativelanguage.googleapis.com/v1beta/openai/`
- Single `create_model()` function handles both providers
- No code changes needed to switch providers

**Implementation Pattern**:
```python
def create_model():
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "gemini":
        client = AsyncOpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        return OpenAIChatCompletionsModel(
            model=os.getenv("GEMINI_DEFAULT_MODEL", "gemini-2.0-flash"),
            openai_client=client
        )

    # Default: OpenAI
    return OpenAIChatCompletionsModel(
        model=os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o-mini"),
        openai_client=AsyncOpenAI()
    )
```

**Alternatives Considered**:
- Runtime provider selection via API parameter - rejected, adds complexity
- Separate agent classes per provider - rejected, code duplication

---

## R3: Docusaurus Custom Component Injection

**Question**: How to inject ChatKit into all Docusaurus pages?

**Decision**: Swizzle the Root component using `@theme/Root`

**Rationale**:
- Root component wraps entire app
- Custom Root can include ChatKit provider and floating component
- Works with both CSR and SSR

**Implementation Pattern**:
```tsx
// src/theme/Root.tsx
import React from 'react';
import { FloatingChatBar } from '@site/src/components/ChatKit';

export default function Root({ children }) {
  return (
    <>
      {children}
      <FloatingChatBar />
    </>
  );
}
```

**Alternatives Considered**:
- Docusaurus plugin - rejected, more complex for this use case
- Manual import on each page - rejected, maintenance burden
- Layout wrapper - rejected, doesn't cover all page types

---

## R4: SSE Streaming Implementation

**Question**: Best approach for streaming AI responses to browser?

**Decision**: Server-Sent Events (SSE) via `sse-starlette`

**Rationale**:
- Native browser support via `EventSource`
- Simpler than WebSockets for unidirectional streaming
- Works well with FastAPI async generators

**Implementation Pattern**:
```python
# Backend
from sse_starlette.sse import EventSourceResponse

@app.post("/chatkit/api")
async def chatkit_api(request: Request):
    event = await request.json()
    return EventSourceResponse(handle_event_stream(event))
```

```typescript
// Frontend
const eventSource = new EventSource('/chatkit/api', {
  method: 'POST',
  body: JSON.stringify({ message: userMessage })
});
eventSource.onmessage = (e) => appendToChat(e.data);
```

**Alternatives Considered**:
- WebSockets - rejected, bidirectional not needed, more complex
- Long polling - rejected, poor UX, inefficient
- Fetch with ReadableStream - considered as fallback

---

## R5: Robotics Tutor Agent Instructions

**Question**: What instructions should the AI tutor agent have?

**Decision**: Educational, curriculum-aware instructions focused on Physical AI & Robotics

**Rationale**:
- Agent should stay on topic (robotics, Physical AI, ROS 2, etc.)
- Should be helpful but redirect off-topic questions
- Should use student-friendly language per constitution

**Implementation**:
```python
TUTOR_INSTRUCTIONS = """
You are a friendly AI tutor for the AI-Native Physical AI & Humanoid Robotics Textbook.

Your expertise covers:
- Physical AI and embodied intelligence concepts
- Robot sensors (LIDAR, cameras, IMUs) and actuators
- Humanoid robot design and bipedal locomotion
- ROS 2, Gazebo, and NVIDIA Isaac Sim
- Vision-Language-Action (VLA) systems

Guidelines:
- Use clear, educational language appropriate for students
- Provide examples and analogies to explain complex concepts
- If asked about unrelated topics, politely redirect to robotics
- Encourage exploration and curiosity
- Reference concepts from the textbook when relevant
- Keep responses concise but informative (2-4 paragraphs typical)

You are helping students learn, not doing their homework for them.
Encourage understanding over memorization.
"""
```

**Alternatives Considered**:
- Generic assistant - rejected, loses educational focus
- Multiple specialized agents - deferred for future enhancement
- RAG-augmented agent - deferred, requires vector DB setup

---

## R6: Error Handling Strategy

**Question**: How to handle errors gracefully in the chat flow?

**Decision**: Layered error handling with user-friendly messages

**Rationale**:
- Users should never see raw error traces
- Errors should be actionable (suggest retry, check connection)
- Backend errors should be logged for debugging

**Implementation**:
```python
# Backend
async def handle_event(event: dict) -> AsyncIterator[dict]:
    try:
        async for chunk in process_message(event):
            yield chunk
    except Exception as e:
        logger.error(f"Chat error: {e}")
        yield {
            "type": "error",
            "content": "Sorry, I encountered an error. Please try again.",
            "done": True
        }
```

```typescript
// Frontend
if (response.type === 'error') {
  setMessages(prev => [...prev, {
    role: 'system',
    content: response.content,
    isError: true
  }]);
}
```

**Alternatives Considered**:
- Expose full error details - rejected, security risk
- Silent failures - rejected, poor UX

---

## Summary

All research questions resolved. No NEEDS CLARIFICATION items remain.

| Topic | Decision | Status |
|-------|----------|--------|
| Agents SDK Integration | `run_streamed()` + `stream_agent_response()` | ✅ Resolved |
| Provider Factory | Environment-based factory function | ✅ Resolved |
| Docusaurus Injection | Swizzle Root component | ✅ Resolved |
| Streaming Protocol | SSE via sse-starlette | ✅ Resolved |
| Tutor Instructions | Educational, curriculum-aware | ✅ Resolved |
| Error Handling | Layered with user-friendly messages | ✅ Resolved |
