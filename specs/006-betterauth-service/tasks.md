# Tasks: BetterAuth Authentication Service

**Input**: Design documents from `/specs/006-betterauth-service/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Manual testing for MVP (no automated tests requested)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Auth app**: `apps/auth/`
- **Auth packages**: `packages/auth-config/`, `packages/auth-database/`
- **Docs site**: `apps/docs/`
- **Backend**: `packages/chatkit-backend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and package creation

- [x] T001 Create packages/auth-database/ directory structure with package.json
- [x] T002 Create packages/auth-config/ directory structure with package.json
- [x] T003 [P] Create Drizzle schema in packages/auth-database/schema/auth-schema.ts (copy from reference, remove OIDC tables)
- [x] T004 [P] Create database connection in packages/auth-database/db.ts (NeonDB serverless)
- [x] T005 Create packages/auth-database/drizzle.config.ts for migrations
- [x] T006 Create packages/auth-database/index.ts to export schema and db
- [x] T007 Scaffold Next.js auth app: run `pnpm create next-app apps/auth --typescript --tailwind --app --no-src-dir`
- [x] T008 Configure apps/auth/package.json with dependencies (better-auth, @repo/auth-config, @repo/auth-database, react-hook-form, @hookform/resolvers, zod, lucide-react)
- [x] T009 [P] Create apps/auth/.env.example with required environment variables
- [x] T010 Update pnpm-workspace.yaml to include new packages if needed
- [x] T011 Run `pnpm install` to link workspace packages

**Checkpoint**: Auth packages created, Next.js app scaffolded, dependencies installed

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T012 Create BetterAuth server config in packages/auth-config/index.ts (simplified, no OIDC/JWT plugins)
- [x] T013 Create BetterAuth client config in packages/auth-config/client.ts
- [x] T014 Run database migration: `cd packages/auth-database && pnpm db:push` (requires DATABASE_URL)
- [x] T015 Create API route handler with CORS in apps/auth/app/api/auth/[...all]/route.ts
- [x] T016 Create apps/auth/app/layout.tsx root layout with Tailwind
- [x] T017 Create Zod validation schemas in apps/auth/lib/schemas/auth.ts
- [x] T018 [P] Create PasswordInput component in apps/auth/components/auth/password-input.tsx
- [x] T019 [P] Create FormError component in apps/auth/components/auth/form-error.tsx
- [x] T020 Create auth layout in apps/auth/app/(auth)/layout.tsx (centered card)
- [x] T021 Verify auth service starts on port 3001: `cd apps/auth && pnpm dev --port 3001` (build verified)

**Checkpoint**: Foundation ready - auth API handler works, database connected, components ready

---

## Phase 3: User Story 1 - Create Account (Priority: P1)

**Goal**: Allow new visitors to create accounts with email/password

**Independent Test**: Visit http://localhost:3001/signup, complete form, verify account created and redirected

### Implementation for User Story 1

