import React, { useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { useUser } from '../../context/UserContext';
import styles from './PersonalizedLesson.module.css';

interface PersonalizedContentProps {
  lessonSlug: string;
  originalContent: string;
  fallback: ReactNode;
}

const API_BASE = 'http://localhost:8000/api';

/**
 * Fetches and displays personalized content for a lesson.
 */
export function PersonalizedContent({
  lessonSlug,
  originalContent,
  fallback,
}: PersonalizedContentProps): React.ReactElement {
  const { userId } = useUser();
  const [content, setContent] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [cached, setCached] = useState(false);

  useEffect(() => {
    if (!userId || !originalContent) {
      return;
    }

    const fetchPersonalizedContent = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await fetch(`${API_BASE}/personalize`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-User-ID': userId,
          },
          body: JSON.stringify({
            lesson_slug: lessonSlug,
            original_content: originalContent,
          }),
        });

        if (response.ok) {
          const data = await response.json();
          setContent(data.personalized_content);
          setCached(data.cached);
        } else {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to personalize content');
        }
      } catch (err) {
        console.error('Personalization error:', err);
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setIsLoading(false);
      }
    };

    fetchPersonalizedContent();
  }, [userId, lessonSlug, originalContent]);

  if (isLoading) {
    return (
      <div className={styles.loading}>
        <div className={styles.spinner} />
        <p>Personalizing content for you...</p>
        <p className={styles.loadingSubtext}>
          This may take a few seconds on first load.
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.error}>
        <p>Unable to personalize content: {error}</p>
        <p>Showing original content instead.</p>
        <div className={styles.fallbackContent}>{fallback}</div>
      </div>
    );
  }

  if (!content) {
    return <>{fallback}</>;
  }

  return (
    <div className={styles.personalizedWrapper}>
      {cached && (
        <div className={styles.cachedBadge}>
          Cached
        </div>
      )}
      <div
        className={styles.personalizedContent}
        dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
      />
    </div>
  );
}

/**
 * Markdown to HTML renderer.
 */
function renderMarkdown(markdown: string): string {
  let html = markdown
    // Code blocks (must be before other replacements)
    .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>')
    // Headers
    .replace(/^#### (.*$)/gm, '<h4>$1</h4>')
    .replace(/^### (.*$)/gm, '<h3>$1</h3>')
    .replace(/^## (.*$)/gm, '<h2>$1</h2>')
    .replace(/^# (.*$)/gm, '<h1>$1</h1>')
    // Bold
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    // Italic (but not in code)
    .replace(/(?<!`)\*([^*]+)\*(?!`)/g, '<em>$1</em>')
    // Inline code
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // Links
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')
    // Unordered lists
    .replace(/^[\-\*] (.*$)/gm, '<li>$1</li>')
    // Ordered lists
    .replace(/^\d+\. (.*$)/gm, '<li>$1</li>')
    // Blockquotes
    .replace(/^> (.*$)/gm, '<blockquote>$1</blockquote>')
    // Horizontal rules
    .replace(/^---$/gm, '<hr/>')
    // Paragraphs (double newlines)
    .replace(/\n\n+/g, '</p><p>')
    // Line breaks
    .replace(/\n/g, '<br/>');

  // Wrap in paragraph
  html = '<p>' + html + '</p>';

  // Fix consecutive list items
  html = html.replace(/<\/li><br\/><li>/g, '</li><li>');
  html = html.replace(/<p><li>/g, '<ul><li>');
  html = html.replace(/<\/li><\/p>/g, '</li></ul>');
  html = html.replace(/<\/li><p>/g, '</li></ul><p>');

  // Fix blockquotes
  html = html.replace(/<\/blockquote><br\/><blockquote>/g, '</blockquote><blockquote>');

  // Clean up empty paragraphs
  html = html.replace(/<p><\/p>/g, '');
  html = html.replace(/<p><br\/><\/p>/g, '');

  return html;
}

export default PersonalizedContent;
