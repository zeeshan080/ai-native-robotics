'use client';

import { useEffect, useState } from 'react';
import { authClient } from './client';

export type SessionUser = {
  id: string;
  email: string;
  name: string;
};

export type SessionData = {
  user: SessionUser | null;
  isLoading: boolean;
  isAuthenticated: boolean;
};

/**
 * Hook to get current session from any frontend app
 * Works cross-origin with cookies (credentials: include)
 */
export function useSession(): SessionData {
  const [user, setUser] = useState<SessionUser | null>(null);
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

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
  };
}
