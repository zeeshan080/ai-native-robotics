# Research: BetterAuth Authentication Service

**Feature**: 006-betterauth-service
**Date**: 2025-11-30
**Status**: Complete

## Research Questions

### RQ-001: BetterAuth Configuration for Email/Password Only

**Question**: What is the minimal BetterAuth configuration for email/password authentication without OIDC, JWT plugins, or social OAuth?

**Research Method**: Analyzed reference SSO project at `/home/dell/pana-sso/sso/sso-monorepo`

**Findings**:
The reference SSO uses many plugins we don't need:
- `jwt()` plugin - for JWT token generation (skip for MVP)
- `oidcProvider()` plugin - for acting as OIDC provider (skip for MVP)
- `socialProviders` - GitHub, Google OAuth (skip for MVP)
- `emailVerification` - sends verification emails (skip for MVP)

**Decision**: Use minimal config with only `emailAndPassword` enabled
```typescript
export const auth = betterAuth({
  database: drizzleAdapter(getDb(), { provider: 'pg' }),
  secret: process.env.BETTER_AUTH_SECRET,
  baseURL: process.env.BETTER_AUTH_URL,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
    minPasswordLength: 8,
    maxPasswordLength: 128,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7,
    updateAge: 60 * 60 * 24,
  },
  trustedOrigins: [...],
});
```

**Rationale**: Simplest possible config that meets MVP requirements

---

### RQ-002: Cross-Origin Session Sharing

**Question**: How do we share sessions between auth service (3001), docs site (3000), and backend (8000)?

**Research Method**: Studied BetterAuth documentation and reference SSO CORS handling

**Findings**:
1. BetterAuth uses cookies for session management by default
2. Cross-origin requires:
   - `trustedOrigins` configuration in BetterAuth
   - CORS headers with `Access-Control-Allow-Credentials: true`
   - `credentials: 'include'` in client fetch options
3. Cookies are set on the auth service domain (localhost:3001)
4. Other services can validate by calling auth service `/api/auth/session`

**Decision**:
- Configure `trustedOrigins` in BetterAuth config
- Wrap API route handler with CORS middleware (copy from reference)
- Use `credentials: 'include'` in client config
- FastAPI validates by calling auth service session endpoint

**Rationale**: Follows reference SSO pattern, proven to work

---

### RQ-003: Database Schema Simplification

**Question**: What tables do we need for email/password auth only?

**Research Method**: Analyzed reference SSO schema at `packages/database/schema/auth-schema.ts`

**Findings**:
Reference SSO has these tables:
- `user` - Required
- `session` - Required
- `account` - Required (stores password hash)
- `verification` - Required (for future email verification)
- `jwks` - **Skip** (JWT plugin only)
- `oauthApplication` - **Skip** (OIDC provider only)
- `oauthAccessToken` - **Skip** (OIDC provider only)
- `oauthConsent` - **Skip** (OIDC provider only)

**Decision**: Keep only `user`, `session`, `account`, `verification` tables

**Rationale**: Minimal schema for email/password auth with room for future email verification

---

### RQ-004: FastAPI Session Validation

**Question**: How should FastAPI validate BetterAuth sessions?

**Research Method**: Explored BetterAuth API endpoints and session validation options

**Findings**:
Options considered:
1. **JWT validation** - Requires JWT plugin, JWKS endpoint, public key verification
2. **Session cookie forwarding** - Forward cookie to auth service `/api/auth/session`
3. **Direct database lookup** - Query session table directly

**Decision**: Use session cookie forwarding (Option 2)
```python
async def validate_session(request: Request) -> Optional[str]:
    session_cookie = request.cookies.get('better-auth.session_token')
    if not session_cookie:
        return None

    response = await httpx.get(
        f"{AUTH_SERVICE_URL}/api/auth/session",
        cookies={'better-auth.session_token': session_cookie}
    )
    if response.status_code == 200:
        return response.json().get('user', {}).get('id')
    return None
```

