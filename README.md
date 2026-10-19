# Knowledge Stash v0.2 — Advanced Learning Edition

**Free Android-first progressive web app. No paid service, API key, login, tracking or build tools required.** Contains **8 original multi-stage deep lessons** (each around 700–760 words of teaching text plus interactive graphics and 6 assessment questions) and **all 32 original v0.1 quick cards**.

## Upgrade your current GitHub Pages app safely

1. In your running **v0.1 app**, open **Settings → Export backup**. Save the backup somewhere safe **before** updating GitHub. Do not clear your phone's Chrome storage.
2. In GitHub, keep your current `knowledge-stash` repository and URL. (Optional safety: tag or download the existing files.)
3. Download this new ZIP, extract it, and replace **all old files** at your repository root with the **contents** of `Knowledge-Stash-v0.2/`. Do not upload the ZIP as a single file. Upload `index.html`, `app.js`, `data.js`, `style.css`, `visuals.js`, `sw.js`, `manifest.webmanifest`, `.nojekyll`, `icons/`, `lessons/` and `packs/`. GitHub web uploader may not upload folder objects; open an existing folder in GitHub to upload its files, or use the GitHub file editor to create any missing folder by naming a file `folder/file.ext`.
4. Your GitHub Pages configuration remains **Settings → Pages → main → /(root)**. Keep the **same hostname and repository path**, otherwise local progress cannot follow automatically.
5. On Android, open the app using Chrome. With internet connected, refresh once, then reopen. Your old local data is migrated from `knowledge-stash-v1` to `knowledge-stash-v2` on first use (the old key is preserved). If an older app appears due to service-worker cache, close and reopen Chrome and reload while online; do not clear storage.
6. Check My Stash and Review, then in **Settings → Export full backup** save a fresh v0.2 backup. After loading online, switch off internet and confirm lessons and quizzes work.

**Note:** Imported lessons and progress live on the **specific phone and site origin**. GitHub only publishes bundled lessons and `packs/community.json`. It does **not** sync personal progress. Back up regularly and before changing devices.

## Add new content (simple workflow)

**For a personal lesson on your phone:** Tap **＋ → Copy AI lesson prompt**, replace `[INSERT TOPIC]`, send to ChatGPT, copy the JSON, then paste in **＋ → Advanced lesson JSON → Validate & preview → Import**. You can also upload a downloaded `.json` file. The importer checks all required fields, the 6-question assessments, stable IDs, model names and HTTPS references. Rejected content does not change your library.

**For permanent lessons hosted on GitHub (available to all visitors and devices):** Import your approved lessons in the app, then select **Settings → Export publishable lesson pack**. Downloaded `community.json` contains **content only** (no bookmarks or learning progress). In GitHub, open `packs/community.json`, edit it or upload your exported file to replace it, then commit. Reload online: the pack will appear in Discover. If you want to update a published lesson, generate the same `id` with a **higher `version`**. Note: on-phone imports also need newer versions for an existing ID.

**Quick cards:** Tap **＋ → Add a quick idea** and fill in the fields. The original v0.1 `data.js` quick library remains readable.

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
