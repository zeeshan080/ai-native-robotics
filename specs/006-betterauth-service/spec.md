# Feature Specification: BetterAuth Authentication Service

**Feature Branch**: `006-betterauth-service`
**Created**: 2025-11-30
**Status**: Draft
**Input**: Add BetterAuth authentication as a standalone Next.js service. Copy patterns from existing SSO project. Features: email/password sign-up, sign-in, session management. Separate NeonDB with Drizzle ORM. Skip email verification for MVP. Port 3001. Integrate with Docusaurus and FastAPI.

**Reference Implementation**: `/home/dell/pana-sso/sso/sso-monorepo` (working BetterAuth SSO project to copy patterns from)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Account (Priority: P1)

A new visitor to the AI-Native Robotics Textbook wants to create an account so they can access personalized learning features.

**Why this priority**: Account creation is the gateway to all authenticated features. Without this, no other user stories can function.

**Independent Test**: Visit auth service at port 3001, complete sign-up form with email and password, verify account is created and user is logged in.

**Acceptance Scenarios**:

1. **Given** a visitor on the sign-up page, **When** they enter valid email, name, and password (8+ characters), **Then** account is created and user is redirected to the docs site as authenticated.
2. **Given** a visitor on the sign-up page, **When** they enter an email that already exists, **Then** they see an error message indicating the account exists.
3. **Given** a visitor on the sign-up page, **When** they enter a password shorter than 8 characters, **Then** they see a validation error.

---

### User Story 2 - Sign In to Existing Account (Priority: P1)

A returning user wants to sign in with their existing email and password to resume their personalized learning experience.

**Why this priority**: Sign-in is equally critical as sign-up - users must be able to access their accounts repeatedly.

**Independent Test**: Navigate to sign-in page, enter valid credentials, verify user is authenticated and redirected to docs site with session active.

**Acceptance Scenarios**:

1. **Given** a user with an existing account on the sign-in page, **When** they enter correct email and password, **Then** they are authenticated and redirected to the docs site.
2. **Given** a user on the sign-in page, **When** they enter incorrect password, **Then** they see an "Invalid credentials" error message.
3. **Given** a user on the sign-in page, **When** they enter a non-existent email, **Then** they see an "Invalid credentials" error message (same as wrong password for security).

---

### User Story 3 - Maintain Session Across Sites (Priority: P1)

An authenticated user navigating between the auth service and docs site expects to remain logged in without re-authenticating.

**Why this priority**: Session persistence is fundamental to user experience - without it, authentication is useless.

**Independent Test**: Sign in on auth service, navigate to docs site, verify user is recognized as authenticated and their identity is available to the application.

**Acceptance Scenarios**:

1. **Given** an authenticated user on the auth service, **When** they navigate to the docs site, **Then** the docs site recognizes them as logged in.
2. **Given** an authenticated user's session that is 7 days old, **When** they visit any site, **Then** the session is expired and they must re-authenticate.
3. **Given** an authenticated user on the docs site, **When** they click "Sign Out", **Then** their session is terminated across all sites.

---

### User Story 4 - Backend API Authorization (Priority: P2)

The FastAPI backend needs to verify that API requests come from authenticated users and identify who is making the request.

**Why this priority**: Required for personalization features to work with authenticated users instead of anonymous UUIDs.

**Independent Test**: Make API request from docs site to FastAPI backend, verify backend can validate the auth token and extract user identity.

**Acceptance Scenarios**:

1. **Given** an authenticated user on the docs site, **When** an API request is made to the backend, **Then** the backend receives and validates the user's authentication.
2. **Given** an unauthenticated visitor, **When** an API request is made to a protected endpoint, **Then** the backend returns a 401 Unauthorized response.
3. **Given** an authenticated user's expired session, **When** an API request is made, **Then** the backend returns a 401 and the user is prompted to re-authenticate.

---

### User Story 5 - Docusaurus Login Integration (Priority: P1)

Users browsing the docs site need a visible login option in the navbar and must be prompted to login when accessing personalization features.

**Why this priority**: This is the user-facing entry point for authentication from the docs site - critical for discoverability and UX.

**Independent Test**: Visit docs site, see Login button in navbar, click it, get redirected to auth service, login, return to docs site as authenticated user.

**Acceptance Scenarios**:

