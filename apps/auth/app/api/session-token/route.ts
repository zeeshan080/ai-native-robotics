import { auth } from "@repo/auth-config";
import { NextRequest, NextResponse } from "next/server";

/**
 * GET /api/session-token
 *
 * Returns the session token for authenticated users.
 * Used for cross-domain authentication (GitHub Pages -> Vercel).
 *
 * The token can be stored in localStorage on the client and used
 * to validate sessions across different domains.
 */
export async function GET(request: NextRequest) {
  try {
    // Get session from cookie (server-side)
    const session = await auth.api.getSession({
      headers: request.headers,
    });

    if (!session || !session.user) {
      return NextResponse.json(
        { error: 'No active session' },
        { status: 401 }
      );
    }

    // Extract session token from cookies
    const sessionCookie = request.cookies.get('better-auth.session_token');

    if (!sessionCookie) {
      return NextResponse.json(
        { error: 'Session token not found' },
        { status: 401 }
      );
    }

    // Return the token
    return NextResponse.json({
      token: sessionCookie.value,
      user: {
        id: session.user.id,
        email: session.user.email,
        name: session.user.name,
      },
    });
  } catch (error) {
    console.error('Failed to get session token:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