**Rationale**:
- No JWT complexity
- Single source of truth (auth service)
- Works with standard BetterAuth setup

---

### RQ-005: Password Complexity Requirements

**Question**: What password validation rules should we use?

**Research Method**: Reviewed reference SSO Zod schema and BetterAuth defaults

**Findings**:
Reference SSO uses complex rules:
```typescript
password: z.string()
  .min(8, 'Password must be at least 8 characters')
  .regex(/[A-Z]/, 'Must contain an uppercase letter')
  .regex(/[a-z]/, 'Must contain a lowercase letter')
  .regex(/[0-9]/, 'Must contain a number')
  .regex(/[^A-Za-z0-9]/, 'Must contain a special character')
```

**Decision**: Use simplified rules for MVP
```typescript
password: z.string()
  .min(8, 'Password must be at least 8 characters')
```

**Rationale**:
- MVP focus on getting auth working
- Complex rules can frustrate users
- Can add complexity later if needed

---

## Technology Decisions Summary

| Decision | Choice | Alternatives Rejected |
|----------|--------|----------------------|
| Auth library | BetterAuth | Auth.js, NextAuth (constitution mandates BetterAuth) |
| ORM | Drizzle | Prisma, raw SQL (match reference SSO) |
| Database | NeonDB Postgres | Supabase, PlanetScale (constitution mandates Neon) |
| Session validation | HTTP forwarding | JWT, direct DB lookup |
| Password rules | 8+ chars only | Complex regex (simpler for MVP) |
| Email verification | Disabled | Enabled (faster onboarding for MVP) |
| OAuth providers | None | GitHub, Google (out of scope) |

## Files to Copy from Reference SSO

| Source | Target | Modifications |
|--------|--------|---------------|
| `packages/database/db.ts` | `packages/auth-database/db.ts` | None |
| `packages/database/schema/auth-schema.ts` | `packages/auth-database/schema/auth-schema.ts` | Remove OIDC tables |
| `packages/database/drizzle.config.ts` | `packages/auth-database/drizzle.config.ts` | Update paths |
| `packages/auth-config/index.ts` | `packages/auth-config/index.ts` | Remove plugins, social providers |
| `packages/auth-config/client.ts` | `packages/auth-config/client.ts` | Update baseURL |
| `apps/sso-server/app/api/auth/[...all]/route.ts` | `apps/auth/app/api/auth/[...all]/route.ts` | Same CORS pattern |
| `apps/sso-server/app/(auth)/layout.tsx` | `apps/auth/app/(auth)/layout.tsx` | None |
| `apps/sso-server/app/(auth)/signin/` | `apps/auth/app/(auth)/signin/` | Remove social buttons |
| `apps/sso-server/app/(auth)/signup/` | `apps/auth/app/(auth)/signup/` | Remove social buttons, email verify |
| `apps/sso-server/lib/schemas/auth.ts` | `apps/auth/lib/schemas/auth.ts` | Simplify password rules |
| `apps/sso-server/components/auth/password-input.tsx` | `apps/auth/components/auth/password-input.tsx` | None |
| `apps/sso-server/components/auth/form-error.tsx` | `apps/auth/components/auth/form-error.tsx` | None |

## Dependencies

### packages/auth-database/package.json
```json
{
  "dependencies": {
    "@neondatabase/serverless": "^1.0.2",
    "drizzle-orm": "^0.44.7"
  },
  "devDependencies": {
    "drizzle-kit": "^0.31.7"
  }
}
```

### packages/auth-config/package.json
```json
{
  "dependencies": {
    "@repo/auth-database": "workspace:*",
    "better-auth": "latest"
  }
}
```

### apps/auth/package.json (key deps)
```json
{
  "dependencies": {
    "@repo/auth-config": "workspace:*",
    "next": "15.x",
    "react": "^18",
    "react-hook-form": "^7",
    "@hookform/resolvers": "^3",
    "zod": "^3",
    "lucide-react": "latest",
    "tailwindcss": "^3"
  }
}
```
