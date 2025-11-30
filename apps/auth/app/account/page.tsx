'use client';

import { useSessionContext } from '@/lib/providers/session-provider';
import { signOut } from '@/lib/auth/signout';
import { Navbar } from '@/components/layout/navbar';
import { Card, CardHeader, CardTitle, CardContent, Button } from '@repo/ui';
import { Loader2, User, Mail, LogOut } from 'lucide-react';
import { redirect } from 'next/navigation';
import { useEffect } from 'react';

export default function AccountPage() {
  const { user, isLoading, isAuthenticated } = useSessionContext();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      redirect('/signin');
    }
  }, [isLoading, isAuthenticated]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Navbar />
        <div className="flex justify-center items-center h-[60vh]">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      <main className="max-w-2xl mx-auto py-12 px-4">
        <Card>
          <CardHeader>
            <CardTitle>Your Account</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="flex items-center space-x-3">
              <User className="h-5 w-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-500">Name</p>
                <p className="font-medium">{user.name || 'Not set'}</p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <Mail className="h-5 w-5 text-gray-400" />
              <div>
                <p className="text-sm text-gray-500">Email</p>
                <p className="font-medium">{user.email}</p>
              </div>
            </div>

            <div className="pt-4 border-t">
              <Button
                variant="outline"
                onClick={() => signOut()}
                className="w-full"
              >
                <LogOut className="h-4 w-4 mr-2" />
                Sign out
              </Button>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
