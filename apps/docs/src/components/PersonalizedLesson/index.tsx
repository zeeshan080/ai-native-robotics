import React, { useState, useCallback, useEffect } from 'react';
import type { ReactNode } from 'react';
import { createAuthClient } from 'better-auth/react';
import { useUser } from '../../context/UserContext';
import { PersonalizedContent } from './PersonalizedContent';
import { LoginPrompt } from '../LoginPrompt';
import styles from './PersonalizedLesson.module.css';

// Determine auth service URL based on environment
const getAuthUrl = () => {
  if (typeof window === 'undefined') return 'http://localhost:3001';
  if (window.location.hostname.includes('github.io')) {
    return 'https://ai-native-robotics-auth.vercel.app';
  }
  return 'http://localhost:3001';
};

// Create auth client directly to avoid server-side dependencies from @repo/auth-config
const authClient = createAuthClient({
  baseURL: getAuthUrl(),
  fetchOptions: {
    credentials: 'include',
  },
});

interface AuthUser {
  id: string;
  email: string;
  name: string;
}

interface PersonalizedLessonProps {
  children: ReactNode;
  lessonSlug?: string;
}

/**
 * PersonalizedLesson component that shows Original and Personalized tabs.
 * Wraps lesson content and provides personalization on demand.
 * Shows LoginPrompt if user is not authenticated when clicking Personalize tab.
 */
export function PersonalizedLesson({ children, lessonSlug }: PersonalizedLessonProps): React.ReactElement {
  const { onboardingCompleted, isLoading: userLoading } = useUser();
  const [activeTab, setActiveTab] = useState<'original' | 'personalized'>('original');
  const [extractedContent, setExtractedContent] = useState<string>('');

  // Auth state
  const [authUser, setAuthUser] = useState<AuthUser | null>(null);
  const [authLoading, setAuthLoading] = useState(true);

  // Get lesson slug from URL if not provided
  const slug = lessonSlug || (typeof window !== 'undefined' ? window.location.pathname : '');

  // Check authentication status on mount
  useEffect(() => {
    async function checkAuth() {
      try {
        const session = await authClient.getSession();
        if (session.data?.user) {
          setAuthUser({
            id: session.data.user.id,
            email: session.data.user.email,
            name: session.data.user.name || '',
          });
        }
      } catch (error) {
        console.error('Auth check failed:', error);
      } finally {
        setAuthLoading(false);
      }
    }
    checkAuth();
  }, []);

  // Use callback ref to detect when the content div is mounted
  const contentRef = useCallback((node: HTMLDivElement | null) => {
    if (node && !extractedContent) {
      const textContent = node.innerText || node.textContent || '';
      if (textContent.trim()) {
        setExtractedContent(textContent.trim());
      }
    }
  }, [extractedContent]);

  // Determine if user can access personalization
  const isAuthenticated = !!authUser;
  const canPersonalize = isAuthenticated && onboardingCompleted;
  const isLoading = authLoading || userLoading;

  // Always show tabs - loading state only affects what shows in Personalized tab
  return (
    <div className={styles.container}>
      <div className={styles.tabs}>
        <button
          className={`${styles.tab} ${activeTab === 'original' ? styles.tabActive : ''}`}
          onClick={() => setActiveTab('original')}
          type="button"
        >
          Original
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'personalized' ? styles.tabActive : ''}`}
          onClick={() => setActiveTab('personalized')}
          type="button"
        >
          Personalized
        </button>
      </div>

      <div className={styles.content}>
        {/* Always render original content, hide when personalized is active */}
        <div
          ref={contentRef}
          style={{ display: activeTab === 'original' ? 'block' : 'none' }}
        >
          {children}
        </div>

        {/* Handle personalized tab */}
        {activeTab === 'personalized' && (
          <>
            {/* Show loading state while checking auth */}
            {isLoading && (
              <div className={styles.loading}>
                <div className={styles.spinner} />
                <p>Checking authentication...</p>
              </div>
            )}

            {/* Show login prompt if not authenticated (and not loading) */}
            {!isLoading && !isAuthenticated && (
              <LoginPrompt
                message="Sign in to unlock personalized content tailored to your learning level and goals."
                buttonText="Login to Personalize"
              />
            )}

            {/* Show onboarding prompt if authenticated but onboarding not complete */}
            {!isLoading && isAuthenticated && !onboardingCompleted && (
              <div
                style={{
                  textAlign: 'center',
                  padding: '2rem',
                  backgroundColor: 'var(--ifm-background-surface-color)',
                  borderRadius: '8px',
                  border: '1px solid var(--ifm-color-emphasis-200)',
                }}
              >
                <h3>Complete Your Profile</h3>
                <p>Please complete the onboarding questionnaire to enable personalization.</p>
                <a
                  href="/onboarding"
                  style={{
                    display: 'inline-block',
                    padding: '0.75rem 1.5rem',
                    backgroundColor: 'var(--ifm-color-primary)',
                    color: 'white',
                    borderRadius: '6px',
                    textDecoration: 'none',
                    marginTop: '1rem',
                  }}
                >
                  Complete Onboarding
                </a>
              </div>
            )}

            {/* Show personalized content if fully authenticated and onboarded */}
            {!isLoading && canPersonalize && (
              <PersonalizedContent
                lessonSlug={slug}
                originalContent={extractedContent}
                fallback={children}
              />
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default PersonalizedLesson;