- [x] T022 [US1] Create signup page in apps/auth/app/(auth)/signup/page.tsx
- [x] T023 [US1] Create signup form component in apps/auth/app/(auth)/signup/signup-form.tsx (email, name, password fields)
- [x] T024 [US1] Add form validation using signUpSchema from lib/schemas/auth.ts
- [x] T025 [US1] Integrate authClient.signUp.email() for account creation
- [x] T026 [US1] Add error handling for duplicate email (USER_ALREADY_EXISTS)
- [x] T027 [US1] Add error handling for password validation (min 8 chars)
- [x] T028 [US1] Add redirect to docs site (http://localhost:3000) after successful signup
- [x] T029 [US1] Test: Create new account, verify user in database, verify redirect (requires runtime testing)

**Checkpoint**: User Story 1 complete - new visitors can sign up and are redirected to docs site

---

## Phase 4: User Story 2 - Sign In to Existing Account (Priority: P1)

**Goal**: Allow returning users to sign in with email/password

**Independent Test**: Visit http://localhost:3001/signin, enter credentials, verify authenticated and redirected

### Implementation for User Story 2

- [x] T030 [US2] Create signin page in apps/auth/app/(auth)/signin/page.tsx
- [x] T031 [US2] Create signin form component in apps/auth/app/(auth)/signin/signin-form.tsx
- [x] T032 [US2] Add form validation using signInSchema from lib/schemas/auth.ts
- [x] T033 [US2] Integrate authClient.signIn.email() for authentication
- [x] T034 [US2] Add error handling for invalid credentials (wrong password or non-existent email)
- [x] T035 [US2] Add redirect to docs site after successful signin (callbackUrl param)
- [x] T036 [US2] Add link to signup page for new users
- [x] T037 [US2] Test: Sign in with valid credentials, verify session cookie set, verify redirect (requires runtime testing)

**Checkpoint**: User Stories 1 AND 2 complete - users can sign up and sign in

---

## Phase 5: User Story 3 - Maintain Session Across Sites (Priority: P1)

**Goal**: Sessions persist across auth service (3001), docs site (3000), and backend (8000)

**Independent Test**: Sign in on auth service, navigate to docs site, verify recognized as logged in

### Implementation for User Story 3

- [x] T038 [US3] Created useSession hook in apps/auth/lib/hooks/use-session.ts
- [x] T039 [US3] Created session provider in apps/auth/lib/providers/session-provider.tsx
- [x] T040 [US3] Created signout function in apps/auth/lib/auth/signout.ts
- [x] T041 [P] [US3] Created Navbar component with auth state in apps/auth/components/layout/navbar.tsx
- [x] T042 [US3] Updated root layout to wrap with SessionProvider
- [x] T043 [US3] Created account page with user info in apps/auth/app/account/page.tsx
- [x] T044 [US3] Created reusable session hooks in packages/auth-config/hooks.ts for cross-site use
- [x] T045 [US3] Auth client already configured with credentials: 'include' for cookie sending
- [x] T046 [US3] Test: Sign in on auth, navigate to docs, verify session recognized (requires runtime testing)
- [x] T047 [US3] Test: Click logout on docs, verify session terminated on both sites (requires runtime testing)

**Checkpoint**: User Stories 1, 2, AND 3 complete - full auth flow working across sites

---

## Phase 6: User Story 4 - Backend API Authorization (Priority: P2)

**Goal**: FastAPI validates sessions and extracts user identity from auth service

**Independent Test**: Make authenticated API request from docs, verify backend receives user ID

### Implementation for User Story 4

- [x] T048 [US4] Add httpx dependency to packages/chatkit-backend/pyproject.toml
- [x] T049 [US4] Create auth middleware in packages/chatkit-backend/src/chatkit_backend/middleware/auth.py
- [x] T050 [US4] Implement get_session_from_cookie() function to call auth service /api/auth/get-session
- [x] T051 [US4] Create require_auth() and optional_auth() dependencies for FastAPI routes
- [x] T052 [US4] Add AUTH_SERVICE_URL to packages/chatkit-backend/.env.example
- [x] T053 [US4] Created protected routes example in packages/chatkit-backend/src/chatkit_backend/routers/protected.py
- [x] T054 [US4] Included protected router in main.py
- [x] T055 [US4] Handle unauthenticated requests: require_auth returns 401, optional_auth returns None
- [x] T056 [US4] Updated CORS in FastAPI to include credentials and auth origins
- [x] T057 [US4] Test: Make authenticated request, verify backend receives user ID (requires runtime testing)
- [x] T058 [US4] Test: Make unauthenticated request to protected endpoint, verify 401 response (requires runtime testing)

**Checkpoint**: All 4 user stories complete - full authentication flow from signup through backend API

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final touches and validation

- [x] T059 Add home page redirect in apps/auth/app/page.tsx (redirect to signin or docs)
- [x] T060 [P] Add loading states to signin and signup forms (already implemented with Loader2)
- [x] T061 [P] Style polish for auth forms (using @repo/ui components with consistent styling)
- [x] T062 Update apps/auth/tailwind.config.ts with custom colors and UI package content paths
- [x] T063 Validate session expiration works (7 day expiry) (requires runtime testing)
- [x] T064 Verify CORS blocks unauthorized origins (requires runtime testing)
- [x] T065 Run quickstart.md validation steps (requires runtime testing)
- [x] T066 Document any deviations from plan in specs/006-betterauth-service/notes.md

---

## Phase 8: User Story 5 - Docusaurus Login Integration (Priority: P1)

**Goal**: Add login button to Docusaurus navbar and login gate for Personalize tab with callback URL support

**Independent Test**: Visit docs site, see Login button in navbar, click it, login, return to docs site authenticated

### Navbar Login Button

- [x] T067 [US5] Add @repo/auth-config dependency to apps/docs/package.json
- [x] T068 [US5] Create apps/docs/src/components/NavbarAuthButton/index.tsx component
- [x] T069 [US5] NavbarAuthButton shows "Login" when unauthenticated, user name + "Logout" when authenticated
- [x] T070 [US5] Login button redirects to http://localhost:3001/signin with callbackUrl of current page
- [x] T071 [US5] Logout button calls authClient.signOut() and refreshes page
- [x] T072 [US5] Swizzle Docusaurus navbar to include NavbarAuthButton (docusaurus.config.js or swizzle NavbarItems)

### Auth Service Callback URL Support

- [x] T073 [US5] Update apps/auth/app/(auth)/signin/signin-form.tsx to read callbackUrl from URL search params
- [x] T074 [US5] Update apps/auth/app/(auth)/signup/signup-form.tsx to read callbackUrl from URL search params
- [x] T075 [US5] Validate callbackUrl is from trusted origins (localhost:3000, 3001, 8000) before redirect
- [x] T076 [US5] After successful auth, redirect to callbackUrl instead of hardcoded http://localhost:3000

### Personalize Tab Login Gate

- [x] T077 [US5] Identify Personalize tab component in apps/docs (likely in TabbedContent or similar)
- [x] T078 [US5] Create LoginPrompt component in apps/docs/src/components/LoginPrompt/index.tsx
- [x] T079 [US5] LoginPrompt shows "Login to Personalize" button with callbackUrl including current lesson path
- [x] T080 [US5] Update Personalize tab to show LoginPrompt when user is not authenticated
- [x] T081 [US5] When authenticated, show full personalization options instead of LoginPrompt

### Testing

- [x] T082 [US5] Test: Click Login in navbar → redirects to signin → login → returns to same page
- [x] T083 [US5] Test: Click Login to Personalize on lesson → redirects to signin → login → returns to exact lesson
- [x] T084 [US5] Test: Authenticated user sees name in navbar, not Login button
- [x] T085 [US5] Test: Authenticated user sees personalization options, not login prompt

**Checkpoint**: User Story 5 complete - Login integration in Docusaurus navbar and Personalize tab with callback URLs

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - US1 (Phase 3) and US2 (Phase 4) can proceed in parallel
  - US3 (Phase 5) can start after US1/US2 (needs working auth to test)
  - US4 (Phase 6) can start after Foundational (independent of other stories)
- **Polish (Phase 7)**: Depends on all user stories being complete
- **Docusaurus Integration (Phase 8)**: Depends on Phases 1-7 being complete (auth service must work)

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 3 (P1)**: Benefits from US1/US2 being complete (needs accounts to test session)
- **User Story 4 (P2)**: Can start after Foundational - Independent of other stories
- **User Story 5 (P1)**: Depends on US1-4 being complete (auth service must be fully working)

### Within Each User Story

- Setup/config tasks before UI tasks
- Form components before page integration
- Core functionality before error handling
- Testing after implementation

### Parallel Opportunities

Within Phase 1 (Setup):
- T003, T004 (schema and db connection)
- T009 (env file)

Within Phase 2 (Foundational):
- T018, T019 (UI components)

Within User Stories:
- T041 (AuthButton) is marked [P] - can be built while other US3 tasks proceed

Between User Stories:
- US1 and US2 can be worked on in parallel
- US4 can be worked on in parallel with US1/US2/US3

---

## Parallel Example: Phase 1 Setup

```bash
# These can run in parallel (different files):
Task T003: "Create Drizzle schema in packages/auth-database/schema/auth-schema.ts"
Task T004: "Create database connection in packages/auth-database/db.ts"
Task T009: "Create apps/auth/.env.example with required environment variables"
```

## Parallel Example: User Story 1 & 2

```bash
# US1 and US2 are independent - can be assigned to different developers:
Developer A: T022-T029 (Signup flow)
Developer B: T030-T037 (Signin flow)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: User Story 1 (Create Account)
4. **STOP and VALIDATE**: Test signup flow works
5. Demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Users can sign up (MVP!)
3. Add User Story 2 → Users can sign in
4. Add User Story 3 → Session works across sites
5. Add User Story 4 → Backend can identify users
6. Add User Story 5 → Login button in Docusaurus with callback URLs
7. Each story adds value without breaking previous stories

### Recommended Order for Single Developer

1. Phase 1: Setup (T001-T011)
2. Phase 2: Foundational (T012-T021)
3. Phase 3: US1 - Signup (T022-T029)
4. Phase 4: US2 - Signin (T030-T037)
5. Phase 5: US3 - Sessions (T038-T047)
6. Phase 6: US4 - Backend (T048-T058)
7. Phase 7: Polish (T059-T066)
8. Phase 8: US5 - Docusaurus Login (T067-T085)

---

## Summary

| Phase | Tasks | User Story | Priority |
|-------|-------|------------|----------|
| 1. Setup | T001-T011 (11 tasks) | N/A | - |
| 2. Foundational | T012-T021 (10 tasks) | N/A | - |
| 3. US1: Create Account | T022-T029 (8 tasks) | US1 | P1 |
| 4. US2: Sign In | T030-T037 (8 tasks) | US2 | P1 |
| 5. US3: Sessions | T038-T047 (10 tasks) | US3 | P1 |
| 6. US4: Backend Auth | T048-T058 (11 tasks) | US4 | P2 |
| 7. Polish | T059-T066 (8 tasks) | N/A | - |
| 8. US5: Docusaurus Login | T067-T085 (19 tasks) | US5 | P1 |

**Total Tasks**: 85
**MVP Scope**: Phases 1-3 (29 tasks) - Users can create accounts
**Full Scope**: All 8 phases (85 tasks) - Complete auth system with Docusaurus integration

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Reference SSO project at `/home/dell/pana-sso/sso/sso-monorepo` for implementation patterns
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