1. **Given** an unauthenticated visitor on the docs site, **When** they view the navbar, **Then** they see a "Login" button.
2. **Given** an unauthenticated visitor, **When** they click the Login button in the navbar, **Then** they are redirected to `http://localhost:3001/signin`.
3. **Given** an authenticated user on the docs site, **When** they view the navbar, **Then** they see their name/email and a "Logout" button instead of "Login".
4. **Given** an unauthenticated visitor viewing a lesson, **When** they click the "Personalize" tab, **Then** they see a "Login to Personalize" button instead of personalization options.
5. **Given** an unauthenticated visitor on a lesson page, **When** they click "Login to Personalize", **Then** they are redirected to auth service with a `callbackUrl` parameter that includes the current page URL.
6. **Given** a user who logged in from the Personalize tab, **When** authentication completes, **Then** they are redirected back to the exact lesson page they came from.
7. **Given** an authenticated user viewing a lesson, **When** they click the "Personalize" tab, **Then** they see the full personalization options (not a login prompt).

---

### Edge Cases

- What happens when a user tries to access the docs site without signing in? → They can browse freely but personalization features prompt for sign-in.
- What happens if the auth service is unavailable? → The docs site shows a friendly error and allows browsing without personalization.
- What happens if a user's password is compromised? → Password reset flow (deferred to future iteration).
- What happens during network interruption during sign-up? → User sees a retry option; partial registrations are cleaned up.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a standalone authentication service accessible at port 3001
- **FR-002**: System MUST allow users to create accounts with email, name, and password
- **FR-003**: System MUST validate passwords are at least 8 characters with reasonable complexity
- **FR-004**: System MUST allow users to sign in with email and password
- **FR-005**: System MUST maintain user sessions for 7 days with automatic refresh
- **FR-006**: System MUST share session state between auth service (3001), docs site (3000), and backend (8000)
- **FR-007**: System MUST store user data in a separate NeonDB PostgreSQL database using Drizzle ORM
- **FR-008**: System MUST expose session validation endpoints for the FastAPI backend
- **FR-009**: System MUST handle CORS correctly for cross-origin requests between services
- **FR-010**: System MUST display user-friendly error messages for authentication failures
- **FR-011**: System MUST allow users to sign out, terminating their session across all services
- **FR-012**: System MUST reuse patterns and code from the reference SSO implementation at `/home/dell/pana-sso/sso/sso-monorepo`

### Non-Functional Requirements

- **NFR-001**: Authentication response time MUST be under 2 seconds
- **NFR-002**: System MUST securely hash passwords (never store plaintext)
- **NFR-003**: System MUST use HTTPS-only cookies in production
- **NFR-004**: System MUST not expose sensitive error details to users

### Key Entities

- **User**: Represents an authenticated user with id, email, name, email verification status, profile image, and timestamps
- **Session**: Represents an active login session with id, token, expiration, IP address, user agent, and user reference
- **Account**: Represents authentication credentials with provider type, password hash, and user reference
- **Verification**: Represents email verification or password reset tokens (for future use)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete account creation (sign-up) in under 1 minute
- **SC-002**: Users can sign in to their account in under 30 seconds
- **SC-003**: Session remains valid for 7 days without requiring re-authentication
- **SC-004**: Docs site correctly identifies authenticated users on page load
- **SC-005**: FastAPI backend correctly validates authentication for 100% of protected requests
- **SC-006**: Zero plaintext passwords stored in database (verified by schema inspection)
- **SC-007**: CORS configuration correctly blocks unauthorized origins

## Assumptions

- User will provide NeonDB connection string for the auth database
- Email verification is intentionally skipped for MVP (users can sign in immediately after sign-up)
- Password reset functionality is deferred to a future iteration
- Social OAuth providers (Google, GitHub) are not required for MVP
- The reference SSO project structure and patterns are the source of truth for BetterAuth configuration

## Out of Scope

- Email verification flow
- Password reset/forgot password flow
- Social OAuth providers (Google, GitHub, etc.)
- Two-factor authentication
- Admin dashboard for user management
- Rate limiting (can be added later)
- OIDC provider functionality

## Dependencies

- Existing docs site at `apps/docs` (port 3000)
- Existing FastAPI backend at `packages/chatkit-backend` (port 8000)
- Reference SSO implementation at `/home/dell/pana-sso/sso/sso-monorepo`
- NeonDB PostgreSQL database (separate from personalization database)
- BetterAuth library and Drizzle ORM
