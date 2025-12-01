import { auth } from "@repo/auth-config";
import { toNextJsHandler } from "better-auth/next-js";
import { NextRequest, NextResponse } from "next/server";

const handler = toNextJsHandler(auth);

// Get allowed origins at runtime (not build time)
function getAllowedOrigins(): string[] {
  const envOrigins = process.env.CORS_ALLOWED_ORIGINS || '';
  const docsUrl = process.env.NEXT_PUBLIC_DOCS_URL || '';

  const origins = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:8000',
    'https://zeeshan080.github.io', // GitHub Pages (hardcoded as fallback)
  ];

  // Add from CORS_ALLOWED_ORIGINS env var
  if (envOrigins) {
    const additional = envOrigins.split(',').map(o => o.trim()).filter(Boolean);
    origins.push(...additional);
  }

  // Add docs URL if set
  if (docsUrl) {
    // Extract origin from full URL (remove path)
    try {
      const url = new URL(docsUrl);
      origins.push(url.origin);
    } catch {
      origins.push(docsUrl);
    }
  }

  // Remove duplicates
  return [...new Set(origins)];
}

function getCorsHeaders(origin: string | null) {
  const allowedOrigins = getAllowedOrigins();

  const headers: Record<string, string> = {
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Credentials': 'true',
  };

  // Check if origin is allowed
  if (origin && allowedOrigins.includes(origin)) {
    headers['Access-Control-Allow-Origin'] = origin;
  } else if (!origin) {
    // Allow same-origin requests
    headers['Access-Control-Allow-Origin'] = allowedOrigins[0];
  }

  return headers;
}

// Handle OPTIONS preflight requests
export async function OPTIONS(request: NextRequest) {
  const origin = request.headers.get('origin');
  const corsHeaders = getCorsHeaders(origin);

  return new NextResponse(null, {
    status: 204,
    headers: corsHeaders,
  });
}

// Wrap GET handler with CORS headers
export async function GET(request: NextRequest) {
  const origin = request.headers.get('origin');
  const corsHeaders = getCorsHeaders(origin);

  const response = await handler.GET(request);

  // Add CORS headers to response
  Object.entries(corsHeaders).forEach(([key, value]) => {
    response.headers.set(key, value);
  });

  return response;
}

// Wrap POST handler with CORS headers
export async function POST(request: NextRequest) {
  const origin = request.headers.get('origin');
  const corsHeaders = getCorsHeaders(origin);

  // Clone request and ensure valid JSON body (better-auth fails on empty body)
  let modifiedRequest = request;
  const contentType = request.headers.get('content-type');

  if (contentType?.includes('application/json')) {
    try {
      const text = await request.text();
      // If body is empty, provide empty object
      const body = text ? text : '{}';

      modifiedRequest = new NextRequest(request.url, {
        method: request.method,
        headers: request.headers,
        body: body,
      });
    } catch {
      // If we can't read body, create request with empty object
      modifiedRequest = new NextRequest(request.url, {
        method: request.method,
        headers: request.headers,
        body: '{}',
      });
    }
  }

  const response = await handler.POST(modifiedRequest);

  // Add CORS headers to response
  Object.entries(corsHeaders).forEach(([key, value]) => {
    response.headers.set(key, value);
  });

  return response;
}
