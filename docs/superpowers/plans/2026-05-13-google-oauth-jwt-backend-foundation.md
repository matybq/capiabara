# Google OAuth + JWT Backend Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add server-verified Google sign-in and a 30-day internal JWT so CapIAbara can authenticate users and scope notes to the authenticated owner.

**Architecture:** The backend will verify Google ID tokens server-side, then link or create a local user row using `google_sub` first and email as a legacy fallback. After that, the API will issue its own HS256 JWT with `exp`, `iat`, `iss`, and `aud` claims, and routers will depend on `current_user` instead of caller-supplied `user_id` for note ownership.

**Tech Stack:** FastAPI, SQLAlchemy, Alembic, Pydantic Settings, google-auth, python-jose[cryptography], uv

---

## File map

| File | Responsibility |
|---|---|
| `backend/pyproject.toml` | Add `google-auth` and `python-jose[cryptography]` runtime dependencies. |
| `backend/app/core/config.py` | Add auth, JWT, and explicit CORS settings sourced from `.env`. |
| `backend/app/core/security.py` | Verify Google ID tokens, issue/decode app JWTs, and resolve `current_user`. |
| `backend/app/core/exceptions.py` | Define auth-specific exceptions used by routers and services. |
| `backend/app/models/user.py` | Persist Google identity fields and active-state flags. |
| `backend/app/schemas/user.py` | Expose a public user profile shape plus a separate internal/current-user shape for auth/session responses. |
| `backend/app/schemas/note.py` | Remove caller-supplied ownership from note creation input. |
| `backend/app/schemas/auth.py` | Define auth exchange request/response payloads. |
| `backend/app/repositories/user_repository.py` | Add identity lookup and update helpers for Google-linked users. |
| `backend/app/repositories/note_repository.py` | Add ownership-scoped note lookup and delete helpers. |
| `backend/app/services/user_service.py` | Link or create users from Google claims and enforce active/deleted state. |
| `backend/app/services/note_service.py` | Scope note operations to the authenticated user. |
| `backend/app/routers/auth.py` | Add Google sign-in exchange and session introspection endpoints. |
| `backend/app/routers/notes.py` | Remove `user_id` from request handling and depend on `current_user`. |
| `backend/app/routers/users.py` | Add authenticated self-profile access. |
| `backend/app/main.py` | Register auth router and wire explicit CORS middleware. |
| `backend/alembic/versions/20260513_add_google_identity_fields.py` | Add nullable identity columns and activation state to `users`. |
| `backend/.env.example` | Document new auth, JWT, and CORS environment variables. |
| `backend/alembic.ini` | Neutralize the placeholder DSN (`driver://user:pass@localhost/dbname`) so it is never mistaken for usable credentials; `backend/alembic/env.py` remains the authoritative URL source from settings. |

## Security and data rules

- Verify Google ID tokens server-side with `google.oauth2.id_token.verify_oauth2_token(token, request, audience=client_id)`.
- Match accounts by `google_sub` first; use email only as a fallback to link pre-existing local rows during migration.
- Do not store Google access or refresh tokens; the backend keeps only the local user record and its own JWT session.
- No refresh tokens in MVP; the auth endpoint returns a single app JWT plus the user payload.
- Notes ownership comes from `current_user`; routers never accept caller-supplied `user_id` for note creation, listing, or deletion.
- Reject soft-deleted or inactive users everywhere auth is resolved.
- Configure explicit CORS origins from environment instead of `*`.
- Internal JWT lifetime is 30 days.

## Migration strategy

- Add `email`, `google_sub`, and `is_active` as nullable columns first so the schema can deploy without breaking existing rows.
- Backfill or link existing dev rows only where the current data is trustworthy and unique.
- If local SQLite data conflicts with unique identity constraints, reset or rebuild the dev database instead of writing a brittle migration path.
- After the nullable-first window, enforce uniqueness on `email` and `google_sub`.

### Task 1: Core auth settings, dependencies, and CORS wiring

**Files:**
- Modify `backend/pyproject.toml`
- Modify `backend/app/core/config.py`
- Modify `backend/app/main.py`
- Modify `backend/.env.example`
- Inspect `backend/alembic.ini`

- [ ] **Step 1: Add runtime dependencies**

Add `google-auth` for Google ID token verification and `python-jose[cryptography]` for app-issued JWTs.

