/**
 * useThreads Hook
 *
 * Manages thread persistence for authenticated users.
 * Provides methods to create threads, add messages, and list threads.
 *
 * Usage:
 *   const { currentThread, createThread, addMessage, loadThread, listThreads } = useThreads(apiUrl, userId);
 */

import { useState, useCallback, useRef } from 'react';
import type {
  Thread,
  ThreadItem,
  ThreadListResponse,
  CreateThreadRequest,
  AddMessageRequest,
} from './types';

interface UseThreadsState {
  currentThread: Thread | null;
  threads: Thread[];
  isLoading: boolean;
  error: string | null;
  nextCursor: string | null;
}

interface UseThreadsReturn extends UseThreadsState {
  createThread: (title?: string) => Promise<Thread | null>;
  loadThread: (threadId: string) => Promise<Thread | null>;
  addMessage: (role: 'user' | 'assistant' | 'system', content: string) => Promise<ThreadItem | null>;
  listThreads: (reset?: boolean) => Promise<void>;
  deleteThread: (threadId: string) => Promise<boolean>;
  setCurrentThread: (thread: Thread | null) => void;
  clearError: () => void;
}

/**
 * Hook for managing thread persistence
 *
 * @param apiUrl - Base URL for the ChatKit API
 * @param userId - User ID for thread ownership (null for anonymous users)
 * @returns Thread management functions and state
 */
export function useThreads(apiUrl: string, userId: string | null): UseThreadsReturn {
  const [state, setState] = useState<UseThreadsState>({
    currentThread: null,
    threads: [],
    isLoading: false,
    error: null,
    nextCursor: null,
  });

  // Track if thread operations should be enabled
  const isEnabled = Boolean(userId);

  // Ref to track current thread ID to avoid stale closures
  const currentThreadIdRef = useRef<string | null>(null);

  /**
   * Create a new thread
   */
  const createThread = useCallback(async (title?: string): Promise<Thread | null> => {
    if (!isEnabled || !userId) {
      console.log('Thread creation skipped: user not authenticated');
      return null;
    }

    setState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const request: CreateThreadRequest = {
        user_id: userId,
        title,
      };

      const response = await fetch(`${apiUrl}/api/threads`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`Failed to create thread: ${response.status}`);
      }

      const thread: Thread = await response.json();

      setState(prev => ({
        ...prev,
        currentThread: thread,
        threads: [thread, ...prev.threads],
        isLoading: false,
      }));

      currentThreadIdRef.current = thread.id;
      return thread;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to create thread';
      setState(prev => ({ ...prev, error: message, isLoading: false }));
      return null;
    }
  }, [apiUrl, userId, isEnabled]);

  /**
   * Load a thread with its messages
   */
  const loadThread = useCallback(async (threadId: string): Promise<Thread | null> => {
    if (!isEnabled || !userId) {
      return null;
    }

    setState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await fetch(
        `${apiUrl}/api/threads/${threadId}?user_id=${encodeURIComponent(userId)}`,
        { method: 'GET' }
      );

      if (!response.ok) {
        if (response.status === 404) {
          // Thread not found, clear current thread
          setState(prev => ({
            ...prev,
            currentThread: null,
            isLoading: false,
          }));
          currentThreadIdRef.current = null;
          return null;
        }
        throw new Error(`Failed to load thread: ${response.status}`);
      }

      const thread: Thread = await response.json();

      setState(prev => ({
        ...prev,
        currentThread: thread,
        isLoading: false,
      }));

      currentThreadIdRef.current = thread.id;
      return thread;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to load thread';
      setState(prev => ({ ...prev, error: message, isLoading: false }));
      return null;
    }
  }, [apiUrl, userId, isEnabled]);

  /**
   * Add a message to the current thread
   */
  const addMessage = useCallback(async (
    role: 'user' | 'assistant' | 'system',
    content: string
  ): Promise<ThreadItem | null> => {
    if (!isEnabled || !userId) {
      return null;
    }

    const threadId = currentThreadIdRef.current;
    if (!threadId) {
      console.log('No current thread, message not persisted');
      return null;
    }

    try {
      const request: AddMessageRequest = {
        role,
        content,
      };

      const response = await fetch(
        `${apiUrl}/api/threads/${threadId}/messages?user_id=${encodeURIComponent(userId)}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(request),
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to add message: ${response.status}`);
      }

      const item: ThreadItem = await response.json();

      // Update current thread with new message
      setState(prev => {
        if (!prev.currentThread || prev.currentThread.id !== threadId) {
          return prev;
        }
        return {
          ...prev,
          currentThread: {
            ...prev.currentThread,
            items: [...prev.currentThread.items, item],
          },
        };
      });

      return item;
    } catch (error) {
      console.error('Failed to persist message:', error);
      // Don't set error state - message persistence failures shouldn't block UI
      return null;
    }
  }, [apiUrl, userId, isEnabled]);

  /**
   * List threads for the current user
   */
  const listThreads = useCallback(async (reset: boolean = false): Promise<void> => {
    if (!isEnabled || !userId) {
      return;
    }

    setState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const cursor = reset ? null : state.nextCursor;
      let url = `${apiUrl}/api/threads?user_id=${encodeURIComponent(userId)}&limit=20`;
      if (cursor) {
        url += `&cursor=${encodeURIComponent(cursor)}`;
      }

      const response = await fetch(url, { method: 'GET' });

      if (!response.ok) {
        throw new Error(`Failed to list threads: ${response.status}`);
      }

      const data: ThreadListResponse = await response.json();

      setState(prev => ({
        ...prev,
        threads: reset ? data.threads : [...prev.threads, ...data.threads],
        nextCursor: data.next_cursor,
        isLoading: false,
      }));
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to list threads';
      setState(prev => ({ ...prev, error: message, isLoading: false }));
    }
  }, [apiUrl, userId, isEnabled, state.nextCursor]);

  /**
   * Delete a thread
   */
  const deleteThread = useCallback(async (threadId: string): Promise<boolean> => {
    if (!isEnabled || !userId) {
      return false;
    }

    setState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const response = await fetch(
        `${apiUrl}/api/threads/${threadId}?user_id=${encodeURIComponent(userId)}`,
        { method: 'DELETE' }
      );

      if (!response.ok && response.status !== 204) {
        throw new Error(`Failed to delete thread: ${response.status}`);
      }

      // Remove from threads list and clear current if it was selected
      setState(prev => ({
        ...prev,
        threads: prev.threads.filter(t => t.id !== threadId),
        currentThread: prev.currentThread?.id === threadId ? null : prev.currentThread,
        isLoading: false,
      }));

      if (currentThreadIdRef.current === threadId) {
        currentThreadIdRef.current = null;
      }

      return true;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to delete thread';
      setState(prev => ({ ...prev, error: message, isLoading: false }));
      return false;
    }
  }, [apiUrl, userId, isEnabled]);

  /**
   * Set the current thread directly
   */
  const setCurrentThread = useCallback((thread: Thread | null) => {
    setState(prev => ({ ...prev, currentThread: thread }));
    currentThreadIdRef.current = thread?.id ?? null;
  }, []);

  /**
   * Clear any error
   */
  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }));
  }, []);

  return {
    ...state,
    createThread,
    loadThread,
    addMessage,
    listThreads,
    deleteThread,
    setCurrentThread,
    clearError,
  };
}

export default useThreads;
