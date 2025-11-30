/**
 * Get the docs site URL from environment or default
 */
const getDocsUrl = () => process.env.NEXT_PUBLIC_DOCS_URL || 'http://localhost:3000';
const getAuthUrl = () => process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3001';

/**
 * Get trusted origins from environment or defaults
 */
const getTrustedOrigins = (): string[] => {
  const origins = [
    getDocsUrl(),
    getAuthUrl(),
    'http://localhost:3000', // Local docs
    'http://localhost:3001', // Local auth
    'http://localhost:8000', // Local API
  ];

  // Add production origins
  if (process.env.CORS_ALLOWED_ORIGINS) {
    origins.push(...process.env.CORS_ALLOWED_ORIGINS.split(','));
  }

  return [...new Set(origins)]; // Remove duplicates
};

/**
 * Validates a callback URL against trusted origins
 * @param url - The callback URL from search params
 * @returns A validated URL string or default URL if invalid
 */
export function validateCallbackUrl(url: string | null): string {
  const defaultUrl = getDocsUrl();

  if (!url) {
    return defaultUrl;
  }

  try {
    const parsed = new URL(url);
    const origin = parsed.origin;

    if (getTrustedOrigins().includes(origin)) {
      return url;
    }
  } catch {
    // Invalid URL format
    console.warn('Invalid callback URL format:', url);
  }

  // Return default if URL is not from a trusted origin
  return defaultUrl;

}

/**
 * Get the default docs URL for redirects
 */
export function getDefaultDocsUrl(): string {
  return getDocsUrl();
}
