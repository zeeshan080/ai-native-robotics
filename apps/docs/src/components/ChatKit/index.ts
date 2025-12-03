/**
 * ChatKit Component Exports
 */

export { default as FloatingChatBar } from './FloatingChatBar';
export { default as ChatMessage } from './ChatMessage';
export { default as SelectionTooltip } from './SelectionTooltip';
export { default as MessageLimitWarning } from './MessageLimitWarning';
export { default as MessageLimitReached } from './MessageLimitReached';
export { useTextSelection } from './useTextSelection';
export { useThreads } from './useThreads';
export { useAnonymousMessages } from './useAnonymousMessages';

// View Mode Context and Hook
export {
  ChatViewModeProvider,
  useChatViewMode,
  getViewModeClassName,
  canShowDockButtons,
} from './ChatViewModeContext';

export type { TextSelection } from './useTextSelection';
export type { SelectionAction as TooltipAction, SelectionTooltipProps } from './SelectionTooltip';
export type { MessageLimitWarningProps } from './MessageLimitWarning';
export type { MessageLimitReachedProps } from './MessageLimitReached';
export type { UseAnonymousMessagesReturn, AnonymousMessagesState } from './useAnonymousMessages';

export type {
  Message,
  ChatState,
  SelectionState,
  SelectionActionType,
  SelectionAction,
  ChatEvent,
  ChatRequest,
  // Thread types
  Thread,
  ThreadItem,
  ThreadListResponse,
  CreateThreadRequest,
  AddMessageRequest,
} from './types';

export type {
  ChatViewMode,
  SideDockPosition,
  ChatViewModeContextValue,
  ChatViewModeProviderProps,
} from './ChatViewModeContext';
