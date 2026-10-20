# Knowledge Stash v0.3 — Demo Accounts & Connected Learning

**Free Android-first progressive web app. No paid service, API key, tracking or build tools required.** Contains **8 full lessons and 8 matching quick cards**. Quick cards open without an account; demo sign-in opens the full lessons.

v0.3 adds a public welcome page, fictional demo accounts with separate local learning spaces, and quick cards that connect directly to full lessons after sign-in. See [CHANGELOG.md](CHANGELOG.md) for release changes and current limitations. Learning data, backups and lesson packs remain on schema version 2; the app version change does not reset browser data.

## Demo sign-in prototype

The signed-out home includes clickable quick cards and a free interactive market sample. **Explore the cards** opens the short-card collection; every public quick card has an **Explore more** button leading to its matching full lesson. Signed-out visitors are asked to sign in first, then continue directly to that lesson. Choose Alex or Sam to fill the demo form. Both use the public password `demo-learning-only` with `alex@knowledge-stash.test` or `sam@knowledge-stash.test`. This is a local UI/data prototype, not real authentication or secure content protection: the accounts, credentials and lesson files are public. Do not enter real credentials.

`#welcome` is the public home; `#today` is the learning dashboard. A normal sign-in opens the dashboard; sign-in from a card resumes that full lesson. Signing out returns to the public home. Guests can browse, read and save quick cards. Direct full-lesson and review links display a sign-in gate before creating any learning progress. Merely reading a quick card or using the welcome sample sliders does not mark a full lesson started, completed or understood.

Each demo profile has separate bookmarks, imports, progress and preferences on this browser. Sign-out returns to the original Guest library. Existing v0.1/v0.2 guest data is never copied into a demo account. Backups, restoration and reset apply only to the current profile; keep backups before clearing browser data. The session remembers the last selected demo account on reload, but there is no cross-device synchronization. Already-open tabs retain their selected profile until reloaded.

`auth.js` exposes a small replaceable account-provider API; `demo/accounts.json` supplies fictional account fixtures. JSON files on GitHub Pages are read-only to the app: session and learning changes are saved in browser storage, not written back to the file. No signup or password-recovery service is included. See [demo/README.md](demo/README.md) for the storage and future migration contract.

Content can continue to be authored directly in repository files: quick cards in `data.js`, bundled lessons in `lessons/builtin.js`, and published additions in `packs/community.json`. A public quick card requires a valid `lessonId` pointing to a full lesson in the same category; missing targets are not listed. App-based importing remains optional. Sign in to the intended demo profile before importing a personal full lesson.

## Upgrade your current GitHub Pages app safely

1. In the existing app, open **Settings → Export backup** and keep the file safe before updating. Export each local demo profile separately if you have used them. Do not clear browser storage.
2. Keep the same GitHub Pages hostname and repository path, so existing browser data remains associated with the app.
3. Review and merge the v0.3 source changes through your normal publishing branch. Include `auth.js`, `demo/accounts.json`, and the lowercase `icons/` and `packs/` paths with the existing application files. Standalone preview ZIPs are disposable review copies, not the deployable source tree.
4. Wait for the configured GitHub Pages deployment to succeed. Open the app online in Chrome and accept an offered app update when you are ready to leave the current learning session.
5. Existing v0.2 learning state remains in `knowledge-stash-v2`. Legacy `knowledge-stash-v1` is migrated only into Guest and is preserved. Historical saved cards remain accessible even though the public card collection has changed.
6. Verify Guest bookmarks, profile selection, a linked quick card and its full lesson. Export a fresh backup, then check cached sign-in and lessons offline. Android install/update behavior remains a manual release check.

**Note:** Imported lessons and progress live on the **specific phone and site origin**. GitHub only publishes bundled lessons and `packs/community.json`. It does **not** sync personal progress. Back up regularly and before changing devices.

## Add new content (simple workflow)

**For a personal lesson on your phone:** Tap **＋ → Copy AI lesson prompt**, replace `[INSERT TOPIC]`, send to ChatGPT, copy the JSON, then paste in **＋ → Advanced lesson JSON → Validate & preview → Import**. You can also upload a downloaded `.json` file. The importer checks all required fields, the 6-question assessments, stable IDs, model names and HTTPS references. Rejected content does not change your library.

