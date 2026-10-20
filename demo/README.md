# Demo accounts and future authentication

This is a public, static login prototype. It does not provide authentication, authorization, encryption, secure sessions, or server-side storage. Never put real user details or real passwords into this directory or the repository. The fictional `.test` accounts are intentionally visible and both use `demo-learning-only`.

`accounts.json` has `schemaVersion: 1` and an `accounts` array. Each fixture has a stable `demo-` ID, name, `.test` email and public demo password. Editing these fixtures is a developer workflow; the browser cannot write changes to a GitHub Pages JSON file. Seeded accounts are read-only, and sign-up is not implemented.

## Provider boundary

`auth.js` exposes `window.KSAuth`:

- `initialize()` asynchronously loads/validates the relative fixture and restores a known demo session; returns `{id, name, email}` or `null`.
- `signIn(email, password)` asynchronously checks only fictional fixture credentials and returns the public user.
- `signOut()` asynchronously clears only the demo session.
- `getCurrentUser()` returns a copy of the current public user.
- `getDemoAccounts()` supplies public fictional fixture details for the demo picker. This is a demo-only method; never expose passwords through a real provider.

The fixture is cached with the app for offline demo sign-in. A missing fixture leaves Guest available. Invalid session IDs are rejected. Storage failures are reported instead of claiming a successful sign-in or sign-out. Fetching is bounded to avoid blocking startup indefinitely.

## Storage and preservation

- `knowledge-stash-v1`: preserved legacy guest records.
- `knowledge-stash-v2`: original Guest library and progress; only Guest can migrate v1 data.
- `knowledge-stash-v2:profile:<demo-id>`: separate learning state for a demo profile.
- `knowledge-stash-demo-session-v1`: only `{schemaVersion: 1, userId}`. No password or password hash is persisted here.

Profile state uses the existing v2 learning schema and backup envelope. A full backup contains only the active profile's learning data plus optional descriptive profile metadata, not credentials or sessions. Restoration changes the active profile after confirmation; it never switches identity. Export/reset/restore leave all other profiles and legacy records alone. A profile switch does not copy, merge or delete Guest data. Open tabs retain their selected identity; the last stored session determines identity on reload. Same-profile concurrent editing is not synchronized.

Unreadable stored JSON remains intact and ordinary writes are blocked. Settings exports its original bytes as a recovery `.txt` file. A user-confirmed reset or valid backup restore can explicitly replace that profile's unreadable storage. Keep the recovery file; it may need manual repair and is not necessarily a valid importable backup.

## Replacing the prototype later

Use a real authentication service/backend to verify credentials and enforce access. Replace the demo provider calls with that API; do not move public JSON password comparison to production. A database alone is not an authentication implementation. Keep session credentials out of learning-state exports and use the chosen provider's secure session mechanism.

Introduce an explicit data migration/mapping from demo/local IDs to stable real account IDs. Offer a user-reviewed import of local learning data rather than silently uploading or merging it. Define conflict resolution, offline synchronization, account deletion, password recovery, rate limiting and server authorization when real accounts become part of the product. The current per-profile browser storage is still local, inspectable data, not access-controlled private account storage.