- [ ] **Step 2: Extend settings**

Add settings for Google client ID, JWT secret, JWT issuer, JWT audience, JWT algorithm defaulting to `HS256`, JWT expiration days defaulting to `30`, and a comma-delimited explicit CORS allowlist.

- [ ] **Step 3: Wire CORS in the FastAPI app**

Read the allowlist from settings and register `CORSMiddleware` with explicit origins only.

- [ ] **Step 4: Document the environment contract**

Update `.env.example` with the new auth, JWT, and CORS variables; keep secrets blank and show the local frontend origins explicitly.

- [ ] **Step 5: Neutralize the Alembic placeholder DSN**

Inspect `backend/alembic.ini` together with `backend/alembic/env.py`; make the placeholder `driver://user:pass@localhost/dbname` explicitly non-usable so it cannot be mistaken for a real credential-shaped config, while `env.py` stays authoritative and overrides `sqlalchemy.url` from `settings.database_url`.

**Verification / inspection notes:** Run `cd backend && uv sync`. Then inspect `backend/app/core/config.py`, `backend/app/main.py`, and `backend/alembic.ini` to confirm the app reads settings once, exposes explicit CORS origins, and that the Alembic placeholder DSN is deliberately neutralized while `env.py` remains the source of truth.

### Task 2: Auth exceptions and token helpers

**Files:**
- Modify `backend/app/core/exceptions.py`
- Create or modify `backend/app/core/security.py`

- [ ] **Step 1: Define auth-focused exceptions**

Add exceptions for invalid Google tokens, unauthenticated requests, inactive users, and authorization failures. Keep messages safe for API responses.

- [ ] **Step 2: Add Google token verification**

Implement a helper that accepts the Google `credential` string, verifies it with `verify_oauth2_token`, and extracts the claims needed for account linking: `sub`, `email`, `name`, `picture`, and `email_verified`.

- [ ] **Step 3: Add app JWT issue and decode helpers**

Issue HS256 JWTs with `sub`, `email`, `google_sub`, `iss`, `aud`, `iat`, and `exp`, using the 30-day expiration setting. Decode must validate expiry and claim consistency before a user is returned.

- [ ] **Step 4: Add the `current_user` dependency**

Read the bearer token from `Authorization`, decode the app JWT, load the user from the database through the service layer, and reject deleted or inactive users.

**Verification / inspection notes:** Inspect `backend/app/core/security.py` to confirm there is no refresh-token flow and that JWT verification checks claims before user lookup.

### Task 3: User identity model, schemas, repository, service, and migration

**Files:**
- Modify `backend/app/models/user.py`
- Modify `backend/app/schemas/user.py`
- Modify `backend/app/repositories/user_repository.py`
- Modify `backend/app/services/user_service.py`
- Create `backend/alembic/versions/20260513_add_google_identity_fields.py`

- [ ] **Step 1: Extend the persisted user record**

Add nullable `email` and `google_sub` columns plus `is_active` defaulting to `True`. Keep `is_deleted` in place; auth must reject either inactive or deleted users.

- [ ] **Step 2: Expose the new profile fields in schemas**

Update public `UserRead` to include `email`, `is_active`, and `is_deleted`, but do not expose `google_sub` there by default. Add a separate internal/current-user shape, such as `UserCurrentRead`, that includes `google_sub` for auth/session endpoints and service internals.

- [ ] **Step 3: Add repository identity lookups**

Add lookup helpers for `google_sub` and `email`, plus a save/update helper that can attach Google identity fields to an existing user row.

- [ ] **Step 4: Add service-level Google linking**

Implement a user-service method that resolves a Google login in this order: `google_sub`, then trusted email fallback for pre-existing local rows, then create a new user if neither exists. If the matched user is deleted or inactive, reject the login.

- [ ] **Step 5: Apply the migration**

The Alembic revision should add the new columns as nullable first, then enforce uniqueness on identity fields once the columns exist. Keep the migration simple enough that a dev reset is the fallback if local rows conflict with uniqueness.

**Verification / inspection notes:** Run `cd backend && uv run alembic upgrade head`. Inspect the generated migration and model file to confirm the nullable-first rollout and the active-state flag exist together.

### Task 4: Auth router and session response

**Files:**
- Create `backend/app/schemas/auth.py`
- Create `backend/app/routers/auth.py`
- Modify `backend/app/main.py`