**For permanent lessons hosted on GitHub (available to all visitors and devices):** Import your approved lessons in the app, then select **Settings → Export publishable lesson pack**. Downloaded `community.json` contains **content only** (no bookmarks or learning progress). In GitHub, open `packs/community.json`, edit it or upload your exported file to replace it, then commit. Reload online: the pack will appear in Discover. If you want to update a published lesson, generate the same `id` with a **higher `version`**. Note: on-phone imports also need newer versions for an existing ID.

**Quick cards:** The public collection contains one introductory card for each bundled full lesson. New personal quick cards also require a full-lesson link. Unmatched original starter cards have been removed from public browsing; historical bookmarks and review schedules still resolve through an archived copy in `data.js`. Older personal cards remain readable in My Stash and backups, even if they have no linked lesson.

Keep `KNOWLEDGE-STASH-AI-PROMPT.txt` as your **canonical saved AI instructions**. `ADDING-LESSONS.md` explains fields, updates and backups; `docs/EXAMPLE-LESSON-PACK.json` is a ready-to-import demonstration.

## Progress meanings

- **In progress:** Lesson opened; stage location saved.
- **Completed:** All stages passed through and the final quiz submitted, regardless of score.
- **Understood:** Quiz score **at least 80%**.
- **Reviewed:** A **due** spaced quiz passed; next due after 1, 3, 7, 14 or 30-day sequence (depending on step).
- **Retention demonstrated:** At least two successful spaced reviews and at least seven calendar days since first passing assessment. Not a claim of permanent mastery.

Review answers require multiple-choice selections and explanatory feedback. A failed review returns to tomorrow's interval. On lesson content version changes, assessment progress for that lesson resets to avoid certifying understanding of materially changed content.

## Offline, compatibility, privacy

This static site requires **HTTPS** (GitHub Pages) for proper installed-PWA and service-worker behaviour. Cache includes all eight built-in lessons, visuals and community JSON. Your imported lessons, bookmarks and scores are locally saved. Offline external links to academic sources will not work. No cross-device sync and no AI API integration are included. Browser storage is not guaranteed to survive uninstall, data clearance or a device reset; export backups.

The first update from v0.1 uses an existing older service worker and its own cache; while online, allow the new worker to install and reload. This upgrade intentionally leaves the old v0.1 localStorage key untouched for rollback.

## Important constraints

- Lesson packs use **JSON only**, not generated HTML or JavaScript. Teaching visuals are selected from a safe built-in component list. New visual types require code changes, not prompt changes.
- Sources are citation links for user review; the app does not fetch scholarly material for offline storage.
- Public GitHub Pages publishes source code and the community lesson pack **publicly**.
- User-added lesson JSON resides in `localStorage`, which may hit browser capacity after many long imports; import smaller batches and export backups. A future IndexedDB migration can extend capacity.
- `docs/` files are for reference; they are not required for app startup.

## Test locally

Run `python3 -m http.server 8080` from this directory and open `http://localhost:8080`. Chrome supports service workers on localhost. Use the checklist in `TESTING-CHECKLIST.md`; automated smoke tests are in `tests/smoke_test.py` (Playwright browser installation required).

For user-facing previews, always run `python3 tools/build_preview.py --share`. This creates a self-contained HTML file with a content-based filename and a companion ZIP in `previews/`. Share the new HTML rather than the multi-file Index or an older preview link. If an embedded viewer fails, download the ZIP, extract it, and open the included HTML in a normal browser. The shorter `python3 tools/build_preview.py` command still builds `preview.html` for local use.

`index.html` needs its sibling CSS/JavaScript/JSON files and cannot be previewed alone. The generated preview contains the actual styles, scripts, lessons and fictional demo accounts, with no network dependencies. It uses temporary in-memory data that resets on reload and never reads or changes saved app data. It does not install a service worker. Some embedded viewers also restrict downloads and confirmation dialogs; use a normal browser for those actions. Rebuild after editing source files; preview HTML and ZIP files are generated, Git-ignored outputs.
