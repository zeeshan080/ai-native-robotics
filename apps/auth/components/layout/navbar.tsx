'use client';

import Link from 'next/link';
import { useSessionContext } from '@/lib/providers/session-provider';
import { signOut } from '@/lib/auth/signout';
import { Button } from '@repo/ui';
import { Loader2, LogOut, User } from 'lucide-react';

const docsUrl = process.env.NEXT_PUBLIC_DOCS_URL || 'http://localhost:3000';

export function Navbar() {
  const { user, isLoading, isAuthenticated } = useSessionContext();

  return (
    <nav className="border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center">
            <Link href={docsUrl} className="text-xl font-bold text-blue-600">
              AI Robotics
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            {isLoading ? (
              <Loader2 className="h-5 w-5 animate-spin text-gray-400" />
            ) : isAuthenticated && user ? (
              <>
                <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                  <User className="h-4 w-4 mr-2" />
                  {user.name || user.email}
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => signOut()}
                >
                  <LogOut className="h-4 w-4 mr-2" />
                  Sign out
                </Button>
              </>
            ) : (
              <>
                <Link href="/signin">
                  <Button variant="ghost" size="sm">Sign in</Button>
                </Link>
                <Link href="/signup">
                  <Button size="sm">Get started</Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
