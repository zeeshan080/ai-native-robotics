/**
 * ChatKit Types
 *
 * Type definitions for the AI Robotics Tutor chat interface
 */

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  status: 'pending' | 'streaming' | 'complete' | 'error';
  isError?: boolean;
}

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
  type: 'text_delta' | 'message_complete' | 'error';
  content?: string;
  done: boolean;
  messageId?: string;
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
  context?: {
    pageUrl?: string;
    pageTitle?: string;
  };
}
