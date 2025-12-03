# Feature Specification: Content Personalization

**Feature Branch**: `005-content-personalization`
**Created**: 2025-11-30
**Status**: Draft
**Input**: User description: "Add content personalization with onboarding questionnaire and lesson adaptation based on user profile"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Complete Onboarding Questionnaire (Priority: P1)

A first-time visitor to the textbook is prompted to complete an onboarding questionnaire to personalize their learning experience. They answer 6 questions about their education level, programming experience, robotics background, AI/ML experience, learning goals, and preferred language.

**Why this priority**: This is the foundation for all personalization. Without user preferences stored, no personalization can occur. It establishes the user profile that drives all subsequent features.

**Independent Test**: Can be fully tested by visiting the site as a new user, completing the questionnaire, and verifying preferences are stored and retrievable.

**Acceptance Scenarios**:

1. **Given** a first-time visitor with no stored user_id, **When** they visit any lesson page, **Then** they are redirected to the onboarding questionnaire
2. **Given** a user on the onboarding page, **When** they complete all 6 questions and submit, **Then** their preferences are saved and they are redirected to the home page
3. **Given** a user who has completed onboarding, **When** they return to the site, **Then** they are not prompted to complete onboarding again

---

### User Story 2 - View Personalized Lesson Content (Priority: P1)

A student who has completed onboarding visits a lesson page and sees two tabs: "Original" and "Personalized". When they click "Personalized", the system generates content adapted to their profile (education level, experience, preferred language).

**Why this priority**: This is the core value proposition - delivering personalized educational content based on the user's background and preferences.

**Independent Test**: Can be fully tested by completing onboarding, navigating to a lesson, clicking "Personalized" tab, and verifying the content is adapted to the user's profile.

**Acceptance Scenarios**:

1. **Given** an onboarded user viewing a lesson, **When** the page loads, **Then** they see "Original" and "Personalized" tabs with "Original" selected by default
2. **Given** a user viewing the Original tab, **When** they click "Personalized", **Then** the system fetches personalized content based on their profile
3. **Given** a beginner programmer user, **When** they view personalized content, **Then** code explanations are expanded with simpler examples
4. **Given** a user with Urdu as preferred language, **When** they view personalized content, **Then** explanatory text is in Urdu while technical terms remain in English

---

### User Story 3 - Update Preferences (Priority: P2)

A returning user wants to update their learning preferences (e.g., they gained more programming experience or want to switch to a different language). They can access their profile settings and modify their preferences.

**Why this priority**: Users' knowledge and goals evolve over time. Allowing preference updates ensures continued relevance of personalized content.

**Independent Test**: Can be fully tested by accessing profile settings, modifying preferences, and verifying personalized content reflects the changes.

**Acceptance Scenarios**:

1. **Given** an onboarded user, **When** they access profile settings, **Then** they see their current preferences pre-filled
2. **Given** a user editing preferences, **When** they update and save, **Then** their new preferences are persisted
3. **Given** a user who updated preferences, **When** they view personalized content, **Then** the content reflects their updated profile

---

### User Story 4 - Cached Personalization (Priority: P3)

For performance, personalized content is cached after first generation. When a user revisits a lesson they've already personalized, the cached version loads instantly instead of regenerating.

**Why this priority**: Performance optimization improves user experience but is not essential for MVP functionality.

**Independent Test**: Can be fully tested by personalizing a lesson, navigating away, returning, and verifying instant load from cache.

**Acceptance Scenarios**:

1. **Given** a user requesting personalized content for the first time, **When** the content is generated, **Then** it is cached with a hash of the original content
2. **Given** a user revisiting a previously personalized lesson, **When** the original content hash matches, **Then** cached content is served immediately
3. **Given** a user who updated their preferences, **When** they revisit a previously personalized lesson, **Then** the cache is invalidated and new personalized content is generated

---

### User Story 5 - Browse Book Structure (Priority: P1)

A user can browse the complete book structure through an API that returns the hierarchical organization of Parts, Chapters, and Lessons. Content is stored in a cloud bucket and indexed in a vector database for RAG.

**Why this priority**: Book structure is foundational for progress tracking, recommendations, and RAG-based tutoring.

**Independent Test**: Call GET /api/content/book and verify complete hierarchy is returned with all parts, chapters, and lessons.

**Acceptance Scenarios**:

1. **Given** a user accessing the content API, **When** they request the book structure, **Then** they receive a complete hierarchy of parts → chapters → lessons
2. **Given** a lesson in the database, **When** the content is requested, **Then** the markdown is retrieved from the storage bucket
3. **Given** a lesson with embeddings, **When** a semantic search is performed, **Then** relevant lesson chunks are returned from the vector database

