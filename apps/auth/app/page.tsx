import { redirect } from 'next/navigation';

/**
 * Auth App Home Page
 *
 * Redirects to the main docs site. Users should access
 * /signin or /signup directly, or be redirected from docs.
 */
export default function HomePage() {
  redirect('http://localhost:3000');
}
