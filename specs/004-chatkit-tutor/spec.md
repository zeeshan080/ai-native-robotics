# Feature Specification: ChatKit AI Robotics Tutor

**Feature Branch**: `004-chatkit-tutor`
**Created**: 2025-11-29
**Status**: Draft
**Input**: User description: "Implement ChatKit floating chat interface with AI robotics tutor using OpenAI Agents SDK. Floating bottom-center design like Claude Code Docs. Factory pattern for OpenAI/Gemini switching. No user auth for hackathon demo. Text selection actions (explain, translate, summarize) that send to chat."

## Overview

This feature adds an AI-powered chat assistant to the AI-Native Robotics Textbook documentation site. Students can ask questions about robotics concepts, get clarification on lessons, and receive personalized guidance while learning. The chat interface appears as a floating input bar at the bottom-center of the screen, providing contextual help without disrupting the reading experience.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask a Question While Reading (Priority: P1)

A student is reading a lesson about bipedal locomotion and encounters a concept they don't understand. Without leaving the page, they type a question into the floating chat bar and receive an immediate, contextual answer from the AI tutor.

**Why this priority**: This is the core value proposition - enabling real-time Q&A during learning. Without this, the feature has no purpose.

**Independent Test**: Can be fully tested by opening any lesson page, typing a robotics question in the chat bar, and receiving a relevant response within seconds.

**Acceptance Scenarios**:

1. **Given** I am on any lesson page, **When** I click the chat input bar, **Then** I can type my question and the input is focused
2. **Given** I have typed a question, **When** I press Enter or click send, **Then** I see a loading indicator followed by an AI response
3. **Given** the AI responds, **When** I read the response, **Then** it is relevant to robotics and educational in tone
4. **Given** I receive a response, **When** I want to ask a follow-up, **Then** I can continue the conversation in the same thread

---

### User Story 2 - Expand Chat for Full Conversation (Priority: P2)

A student has multiple questions and wants to see the full conversation history. They expand the chat from the minimal input bar to a larger chat panel to review previous messages and continue the discussion.

**Why this priority**: Enables deeper engagement beyond single Q&A. Important for complex topics requiring back-and-forth dialogue.

**Independent Test**: Can be tested by asking 2-3 questions, expanding the chat panel, and verifying all messages are visible and scrollable.

**Acceptance Scenarios**:

1. **Given** I have an ongoing conversation, **When** I click to expand the chat, **Then** a larger panel opens showing full conversation history
2. **Given** the chat panel is expanded, **When** I scroll, **Then** I can see all previous messages in order
3. **Given** the chat panel is expanded, **When** I click to minimize, **Then** it returns to the compact input bar

---

### User Story 3 - Get Context-Aware Help (Priority: P3)

The AI tutor is aware of which lesson the student is currently reading and can provide answers that reference the current topic, suggest related lessons, or explain how concepts connect to the broader curriculum.

**Why this priority**: Enhances learning by connecting questions to the curriculum structure. Valuable but not essential for MVP.

**Independent Test**: Can be tested by asking "What am I learning about?" on different lesson pages and verifying the AI correctly identifies the current topic.

**Acceptance Scenarios**:

1. **Given** I am on the "Embodiment Hypothesis" lesson, **When** I ask "What is this lesson about?", **Then** the AI responds with accurate information about embodiment in robotics
2. **Given** I ask about a concept from a different lesson, **When** the AI responds, **Then** it may suggest I visit the relevant lesson for more details

---

### User Story 4 - Text Selection Actions (Priority: P2)

A student is reading a lesson and encounters a technical term or complex paragraph they want to understand better. They highlight the text, and a floating tooltip appears with three options: "Explain", "Translate", and "Summarize". Clicking any option automatically opens the chat and sends the selected text with the chosen action.

**Why this priority**: Enables seamless interaction without manual copy-paste. Critical for engagement and learning flow. Same priority as US2 since both enhance core chat experience.

**Independent Test**: Can be tested by highlighting any text on a lesson page, verifying tooltip appears with 3 buttons, clicking "Explain", and verifying chat opens with the selected text and receives an explanation.

**Acceptance Scenarios**:

1. **Given** I am on any lesson page, **When** I highlight text (select with mouse or touch), **Then** a floating tooltip appears near the selection with "Explain", "Translate", "Summarize" buttons
2. **Given** the tooltip is visible, **When** I click "Explain", **Then** the chat opens/expands and shows "Explain: [selected text]" as my message
3. **Given** the tooltip is visible, **When** I click "Translate", **Then** the chat opens and shows "Translate to Urdu: [selected text]" as my message
4. **Given** the tooltip is visible, **When** I click "Summarize", **Then** the chat opens and shows "Summarize: [selected text]" as my message
5. **Given** I sent a selection action, **When** the AI responds, **Then** it performs the requested action (explanation, translation, or summary) on the selected text
6. **Given** the tooltip is visible, **When** I click elsewhere or clear selection, **Then** the tooltip disappears

