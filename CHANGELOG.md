# Changelog

## 0.3.0 — 20 October 2026

### Learning and account flow

- Added a public welcome page with readable quick cards, subject browsing and an interactive market sample.
- Added fictional Alex and Sam demo sign-in profiles. Each has separate local bookmarks, imports, preferences and learning progress; Guest and legacy records remain intact.
- Replaced the public collection of 32 independent starter cards with eight quick cards paired with the eight full lessons. Previously saved or reviewed cards remain available in personal views.
- Added **Explore more**: visitors sign in and continue directly to the selected full lesson. Direct lesson and review URLs show a sign-in gate while signed out.
- Kept public quick-card reading separate from full-lesson completion and understanding. New personal quick cards require an available full-lesson link.

### Reliability and previews

- Corrected `Icons/` and `Packs/` path casing for Linux/GitHub Pages and refreshed offline app assets.
- Separated caches by application path and fixed the update banner appearing on first installation.
- Protected unreadable saved data from ordinary writes, added original-data recovery export, and prevented delayed file reads from crossing profile boundaries.
- Improved dialog focus, dark-mode button contrast, and save/unsave feedback.
- Added a self-contained preview builder with isolated temporary data, content-based filenames and downloadable ZIPs. The maintained application remains modular.
- Added browser regression coverage for demo accounts, public welcome pages, linked cards, profile preservation and restricted/offline previews; made existing tests portable.

### Compatibility and limitations

- App release version is **0.3.0**. Existing learning-data keys, backup format version 2, lesson-pack schema version 2 and lesson content versions are unchanged. The canonical and in-app AI prompts remain synchronized.
- Authentication is a **demo UI prototype**. Credentials and lesson files are public. There is no real signup, secure account authorization, password recovery or cross-device synchronization.
- Malformed backup progress records, review-quiz retry scheduling/grading, and public pack exports above 40 lessons are known pre-existing issues not resolved in this release.
- Real Android installation, service-worker upgrades on existing phones, and GitHub Pages deployment need the manual checks in `TESTING-CHECKLIST.md`. Browser tests do not establish that those deployments have occurred.