- [ ] **Step 1: Define auth payloads**

Add a Google token exchange request with the Google `credential` string and an auth session response containing `token`, `token_type`, `expires_in`, and `user`.

- [ ] **Step 2: Add the Google exchange endpoint**

Implement `POST /auth/google` to verify the Google credential, upsert or link the local user, and return the 30-day app JWT without storing any Google token.

- [ ] **Step 3: Add the current-session endpoint**

Implement `GET /auth/me` so the frontend can validate the bearer token and read the authenticated user profile.

- [ ] **Step 4: Register auth routes**

Include the auth router in `backend/app/main.py` alongside the existing routers.

**Verification / inspection notes:** Inspect the route signatures so invalid Google credentials fail before user creation and unauthenticated `GET /auth/me` returns 401.

### Task 5: Notes ownership enforcement

**Files:**
- Modify `backend/app/schemas/note.py`
- Modify `backend/app/repositories/note_repository.py`
- Modify `backend/app/services/note_service.py`
- Modify `backend/app/routers/notes.py`

- [ ] **Step 1: Remove caller-supplied ownership from the note create schema**

Drop `user_id` from `NoteCreate`. Creation input should only describe the note content and optional title.

- [ ] **Step 2: Scope repository helpers by owner**

Add note lookup and soft-delete helpers that filter by both `note_id` and `user_id` so foreign notes behave like missing notes.

- [ ] **Step 3: Update note service signatures**

Change note service methods to accept `current_user` explicitly for create, list, read, and delete flows.

- [ ] **Step 4: Rewrite the notes router to depend on auth**

Inject `current_user` with `Depends(get_current_user)` and remove `user_id` from all note endpoints.

- [ ] **Step 5: Keep soft delete behavior intact**

Continue returning and hiding soft-deleted notes, but do not leak ownership details across users.

**Verification / inspection notes:** Inspect `backend/app/routers/notes.py` to confirm there is no `user_id` query parameter or body field anywhere in the public notes API.

### Task 6: User self-access endpoint and auth-aware user service

**Files:**
- Modify `backend/app/routers/users.py`
- Modify `backend/app/services/user_service.py`
- Modify `backend/app/schemas/user.py`
- Modify `backend/app/core/security.py` if the current-user dependency needs a helper import

- [ ] **Step 1: Add `GET /users/me`**

Return the authenticated user profile directly from `current_user` so the frontend can hydrate session state. Use the internal/current-user schema here, not the public `UserRead` shape.

- [ ] **Step 2: Protect manual user creation for development**

  Do not remove the manual user creation endpoint. Instead, gate it 
  behind an environment flag: if `DEBUG=true` in `.env`, `POST /users/` 
  remains accessible without authentication for creating test users. 
  If `DEBUG=false` (production), the endpoint returns 403 immediately. 
  Add `DEBUG` to `.env.example` with a default value of `false`.

- [ ] **Step 3: Keep `GET /users/{id}` out of session hydration**

Treat `GET /users/{id}` as an internal/admin lookup only if it remains at all; it must not be used to hydrate the current session and must not create an IDOR path for ordinary users.

- [ ] **Step 4: Keep auth-state checks centralized**

Use the user service to reject deleted or inactive users wherever a current session is resolved.

**Verification / inspection notes:** Inspect that `GET /users/me` requires authentication, returns the same internal/current-user shape used by `GET /auth/me`, and that `GET /users/{id}` is not part of session hydration or public self-lookup.

### Task 7: Verification and manual checks

**Files:**
- None; this is a validation pass over the backend after the code changes above.

- [ ] **Step 1: Sync dependencies**

Run `cd backend && uv sync`.

- [ ] **Step 2: Apply migrations**

Run `cd backend && uv run alembic upgrade head`.

- [ ] **Step 3: Run automated tests**

Run `cd backend && uv run pytest`.

- [ ] **Step 4: Perform manual endpoint checks**

Confirm that unauthenticated `GET /notes` is rejected, invalid Google tokens are rejected by the auth endpoint, and authenticated note reads/writes are scoped only to the current user.

**Expected result:** Dependency resolution succeeds, migrations apply cleanly, tests pass, and the auth/ownership boundary is enforced end to end.

## Execution handoff

- Next action is user approval to execute this plan.
- Implementation must be delegated to builder first, then tester, then code-reviewer because auth is security-sensitive.
