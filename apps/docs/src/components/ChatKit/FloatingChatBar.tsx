import React, { useState, useEffect, useRef, useCallback } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import ChatMessage from './ChatMessage';
import type { Message, ChatState, ChatRequest, ChatEvent } from './types';

const MAX_INPUT_LENGTH = 2000;

/**
 * FloatingChatBar Component
 *
 * Bottom-center floating chat interface with:
 * - Expandable panel for message history
 * - SSE streaming for real-time responses
 * - Keyboard shortcuts (Ctrl+I / Cmd+I to focus)
 * - Character counter and validation
 */
export default function FloatingChatBar(): React.ReactElement {
  const { siteConfig } = useDocusaurusContext();
  const apiUrl = (siteConfig.customFields?.chatkitApiUrl as string) || 'http://localhost:8000';

  const [state, setState] = useState<ChatState>({
    isOpen: false,
    isLoading: false,
    messages: [],
    inputValue: '',
    error: null,
  });

  const inputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

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
        setState(prev => ({ ...prev, isOpen: true }));
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Listen for programmatic message sending (from SelectionTooltip)
  useEffect(() => {
    const handleSendEvent = (e: CustomEvent<{ message: string }>) => {
      const { message } = e.detail;
      if (message) {
        setState(prev => ({ ...prev, inputValue: message, isOpen: true }));
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
  }, []);

  /**
   * Send message and handle SSE streaming response
   */
  const handleSendMessage = useCallback(async () => {
    const trimmedInput = state.inputValue.trim();
    if (!trimmedInput || state.isLoading) return;

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

    // Prepare request payload
    const request: ChatRequest = {
      type: 'user_message',
      message: {
        id: userMessage.id,
        content: trimmedInput,
      },
      context: {
        pageUrl: window.location.pathname,
        pageTitle: document.title,
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
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Response body is not readable');
      }

      let accumulatedContent = '';

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
              } else if (event.type === 'message_complete') {
                // Mark as complete
                setState(prev => ({
                  ...prev,
                  messages: prev.messages.map(msg =>
                    msg.id === assistantMessageId
                      ? { ...msg, status: 'complete' }
                      : msg
                  ),
                  isLoading: false,
                }));
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
  }, [state.inputValue, state.isLoading, apiUrl]);

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

  const togglePanel = () => {
    setState(prev => ({ ...prev, isOpen: !prev.isOpen }));
  };

  const startNewChat = () => {
    // Cancel any ongoing request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    // Reset to fresh state
    setState({
      isOpen: true,
      isLoading: false,
      messages: [],
      inputValue: '',
      error: null,
    });
    inputRef.current?.focus();
  };

  const characterCount = state.inputValue.length;
  const isNearLimit = characterCount > MAX_INPUT_LENGTH * 0.9;

  return (
    <>
      {/* Expanded Chat Panel */}
      {state.isOpen && (
        <div className="chatkit-panel">
          <div className="chatkit-panel__header">
            <h3 className="chatkit-panel__title">AI Robotics Tutor</h3>
            <div className="chatkit-panel__actions">
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
                onClick={togglePanel}
                aria-label="Minimize chat"
                title="Minimize"
              >
                ×
              </button>
            </div>
          </div>

          <div className="chatkit-panel__messages">
            {state.messages.length === 0 ? (
              <div className="chatkit-panel__empty">
                <p>👋 Hi! I'm your AI robotics tutor.</p>
                <p>Ask me anything about the lesson content!</p>
              </div>
            ) : (
              state.messages.map(message => (
                <ChatMessage key={message.id} message={message} />
              ))
            )}
            <div ref={messagesEndRef} />
          </div>

          {state.error && (
            <div className="chatkit-panel__error">
              {state.error}
            </div>
          )}
        </div>
      )}

      {/* Floating Chat Bar */}
      <div className="chatkit-bar">
        <div className="chatkit-bar__container">
          <input
            ref={inputRef}
            type="text"
            className="chatkit-input"
            placeholder="Ask a question... (Ctrl+I)"
            value={state.inputValue}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            onFocus={() => setState(prev => ({ ...prev, isOpen: true }))}
            disabled={state.isLoading}
            maxLength={MAX_INPUT_LENGTH}
          />

          <button
            className="chatkit-send-btn"
            onClick={handleSendMessage}
            disabled={!state.inputValue.trim() || state.isLoading}
            aria-label="Send message"
          >
            {state.isLoading ? (
              <span className="chatkit-spinner" />
            ) : (
              '↑'
            )}
          </button>

          {!state.isOpen && state.messages.length > 0 && (
            <button
              className="chatkit-expand-btn"
              onClick={togglePanel}
              aria-label="Expand chat"
            >
              💬 {state.messages.length}
            </button>
          )}
        </div>

        {characterCount > 0 && (
          <div className={`chatkit-bar__counter ${isNearLimit ? 'chatkit-bar__counter--warning' : ''}`}>
            {characterCount} / {MAX_INPUT_LENGTH}
          </div>
        )}
      </div>
    </>
  );
}
