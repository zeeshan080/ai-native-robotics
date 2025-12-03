import React from 'react';
import Content from '@theme-original/DocItem/Content';
import type ContentType from '@theme/DocItem/Content';
import type { WrapperProps } from '@docusaurus/types';
import { useLocation } from '@docusaurus/router';
import { PersonalizedLesson } from '../../../components/PersonalizedLesson';

type Props = WrapperProps<typeof ContentType>;

/**
 * Check if the current page is a lesson page based on URL pattern.
 * Lesson pages contain "lesson-" or end with "/lab" in their path.
 * Note: Docusaurus strips numeric prefixes from URLs (01-lesson becomes lesson)
 */
function isLessonPage(pathname: string): boolean {
  // Match "lesson-" anywhere in path, or path ending with "/lab"
  return /lesson-|\/lab$/.test(pathname);
}

/**
 * Wrapper for DocItem/Content that adds personalization tabs.
 * Only shows tabs on lesson pages (files with "lesson" or "lab" in the name).
 */
export default function ContentWrapper(props: Props): JSX.Element {
  const location = useLocation();

  // Only wrap lesson pages with PersonalizedLesson
  if (isLessonPage(location.pathname)) {
    return (
      <PersonalizedLesson>
        <Content {...props} />
      </PersonalizedLesson>
    );
  }

  // For non-lesson pages, render content directly
  return <Content {...props} />;
}
