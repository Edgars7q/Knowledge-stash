# Local validation

Python 3, the Python Playwright package and Chromium are required for browser checks. The tests use `/usr/bin/chromium` and need no paid service or credentials.

From the repository root:

```sh
python3 tests/content_validation.py
python3 tests/browser_dom_test.py
python3 tests/migration_dom_test.py
python3 tests/auth_test.py
python3 tests/preview_test.py
python3 tests/standalone_preview_test.py
python3 tests/welcome_test.py
python3 tests/quick_cards_test.py
```

The authentication suite starts its own temporary HTTP server and tests fictional demo accounts, invalid credentials, profile isolation, guest-data preservation, profile backups/reset/restore, offline sign-in and repository-subpath hosting. No real accounts or passwords should be used.

The preview suite renders the actual app in an opaque sandboxed iframe. It checks startup and navigation when browser History, storage, and relative JSON fetches are unavailable; Guest learning remains accessible in this restricted mode.

The standalone-preview suite runs `tools/build_preview.py` and opens its exact generated HTML with every network request blocked. It checks real computed styling, demo sign-in, lessons, quizzes and temporary data isolation. It does not assemble or inline resources inside the test, so missing files in the delivered preview cannot be hidden by the test harness.

The welcome suite checks the public home, Guest continuation, sign-in/dashboard/sign-out transitions, mobile layout, theme, and preservation of existing guest data. Existing learning tests enter Guest explicitly before checking the dashboard.

The quick-card suite checks all eight quick-to-full links, free signed-out previews, required demo sign-in with lesson continuation, cancelled and failed sign-ins, direct lesson/review gates, unavailable targets, and historical/personal card preservation. Full-lesson tests sign in before assessing lesson behavior; guest tests verify that blocked full lessons create no progress.

For the existing full application smoke suite, start a server in another terminal:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Then run:

```sh
python3 tests/smoke_test.py
```

Screenshots are written to temporary directories outside the checkout. DOM-only suites intentionally stub storage and network; they exercise learning flows and Guest migration, using demo sign-in for full lessons, and do not replace HTTP/offline/authentication checks. Use `TESTING-CHECKLIST.md` for manual Android install, update and touch checks.
