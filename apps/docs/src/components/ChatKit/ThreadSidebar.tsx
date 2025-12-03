/**
 * ThreadSidebar Component
 *
 * Collapsible sidebar showing chat history threads (like ChatGPT).
 * Hidden by default, toggle to show, select thread, auto-hides.
 */

import React, { useEffect, useState } from 'react';
import type { Thread } from './types';

/**
 * Confirmation Dialog Component
 */
interface ConfirmDialogProps {
  isOpen: boolean;
  title: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm: () => void;
  onCancel: () => void;
}

function ConfirmDialog({
  isOpen,
  title,
  message,
  confirmLabel = 'Delete',
  cancelLabel = 'Cancel',
  onConfirm,
  onCancel,
}: ConfirmDialogProps): React.ReactElement | null {
  // Close on escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onCancel();
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onCancel]);

  if (!isOpen) return null;

  return (
    <div className="chatkit-confirm-backdrop" onClick={onCancel}>
      <div
        className="chatkit-confirm-dialog"
        onClick={(e) => e.stopPropagation()}
        role="alertdialog"
        aria-labelledby="confirm-title"
        aria-describedby="confirm-message"
      >
        <h4 id="confirm-title" className="chatkit-confirm-title">{title}</h4>
        <p id="confirm-message" className="chatkit-confirm-message">{message}</p>
        <div className="chatkit-confirm-actions">
          <button
            className="chatkit-confirm-btn chatkit-confirm-btn--cancel"
            onClick={onCancel}
          >
            {cancelLabel}
          </button>
          <button
            className="chatkit-confirm-btn chatkit-confirm-btn--confirm"
            onClick={onConfirm}
            autoFocus
          >
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}

interface ThreadSidebarProps {
  isOpen: boolean;
  onClose: () => void;
  threads: Thread[];
  currentThreadId: string | null;
  onSelectThread: (thread: Thread) => void;
  onDeleteThread: (threadId: string) => void;
  onNewChat: () => void;
  onLoadMore: () => void;
  hasMore: boolean;
  isLoading: boolean;
}

/**
 * Format relative time (e.g., "2 hours ago", "Yesterday")
 */
function formatRelativeTime(dateStr: string): string {
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays}d ago`;
  return date.toLocaleDateString();
}

/**
 * Truncate text with ellipsis
 */
function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength - 3) + '...';
}

export default function ThreadSidebar({
  isOpen,
  onClose,
  threads,
  currentThreadId,
  onSelectThread,
  onDeleteThread,
  onNewChat,
  onLoadMore,
  hasMore,
  isLoading,
}: ThreadSidebarProps): React.ReactElement | null {
  // State for delete confirmation dialog
  const [deleteThreadId, setDeleteThreadId] = useState<string | null>(null);

  // Close on escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen && !deleteThreadId) {
        onClose();
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose, deleteThreadId]);

  // Handle thread selection
  const handleSelect = (thread: Thread) => {
    onSelectThread(thread);
    onClose(); // Auto-hide after selection
  };

  // Handle new chat
  const handleNewChat = () => {
    onNewChat();
    onClose(); // Auto-hide after creating new chat
  };

  // Handle thread deletion - show confirmation dialog
  const handleDeleteClick = (e: React.MouseEvent, threadId: string) => {
    e.stopPropagation(); // Prevent thread selection
    setDeleteThreadId(threadId);
  };

  // Confirm deletion
  const confirmDelete = () => {
    if (deleteThreadId) {
      onDeleteThread(deleteThreadId);
      setDeleteThreadId(null);
    }
  };

  // Cancel deletion
  const cancelDelete = () => {
    setDeleteThreadId(null);
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="chatkit-sidebar-backdrop"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Sidebar panel */}
      <div className="chatkit-sidebar" role="dialog" aria-label="Chat History">
        {/* Header */}
        <div className="chatkit-sidebar-header">
          <h3>Chat History</h3>
          <button
            className="chatkit-sidebar-close"
            onClick={onClose}
            aria-label="Close sidebar"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M18 6L6 18M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* New Chat button */}
        <button
          className="chatkit-sidebar-new-chat"
          onClick={handleNewChat}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 5v14M5 12h14" />
          </svg>
          New Chat
        </button>

        {/* Thread list */}
        <div className="chatkit-sidebar-threads">
          {threads.length === 0 && !isLoading && (
            <div className="chatkit-sidebar-empty">
              No previous conversations
            </div>
          )}

          {threads.map((thread) => (
            <div
              key={thread.id}
              className={`chatkit-sidebar-thread ${thread.id === currentThreadId ? 'active' : ''}`}
            >
              <button
                className="chatkit-sidebar-thread-content"
                onClick={() => handleSelect(thread)}
              >
                <div className="chatkit-sidebar-thread-title">
                  {truncate(thread.title || 'Untitled conversation', 30)}
                </div>
                <div className="chatkit-sidebar-thread-time">
                  {formatRelativeTime(thread.updated_at)}
                </div>
              </button>
              <button
                className="chatkit-sidebar-thread-delete"
                onClick={(e) => handleDeleteClick(e, thread.id)}
                aria-label="Delete conversation"
                title="Delete conversation"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
                </svg>
              </button>
            </div>
          ))}

          {/* Load more button */}
          {hasMore && (
            <button
              className="chatkit-sidebar-load-more"
              onClick={onLoadMore}
              disabled={isLoading}
            >
              {isLoading ? 'Loading...' : 'Load more'}
            </button>
          )}
        </div>
      </div>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={!!deleteThreadId}
        title="Delete Conversation"
        message="Are you sure you want to delete this conversation? This action cannot be undone."
        confirmLabel="Delete"
        cancelLabel="Cancel"
        onConfirm={confirmDelete}
        onCancel={cancelDelete}
      />
    </>
  );
}
