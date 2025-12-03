import React, { useState, useEffect, useRef, useCallback } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { createAuthClient } from 'better-auth/client';
import ChatMessage from './ChatMessage';
import { useChatViewMode, getViewModeClassName, canShowDockButtons } from './ChatViewModeContext';
import { useThreads } from './useThreads';
import { useAnonymousMessages } from './useAnonymousMessages';
import MessageLimitWarning from './MessageLimitWarning';
import MessageLimitReached from './MessageLimitReached';
import ThreadSidebar from './ThreadSidebar';
import { useUser } from '../../context/UserContext';
import type { Message, ChatState, ChatRequest, ChatEvent, Thread, ChatMessage as ChatMessageType, HistoryMessage, Reference } from './types';

// BetterAuth client for session fetching
const AUTH_BASE_URL = typeof window !== 'undefined' && window.location.hostname !== 'localhost'
  ? 'https://ai-native-robotics.vercel.app'
  : 'http://localhost:3001';

const authClient = createAuthClient({
  baseURL: AUTH_BASE_URL,
  fetchOptions: { credentials: 'include' },
});

// Session hook for BetterAuth
type AuthUser = { id: string; email: string; name: string };

function useAuthSession() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchSession() {
      try {
        const session = await authClient.getSession();
        if (session.data?.user) {
          setUser({
            id: session.data.user.id,
            email: session.data.user.email,
            name: session.data.user.name || '',
          });
        }
      } catch (error) {
        console.error('Failed to fetch session:', error);
      } finally {
        setIsLoading(false);
      }
    }
    fetchSession();
  }, []);

  return { user, isLoading, isAuthenticated: !!user };
}

const MAX_INPUT_LENGTH = 2000;
const USER_ID_KEY = 'chatkit-user-id';
const CURRENT_THREAD_KEY = 'chatkit-current-thread-id';

// Auth redirect URL (environment-based)
const AUTH_URL = typeof window !== 'undefined' && window.location.hostname !== 'localhost'
  ? 'https://ai-native-robotics.vercel.app/onboarding'
  : '/onboarding';

/**
 * Get or create a persistent user ID from localStorage
 */
function getUserId(): string | null {
  if (typeof window === 'undefined') return null;

  let userId = localStorage.getItem(USER_ID_KEY);
  if (!userId) {
    userId = crypto.randomUUID();
    localStorage.setItem(USER_ID_KEY, userId);
  }
  return userId;
}

/**
 * Get current thread ID from localStorage
 */
function getCurrentThreadId(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(CURRENT_THREAD_KEY);
}

/**
 * Save current thread ID to localStorage
 */
function saveCurrentThreadId(threadId: string | null): void {
  if (typeof window === 'undefined') return;
  if (threadId) {
    localStorage.setItem(CURRENT_THREAD_KEY, threadId);
  } else {
    localStorage.removeItem(CURRENT_THREAD_KEY);
  }
}

/**
 * Convert thread items to Message format
 */
function threadItemsToMessages(thread: Thread): Message[] {
  return thread.items.map(item => ({
    id: item.id,
    role: item.role,
    content: item.content,
    timestamp: new Date(item.created_at),
    status: 'complete' as const,
  }));
}

/**
 * FloatingChatBar Component
 *
 * Bottom-center floating chat interface with:
 * - Multiple view modes: compact, fullpage, sidedock-left, sidedock-right
 * - Expandable panel for message history
 * - SSE streaming for real-time responses
 * - Keyboard shortcuts (Ctrl+I / Cmd+I to focus, Escape to minimize)
 * - Character counter and validation
 * - Anonymous user trial with 10 message limit (US5)
 * - Thread persistence for authenticated users (US6)
 */
