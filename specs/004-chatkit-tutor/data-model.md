# Data Model: ChatKit AI Robotics Tutor

**Feature**: 004-chatkit-tutor
**Date**: 2025-11-29
**Status**: Complete

## Overview

This document defines the data entities and their relationships for the ChatKit feature. Since the MVP uses session-based storage (no database persistence), entities exist only in memory during a browser session.

---

## Entities

### Message

A single chat message in a conversation.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | string | Unique identifier | UUID v4, required |
| `role` | enum | Message sender | "user" \| "assistant" \| "system" |
| `content` | string | Message text content | Max 10,000 chars |
| `timestamp` | datetime | When message was created | ISO 8601, UTC |
| `status` | enum | Message delivery status | "pending" \| "streaming" \| "complete" \| "error" |
| `isError` | boolean | Whether this is an error message | Default: false |

**Validation Rules**:
- `content` must not be empty for user messages
- `content` max length enforced on frontend (2000 chars input)
- `timestamp` auto-generated on creation

**State Transitions**:
```
User Message:    [pending] → [complete] or [error]
Assistant:       [streaming] → [complete] or [error]
```

---

### Conversation

A collection of messages forming a chat thread.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | string | Unique identifier | UUID v4, required |
| `messages` | Message[] | Ordered list of messages | Chronological order |
| `createdAt` | datetime | Conversation start time | ISO 8601, UTC |
| `lastMessageAt` | datetime | Most recent message time | ISO 8601, UTC |

**Validation Rules**:
- Conversations are session-scoped (cleared on page refresh)
- No limit on message count for MVP (may add later)

**Relationships**:
- Contains 0..n Messages (one-to-many)

---

### ChatEvent (Backend → Frontend)

Events sent from backend to frontend during streaming.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `type` | enum | Event type | "text_delta" \| "message_complete" \| "error" |
| `content` | string | Text content or error message | Optional for complete events |
| `done` | boolean | Whether stream is finished | Required |
| `messageId` | string | ID of the message being streamed | UUID v4 |

**Event Types**:

```typescript
// Text chunk during streaming
{ type: "text_delta", content: "Hello", done: false, messageId: "..." }

// Stream complete
{ type: "message_complete", done: true, messageId: "..." }

// Error occurred
{ type: "error", content: "Connection lost", done: true, messageId: "..." }
```

---

### ChatRequest (Frontend → Backend)

Request payload sent to the backend API.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `type` | string | Request type | Always "user_message" for MVP |
| `message` | object | Message payload | Required |
| `message.content` | string | User's question | Max 2000 chars, required |
| `message.id` | string | Client-generated ID | UUID v4, required |
| `context` | object | Optional context | See below |
| `context.pageUrl` | string | Current page URL | Optional, for context-awareness |
| `context.pageTitle` | string | Current page title | Optional |

**Example**:
```json
{
  "type": "user_message",
  "message": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "content": "What is bipedal locomotion?"
  },
  "context": {
    "pageUrl": "/docs/Physical-AI-Foundations/what-is-physical-ai/lesson-embodiment-hypothesis",
    "pageTitle": "The Embodiment Hypothesis"
  }
}
```

---

### SelectionAction (Frontend Only)

Represents a text selection action triggered by the user.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `type` | enum | Action type | "explain" \| "translate" \| "summarize" |
| `selectedText` | string | Text highlighted by user | Max 500 chars (truncated if longer) |
| `position` | object | Tooltip position | { x: number, y: number } |

**Selection Action Flow**:
```
User selects text → SelectionAction created → Tooltip shown at position
User clicks action → Message created with prefix → Sent to chat
```

**Message Prefixes by Action**:
| Action | Message Prefix |
|--------|---------------|
| explain | "Explain: [selected text]" |
| translate | "Translate to Urdu: [selected text]" |
| summarize | "Summarize: [selected text]" |

---

### TextSelection (Frontend State)

State for tracking current text selection.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `text` | string \| null | Currently selected text | Null when no selection |
| `rect` | DOMRect \| null | Bounding rectangle of selection | For tooltip positioning |
| `isVisible` | boolean | Whether tooltip should show | False when selection cleared |

---

## Frontend State Model (React)

```typescript
interface ChatState {
  isOpen: boolean;           // Panel expanded or minimized
  isLoading: boolean;        // Waiting for response
  messages: Message[];       // Conversation history
  inputValue: string;        // Current input text
  error: string | null;      // Error to display
}

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  status: 'pending' | 'streaming' | 'complete' | 'error';
  isError?: boolean;
}

// Text Selection State
interface SelectionState {
  text: string | null;       // Currently selected text
  rect: DOMRect | null;      // Position for tooltip
  isVisible: boolean;        // Whether to show tooltip
}

type SelectionActionType = 'explain' | 'translate' | 'summarize';

interface SelectionAction {
  type: SelectionActionType;
  selectedText: string;
  position: { x: number; y: number };
}
```

---

## Backend Models (Pydantic)

```python
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from uuid import UUID

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class MessageStatus(str, Enum):
    PENDING = "pending"
    STREAMING = "streaming"
    COMPLETE = "complete"
    ERROR = "error"

class EventType(str, Enum):
    TEXT_DELTA = "text_delta"
    MESSAGE_COMPLETE = "message_complete"
    ERROR = "error"

class MessageContent(BaseModel):
    id: UUID
    content: str = Field(..., max_length=2000)

class PageContext(BaseModel):
    pageUrl: str | None = None
    pageTitle: str | None = None

class ChatRequest(BaseModel):
    type: str = "user_message"
    message: MessageContent
    context: PageContext | None = None

class ChatEvent(BaseModel):
    type: EventType
    content: str | None = None
    done: bool
    messageId: UUID | None = None
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Browser)                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │  ChatState   │────│   Message    │────│   Message    │  │
│   │  (React)     │    │   (user)     │    │ (assistant)  │  │
│   └──────────────┘    └──────────────┘    └──────────────┘  │
│          │                                                   │
│          │ ChatRequest                                       │
│          ▼                                                   │
└──────────────────────────────────────────────────────────────┘
                              │
                              │ POST /chatkit/api
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │ ChatRequest  │───▶│   Agent      │───▶│  ChatEvent   │  │
│   │  (Pydantic)  │    │   Runner     │    │  (stream)    │  │
│   └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                  │           │
│                                                  │ SSE       │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │  ChatEvent   │
                    │  (stream)    │
                    └──────────────┘
```

---

## Storage Strategy

### MVP (Hackathon)
- **Frontend**: React state (in-memory)
- **Backend**: Stateless (no conversation persistence)
- Conversations cleared on page refresh

### Future Enhancement
- **Frontend**: LocalStorage for draft messages
- **Backend**: PostgreSQL for conversation history
- User authentication via BetterAuth
- Conversation retrieval by user ID

---

## Validation Summary

| Entity | Validation Location | Rules |
|--------|---------------------|-------|
| Message.content | Frontend | Max 2000 chars, non-empty |
| Message.id | Frontend | Valid UUID v4 |
| ChatRequest | Backend (Pydantic) | Type, message required |
| ChatEvent | Backend | Type enum validation |
