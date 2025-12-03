/**
 * ChatKit Types
 *
 * Type definitions for the AI Robotics Tutor chat interface
 */

/**
 * Reference to textbook content from RAG
 */
export interface Reference {
  title: string;
  url: string;
  location?: string;
  content_type?: string;
  score?: number;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  status: 'pending' | 'streaming' | 'complete' | 'error';
  isError?: boolean;
  references?: Reference[];
}

/**
 * Alias for Message used in anonymous messages storage
 * (serializable to/from localStorage)
 */
export type ChatMessage = Message;

export interface ChatState {
  isOpen: boolean;           // Panel expanded or minimized
  isLoading: boolean;        // Waiting for response
  messages: Message[];       // Conversation history
  inputValue: string;        // Current input text
  error: string | null;      // Error to display
}

export interface SelectionState {
  text: string | null;       // Currently selected text
  rect: DOMRect | null;      // Position for tooltip
  isVisible: boolean;        // Whether to show tooltip
}

export type SelectionActionType = 'explain' | 'translate' | 'summarize';

export interface SelectionAction {
  type: SelectionActionType;
  selectedText: string;
  position: { x: number; y: number };
}

/**
 * SSE Event from backend
 */
export interface ChatEvent {
  type: 'text_delta' | 'message_complete' | 'references' | 'error';
  content?: string;
  done: boolean;
  messageId?: string;
  references?: Reference[];
}

/**
 * History message for conversation context
 */
export interface HistoryMessage {
  role: 'user' | 'assistant';
  content: string;
}

/**
 * Request payload sent to backend
 */
export interface ChatRequest {
  type: string;
  message: {
    id: string;
    content: string;
  };
  history?: HistoryMessage[];
  context?: {
    pageUrl?: string;
    pageTitle?: string;
    userName?: string;
    user_id?: string; // BetterAuth user ID for authenticated users
  };
}

/**
 * Thread types for persistent conversations
 */
export interface ThreadItem {
  id: string;
  thread_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface Thread {
  id: string;
  user_id: string;
  title: string | null;
  metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
  items: ThreadItem[];
}

export interface ThreadListResponse {
  threads: Thread[];
  next_cursor: string | null;
}

export interface CreateThreadRequest {
  user_id: string;
  title?: string;
  metadata?: Record<string, unknown>;
}

export interface AddMessageRequest {
  role: 'user' | 'assistant' | 'system';
  content: string;
  metadata?: Record<string, unknown>;
}
