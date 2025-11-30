/**
 * Trusted origins for callback URL validation
 * Only allow redirects to these origins for security
 */
const TRUSTED_ORIGINS = [
  'http://localhost:3000', // Docs site
  'http://localhost:3001', // Auth service
  'http://localhost:8000', // API service
];

/**
 * Validates a callback URL against trusted origins
 * @param url - The callback URL from search params
 * @returns A validated URL string or default URL if invalid
 */
export function validateCallbackUrl(url: string | null): string {
  const defaultUrl = 'http://localhost:3000';

  if (!url) {
    return defaultUrl;
  }

  try {
    const parsed = new URL(url);
    const origin = parsed.origin;

    if (TRUSTED_ORIGINS.includes(origin)) {
      return url;
    }
  } catch {
    // Invalid URL format
    console.warn('Invalid callback URL format:', url);
  }

  // Return default if URL is not from a trusted origin
  return defaultUrl;
}
