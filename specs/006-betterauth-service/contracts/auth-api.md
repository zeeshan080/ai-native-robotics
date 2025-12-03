# API Contract: BetterAuth Authentication Service

**Base URL**: `http://localhost:3001/api/auth`
**Content-Type**: `application/json`

## Overview

BetterAuth provides a REST API for authentication. All endpoints are handled by the BetterAuth library through the catch-all route at `/api/auth/[...all]`.

## Endpoints

### Sign Up

Create a new user account with email and password.

**Endpoint**: `POST /api/auth/sign-up/email`

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
```

**Success Response** (200):
```json
{
  "user": {
    "id": "abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerified": false,
    "image": null,
    "createdAt": "2025-11-30T10:00:00.000Z",
    "updatedAt": "2025-11-30T10:00:00.000Z"
  },
  "session": {
    "id": "session123",
    "token": "sess_xxxxx",
    "expiresAt": "2025-12-07T10:00:00.000Z"
  }
}
```

**Error Response** (400):
```json
{
  "error": {
    "code": "USER_ALREADY_EXISTS",
    "message": "User with this email already exists"
  }
}
```

**Validation**:
- `email`: Required, valid email format, max 255 chars
- `password`: Required, min 8 characters
- `name`: Required, max 100 chars

---

### Sign In

Authenticate an existing user.

**Endpoint**: `POST /api/auth/sign-in/email`

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Success Response** (200):
```json
{
  "user": {
    "id": "abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerified": false,
    "image": null,
    "createdAt": "2025-11-30T10:00:00.000Z",
    "updatedAt": "2025-11-30T10:00:00.000Z"
  },
  "session": {
    "id": "session456",
    "token": "sess_xxxxx",
    "expiresAt": "2025-12-07T10:00:00.000Z"
  }
}
```

**Error Response** (401):
```json
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
}
```

**Cookies Set**:
- `better-auth.session_token`: Session token for authentication

---

### Get Session

Retrieve current user session information.

**Endpoint**: `GET /api/auth/session`

**Headers**:
- Cookie: `better-auth.session_token=sess_xxxxx`

**Success Response** (200):
```json
{
  "user": {
    "id": "abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerified": false,
    "image": null,
    "createdAt": "2025-11-30T10:00:00.000Z",
    "updatedAt": "2025-11-30T10:00:00.000Z"
  },
  "session": {
    "id": "session456",
    "token": "sess_xxxxx",
    "expiresAt": "2025-12-07T10:00:00.000Z"
  }
}
```

**No Session Response** (200):
```json
{
  "user": null,
  "session": null
}
```

---

### Sign Out

Terminate the current session.

**Endpoint**: `POST /api/auth/sign-out`

**Headers**:
- Cookie: `better-auth.session_token=sess_xxxxx`

**Success Response** (200):
```json
{
  "success": true
}
```

**Cookies Cleared**:
- `better-auth.session_token`: Removed

---

## CORS Configuration

The auth service allows cross-origin requests from:
- `http://localhost:3000` (Docusaurus docs)
- `http://localhost:3001` (Auth service itself)
- `http://localhost:8000` (FastAPI backend)

**Required Headers**:
```
Access-Control-Allow-Origin: <requesting-origin>
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

## Client Usage Examples

### JavaScript/TypeScript (using BetterAuth client)

```typescript
import { createAuthClient } from "better-auth/client";

const authClient = createAuthClient({
  baseURL: "http://localhost:3001",
  fetchOptions: {
    credentials: "include",
  },
});

// Sign up
const signUpResult = await authClient.signUp.email({
  email: "user@example.com",
  password: "securepassword123",
  name: "John Doe",
});

// Sign in
const signInResult = await authClient.signIn.email({
  email: "user@example.com",
  password: "securepassword123",
});

// Get session
const session = await authClient.getSession();

// Sign out
await authClient.signOut();
```

### Fetch API

```typescript
// Sign in
const response = await fetch("http://localhost:3001/api/auth/sign-in/email", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  credentials: "include",
  body: JSON.stringify({
    email: "user@example.com",
    password: "securepassword123",
  }),
});

// Get session
const sessionResponse = await fetch("http://localhost:3001/api/auth/session", {
  credentials: "include",
});
```

### Python (FastAPI backend validation)

```python
import httpx

async def validate_session(session_cookie: str) -> dict | None:
    """Validate session by calling auth service."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:3001/api/auth/session",
            cookies={"better-auth.session_token": session_cookie}
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("user"):
                return data["user"]

    return None
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `USER_ALREADY_EXISTS` | 400 | Email already registered |
| `INVALID_CREDENTIALS` | 401 | Wrong email or password |
| `SESSION_EXPIRED` | 401 | Session has expired |
| `VALIDATION_ERROR` | 400 | Invalid input data |

## Rate Limiting

Not implemented for MVP. Consider adding in production:
- Sign up: 5 requests per minute per IP
- Sign in: 10 requests per minute per IP
- Session: 60 requests per minute per IP
