import React, { useCallback } from 'react';
import {
  FloatingChatBar,
  SelectionTooltip,
  useTextSelection,
  ChatViewModeProvider,
} from '../components/ChatKit';
import type { SelectionAction } from '../components/ChatKit/SelectionTooltip';
import { UserProvider } from '../context/UserContext';
import '../css/chatkit.css';

/**
 * Root Theme Wrapper
 *
 * Injects the ChatKit floating chat bar and text selection tooltip
 * globally across all Docusaurus pages.
 *
 * Wraps ChatKit with ChatViewModeProvider (T067) to enable
 * compact, fullpage, and sidedock view modes with localStorage persistence.
 */
export default function Root({ children }: { children: React.ReactNode }): React.ReactElement {
  const { selection, clearSelection } = useTextSelection();

  const handleSelectionAction = useCallback((action: SelectionAction, text: string) => {
    // Format the message based on the action
    let message = '';
    switch (action) {
      case 'explain':
        message = `Explain: ${text}`;
        break;
      case 'translate':
        message = `Translate to Urdu: ${text}`;
        break;
      case 'summarize':
        message = `Summarize: ${text}`;
        break;
    }

    // Dispatch custom event to FloatingChatBar
    window.dispatchEvent(new CustomEvent('chatkit:sendMessage', {
      detail: { message }
    }));
  }, []);

  return (
    <UserProvider>
      {children}
      <SelectionTooltip
        selection={selection}
        onAction={handleSelectionAction}
        onClose={clearSelection}
      />
      <ChatViewModeProvider>
        <FloatingChatBar />
      </ChatViewModeProvider>
    </UserProvider>
  );
}
