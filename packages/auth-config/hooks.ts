/**
 * Auth hooks for cross-site session management
 *
 * This file re-exports hooks that can be used from any frontend app
 * (Docusaurus, Auth app, etc.) to check session state.
 */

export { useSession, type SessionData, type SessionUser } from './use-session-core';