---

### User Story 6 - Track Learning Progress (Priority: P2)

A user's progress through the textbook is tracked automatically. When they start or complete a lesson, this is recorded and persisted. They can view their overall progress summary.

**Why this priority**: Progress tracking enables recommendations and helps users understand their learning journey.

**Independent Test**: Start a lesson → verify progress marked as "in_progress" → complete it → verify marked as "completed" → view progress summary.

**Acceptance Scenarios**:

1. **Given** a user viewing a lesson, **When** they start reading, **Then** their progress is recorded as "in_progress"
2. **Given** a user who finished a lesson, **When** they mark it complete, **Then** their progress is recorded as "completed" with timestamp
3. **Given** a user with partial progress, **When** they request progress summary, **Then** they see completion percentages per part and chapter
4. **Given** a user tracking time, **When** they spend time on a lesson, **Then** time_spent_seconds is accumulated

---

### User Story 7 - Get Personalized Recommendations (Priority: P2)

Based on a user's preferences, completed lessons, and current progress, the system recommends the next lessons to study. Recommendations consider prerequisites and learning goals.

**Why this priority**: Smart recommendations improve learning outcomes by guiding users through optimal paths.

**Independent Test**: Complete some lessons → request recommendations → verify suggested lessons match user's goals and respect prerequisites.

**Acceptance Scenarios**:

1. **Given** a user with completed lessons, **When** they request recommendations, **Then** they receive next sequential lessons in incomplete chapters
2. **Given** a user with specific learning goals, **When** recommendations are generated, **Then** lessons aligned with those goals are prioritized
3. **Given** a lesson with prerequisites, **When** a user hasn't completed prerequisites, **Then** that lesson is not recommended
4. **Given** a beginner user, **When** recommendations are generated, **Then** L1/L2 layer lessons are prioritized over advanced layers

---

### Edge Cases

- What happens when a user clears localStorage? They are treated as a new user and prompted to complete onboarding again.
- What happens if personalization request fails? Display error message and allow retry, with Original content still accessible.
- What happens with very long lesson content? Personalization request includes pagination or chunking to handle large content.
- What happens if user skips onboarding? They can still view Original content; Personalized tab shows prompt to complete onboarding.
- What happens if the backend is unavailable? Original content remains accessible; Personalized tab shows connection error.

## Requirements *(mandatory)*

### Functional Requirements

**User Management**
- **FR-001**: System MUST generate a unique user identifier for each new visitor
- **FR-002**: System MUST persist user identifier in browser local storage
- **FR-003**: System MUST retrieve user identifier on subsequent visits

**Onboarding**
- **FR-004**: System MUST present a 6-question onboarding questionnaire to new users
- **FR-005**: Questionnaire MUST include: Education Level (high school/undergraduate/graduate/professional)
- **FR-006**: Questionnaire MUST include: Programming Experience (none/beginner/intermediate/advanced)
- **FR-007**: Questionnaire MUST include: Robotics Background (yes/no)
- **FR-008**: Questionnaire MUST include: AI/ML Experience (none/basic/intermediate/advanced)
- **FR-009**: Questionnaire MUST include: Learning Goals (multi-select: career change/research/hobby/teaching/building projects)
- **FR-010**: Questionnaire MUST include: Preferred Language (English/Urdu)
- **FR-011**: System MUST store user preferences upon questionnaire completion
- **FR-012**: System MUST redirect users to home page after completing onboarding

**Lesson Personalization**
- **FR-013**: Lesson pages MUST display "Original" and "Personalized" tabs
- **FR-014**: System MUST fetch personalized content when user clicks "Personalized" tab
- **FR-015**: Personalized content MUST adapt explanations based on programming experience level
- **FR-016**: Personalized content MUST add analogies and real-world examples for users without robotics background
- **FR-017**: Personalized content MUST translate to Urdu when preferred language is Urdu, keeping technical terms in English
- **FR-018**: System MUST display loading indicator while personalization is in progress

**Caching**
- **FR-019**: System MUST cache personalized content after generation
- **FR-020**: System MUST serve cached content when original content hash matches
- **FR-021**: System MUST invalidate cache when user preferences change

**Preferences Management**
- **FR-022**: Users MUST be able to view their current preferences
- **FR-023**: Users MUST be able to update their preferences
- **FR-024**: System MUST clear personalization cache when preferences are updated

