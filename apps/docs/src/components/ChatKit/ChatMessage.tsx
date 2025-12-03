import React from 'react';
import type { Message, Reference } from './types';

export interface ChatMessageProps {
  message: Message;
}

/**
 * Render references as clickable links
 */
const ReferenceLinks: React.FC<{ references: Reference[] }> = ({ references }) => {
  if (!references || references.length === 0) return null;

  return (
    <div className="chatkit-message__references">
      <div className="chatkit-message__references-header">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
        </svg>
        <span>Sources</span>
      </div>
      <div className="chatkit-message__references-list">
        {references.map((ref, idx) => (
          <a
            key={idx}
            href={ref.url}
            className="chatkit-message__reference-link"
            title={ref.location || ref.title}
          >
            {ref.title}
          </a>
        ))}
      </div>
    </div>
  );
};

/**
 * ChatMessage Component
 *
 * Displays a single chat message with role-based styling.
 * Supports streaming indicators, error states, and reference links.
 */
const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const isStreaming = message.status === 'streaming';
  const isError = message.isError || message.status === 'error';

  return (
    <div className={`chatkit-message chatkit-message--${message.role}`}>
      <div className="chatkit-message__header">
        <span className="chatkit-message__role">
          {isUser ? 'You' : 'AI Tutor'}
        </span>
        <span className="chatkit-message__timestamp">
          {message.timestamp.toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
          })}
        </span>
      </div>

      <div className={`chatkit-message__content ${isError ? 'chatkit-message__content--error' : ''}`}>
        {message.content}

        {isStreaming && (
          <span className="chatkit-message__streaming-indicator">
            <span className="chatkit-wave-dots">
              <span className="chatkit-wave-dot"></span>
              <span className="chatkit-wave-dot"></span>
              <span className="chatkit-wave-dot"></span>
            </span>
          </span>
        )}
      </div>

      {/* Display references for assistant messages */}
      {!isUser && message.references && message.references.length > 0 && (
        <ReferenceLinks references={message.references} />
      )}

      {isError && (
        <div className="chatkit-message__error-badge">
          Error
        </div>
      )}
    </div>
  );
};

export default ChatMessage;
