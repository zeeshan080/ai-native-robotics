/**
 * ChatKit Component Exports
 */

export { default as FloatingChatBar } from './FloatingChatBar';
export { default as ChatMessage } from './ChatMessage';
export { default as SelectionTooltip } from './SelectionTooltip';
export { useTextSelection } from './useTextSelection';

export type { TextSelection } from './useTextSelection';
export type { SelectionAction as TooltipAction, SelectionTooltipProps } from './SelectionTooltip';

export type {
  Message,
  ChatState,
  SelectionState,
  SelectionActionType,
  SelectionAction,
  ChatEvent,
  ChatRequest,
} from './types';
