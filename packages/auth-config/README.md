# @repo/auth-config

BetterAuth configuration package for the AI-Native Robotics Textbook platform.

## Overview

This package provides:
- **Server-side auth configuration** (`index.ts`) - BetterAuth setup with Drizzle adapter
- **Client-side auth client** (`client.ts`) - Frontend authentication client

## Features

- Email/password authentication
- Session management (7-day expiry)
- PostgreSQL via Drizzle ORM
- CORS support for local dev and production
- TypeScript support

## Installation

This is a workspace package. Install dependencies from the root:

```bash
pnpm install
```

## Environment Variables

### Server-side (required)

```bash
# Secret for signing sessions (generate with: openssl rand -base64 32)
BETTER_AUTH_SECRET=your-secret-key-here

# Base URL for auth service
BETTER_AUTH_URL=http://localhost:3001

# Optional: Production URL for CORS
PRODUCTION_URL=https://your-domain.com
```

### Client-side (required)

```bash
# Auth service URL (must be public for client-side)
NEXT_PUBLIC_AUTH_URL=http://localhost:3001
```

## Usage

### Server-side (API routes, backend)

```typescript
import { auth } from '@repo/auth-config';

// Use in API route handler
export const { GET, POST } = auth.handler;

// Or use auth methods directly
const session = await auth.api.getSession({ headers });
```

### Client-side (React, Docusaurus)

```typescript
import { authClient } from '@repo/auth-config/client';

// Sign up
const result = await authClient.signUp.email({
  email: 'user@example.com',
  password: 'securepassword',
  name: 'John Doe',
});

// Sign in
await authClient.signIn.email({
  email: 'user@example.com',
  password: 'securepassword',
});

// Get current session
const session = await authClient.getSession();

// Sign out
await authClient.signOut();
```

## Architecture

### Simplified for MVP

This configuration is intentionally simplified for the MVP:

- **No OIDC/JWT plugins** - Using standard BetterAuth sessions
- **No social OAuth** - Email/password only
- **Email verification disabled** - Can be enabled for production

### What's included

- ✅ Email/password authentication
- ✅ Session management
- ✅ Drizzle ORM adapter (PostgreSQL)
- ✅ CORS configuration
- ✅ TypeScript types

### What's NOT included (can be added later)

- ❌ Social OAuth (Google, GitHub, etc.)
- ❌ OIDC/JWT tokens
- ❌ Email verification (disabled for MVP)
- ❌ Two-factor authentication
- ❌ Magic link authentication

## Security Notes

1. **NEVER commit BETTER_AUTH_SECRET** - Use `.env` files and keep them in `.gitignore`
2. **Generate strong secrets** - Use `openssl rand -base64 32`
3. **Enable email verification in production** - Set `requireEmailVerification: true`
4. **Use HTTPS in production** - Configure `baseURL` with `https://`
5. **Review CORS origins** - Only add trusted domains to `trustedOrigins`

## Dependencies

- `better-auth` - Authentication framework
- `@repo/auth-database` - Database schema and connection (workspace package)

## Related Packages

- `@repo/auth-database` - Database models and migrations
- `apps/auth-service` - Standalone auth service (if using separate deployment)

## Development

```bash
# Type check
pnpm type-check

# Build (if needed)
pnpm build
```

## References

- [BetterAuth Documentation](https://www.better-auth.com/)
- [Drizzle ORM](https://orm.drizzle.team/)
- Constitution: `.specify/memory/constitution.md` (Technical Stack section)
