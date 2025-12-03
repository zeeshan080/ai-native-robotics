'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useSearchParams } from 'next/navigation';
import { authClient } from '@repo/auth-config/client';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  Button,
  Input
} from '@repo/ui';
import { signInSchema, type SignInFormData } from '@/lib/schemas/auth';
import { FormError } from '@/components/auth/form-error';
import { PasswordInput } from '@/components/auth/password-input';
import { validateCallbackUrl } from '@/lib/utils/callback-url';
import { Loader2 } from 'lucide-react';

export function SignInForm() {
  const searchParams = useSearchParams();
  const [formError, setFormError] = useState<string>('');

  const form = useForm<SignInFormData>({
    resolver: zodResolver(signInSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  const { isSubmitting } = form.formState;

  async function onSubmit(data: SignInFormData) {
    try {
      setFormError('');

      // Use better-auth client for sign in
      const result = await authClient.signIn.email({
        email: data.email,
        password: data.password,
      });

      if (result.error) {
        // Handle specific error cases
        const errorMessage = result.error.message || 'Sign in failed';

        // Check for invalid credentials
        if (
          errorMessage.includes('INVALID_CREDENTIALS') ||
          errorMessage.includes('Invalid credentials') ||
          errorMessage.includes('Invalid email or password')
        ) {
          setFormError('Invalid email or password');
        } else if (
          errorMessage.includes('USER_NOT_FOUND') ||
          errorMessage.includes('User not found')
        ) {
          setFormError('No account found with this email');
        } else {
          setFormError(errorMessage);
        }

        return;
      }

      // Success - get session token from response and redirect
      if (result.data) {
        // BetterAuth returns the session token directly in result.data.token
        const sessionToken = result.data.token;

        console.log('[SignIn] Result data:', JSON.stringify(result.data, null, 2));

        if (!sessionToken) {
          console.error('[SignIn] No token in response:', result.data);
          setFormError('Session token not found in response');
          return;
        }

        // Redirect with token in URL (will be extracted and stored in localStorage)
        const callbackUrl = validateCallbackUrl(searchParams.get('callbackUrl'));
        const separator = callbackUrl.includes('?') ? '&' : '?';
        window.location.href = `${callbackUrl}${separator}session_token=${sessionToken}`;
      }
    } catch (error) {
      console.error('Signin error:', error);
      setFormError('An unexpected error occurred. Please try again.');
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        {formError && <FormError message={formError} />}

        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input
                  type="email"
                  placeholder="john@example.com"
                  autoComplete="email"
                  disabled={isSubmitting}
                  autoFocus
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <PasswordInput
                  placeholder="••••••••"
                  autoComplete="current-password"
                  disabled={isSubmitting}
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button
          type="submit"
          className="w-full"
          disabled={isSubmitting}
        >
          {isSubmitting ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Signing in...
            </>
          ) : (
            'Sign in'
          )}
        </Button>
      </form>
    </Form>
  );
}
