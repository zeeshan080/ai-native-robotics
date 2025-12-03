/**
 * MessageLimitWarning Component
 *
 * Displays a warning banner when anonymous users are approaching
 * the message limit (< 4 messages remaining).
 *
 * Shows: "X messages remaining. Sign in to save your chat."
 */

import React from 'react';

// ============================================================================
// Types
// ============================================================================

export interface MessageLimitWarningProps {
  /** Number of messages remaining */
  remaining: number;
  /** Callback when sign-in link is clicked */
  onSignInClick?: () => void;
}

// ============================================================================
// Component
// ============================================================================

export function MessageLimitWarning({
  remaining,
  onSignInClick,
}: MessageLimitWarningProps): React.ReactElement | null {
  // Don't show if plenty of messages remaining
  if (remaining >= 4 || remaining <= 0) {
    return null;
  }

  return (
    <div className="chatkit-message-limit-warning">
      <span className="chatkit-warning-icon">⚠️</span>
      <span className="chatkit-warning-text">
        {remaining} {remaining === 1 ? 'message' : 'messages'} remaining.{' '}
        <button
          type="button"
          className="chatkit-warning-link"
          onClick={onSignInClick}
        >
          Sign in
        </button>
        {' '}to save your chat.
      </span>
    </div>
  );
}

export default MessageLimitWarning;
