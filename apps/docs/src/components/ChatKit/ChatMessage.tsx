import React from 'react';
import type { Message } from './types';

export interface ChatMessageProps {
  message: Message;
}

/**
 * ChatMessage Component
 *
 * Displays a single chat message with role-based styling.
 * Supports streaming indicators and error states.
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
            <span className="chatkit-message__cursor">|</span>
          </span>
        )}
      </div>

      {isError && (
        <div className="chatkit-message__error-badge">
          Error
        </div>
      )}
    </div>
  );
};

export default ChatMessage;
