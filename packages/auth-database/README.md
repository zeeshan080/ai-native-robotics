# @repo/auth-database

Drizzle ORM database schema and connection for BetterAuth authentication.

## Features

- **Drizzle ORM**: Type-safe database access
- **NeonDB**: Serverless Postgres connection
- **BetterAuth Schema**: User, session, account, and verification tables
- **Build-safe**: Graceful handling of missing DATABASE_URL during builds

## Tables

### user
- Core user information (id, name, email, emailVerified, image)
- Timestamps: createdAt, updatedAt

### session
- User sessions with token-based authentication
- Fields: token, expiresAt, ipAddress, userAgent
- Foreign key: userId → user.id (cascade delete)

### account
- OAuth and password accounts linked to users
- Fields: accountId, providerId, accessToken, refreshToken, password
- Foreign key: userId → user.id (cascade delete)

### verification
- Email verification and password reset tokens
- Fields: identifier, value, expiresAt

## Usage

```typescript
import { db, user, session } from '@repo/auth-database';

// Query users
const users = await db.select().from(user);

// Insert session
await db.insert(session).values({
  id: 'session-123',
  userId: 'user-456',
  token: 'token-789',
  expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
});
```

## Scripts

```bash
# Generate migrations
pnpm db:generate

# Push schema to database
pnpm db:push

# Open Drizzle Studio
pnpm db:studio
```

## Environment Variables

Required in `.env` at monorepo root:

```env
DATABASE_URL=postgresql://user:password@host/database
```

## Notes

- OIDC tables (jwks, oauthApplication, oauthAccessToken, oauthConsent) are NOT included
- Uses NeonDB serverless driver for optimal performance
- Schema follows BetterAuth conventions
