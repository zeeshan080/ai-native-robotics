import { redirect } from 'next/navigation';

/**
 * Auth App Home Page
 *
 * Redirects to the main docs site. Users should access
 * /signin or /signup directly, or be redirected from docs.
 */
export default function HomePage() {
  const docsUrl = process.env.NEXT_PUBLIC_DOCS_URL || 'http://localhost:3000';
  redirect(docsUrl);
}
