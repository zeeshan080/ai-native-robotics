import type { Metadata } from "next";
import { Inter } from 'next/font/google';
import "./globals.css";
import { SessionProvider } from '@/lib/providers/session-provider';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: "AI-Native Robotics Auth",
  description: "Authentication for AI-Native Physical AI & Humanoid Robotics Textbook",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <SessionProvider>
          {children}
        </SessionProvider>
      </body>
    </html>
  );
}
