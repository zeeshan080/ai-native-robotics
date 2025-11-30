import { createAuthClient } from "better-auth/client";

/**
 * BetterAuth client configuration
 *
 * Used in frontend applications (Docusaurus, React components) to:
 * - Sign up new users
 * - Sign in existing users
 * - Manage sessions
 * - Get current user info
 *
 * Environment variables:
 * - NEXT_PUBLIC_AUTH_URL: Auth service URL (must be PUBLIC for client-side)
 *
 * Usage example:
 *
 * ```typescript
 * import { authClient } from '@repo/auth-config/client';
 *
 * // Sign up
 * const result = await authClient.signUp.email({
 *   email: 'user@example.com',
 *   password: 'securepassword',
 *   name: 'John Doe',
 * });
 *
 * // Sign in
 * const session = await authClient.signIn.email({
 *   email: 'user@example.com',
 *   password: 'securepassword',
 * });
 *
 * // Get current session
 * const currentSession = await authClient.getSession();
 *
 * // Sign out
 * await authClient.signOut();
 * ```
 */
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_AUTH_URL || "http://localhost:3001",

  // Include credentials for cross-origin requests (cookies)
  fetchOptions: {
    credentials: 'include',
  },
});

export type AuthClient = typeof authClient;
