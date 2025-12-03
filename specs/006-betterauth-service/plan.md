# Implementation Plan: BetterAuth Authentication Service

**Branch**: `006-betterauth-service` | **Date**: 2025-11-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-betterauth-service/spec.md`

## Summary

Add BetterAuth authentication as a standalone Next.js service (port 3001) with email/password authentication, session management, and cross-origin support for the existing Docusaurus docs site (3000) and FastAPI backend (8000). Uses patterns directly from the reference SSO project at `/home/dell/pana-sso/sso/sso-monorepo`.

## Technical Context

**Language/Version**: TypeScript 5.x (auth service), Python 3.11+ (backend integration)
**Primary Dependencies**: BetterAuth, Next.js 15, Drizzle ORM, React Hook Form, Zod
**Storage**: NeonDB PostgreSQL (separate database from personalization)
**Testing**: Manual testing for MVP
**Target Platform**: Linux/WSL (development), production deployment TBD
**Project Type**: Monorepo with apps + packages (Turborepo)
**Performance Goals**: Auth response < 2 seconds
**Constraints**: HTTPS-only cookies in production, no plaintext passwords
**Scale/Scope**: Single-tenant educational platform

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| **Auth Library: BetterAuth** | PASS | Using BetterAuth as required |
| **Data Storage: Neon Postgres** | PASS | Separate NeonDB for auth |
| **Frontend: Docusaurus 3** | PASS | Integrating with existing docs site |
| **Backend: FastAPI** | PASS | Adding auth validation to existing FastAPI |
| **Spec-First Development** | PASS | Created spec.md before plan.md |

**All gates passed - no violations.**

## Project Structure

### Documentation (this feature)

```text
specs/006-betterauth-service/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── auth-api.md      # API endpoint documentation
└── tasks.md             # Phase 2 output (via /sp.tasks)
```

### Source Code (repository root)

```text
ai-native-robotics/
├── apps/
│   ├── docs/                    # Existing Docusaurus site (port 3000)
│   │   └── src/
│   │       ├── context/
│   │       │   └── UserContext.tsx  # UPDATE: Add auth integration
│   │       └── components/
│   │           └── AuthButton.tsx   # NEW: Login/logout button
│   │
│   └── auth/                    # NEW: BetterAuth Next.js service (port 3001)
│       ├── app/
│       │   ├── api/auth/[...all]/
│       │   │   └── route.ts     # BetterAuth API handler
│       │   ├── (auth)/
│       │   │   ├── layout.tsx   # Centered card layout
│       │   │   ├── signin/
│       │   │   │   ├── page.tsx
│       │   │   │   └── signin-form.tsx
│       │   │   └── signup/
│       │   │       ├── page.tsx
│       │   │       └── signup-form.tsx
│       │   └── layout.tsx
│       ├── components/auth/
│       │   ├── password-input.tsx
│       │   └── form-error.tsx
│       └── lib/
│           └── schemas/auth.ts   # Zod validation schemas
│
├── packages/
│   ├── chatkit-backend/         # Existing FastAPI backend (port 8000)
│   │   └── src/chatkit_backend/
│   │       ├── middleware/
│   │       │   └── auth.py      # NEW: Session validation
│   │       └── routers/
│   │           └── *.py         # UPDATE: Use auth middleware
│   │
│   ├── auth-config/             # NEW: Shared BetterAuth configuration
│   │   ├── package.json
│   │   ├── index.ts             # Server-side auth config
│   │   └── client.ts            # Client-side auth config
│   │
│   └── auth-database/           # NEW: Drizzle schema + migrations
│       ├── package.json
│       ├── drizzle.config.ts
│       ├── db.ts
│       ├── index.ts
│       └── schema/
│           └── auth-schema.ts
```

**Structure Decision**: Monorepo with shared packages pattern (same as reference SSO project). Auth packages in `packages/` are reusable across apps. Auth app in `apps/auth/` is standalone.

## Architecture Decisions

### AD-001: Separate NeonDB for Auth
**Decision**: Use a separate NeonDB database for authentication, distinct from the personalization database.
**Rationale**:
- Clean separation of concerns
- Auth data (users, sessions) vs learning data (preferences, cache)
- Easier to manage access and backups
- Matches reference SSO pattern

### AD-002: Simplified BetterAuth Config
**Decision**: Strip OIDC, JWT plugins, and social OAuth from reference SSO config.
**Rationale**:
- MVP focuses on email/password only
- Reduces complexity and attack surface
- Can add OAuth later if needed
- Email verification skipped for faster onboarding

### AD-003: Session-Based Auth for FastAPI
**Decision**: Validate sessions by calling auth service `/api/auth/session` endpoint.
**Rationale**:
- No JWT complexity for MVP
- Session cookies automatically handled by BetterAuth
- FastAPI just needs to verify session is valid and extract user ID
- Simpler than JWKS verification

### AD-004: Cross-Origin Cookie Strategy
**Decision**: Use `sameSite: 'lax'` cookies with explicit trusted origins.
**Rationale**:
- BetterAuth handles cookie settings
- Trust localhost:3000, 3001, 8000 for development
- Production will use proper HTTPS and same-domain cookies

## Key Patterns from Reference SSO

### 1. Auth Config Pattern (packages/auth-config/index.ts)
```typescript
export const auth = betterAuth({
  database: drizzleAdapter(getDb(), { provider: 'pg' }),
  secret: process.env.BETTER_AUTH_SECRET,
  baseURL: process.env.BETTER_AUTH_URL,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,  // Skip for MVP
    minPasswordLength: 8,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7,  // 7 days
    updateAge: 60 * 60 * 24,       // Refresh daily
  },
  trustedOrigins: [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:8000',
  ],
});
```

### 2. Client Config Pattern (packages/auth-config/client.ts)
```typescript
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_AUTH_URL || 'http://localhost:3001',
  fetchOptions: {
    credentials: 'include',  // Essential for cross-origin cookies
  },
});
```

### 3. CORS Handler Pattern (apps/auth/app/api/auth/[...all]/route.ts)
```typescript
const allowedOrigins = ['http://localhost:3000', 'http://localhost:3001', 'http://localhost:8000'];

