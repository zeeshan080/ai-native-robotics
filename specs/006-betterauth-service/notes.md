# BetterAuth Service - Implementation Notes

## Deviations from Original Plan

### 1. Simplified Authentication
- **Planned**: Full BetterAuth with OIDC, JWT plugins, social OAuth
- **Implemented**: Email/password only (MVP scope)
- **Reason**: Reduce complexity for hackathon; social OAuth can be added later

### 2. Email Verification
- **Planned**: Email verification flow
- **Implemented**: Skipped for MVP
- **Reason**: Requires SMTP setup; can be enabled later by uncommenting plugin

### 3. Password Complexity
- **Planned**: Complex password requirements (uppercase, lowercase, numbers, symbols)
- **Implemented**: Minimum 8 characters only
- **Reason**: Simpler UX for hackathon; can be enhanced later

### 4. Session Duration
- **Planned**: Standard BetterAuth defaults
- **Implemented**: 7 days with daily refresh
- **Reason**: Better UX for returning students; documented in auth-config

### 5. FastAPI Integration Location
- **Planned**: Could be in apps/chatkit-backend
- **Implemented**: In packages/chatkit-backend
- **Reason**: Followed existing project structure where chatkit-backend is a package

## Implementation Decisions

### Cross-Site Session Strategy
- Using HTTP-only cookies with `SameSite=Lax`
- `credentials: 'include'` on all fetch requests
- CORS configured with specific origins (not wildcard)
- Trusted origins defined in auth-config

### Package Structure
- `@repo/auth-database`: Schema and database connection
- `@repo/auth-config`: Server and client auth configuration
- `apps/auth`: Next.js frontend (signin/signup/account)

### Environment Variables
- `DATABASE_URL`: NeonDB connection string
- `BETTER_AUTH_SECRET`: 32+ character secret for session signing
- `BETTER_AUTH_URL`: Auth service URL (http://localhost:3001)
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed origins

## Known Limitations

1. **No password reset flow** - Users cannot reset forgotten passwords
2. **No email change** - Users cannot change their email address
3. **No account deletion** - Self-service account deletion not implemented
4. **Single session only** - No multi-device session management UI

## Future Enhancements

1. Add social OAuth providers (Google, GitHub)
2. Implement email verification
3. Add password reset flow
4. Add account settings page (change password, delete account)
5. Add session management (view active sessions, logout all)
6. Add rate limiting to auth endpoints
7. Add CSRF protection for mutations

## Testing Notes

### Manual Testing Checklist
- [ ] Sign up with new email
- [ ] Sign in with existing account
- [ ] Sign out from navbar
- [ ] Visit /account page while authenticated
- [ ] Verify redirect to signin when not authenticated
- [ ] Test cross-origin session from docs site (localhost:3000)
- [ ] Test backend auth middleware (/api/protected/me)

### Environment Setup
1. Copy `.env.example` to `.env` in apps/auth
2. Set `DATABASE_URL` to NeonDB connection
3. Generate `BETTER_AUTH_SECRET` with: `openssl rand -base64 32`
4. Run database migration: `pnpm --filter @repo/auth-database db:push`
5. Start auth service: `pnpm --filter auth dev`
