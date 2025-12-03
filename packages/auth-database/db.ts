import { drizzle } from 'drizzle-orm/neon-http';
import { neon } from '@neondatabase/serverless';
import * as schema from './schema/auth-schema';

// Handle missing DATABASE_URL during build
const getDatabaseUrl = () => {
  if (process.env.DATABASE_URL) {
    return process.env.DATABASE_URL;
  }

  // During build, use placeholder
  if (process.env.NODE_ENV === 'production' || process.env.NEXT_PHASE === 'phase-production-build') {
    console.warn('DATABASE_URL not found during build, using placeholder');
    return 'postgresql://placeholder:placeholder@placeholder/placeholder';
  }

  throw new Error('DATABASE_URL is not set! Check your .env file.');
};

const databaseUrl = getDatabaseUrl();
const sql = neon(databaseUrl);

export const db = drizzle(sql, { schema });