function getCorsHeaders(origin: string | null) {
  return {
    'Access-Control-Allow-Origin': origin && allowedOrigins.includes(origin) ? origin : allowedOrigins[0],
    'Access-Control-Allow-Credentials': 'true',
    // ... other headers
  };
}
```

### 4. Zod Schema Pattern (apps/auth/lib/schemas/auth.ts)
```typescript
export const signUpSchema = z.object({
  email: z.string().min(1).email().max(255),
  password: z.string().min(8),  // Simplified for MVP
  name: z.string().min(1).max(100),
});
```

## Environment Variables

### apps/auth/.env
```env
DATABASE_URL=postgresql://...  # Separate NeonDB for auth
BETTER_AUTH_SECRET=...         # 32+ character secret
BETTER_AUTH_URL=http://localhost:3001
NEXT_PUBLIC_DOCS_URL=http://localhost:3000
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:8000
```

### apps/docs/.env (add)
```env
NEXT_PUBLIC_AUTH_URL=http://localhost:3001
```

### packages/chatkit-backend/.env (add)
```env
AUTH_SERVICE_URL=http://localhost:3001
```

## Port Allocation

| Service | Port | Purpose |
|---------|------|---------|
| Docusaurus docs | 3000 | Main documentation site |
| BetterAuth service | 3001 | Authentication UI + API |
| FastAPI backend | 8000 | Personalization + chat API |

## Integration Points

### 1. Docusaurus → Auth Service
- Login button redirects to `http://localhost:3001/signin?callbackUrl=http://localhost:3000`
- After successful auth, user redirected back to docs site
- `UserContext.tsx` updated to use `authClient.getSession()` instead of localStorage UUID

### 2. Docusaurus Navbar Login Button
- Add `NavbarAuthButton` component to Docusaurus navbar (swizzle NavbarItems)
- Shows "Login" when unauthenticated, user name + "Logout" when authenticated
- Login redirects to auth service with current page as callbackUrl

### 3. Personalize Tab Login Gate
- When unauthenticated user clicks Personalize tab, show "Login to Personalize" button
- Button includes `callbackUrl` with full current page URL (including lesson path)
- After login, auth service redirects back to exact lesson page
- Pattern: `http://localhost:3001/signin?callbackUrl=${encodeURIComponent(window.location.href)}`

### 4. Docusaurus → FastAPI (with auth)
- API requests include session cookie (credentials: 'include')
- FastAPI validates session by calling auth service
- Extract user ID from session for personalization

### 5. Auth Service Callback Handling
- Signin/signup forms read `callbackUrl` from URL query params
- After successful auth, redirect to callbackUrl (defaults to docs site root)
- Validation: Only allow callbackUrl to trusted origins (localhost:3000, 3001, 8000)

### 6. FastAPI Session Validation
```python
async def validate_session(request: Request) -> Optional[str]:
    session_cookie = request.cookies.get('better-auth.session_token')
    if not session_cookie:
        return None

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{AUTH_SERVICE_URL}/api/auth/session",
            cookies={'better-auth.session_token': session_cookie}
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('user', {}).get('id')
    return None
```

## Complexity Tracking

> No violations detected - this plan follows constitution requirements.

| Item | Status |
|------|--------|
| Auth Library | BetterAuth (required) |
| Database | NeonDB (required) |
| Frontend | Docusaurus integration (compliant) |
| Backend | FastAPI validation (compliant) |
