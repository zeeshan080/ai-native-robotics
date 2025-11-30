import { z } from 'zod';

/**
 * Sign Up Form Schema
 * Validates email, password (simplified), and name
 */
export const signUpSchema = z.object({
  email: z.string()
    .min(1, 'Email is required')
    .email('Invalid email format')
    .max(255, 'Email is too long'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters'),
  name: z.string()
    .min(1, 'Name is required')
    .max(100, 'Name is too long'),
});

export type SignUpFormData = z.infer<typeof signUpSchema>;

/**
 * Sign In Form Schema
 * Validates email and password (no complexity check on login)
 */
export const signInSchema = z.object({
  email: z.string()
    .min(1, 'Email is required')
    .email('Invalid email format'),
  password: z.string()
    .min(1, 'Password is required'),
});

export type SignInFormData = z.infer<typeof signInSchema>;
