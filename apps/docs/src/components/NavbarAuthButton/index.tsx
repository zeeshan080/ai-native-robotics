import React, { useState, useEffect } from 'react';
import { createAuthClient } from 'better-auth/react';

// Determine auth service URL based on environment
const getAuthUrl = () => {
  if (typeof window === 'undefined') return 'http://localhost:3001';
  // Production: GitHub Pages points to Vercel auth service
  if (window.location.hostname.includes('github.io')) {
    return 'https://ai-native-robotics.vercel.app';
  }
  // Local development
  return 'http://localhost:3001';
};

const AUTH_URL = getAuthUrl();
const SESSION_TOKEN_KEY = 'better_auth_session_token';

// Helper to get token from localStorage
const getStoredToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(SESSION_TOKEN_KEY);
};

// Helper to store token in localStorage
const storeToken = (token: string): void => {
  if (typeof window === 'undefined') return;
  localStorage.setItem(SESSION_TOKEN_KEY, token);
};

// Helper to remove token from localStorage
const removeToken = (): void => {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(SESSION_TOKEN_KEY);
};

// Create auth client with bearer token authentication for cross-domain
const authClient = createAuthClient({
  baseURL: AUTH_URL,
  fetchOptions: {
    credentials: 'include',
    auth: {
      type: 'Bearer',
      token: () => getStoredToken() || '',
    },
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
    async function initAuth() {
      try {
        // Check for session token in URL (from redirect after login)
        if (typeof window !== 'undefined') {
          const urlParams = new URLSearchParams(window.location.search);
          const tokenFromUrl = urlParams.get('session_token');

          if (tokenFromUrl) {
            console.log('[NavbarAuth] Found session token in URL, storing...');
            storeToken(tokenFromUrl);

            // Clean URL by removing token parameter
            urlParams.delete('session_token');
            const cleanUrl = `${window.location.pathname}${urlParams.toString() ? '?' + urlParams.toString() : ''}`;
            window.history.replaceState({}, '', cleanUrl);
          }
        }

        // Fetch session using stored token
        const token = getStoredToken();
        if (!token) {
          console.log('[NavbarAuth] No token found, user not authenticated');
          setIsLoading(false);
          return;
        }

        console.log('[NavbarAuth] Fetching session from:', AUTH_URL);
        const session = await authClient.getSession();
        console.log('[NavbarAuth] Session response:', session);

        if (session.data?.user) {
          console.log('[NavbarAuth] User authenticated:', session.data.user.email);
          setUser({
            id: session.data.user.id,
            email: session.data.user.email,
            name: session.data.user.name || '',
          });
        } else {
          console.log('[NavbarAuth] Invalid session, clearing token');
          removeToken();
        }
      } catch (error) {
        console.error('[NavbarAuth] Failed to fetch session:', error);
        removeToken();
      } finally {
        setIsLoading(false);
      }
    }
    initAuth();
  }, []);

  const handleLogin = () => {
    const callbackUrl = encodeURIComponent(window.location.href);
    window.location.href = `${AUTH_URL}/signin?callbackUrl=${callbackUrl}`;
  };

  const handleLogout = async () => {
    try {
      // Clear local token
      removeToken();

      // Call signOut on server (optional, but recommended)
      await authClient.signOut();

      // Reload page to reset UI
      window.location.reload();
    } catch (error) {
      console.error('Logout error:', error);
      // Still clear token even if server call fails
      removeToken();
      window.location.reload();
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