export default function FloatingChatBar(): React.ReactElement {
  const { siteConfig } = useDocusaurusContext();
  const apiUrl = (siteConfig.customFields?.chatkitApiUrl as string) || 'http://localhost:8000';

  // Get auth state from UserContext (for preferences/onboarding)
  const { userId: localUserId, onboardingCompleted } = useUser();

  // Get BetterAuth session (for real authentication)
  const { user: authUser, isAuthenticated, isLoading: isAuthLoading } = useAuthSession();

  // Use BetterAuth user ID when authenticated, otherwise null
  const userId = isAuthenticated ? authUser?.id : null;

  // Get user's name from BetterAuth session for personalization
  const userName = authUser?.name || null;

  // View mode context
  const {
    mode,
    isOpen,
    isMounted,
    toggleOpen,
    minimize,
    expandFullpage,
    dockToSide,
    isFullpage,
    isSideDocked,
  } = useChatViewMode();

  // Thread persistence (only used when authenticated)
  const {
    currentThread,
    threads,
    createThread,
    loadThread,
    listThreads,
    deleteThread,
    addMessage: persistMessage,
    setCurrentThread,
    isLoading: isThreadLoading,
    error: threadError,
    nextCursor,
  } = useThreads(apiUrl, isAuthenticated ? userId : null);

  // Sidebar state
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  // Anonymous messages (only used when NOT authenticated)
  const {
    messages: anonymousMessages,
    sentCount,
    remaining: messagesRemaining,
    showWarning: showLimitWarning,
    limitReached,
    addMessage: addAnonymousMessage,
    clearMessages: clearAnonymousMessages,
    canSend: canSendAnonymous,
    syncRemainingFromBackend,
    markLimitReached,
  } = useAnonymousMessages();

  const [state, setState] = useState<Omit<ChatState, 'isOpen'>>({
    isLoading: false,
    messages: [],
    inputValue: '',
    error: null,
  });

  // Handle sign-in redirect
  const handleSignInClick = useCallback(() => {
    if (typeof window !== 'undefined') {
      window.location.href = AUTH_URL;
    }
  }, []);

  // Sidebar handlers
  const openSidebar = useCallback(() => {
    if (isAuthenticated) {
      setIsSidebarOpen(true);
      listThreads(true); // Refresh thread list when opening
    }
  }, [isAuthenticated, listThreads]);

  const closeSidebar = useCallback(() => {
    setIsSidebarOpen(false);
  }, []);

  const handleSelectThread = useCallback(async (thread: Thread) => {
    const loadedThread = await loadThread(thread.id);
    if (loadedThread) {
      const messages = threadItemsToMessages(loadedThread);
      setState(prev => ({ ...prev, messages }));
    }
  }, [loadThread]);

  const handleNewChatFromSidebar = useCallback(async () => {
    // Clear current messages and thread
    setState(prev => ({ ...prev, messages: [] }));
    setCurrentThread(null);
    saveCurrentThreadId(null);
  }, [setCurrentThread]);

  const handleLoadMoreThreads = useCallback(() => {
    listThreads(false); // Load next page
  }, [listThreads]);

  const handleDeleteThread = useCallback(async (threadId: string) => {
    const success = await deleteThread(threadId);
    if (success) {
      // If we deleted the current thread, clear messages
      if (currentThread?.id === threadId) {
        setState(prev => ({ ...prev, messages: [] }));
        saveCurrentThreadId(null);
      }
    }
  }, [deleteThread, currentThread]);

  // Track if initial thread load has been attempted
  const initialLoadRef = useRef(false);

  const inputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  // Load messages on mount only - either from localStorage (anonymous) or thread (authenticated)
  useEffect(() => {
    if (initialLoadRef.current) return;
    initialLoadRef.current = true;

    if (isAuthenticated && userId) {
      // Authenticated: load from thread
      const savedThreadId = getCurrentThreadId();
      if (savedThreadId) {
        loadThread(savedThreadId).then(thread => {
          if (thread) {
            const messages = threadItemsToMessages(thread);
            setState(prev => ({ ...prev, messages }));
          }
        });
      }
    } else if (anonymousMessages.length > 0) {
      // Anonymous: load initial messages from localStorage
      const converted: Message[] = anonymousMessages.map(msg => ({
        ...msg,
        timestamp: msg.timestamp instanceof Date ? msg.timestamp : new Date(msg.timestamp),
      }));
      setState(prev => ({ ...prev, messages: converted }));
    }
  }, [isAuthenticated, userId, loadThread]);
  // NOTE: Removed anonymousMessages from deps to prevent overwriting streaming state

  // Sync current thread ID to localStorage
  useEffect(() => {
    saveCurrentThreadId(currentThread?.id ?? null);
  }, [currentThread?.id]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [state.messages]);

  // Keyboard shortcut: Ctrl+I or Cmd+I to focus input
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'i') {
        e.preventDefault();
        inputRef.current?.focus();
        if (!isOpen) {
          toggleOpen();
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, toggleOpen]);

  // Escape key handler for fullpage mode (T064)
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isFullpage && isOpen) {
        minimize();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isFullpage, isOpen, minimize]);

  // Click-outside handler for fullpage mode (T063)
  useEffect(() => {
    if (!isFullpage || !isOpen) return;

    const handleClickOutside = (e: MouseEvent) => {
      if (panelRef.current && !panelRef.current.contains(e.target as Node)) {
        minimize();
      }
    };

    // Delay adding listener to avoid immediate trigger
    const timer = setTimeout(() => {
      document.addEventListener('mousedown', handleClickOutside);
    }, 100);

    return () => {
      clearTimeout(timer);
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isFullpage, isOpen, minimize]);

  // Listen for programmatic message sending (from SelectionTooltip)
  useEffect(() => {
    const handleSendEvent = (e: CustomEvent<{ message: string }>) => {
      const { message } = e.detail;
      if (message) {
        setState(prev => ({ ...prev, inputValue: message }));
        if (!isOpen) {
          toggleOpen();
        }
        // Trigger send after state update
        setTimeout(() => {
          const sendButton = document.querySelector('.chatkit-send-btn') as HTMLButtonElement;
          if (sendButton && !sendButton.disabled) {
            sendButton.click();
          }
        }, 50);
      }
    };

    window.addEventListener('chatkit:sendMessage', handleSendEvent as EventListener);
    return () => window.removeEventListener('chatkit:sendMessage', handleSendEvent as EventListener);
  }, [isOpen, toggleOpen]);

  /**
   * Send message and handle SSE streaming response
   */
  const handleSendMessage = useCallback(async () => {
    const trimmedInput = state.inputValue.trim();
    if (!trimmedInput || state.isLoading) return;

    // Check anonymous limit
    if (!isAuthenticated && !canSendAnonymous) {
      // Limit reached - don't send
      return;
    }

    // For authenticated users: ensure we have a thread
    let threadId: string | null = null;
    if (isAuthenticated && userId) {
      threadId = currentThread?.id ?? null;
      if (!threadId) {
        const newThread = await createThread();
        if (newThread) {
          threadId = newThread.id;
        }
      }
    }

    // Create user message
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: trimmedInput,
      timestamp: new Date(),
      status: 'complete',
    };

    // Create assistant message placeholder
    const assistantMessageId = crypto.randomUUID();
    const assistantMessage: Message = {
      id: assistantMessageId,
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      status: 'streaming',
    };

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage, assistantMessage],
      inputValue: '',
      isLoading: true,
      error: null,
    }));

    // Store message appropriately
    if (isAuthenticated && threadId) {
      // Authenticated: persist to thread
      persistMessage('user', trimmedInput).catch(err => {
        console.error('Failed to persist user message:', err);
      });
    } else if (!isAuthenticated) {
      // Anonymous: add to localStorage
      addAnonymousMessage(userMessage);
    }

    // Build conversation history from completed messages (exclude the current user message and streaming)
    const history: HistoryMessage[] = state.messages
      .filter(msg => msg.status === 'complete' && (msg.role === 'user' || msg.role === 'assistant'))
      .map(msg => ({
        role: msg.role as 'user' | 'assistant',
        content: msg.content,
      }));

    // Prepare request payload
    const request: ChatRequest = {
      type: 'user_message',
      message: {
        id: userMessage.id,
        content: trimmedInput,
      },
      history,
      context: {
        pageUrl: window.location.pathname,
        pageTitle: document.title,
        userName: userName || undefined, // Pass user's name for personalization
      },
    };

    // Create new abort controller for this request
    abortControllerRef.current = new AbortController();

    try {
      const response = await fetch(`${apiUrl}/chatkit/api`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
        signal: abortControllerRef.current.signal,
      });

      if (!response.ok) {
        // Handle rate limit exceeded (429)
        if (response.status === 429) {
          const errorData = await response.json();
          // Mark limit as reached in frontend state
          markLimitReached();
          throw new Error(errorData.message || 'Rate limit exceeded. Please sign in to continue.');
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Sync remaining count from backend rate limit headers
      const backendRemaining = response.headers.get('X-RateLimit-Remaining');
      if (backendRemaining !== null && !isAuthenticated) {
        syncRemainingFromBackend(parseInt(backendRemaining, 10));
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Response body is not readable');
      }

      let accumulatedContent = '';
      let accumulatedReferences: Reference[] = [];

      // Read SSE stream
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);

            // Skip keep-alive pings
            if (data === '[DONE]' || !data.trim()) continue;

            try {
              const event: ChatEvent = JSON.parse(data);

              if (event.type === 'text_delta' && event.content) {
                accumulatedContent += event.content;

                // Update streaming message
                setState(prev => ({
                  ...prev,
                  messages: prev.messages.map(msg =>
                    msg.id === assistantMessageId
                      ? { ...msg, content: accumulatedContent }
                      : msg
                  ),
                }));
              } else if (event.type === 'references' && event.references) {
                // Accumulate references from RAG
                accumulatedReferences = event.references;
              } else if (event.type === 'message_complete') {
                // Mark as complete with references
                const completedAssistantMessage: Message = {
                  id: assistantMessageId,
                  role: 'assistant',
                  content: accumulatedContent,
                  timestamp: new Date(),
                  status: 'complete',
                  references: accumulatedReferences.length > 0 ? accumulatedReferences : undefined,
                };

                setState(prev => ({
                  ...prev,
                  messages: prev.messages.map(msg =>
                    msg.id === assistantMessageId
                      ? { ...msg, status: 'complete', references: completedAssistantMessage.references }
                      : msg
                  ),
                  isLoading: false,
                }));

                // Store assistant message appropriately
                if (isAuthenticated && accumulatedContent) {
                  // Authenticated: persist to thread
                  persistMessage('assistant', accumulatedContent).catch(err => {
                    console.error('Failed to persist assistant message:', err);
                  });
                } else if (!isAuthenticated && accumulatedContent) {
                  // Anonymous: add to localStorage (doesn't count towards limit)
                  addAnonymousMessage(completedAssistantMessage);
                }
                break;
              } else if (event.type === 'error') {
                throw new Error(event.content || 'Unknown error occurred');
              }
            } catch (parseError) {
              console.error('Failed to parse SSE event:', parseError);
            }
          }
        }
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to send message';

      setState(prev => ({
        ...prev,
        messages: prev.messages.map(msg =>
          msg.id === assistantMessageId
            ? {
                ...msg,
                content: errorMessage,
                status: 'error',
                isError: true,
              }
            : msg
        ),
        error: errorMessage,
        isLoading: false,
      }));
    }
  }, [state.inputValue, state.isLoading, apiUrl, currentThread?.id, userId, createThread, persistMessage, isAuthenticated, canSendAnonymous, addAnonymousMessage, syncRemainingFromBackend, markLimitReached]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (value.length <= MAX_INPUT_LENGTH) {
      setState(prev => ({ ...prev, inputValue: value }));
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const startNewChat = useCallback(() => {
    // Cancel any ongoing request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    if (isAuthenticated) {
      // Authenticated: clear current thread
      setCurrentThread(null);
    } else {
      // Anonymous: clear localStorage messages
      clearAnonymousMessages();
    }

    // Reset to fresh state
    setState({
      isLoading: false,
      messages: [],
      inputValue: '',
      error: null,
    });
    inputRef.current?.focus();
  }, [isAuthenticated, setCurrentThread, clearAnonymousMessages]);

  const characterCount = state.inputValue.length;
  const isNearLimit = characterCount > MAX_INPUT_LENGTH * 0.9;
  const viewModeClass = getViewModeClassName(mode);
  const showDockButtons = canShowDockButtons();

  // Don't render until mounted (prevents hydration mismatch)
  if (!isMounted) {
    return null;
  }

  return (
    <div className={viewModeClass}>
      {/* Blurred backdrop for fullpage mode (T065) */}
      {isFullpage && isOpen && (
        <div className="chatkit-fullpage-backdrop" />
      )}

      {/* Expanded Chat Panel */}
      {isOpen && (
        <div className="chatkit-panel" ref={panelRef}>
          <div className="chatkit-panel__header">
            <h3 className="chatkit-panel__title">AI Robotics Tutor</h3>
            <div className="chatkit-panel__actions">
              {/* Mode toggle buttons (T062) */}
              <div className="chatkit-panel__mode-buttons">
                {/* Fullpage mode button - maximize icon with corner arrows */}
                <button
                  className={`chatkit-panel__mode-btn ${isFullpage ? 'chatkit-panel__mode-btn--active' : ''}`}
                  onClick={expandFullpage}
                  aria-label="Fullpage mode"
                  title="Fullpage"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    {/* Top-left corner */}
                    <polyline points="8,3 3,3 3,8" />
                    {/* Top-right corner */}
                    <polyline points="16,3 21,3 21,8" />
                    {/* Bottom-left corner */}
                    <polyline points="3,16 3,21 8,21" />
                    {/* Bottom-right corner */}
                    <polyline points="21,16 21,21 16,21" />
                  </svg>
                </button>

                {/* Dock left button (T066 - hidden on mobile) */}
                {showDockButtons && (
                  <button
                    className={`chatkit-panel__mode-btn chatkit-panel__mode-btn--dock ${mode === 'sidedock-left' ? 'chatkit-panel__mode-btn--active' : ''}`}
                    onClick={() => dockToSide('left')}
                    aria-label="Dock to left"
                    title="Dock left"
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <rect x="3" y="3" width="18" height="18" rx="2" />
                      <line x1="9" y1="3" x2="9" y2="21" />
                    </svg>
                  </button>
                )}

                {/* Dock right button (T066 - hidden on mobile) */}
                {showDockButtons && (
                  <button
                    className={`chatkit-panel__mode-btn chatkit-panel__mode-btn--dock ${mode === 'sidedock-right' ? 'chatkit-panel__mode-btn--active' : ''}`}
                    onClick={() => dockToSide('right')}
                    aria-label="Dock to right"
                    title="Dock right"
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <rect x="3" y="3" width="18" height="18" rx="2" />
                      <line x1="15" y1="3" x2="15" y2="21" />
                    </svg>
                  </button>
                )}
              </div>

              {/* History button (only for authenticated users) */}
              {isAuthenticated && (
                <button
                  className="chatkit-panel__btn chatkit-panel__btn--history"
                  onClick={openSidebar}
                  aria-label="Chat history"
                  title="Chat history"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 8v4l3 3" />
                    <circle cx="12" cy="12" r="9" />
                  </svg>
                </button>
              )}

              <button
                className="chatkit-panel__btn chatkit-panel__btn--new"
                onClick={startNewChat}
                aria-label="New chat"
                title="Start new chat"
              >
                +
              </button>
              <button
                className="chatkit-panel__btn chatkit-panel__btn--close"
                onClick={minimize}
                aria-label="Minimize chat"
                title="Minimize"
              >
                &times;
              </button>
            </div>
          </div>

          {/* Anonymous user warning banner (T081, T084) */}
          {!isAuthenticated && showLimitWarning && (
            <MessageLimitWarning
              remaining={messagesRemaining}
              onSignInClick={handleSignInClick}
            />
          )}

          <div className="chatkit-panel__messages">
            {isThreadLoading ? (
              <div className="chatkit-panel__loading">
                <span className="chatkit-spinner" />
                <p>Loading conversation...</p>
              </div>
            ) : state.messages.length === 0 ? (
              <div className="chatkit-panel__empty">
                <p>Hi! I'm your AI robotics tutor.</p>
                <p>Ask me anything about the lesson content!</p>
                {!isAuthenticated && (
                  <p style={{ fontSize: '11px', marginTop: '8px', opacity: 0.7 }}>
                    {messagesRemaining} free messages available
                  </p>
                )}
              </div>
            ) : (
              state.messages.map(message => (
                <ChatMessage key={message.id} message={message} />
              ))
            )}
            <div ref={messagesEndRef} />
          </div>

          {(state.error || threadError) && (
            <div className="chatkit-panel__error">
              {state.error || threadError}
            </div>
          )}

          {/* Anonymous user limit reached overlay (T082, T084) */}
          <MessageLimitReached
            show={!isAuthenticated && limitReached}
            onSignInClick={handleSignInClick}
          />

          {/* Input area in panel for fullpage/sidedock modes */}
          {(isFullpage || isSideDocked) && (
            <div className="chatkit-panel__input-area">
              <div className="chatkit-bar__container">
                <input
                  ref={inputRef}
                  type="text"
                  className="chatkit-input"
                  placeholder={limitReached && !isAuthenticated ? "Sign in to continue..." : "Ask a question... (Ctrl+I)"}
                  value={state.inputValue}
                  onChange={handleInputChange}
                  onKeyPress={handleKeyPress}
                  disabled={state.isLoading || (limitReached && !isAuthenticated)}
                  maxLength={MAX_INPUT_LENGTH}
                />

                <button
                  className="chatkit-send-btn"
                  onClick={handleSendMessage}
                  disabled={!state.inputValue.trim() || state.isLoading || (limitReached && !isAuthenticated)}
                  aria-label="Send message"
                >
                  {state.isLoading ? (
                    <span className="chatkit-spinner" />
                  ) : (
                    '\u2191'
                  )}
                </button>
              </div>

              {characterCount > 0 && (
                <div className={`chatkit-bar__counter ${isNearLimit ? 'chatkit-bar__counter--warning' : ''}`}>
                  {characterCount} / {MAX_INPUT_LENGTH}
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Floating Chat Bar (only in compact mode) */}
      {mode === 'compact' && (
        <div className="chatkit-bar">
          <div className="chatkit-bar__container">
            <input
              ref={!isOpen ? inputRef : undefined}
              type="text"
              className="chatkit-input"
              placeholder={limitReached && !isAuthenticated ? "Sign in to continue..." : "Ask a question... (Ctrl+I)"}
              value={state.inputValue}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              onFocus={() => {
                if (!isOpen) toggleOpen();
              }}
              disabled={state.isLoading || (limitReached && !isAuthenticated)}
              maxLength={MAX_INPUT_LENGTH}
            />

            <button
              className="chatkit-send-btn"
              onClick={handleSendMessage}
              disabled={!state.inputValue.trim() || state.isLoading || (limitReached && !isAuthenticated)}
              aria-label="Send message"
            >
              {state.isLoading ? (
                <span className="chatkit-spinner" />
              ) : (
                '\u2191'
              )}
            </button>

            {!isOpen && state.messages.length > 0 && (
              <button
                className="chatkit-expand-btn"
                onClick={toggleOpen}
                aria-label="Expand chat"
              >
                {state.messages.length}
              </button>
            )}
          </div>

          {characterCount > 0 && (
            <div className={`chatkit-bar__counter ${isNearLimit ? 'chatkit-bar__counter--warning' : ''}`}>
              {characterCount} / {MAX_INPUT_LENGTH}
            </div>
          )}
        </div>
      )}

      {/* Thread History Sidebar */}
      <ThreadSidebar
        isOpen={isSidebarOpen}
        onClose={closeSidebar}
        threads={threads}
        currentThreadId={currentThread?.id ?? null}
        onSelectThread={handleSelectThread}
        onDeleteThread={handleDeleteThread}
        onNewChat={handleNewChatFromSidebar}
        onLoadMore={handleLoadMoreThreads}
        hasMore={!!nextCursor}
        isLoading={isThreadLoading}
      />
    </div>
  );
}
