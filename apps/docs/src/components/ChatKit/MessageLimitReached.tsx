/**
 * MessageLimitReached Component
 *
 * Displays an overlay/modal when anonymous user has reached the
 * 10 message limit. Prompts them to sign in to continue.
 *
 * Shows: "Message limit reached. Sign in to continue chatting
 * and save your conversation."
 */

import React from 'react';

// ============================================================================
// Types
// ============================================================================

export interface MessageLimitReachedProps {
  /** Callback when sign-in button is clicked */
  onSignInClick?: () => void;
  /** Whether to show the overlay */
  show: boolean;
}

// ============================================================================
// Component
// ============================================================================

export function MessageLimitReached({
  onSignInClick,
  show,
}: MessageLimitReachedProps): React.ReactElement | null {
  if (!show) {
    return null;
  }

  return (
    <div className="chatkit-limit-reached-overlay">
      <div className="chatkit-limit-reached-content">
        <div className="chatkit-limit-reached-icon">🔒</div>
        <h3 className="chatkit-limit-reached-title">Message Limit Reached</h3>
        <p className="chatkit-limit-reached-description">
          Sign in to continue chatting and save your conversation.
        </p>
        <button
          type="button"
          className="chatkit-limit-reached-button"
          onClick={onSignInClick}
        >
          Sign In to Continue
        </button>
        <p className="chatkit-limit-reached-note">
          Your previous messages will be saved when you sign in.
        </p>
      </div>
    </div>
  );
}

export default MessageLimitReached;