**Book Structure**
- **FR-025**: System MUST store book structure as hierarchical tables (books → parts → chapters → lessons)
- **FR-026**: System MUST store lesson metadata including title, slug, type, layer, and estimated time
- **FR-027**: System MUST store chapter prerequisites as references to other chapters
- **FR-028**: System MUST provide API endpoints to browse book structure at any level
- **FR-029**: System MUST seed database with curriculum data from curriculum.md

**Content Storage (MCP Storage Bucket)**
- **FR-030**: System MUST upload all lesson markdown files to storage bucket
- **FR-031**: System MUST store files with hierarchical paths (books/{slug}/parts/{part}/chapters/{chapter}/lessons/{lesson}.md)
- **FR-032**: System MUST store lesson bucket_path in database for retrieval
- **FR-033**: System MUST compute and store content_hash (SHA-256) for cache invalidation
- **FR-034**: System MUST provide API to retrieve lesson content from bucket

**Content Indexing (MCP Vector Database)**
- **FR-035**: System MUST chunk lesson content for vector embeddings (~500 tokens per chunk)
- **FR-036**: System MUST store chunk embeddings in vector database with lesson metadata
- **FR-037**: System MUST store vector IDs in lessons table for reference
- **FR-038**: System MUST provide semantic search API for RAG queries

**Progress Tracking**
- **FR-039**: System MUST track lesson progress per user (not_started, in_progress, completed)
- **FR-040**: System MUST record timestamps when users start and complete lessons
- **FR-041**: System MUST track time spent on each lesson
- **FR-042**: System MUST provide API to get user progress summary (by part, chapter, overall)

**Recommendations**
- **FR-043**: System MUST recommend next lessons based on completed lessons and prerequisites
- **FR-044**: System MUST factor in user preferences (learning goals, experience level) for recommendations
- **FR-045**: System MUST respect pedagogy layer progression (L1 → L2 → L3 → L4 → L5)
- **FR-046**: System MUST provide API endpoint for personalized recommendations

### Key Entities

- **User**: Represents a visitor to the textbook. Key attributes: unique identifier, onboarding completion status, creation timestamp.
- **UserPreferences**: Stores a user's learning profile. Key attributes: education level, programming experience, robotics background, AI/ML experience, learning goals, preferred language.
- **PersonalizedContentCache**: Stores generated personalized content. Key attributes: user reference, lesson identifier, original content hash, personalized content, generation timestamp.
- **Book**: Represents the textbook. Key attributes: slug, title, description, version.
- **Part**: A major section of the book. Key attributes: number, title, layer, tier, folder_name, week range.
- **Chapter**: A chapter within a part. Key attributes: number, local_number, title, folder_name, prerequisites.
- **Lesson**: Individual content items. Key attributes: number, title, slug, type, content_hash, bucket_path, vector_ids.
- **UserProgress**: Tracks user progress through lessons. Key attributes: user reference, lesson reference, status, started_at, completed_at, time_spent_seconds.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete the onboarding questionnaire in under 2 minutes
- **SC-002**: 90% of new users complete the onboarding questionnaire on first visit
- **SC-003**: Personalized content is generated and displayed within 10 seconds of user request
- **SC-004**: Cached personalized content loads within 1 second
- **SC-005**: Users who view personalized content spend 20% more time on lesson pages compared to original content
- **SC-006**: 80% of users with Urdu preference receive content translated to Urdu
- **SC-007**: System supports at least 100 concurrent personalization requests without degradation
- **SC-008**: Book structure API returns complete hierarchy within 500ms
- **SC-009**: Content retrieval from storage bucket completes within 2 seconds
- **SC-010**: Semantic search returns relevant chunks within 1 second
- **SC-011**: Progress updates are persisted within 200ms
- **SC-012**: Recommendations endpoint returns within 1 second
- **SC-013**: All existing lesson content is synced to storage bucket
- **SC-014**: All lesson content is embedded in vector database for RAG

## Assumptions

- Users have JavaScript enabled in their browsers (required for localStorage)
- The existing ChatKit backend will be extended to support personalization endpoints
- NeonDB serverless Postgres will be used for data persistence
- Content personalization uses the same LLM provider as the ChatKit tutor (Gemini/OpenAI)
- Authentication will be added in a future iteration; MVP uses anonymous user IDs
- Original lesson content is stored as markdown and can be passed to the personalization endpoint
- MCP storage server is running on localhost:8001 with bucket alias `books_main` configured
- MCP vector database server is running on localhost:8002 for embeddings
- Curriculum structure is defined in `.specify/memory/curriculum.md` and used for seeding
- Book has 6 parts, 18 chapters, with currently only Part 1 (3 chapters) written
