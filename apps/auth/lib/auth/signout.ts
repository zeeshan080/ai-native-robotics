import { authClient } from '@repo/auth-config/client';

export async function signOut(redirectTo?: string) {
  try {
    await authClient.signOut();
    // Redirect after sign out
    window.location.href = redirectTo || 'http://localhost:3000';
  } catch (error) {
    console.error('Sign out error:', error);
    // Still redirect on error to ensure clean state
    window.location.href = redirectTo || 'http://localhost:3000';
  }
}
