import React from 'react';
import type { TextSelection } from './useTextSelection';

export type SelectionAction = 'explain' | 'translate' | 'summarize';

export interface SelectionTooltipProps {
  selection: TextSelection;
  onAction: (action: SelectionAction, text: string) => void;
  onClose: () => void;
}

/**
 * SelectionTooltip Component
 *
 * Floating tooltip that appears when text is selected.
 * Provides action buttons for:
 * - Explain: Get a detailed explanation of the selected text
 * - Translate: Translate the text to Urdu
 * - Summarize: Get a concise summary of the selected text
 */
const SelectionTooltip: React.FC<SelectionTooltipProps> = ({
  selection,
  onAction,
  onClose,
}) => {
  if (!selection.isVisible || !selection.text) {
    return null;
  }

  const handleAction = (action: SelectionAction) => {
    onAction(action, selection.text);
    onClose();
  };

  // Calculate position to keep tooltip on screen
  const tooltipStyle: React.CSSProperties = {
    position: 'fixed',
    left: `${Math.max(100, Math.min(selection.x, window.innerWidth - 100))}px`,
    top: `${Math.max(50, selection.y)}px`,
    transform: 'translate(-50%, -100%)',
    zIndex: 10001,
  };

  return (
    <div
      className="chatkit-selection-tooltip"
      style={tooltipStyle}
      role="toolbar"
      aria-label="Text selection actions"
    >
      <button
        className="chatkit-selection-tooltip__btn chatkit-selection-tooltip__btn--explain"
        onClick={() => handleAction('explain')}
        title="Get an explanation of this text"
      >
        Explain
      </button>
      <button
        className="chatkit-selection-tooltip__btn chatkit-selection-tooltip__btn--translate"
        onClick={() => handleAction('translate')}
        title="Translate to Urdu"
      >
        Translate
      </button>
      <button
        className="chatkit-selection-tooltip__btn chatkit-selection-tooltip__btn--summarize"
        onClick={() => handleAction('summarize')}
        title="Summarize this text"
      >
        Summarize
      </button>
    </div>
  );
};

export default SelectionTooltip;
