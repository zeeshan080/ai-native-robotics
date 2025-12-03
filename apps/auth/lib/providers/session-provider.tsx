'use client';

import { createContext, useContext, ReactNode } from 'react';
import { useSession, type SessionData } from '@/lib/hooks/use-session';

const SessionContext = createContext<SessionData | null>(null);

export function SessionProvider({ children }: { children: ReactNode }) {
  const session = useSession();
  return (
    <SessionContext.Provider value={session}>
      {children}
    </SessionContext.Provider>
  );
}

export function useSessionContext(): SessionData {
  const context = useContext(SessionContext);
  if (!context) {
    throw new Error('useSessionContext must be used within SessionProvider');
  }
  return context;
}
