# Quickstart: BetterAuth Authentication Service

**Feature**: 006-betterauth-service
**Date**: 2025-11-30

## Prerequisites

- Node.js 20+
- pnpm 10+
- NeonDB account with a new database for auth
- Access to reference SSO project at `/home/dell/pana-sso/sso/sso-monorepo`

## Setup Steps

### 1. Create NeonDB Database

1. Go to [Neon Console](https://console.neon.tech/)
2. Create a new project for auth (separate from personalization)
3. Copy the connection string: `postgresql://...`

### 2. Create Auth Database Package

```bash
mkdir -p packages/auth-database/schema
cd packages/auth-database
```

Create `package.json`:
```json
{
  "name": "@repo/auth-database",
  "version": "0.0.0",
  "private": true,
  "main": "./index.ts",
  "types": "./index.ts",
  "scripts": {
    "db:generate": "drizzle-kit generate",
    "db:push": "drizzle-kit push",
    "db:studio": "drizzle-kit studio"
  },
  "dependencies": {
    "@neondatabase/serverless": "^1.0.2",
    "drizzle-orm": "^0.44.7"
  },
  "devDependencies": {
    "drizzle-kit": "^0.31.7"
  }
}
```

### 3. Create Auth Config Package

```bash
mkdir -p packages/auth-config
cd packages/auth-config
```

Create `package.json`:
```json
{
  "name": "@repo/auth-config",
  "version": "0.0.0",
  "private": true,
  "main": "./index.ts",
  "types": "./index.ts",
  "exports": {
    ".": "./index.ts",
    "./client": "./client.ts"
  },
  "dependencies": {
    "@repo/auth-database": "workspace:*",
    "better-auth": "latest"
  }
}
```

### 4. Create Auth App

```bash
cd apps
pnpm create next-app auth --typescript --tailwind --eslint --app --no-src-dir
cd auth
```

Add dependencies:
```bash
pnpm add @repo/auth-config @repo/auth-database better-auth react-hook-form @hookform/resolvers zod lucide-react
```

### 5. Configure Environment

Create `apps/auth/.env`:
```env
DATABASE_URL=postgresql://your-neon-connection-string
BETTER_AUTH_SECRET=your-32-character-secret-key-here
BETTER_AUTH_URL=http://localhost:3001
NEXT_PUBLIC_DOCS_URL=http://localhost:3000
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:8000
```

### 6. Apply Database Migrations

```bash
cd packages/auth-database
pnpm db:push
```

### 7. Start Development Servers

```bash
# Terminal 1: Auth service
cd apps/auth && pnpm dev --port 3001

# Terminal 2: Docs site
cd apps/docs && pnpm start

# Terminal 3: Backend
cd packages/chatkit-backend && uv run python -m chatkit_backend.main
```

## Verification

### Test Sign Up

1. Visit `http://localhost:3001/signup`
2. Enter name, email, password
3. Click "Create account"
4. Should be redirected to docs site

### Test Sign In

1. Visit `http://localhost:3001/signin`
2. Enter email, password
3. Click "Sign in"
4. Should be redirected to docs site

### Test Session

```bash
# Check session endpoint
curl -c cookies.txt -b cookies.txt \
  http://localhost:3001/api/auth/session
```

### Test CORS

```bash
# Test from docs site origin
curl -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -X OPTIONS \
  http://localhost:3001/api/auth/sign-in/email -v
```

## File Structure After Setup

```
ai-native-robotics/
├── apps/
│   ├── auth/
│   │   ├── app/
│   │   │   ├── api/auth/[...all]/route.ts
│   │   │   ├── (auth)/
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── signin/
│   │   │   │   └── signup/
│   │   │   └── layout.tsx
│   │   ├── components/auth/
│   │   ├── lib/schemas/auth.ts
│   │   └── .env
│   └── docs/
├── packages/
│   ├── auth-config/
│   │   ├── index.ts
│   │   └── client.ts
│   └── auth-database/
│       ├── db.ts
│       ├── index.ts
│       └── schema/auth-schema.ts
```

## Common Issues

### CORS Errors
- Check `CORS_ALLOWED_ORIGINS` includes all origins
- Ensure `credentials: 'include'` in fetch calls
- Verify `trustedOrigins` in auth config

### Session Not Persisting
- Check cookies are being set (DevTools > Application > Cookies)
- Ensure same origin policy is correct
- Check `sameSite` cookie attribute

### Database Connection Failed
- Verify `DATABASE_URL` is correct
- Check NeonDB project is active
- Try `pnpm db:studio` to test connection

## Next Steps

After basic auth is working:
1. Update `apps/docs/src/context/UserContext.tsx` to use auth
2. Add auth middleware to `packages/chatkit-backend`
3. Add login/logout button to docs site navbar
