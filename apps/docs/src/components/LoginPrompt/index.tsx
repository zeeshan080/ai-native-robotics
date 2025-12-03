import React from 'react';

// Determine auth service URL based on environment
const getAuthUrl = () => {
  if (typeof window === 'undefined') return 'http://localhost:3001';
  if (window.location.hostname.includes('github.io')) {
    return 'https://ai-native-robotics.vercel.app';
  }
  return 'http://localhost:3001';
};

interface LoginPromptProps {
  message?: string;
  buttonText?: string;
}

/**
 * LoginPrompt component - Shows a login button for unauthenticated users
 * in the Personalize tab. Redirects to auth service with callbackUrl
 * pointing back to the current lesson page.
 */
export function LoginPrompt({
  message = 'Sign in to unlock personalized content tailored to your learning level and goals.',
  buttonText = 'Login to Personalize',
}: LoginPromptProps): React.ReactElement {
  const authUrl = getAuthUrl();

  const handleLogin = () => {
    // Get current page URL for callback after login
    const callbackUrl = encodeURIComponent(window.location.href);
    window.location.href = `${authUrl}/signin?callbackUrl=${callbackUrl}`;
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '3rem 2rem',
        textAlign: 'center',
        backgroundColor: 'var(--ifm-background-surface-color)',
        borderRadius: '8px',
        border: '1px solid var(--ifm-color-emphasis-200)',
        margin: '1rem 0',
      }}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="48"
        height="48"
        viewBox="0 0 24 24"
        fill="none"
        stroke="var(--ifm-color-primary)"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        style={{ marginBottom: '1rem' }}
      >
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
        <circle cx="12" cy="7" r="4" />
      </svg>

      <h3
        style={{
          margin: '0 0 0.5rem 0',
          fontSize: '1.25rem',
          fontWeight: 600,
          color: 'var(--ifm-heading-color)',
        }}
      >
        Login Required
      </h3>

      <p
        style={{
          margin: '0 0 1.5rem 0',
          color: 'var(--ifm-color-content-secondary)',
          maxWidth: '400px',
          lineHeight: 1.6,
        }}
      >
        {message}
      </p>

      <button
        onClick={handleLogin}
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.5rem',
          padding: '0.75rem 1.5rem',
          backgroundColor: 'var(--ifm-color-primary)',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          fontSize: '1rem',
          fontWeight: 500,
          cursor: 'pointer',
          transition: 'background-color 0.2s ease',
        }}
        onMouseOver={(e) => {
          e.currentTarget.style.backgroundColor = 'var(--ifm-color-primary-dark)';
        }}
        onMouseOut={(e) => {
          e.currentTarget.style.backgroundColor = 'var(--ifm-color-primary)';
        }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
          <polyline points="10 17 15 12 10 7" />
          <line x1="15" y1="12" x2="3" y2="12" />
        </svg>
        {buttonText}
      </button>

      <p
        style={{
          margin: '1rem 0 0 0',
          fontSize: '0.875rem',
          color: 'var(--ifm-color-content-secondary)',
        }}
      >
        Don't have an account?{' '}
        <a
          href={`${authUrl}/signup?callbackUrl=${encodeURIComponent(typeof window !== 'undefined' ? window.location.href : '')}`}
          style={{
            color: 'var(--ifm-color-primary)',
            textDecoration: 'none',
          }}
        >
          Sign up
        </a>
      </p>
    </div>
  );
}

export default LoginPrompt;
