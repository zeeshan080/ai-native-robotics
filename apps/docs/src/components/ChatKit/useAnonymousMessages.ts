/**
 * useAnonymousMessages Hook
 *
 * Manages chat messages for anonymous (unauthenticated) users using localStorage.
 * Tracks message count and enforces the 10-message trial limit.
 *
 * Features:
 * - Persists messages to localStorage
 * - Tracks sent message count (user messages only)
 * - Provides warning when approaching limit (< 4 remaining)
 * - Blocks new messages when limit reached
 * - Exports messages for migration on sign-in
 */

import { useState, useEffect, useCallback, useMemo } from 'react';
import type { Message } from './types';

// Use Message type for ChatMessage (same shape)
type ChatMessage = Message;

// ============================================================================
// Constants
// ============================================================================

const STORAGE_KEY = 'chatkit-anonymous-messages';
const MESSAGE_LIMIT = 10;
const WARNING_THRESHOLD = 4; // Show warning when remaining < 4

// ============================================================================
// Types
// ============================================================================

export interface AnonymousMessagesState {
  /** All messages in the conversation */
  messages: ChatMessage[];
  /** Number of user messages sent (towards limit) */
  sentCount: number;
  /** Messages remaining before limit */
  remaining: number;
  /** Whether to show warning (remaining < WARNING_THRESHOLD) */
  showWarning: boolean;
  /** Whether limit has been reached */
  limitReached: boolean;
}

export interface UseAnonymousMessagesReturn extends AnonymousMessagesState {
  /** Add a message to the conversation */
  addMessage: (message: ChatMessage) => boolean;
  /** Clear all messages (after migration or manual clear) */
  clearMessages: () => void;
  /** Get messages for migration (returns copy) */
  getMessagesForMigration: () => ChatMessage[];
  /** Check if can send (not at limit) */
  canSend: boolean;
  /** Sync remaining count from backend rate limit headers */
  syncRemainingFromBackend: (remaining: number) => void;
  /** Mark limit as reached (when backend returns 429) */
  markLimitReached: () => void;
}

// ============================================================================
// Storage Helpers
// ============================================================================

interface StoredData {
  messages: ChatMessage[];
  sentCount: number;
}

function loadFromStorage(): StoredData {
  if (typeof window === 'undefined') {
    return { messages: [], sentCount: 0 };
  }

  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const data = JSON.parse(stored) as StoredData;
      // Validate structure
      if (Array.isArray(data.messages) && typeof data.sentCount === 'number') {
        return data;
      }
    }
  } catch {
    // Invalid data, return empty
  }

  return { messages: [], sentCount: 0 };
}

function saveToStorage(data: StoredData): void {
  if (typeof window === 'undefined') return;

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch {
    // Storage full or unavailable
    console.warn('Failed to save anonymous messages to localStorage');
  }
}

function clearStorage(): void {
  if (typeof window === 'undefined') return;

  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    // Ignore errors
  }
}

// ============================================================================
// Hook
// ============================================================================

export function useAnonymousMessages(): UseAnonymousMessagesReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sentCount, setSentCount] = useState(0);
  const [isLoaded, setIsLoaded] = useState(false);

  // Load from localStorage on mount
  useEffect(() => {
    const data = loadFromStorage();
    setMessages(data.messages);
    setSentCount(data.sentCount);
    setIsLoaded(true);
  }, []);

  // Save to localStorage when data changes (after initial load)
  useEffect(() => {
    if (!isLoaded) return;
    saveToStorage({ messages, sentCount });
  }, [messages, sentCount, isLoaded]);

  // Computed values
  const remaining = MESSAGE_LIMIT - sentCount;
  const showWarning = remaining > 0 && remaining < WARNING_THRESHOLD;
  const limitReached = remaining <= 0;
  const canSend = !limitReached;

  // Add a message
  const addMessage = useCallback((message: ChatMessage): boolean => {
    // If it's a user message and we're at limit, reject
    if (message.role === 'user' && limitReached) {
      return false;
    }

    setMessages(prev => [...prev, message]);

    // Only count user messages towards limit
    if (message.role === 'user') {
      setSentCount(prev => prev + 1);
    }

    return true;
  }, [limitReached]);

  // Clear all messages
  const clearMessages = useCallback(() => {
    setMessages([]);
    setSentCount(0);
    clearStorage();
  }, []);

  // Get messages for migration
  const getMessagesForMigration = useCallback((): ChatMessage[] => {
    return [...messages];
  }, [messages]);

  // Sync remaining count from backend (when backend returns rate limit headers)
  const syncRemainingFromBackend = useCallback((backendRemaining: number) => {
    // If backend says fewer messages remain than our local count,
    // sync to backend's count (user may have used limit from another device/browser)
    const backendSentCount = MESSAGE_LIMIT - backendRemaining;
    if (backendSentCount > sentCount) {
      setSentCount(backendSentCount);
    }
  }, [sentCount]);

  // Mark limit as reached (when backend returns 429)
  const markLimitReached = useCallback(() => {
    setSentCount(MESSAGE_LIMIT);
  }, []);

  // Memoize return value
  return useMemo(() => ({
    messages,
    sentCount,
    remaining,
    showWarning,
    limitReached,
    addMessage,
    clearMessages,
    getMessagesForMigration,
    canSend,
    syncRemainingFromBackend,
    markLimitReached,
  }), [
    messages,
    sentCount,
    remaining,
    showWarning,
    limitReached,
    addMessage,
    clearMessages,
    getMessagesForMigration,
    canSend,
    syncRemainingFromBackend,
    markLimitReached,
  ]);
}

export default useAnonymousMessages;
