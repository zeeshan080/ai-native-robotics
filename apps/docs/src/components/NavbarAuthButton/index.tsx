import React, { useState, useEffect } from 'react';
import { createAuthClient } from 'better-auth/react';

// Determine auth service URL based on environment
const getAuthUrl = () => {
  if (typeof window === 'undefined') return 'http://localhost:3001';
  // Production: GitHub Pages points to Vercel auth service
  if (window.location.hostname.includes('github.io')) {
    return 'https://ai-native-robotics-auth.vercel.app';
  }
  // Local development
  return 'http://localhost:3001';
};

const AUTH_URL = getAuthUrl();

// Create auth client directly to avoid server-side dependencies from @repo/auth-config
const authClient = createAuthClient({
  baseURL: AUTH_URL,
  fetchOptions: {
    credentials: 'include',
  },
});

interface AuthUser {
  id: string;
  email: string;
  name: string;
}

/**
 * NavbarAuthButton component for Docusaurus navbar
 *
 * Displays:
 * - "Login" button when unauthenticated
 * - User name + "Logout" button when authenticated
 *
 * Authentication flow:
 * 1. Check BetterAuth session on mount
 * 2. Redirect to auth service (:3001) for login with callback
 * 3. Handle logout and session cleanup
 */
export function NavbarAuthButton(): React.ReactElement {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchSession() {
      try {
        const session = await authClient.getSession();
        if (session.data?.user) {
          setUser({
            id: session.data.user.id,
            email: session.data.user.email,
            name: session.data.user.name || '',
          });
        }
      } catch (error) {
        console.error('Failed to fetch session:', error);
      } finally {
        setIsLoading(false);
      }
    }
    fetchSession();
  }, []);

  const handleLogin = () => {
    const callbackUrl = encodeURIComponent(window.location.href);
    window.location.href = `${AUTH_URL}/signin?callbackUrl=${callbackUrl}`;
  };

  const handleLogout = async () => {
    try {
      await authClient.signOut();
      window.location.reload();
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  if (isLoading) {
    return <span style={{ opacity: 0.5 }}>...</span>;
  }

  if (user) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <span style={{ fontSize: '0.875rem', color: 'var(--ifm-navbar-link-color)' }}>
          {user.name || user.email}
        </span>
        <button
          onClick={handleLogout}
          style={{
            background: 'none',
            border: '1px solid var(--ifm-color-primary)',
            borderRadius: '4px',
            padding: '0.25rem 0.75rem',
            cursor: 'pointer',
            color: 'var(--ifm-color-primary)',
            fontSize: '0.875rem',
          }}
        >
          Logout
        </button>
      </div>
    );
  }

  return (
    <button
      onClick={handleLogin}
      style={{
        background: 'var(--ifm-color-primary)',
        border: 'none',
        borderRadius: '4px',
        padding: '0.5rem 1rem',
        cursor: 'pointer',
        color: 'white',
        fontSize: '0.875rem',
        fontWeight: 500,
      }}
    >
      Login
    </button>
  );
}

export default NavbarAuthButton;