---

### Edge Cases

- What happens when the backend service is unavailable? → Display friendly error message and suggest trying again
- How does the system handle very long messages? → Truncate input at 2000 characters with visible counter
- What happens when multiple messages are sent rapidly? → Queue messages and process in order, show pending indicator
- How does the chat handle non-robotics questions? → AI politely redirects to robotics topics while remaining helpful
- What happens on mobile devices with limited screen space? → Chat bar remains at bottom, panel uses full-screen overlay when expanded
- What happens when user selects very long text? → Truncate to 500 characters with "[...truncated]" indicator
- What happens when user selects text inside code blocks? → Tooltip still appears, works the same way
- What happens when tooltip would appear off-screen? → Position tooltip to stay within viewport bounds
- What happens on touch devices? → Show tooltip on long-press selection completion

## Requirements *(mandatory)*

### Functional Requirements

**Chat Interface**
- **FR-001**: System MUST display a floating chat input bar at the bottom-center of all documentation pages
- **FR-002**: Chat input bar MUST contain a text input field with placeholder text "Ask a question..."
- **FR-003**: Chat input bar MUST include a send button (icon or text)
- **FR-004**: System MUST support keyboard shortcut (Ctrl+I / Cmd+I) to focus the chat input
- **FR-005**: Chat panel MUST expand to show full conversation when user clicks expand control

**AI Responses**
- **FR-006**: System MUST send user messages to the backend AI service and display responses
- **FR-007**: System MUST show a loading indicator while waiting for AI response
- **FR-008**: AI responses MUST stream progressively (word-by-word or chunk-by-chunk) for better UX
- **FR-009**: System MUST maintain conversation history within a single page session

**Backend Service**
- **FR-010**: Backend MUST expose an endpoint that accepts chat messages and returns AI responses
- **FR-011**: Backend MUST support switching between AI providers without frontend changes
- **FR-012**: Backend MUST handle errors gracefully and return appropriate error messages
- **FR-013**: Backend MUST not require user authentication (open access for hackathon demo)

**Error Handling**
- **FR-014**: System MUST display user-friendly error messages when the backend is unavailable
- **FR-015**: System MUST allow retry of failed messages

**Text Selection Actions**
- **FR-016**: System MUST detect text selection on documentation pages
- **FR-017**: System MUST display a floating tooltip near selected text with "Explain", "Translate", "Summarize" buttons
- **FR-018**: Tooltip MUST position itself to remain within viewport bounds
- **FR-019**: Clicking an action button MUST open/expand the chat and send the selected text with the action prefix
- **FR-020**: System MUST truncate selected text longer than 500 characters with "[...truncated]" indicator
- **FR-021**: Tooltip MUST disappear when selection is cleared or user clicks elsewhere
- **FR-022**: Backend MUST recognize action prefixes (Explain:, Translate to Urdu:, Summarize:) and respond appropriately

### Key Entities

- **Message**: A single chat message with content, sender (user/assistant), timestamp, and status (pending/sent/error)
- **Conversation**: A collection of messages in chronological order, associated with a browser session
- **AI Provider**: Configuration for which AI service to use (OpenAI or Gemini), switchable via environment variable
- **SelectionAction**: An action triggered by text selection with type (explain/translate/summarize), selected text, and source location

## Assumptions

1. **No persistence required**: Conversations are session-based and cleared on page refresh. Persistent history is out of scope for hackathon.
2. **Single AI agent**: One general-purpose robotics tutor agent handles all questions. Specialized agents (per topic) are out of scope.
3. **No file uploads**: Users cannot upload images or files to the chat. Text-only interaction.
4. **No authentication**: Anyone visiting the site can use the chat. Rate limiting may be added later but is not required for hackathon.
5. **English only**: AI responses are in English. Multi-language support is out of scope.
6. **Desktop-first**: Mobile support should work but is not the primary design target for hackathon.

## Out of Scope

- User accounts and authentication
- Persistent conversation history across sessions
- File/image uploads
- Voice input/output
- Multi-language support
- Analytics and usage tracking
- Rate limiting
- Custom AI personalities or avatars

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can send a message and receive an AI response within 5 seconds on average
- **SC-002**: Chat interface is visible and functional on 100% of documentation pages
- **SC-003**: AI responses are relevant to robotics topics at least 90% of the time (manual evaluation)
- **SC-004**: Users can complete a 3-message conversation without errors
- **SC-005**: System recovers gracefully from backend errors, displaying helpful error message within 2 seconds
- **SC-006**: Chat interface does not obstruct lesson content when minimized
- **SC-007**: Keyboard shortcut (Ctrl+I / Cmd+I) focuses chat input within 100ms
- **SC-008**: Text selection tooltip appears within 200ms of completing a selection
- **SC-009**: Clicking a selection action opens chat and sends message within 300ms
- **SC-010**: AI correctly performs the requested action (explain/translate/summarize) 90% of the time
