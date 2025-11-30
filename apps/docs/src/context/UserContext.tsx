import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import type { ReactNode } from 'react';

/**
 * User preferences from onboarding questionnaire
 */
export interface UserPreferences {
  education_level: string;
  programming_experience: string;
  robotics_background: boolean;
  ai_ml_experience: string;
  learning_goals: string[];
  preferred_language: string;
}

/**
 * User state managed by context
 */
export interface UserState {
  userId: string | null;
  isLoading: boolean;
  onboardingCompleted: boolean;
  preferences: UserPreferences | null;
  error: string | null;
}

/**
 * Context value including state and actions
 */
export interface UserContextValue extends UserState {
  initializeUser: () => Promise<void>;
  completeOnboarding: (preferences: UserPreferences) => Promise<void>;
  updatePreferences: (preferences: Partial<UserPreferences>) => Promise<void>;
  clearUser: () => void;
}

/**
 * Default context value for SSR
 */
const defaultContextValue: UserContextValue = {
  userId: null,
  isLoading: true,
  onboardingCompleted: false,
  preferences: null,
  error: null,
  initializeUser: async () => {},
  completeOnboarding: async () => {},
  updatePreferences: async () => {},
  clearUser: () => {},
};

const UserContext = createContext<UserContextValue>(defaultContextValue);

const STORAGE_KEY = 'user_id';
const API_BASE = 'http://localhost:8000/api';

/**
 * Generate a UUID v4
 */
function generateUserId(): string {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  // Fallback for older browsers
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

/**
 * Get or create user ID from localStorage
 */
function getOrCreateUserId(): string {
  if (typeof window === 'undefined') return '';
  let userId = localStorage.getItem(STORAGE_KEY);
  if (!userId) {
    userId = generateUserId();
    localStorage.setItem(STORAGE_KEY, userId);
  }
  return userId;
}

interface UserProviderProps {
  children: ReactNode;
}

/**
 * UserProvider component that manages user state
 */
export function UserProvider({ children }: UserProviderProps): React.ReactElement {
  const [state, setState] = useState<UserState>({
    userId: null,
    isLoading: true,
    onboardingCompleted: false,
    preferences: null,
    error: null,
  });

  const [isMounted, setIsMounted] = useState(false);

  // Track if we're in browser
  useEffect(() => {
    setIsMounted(true);
  }, []);

  /**
   * Initialize user - check if exists in backend, create if not
   */
  const initializeUser = useCallback(async () => {
    if (typeof window === 'undefined') return;

    try {
      setState((prev: UserState) => ({ ...prev, isLoading: true, error: null }));

      const userId = getOrCreateUserId();
      if (!userId) return;

      // Try to get existing user
      const response = await fetch(`${API_BASE}/user/${userId}`);

      if (response.ok) {
        const user = await response.json();

        // If user exists and has completed onboarding, fetch preferences
        let preferences = null;
        if (user.onboarding_completed) {
          const prefsResponse = await fetch(`${API_BASE}/user/preferences`, {
            headers: { 'X-User-ID': userId },
          });
          if (prefsResponse.ok) {
            preferences = await prefsResponse.json();
          }
        }

        setState({
          userId,
          isLoading: false,
          onboardingCompleted: user.onboarding_completed,
          preferences,
          error: null,
        });
      } else if (response.status === 404) {
        // Create new user
        const createResponse = await fetch(`${API_BASE}/user/create`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: userId }),
        });

        if (createResponse.ok) {
          setState({
            userId,
            isLoading: false,
            onboardingCompleted: false,
            preferences: null,
            error: null,
          });
        } else {
          throw new Error('Failed to create user');
        }
      } else {
        throw new Error('Failed to fetch user');
      }
    } catch (error) {
      console.error('User initialization error:', error);
      // Still set userId even if backend fails (graceful degradation)
      const userId = getOrCreateUserId();
      setState({
        userId,
        isLoading: false,
        onboardingCompleted: false,
        preferences: null,
        error: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }, []);

  /**
   * Complete onboarding with provided preferences
   */
  const completeOnboarding = useCallback(async (preferences: UserPreferences) => {
    if (!state.userId) return;

    try {
      setState((prev: UserState) => ({ ...prev, isLoading: true, error: null }));

      const response = await fetch(`${API_BASE}/onboarding`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: state.userId,
          ...preferences,
        }),
      });

      if (response.ok) {
        setState((prev: UserState) => ({
          ...prev,
          isLoading: false,
          onboardingCompleted: true,
          preferences,
        }));

        // Redirect to home after onboarding
        if (typeof window !== 'undefined') {
          window.location.href = '/';
        }
      } else {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to save preferences');
      }
    } catch (error) {
      setState((prev: UserState) => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      }));
    }
  }, [state.userId]);

  /**
   * Update existing preferences
   */
  const updatePreferences = useCallback(async (updates: Partial<UserPreferences>) => {
    if (!state.userId) return;

    try {
      setState((prev: UserState) => ({ ...prev, isLoading: true, error: null }));

      const response = await fetch(`${API_BASE}/user/preferences`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': state.userId,
        },
        body: JSON.stringify(updates),
      });

      if (response.ok) {
        const updatedPrefs = await response.json();
        setState((prev: UserState) => ({
          ...prev,
          isLoading: false,
          preferences: updatedPrefs,
        }));

        // Clear personalization cache
        await fetch(`${API_BASE}/personalize/cache`, {
          method: 'DELETE',
          headers: { 'X-User-ID': state.userId },
        });
      } else {
        throw new Error('Failed to update preferences');
      }
    } catch (error) {
      setState((prev: UserState) => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      }));
    }
  }, [state.userId]);

  /**
   * Clear user data (for testing/logout)
   */
  const clearUser = useCallback(() => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(STORAGE_KEY);
    }
    setState({
      userId: null,
      isLoading: false,
      onboardingCompleted: false,
      preferences: null,
      error: null,
    });
  }, []);

  // Initialize user on mount (browser only)
  useEffect(() => {
    if (isMounted) {
      initializeUser();
    }
  }, [isMounted, initializeUser]);

  // Redirect to onboarding if not completed
  useEffect(() => {
    if (
      isMounted &&
      !state.isLoading &&
      state.userId &&
      !state.onboardingCompleted &&
      typeof window !== 'undefined' &&
      !window.location.pathname.includes('/onboarding') &&
      !state.error
    ) {
      window.location.href = '/onboarding';
    }
  }, [isMounted, state.isLoading, state.userId, state.onboardingCompleted, state.error]);

  const value: UserContextValue = {
    ...state,
    initializeUser,
    completeOnboarding,
    updatePreferences,
    clearUser,
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
}

/**
 * Hook to access user context
 */
export function useUser(): UserContextValue {
  return useContext(UserContext);
}
