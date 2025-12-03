import { betterAuth } from 'better-auth';
import { drizzleAdapter } from 'better-auth/adapters/drizzle';
import { bearer } from 'better-auth/plugins';

/**
 * Lazy load database to avoid circular dependencies and initialization issues
 * Database is only loaded when auth methods are actually called
 */
const getDb = () => {
  const { db } = require('@repo/auth-database');
  return db;
};

/**
 * Dynamic trusted origins for CORS
 * Supports local development and production deployments
 */
const getTrustedOrigins = () => {
  const origins = [
    'http://localhost:3000', // Docusaurus docs site
    'http://localhost:3001', // Auth service (if separate)
    'http://localhost:8000', // FastAPI backend
    'https://zeeshan080.github.io', // GitHub Pages docs site (production)
  ];

  // Vercel deployment
  if (process.env.VERCEL_URL) {
    origins.push(`https://${process.env.VERCEL_URL}`);
  }

  // Custom production URL
  if (process.env.PRODUCTION_URL) {
    origins.push(process.env.PRODUCTION_URL);
  }

  // GitHub Pages docs site
  if (process.env.NEXT_PUBLIC_DOCS_URL) {
    origins.push(process.env.NEXT_PUBLIC_DOCS_URL);
  }

  // Additional CORS origins from environment
  if (process.env.CORS_ALLOWED_ORIGINS) {
    const additionalOrigins = process.env.CORS_ALLOWED_ORIGINS.split(',').map(o => o.trim());
    origins.push(...additionalOrigins);
  }

  // Remove duplicates
  return [...new Set(origins)];
};

/**
 * BetterAuth server configuration
 *
 * SIMPLIFIED for MVP - no OIDC, JWT plugins, or social OAuth
 *
 * Features enabled:
 * - Email/password authentication
 * - Session management (7-day expiry)
 * - Drizzle ORM adapter for PostgreSQL
 *
 * Environment variables required:
 * - BETTER_AUTH_SECRET: Secret key for signing sessions (generate with: openssl rand -base64 32)
 * - BETTER_AUTH_URL: Base URL for auth service (e.g., http://localhost:3001)
 *
 * Security notes:
 * - Email verification disabled for MVP (set requireEmailVerification: true for production)
 * - NEVER commit BETTER_AUTH_SECRET to version control
 * - Placeholder secret is ONLY for build-time; change in production
 */
export const auth = betterAuth({
  database: drizzleAdapter(getDb(), {
    provider: 'pg',
  }),

  // Secret for signing sessions - MUST be changed in production
  secret: process.env.BETTER_AUTH_SECRET || 'placeholder-secret-for-build-only-change-in-production',

  // Base URL for auth endpoints
  baseURL: process.env.BETTER_AUTH_URL || 'http://localhost:3001',

  // Email and password authentication
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Disabled for MVP - enable in production
    minPasswordLength: 8,
    maxPasswordLength: 128,
  },

  // Session configuration
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24,     // Update session every 24 hours
  },

  // CORS allowed origins
  trustedOrigins: getTrustedOrigins(),

  // Cross-domain cookie configuration for GitHub Pages + Vercel setup
  advanced: {
    crossSubDomainCookies: {
      enabled: true,
    },
    // Cookie configuration for cross-origin requests
    cookiePrefix: 'better-auth',
    useSecureCookies: process.env.NODE_ENV === 'production',
  },

  // Plugins for cross-domain auth support
  plugins: [
    bearer(), // Enables bearer token auth for cross-domain scenarios
  ],
});

export type Auth = typeof auth;
