import { authClient } from '@repo/auth-config/client';
import { getDefaultDocsUrl } from '@/lib/utils/callback-url';

export async function signOut(redirectTo?: string) {
  const defaultUrl = getDefaultDocsUrl();
  try {
    await authClient.signOut();
    // Redirect after sign out
    window.location.href = redirectTo || defaultUrl;
  } catch (error) {
    console.error('Sign out error:', error);
    // Still redirect on error to ensure clean state
    window.location.href = redirectTo || defaultUrl;
  }
}
