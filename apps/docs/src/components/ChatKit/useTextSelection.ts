import { useState, useEffect, useCallback } from 'react';

export interface TextSelection {
  text: string;
  x: number;
  y: number;
  isVisible: boolean;
}

const MAX_SELECTION_LENGTH = 500;

/**
 * useTextSelection Hook
 *
 * Detects text selection on the page and provides position information
 * for rendering a floating tooltip.
 *
 * Features:
 * - Tracks selected text and its position
 * - Truncates long selections with "[...truncated]" indicator
 * - Clears selection when clicking elsewhere
 * - Excludes selections in input/textarea elements
 */
export function useTextSelection() {
  const [selection, setSelection] = useState<TextSelection>({
    text: '',
    x: 0,
    y: 0,
    isVisible: false,
  });

  const handleMouseUp = useCallback(() => {
    // Small delay to ensure selection is complete
    setTimeout(() => {
      const windowSelection = window.getSelection();
      const selectedText = windowSelection?.toString().trim() || '';

      // Ignore empty selections
      if (!selectedText) {
        setSelection(prev => ({ ...prev, isVisible: false }));
        return;
      }

      // Ignore selections in form elements
      const anchorNode = windowSelection?.anchorNode;
      if (anchorNode) {
        const element = anchorNode.nodeType === Node.TEXT_NODE
          ? anchorNode.parentElement
          : anchorNode as Element;

        if (element?.closest('input, textarea, .chatkit-bar, .chatkit-panel')) {
          return;
        }
      }

      // Get selection position
      const range = windowSelection?.getRangeAt(0);
      if (!range) {
        setSelection(prev => ({ ...prev, isVisible: false }));
        return;
      }

      const rect = range.getBoundingClientRect();

      // Truncate long selections
      let displayText = selectedText;
      if (selectedText.length > MAX_SELECTION_LENGTH) {
        displayText = selectedText.slice(0, MAX_SELECTION_LENGTH) + ' [...truncated]';
      }

      setSelection({
        text: displayText,
        x: rect.left + rect.width / 2,
        y: rect.top - 10, // Position above the selection
        isVisible: true,
      });
    }, 10);
  }, []);

  const handleMouseDown = useCallback((e: MouseEvent) => {
    // Hide tooltip if clicking outside
    const target = e.target as Element;
    if (!target.closest('.chatkit-selection-tooltip')) {
      setSelection(prev => ({ ...prev, isVisible: false }));
    }
  }, []);

  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    // Hide tooltip on Escape
    if (e.key === 'Escape') {
      setSelection(prev => ({ ...prev, isVisible: false }));
      window.getSelection()?.removeAllRanges();
    }
  }, []);

  const clearSelection = useCallback(() => {
    setSelection(prev => ({ ...prev, isVisible: false }));
    window.getSelection()?.removeAllRanges();
  }, []);

  useEffect(() => {
    document.addEventListener('mouseup', handleMouseUp);
    document.addEventListener('mousedown', handleMouseDown);
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
      document.removeEventListener('mousedown', handleMouseDown);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleMouseUp, handleMouseDown, handleKeyDown]);

  return { selection, clearSelection };
}

export default useTextSelection;
