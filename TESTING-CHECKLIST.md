# Knowledge Stash v0.3 release checklist

## Demo profiles
- [ ] Open each public quick card while signed out. Reading it leaves guest lesson progress unchanged.
- [ ] Every public quick card has a working Explore more button for the matching full lesson. Sign-in resumes that lesson; cancelling or using the wrong password leaves it gated.
- [ ] Direct full-lesson and spaced-review links remain gated while signed out. Guest browsing and quick-card bookmarks still work.
- [ ] Unmatched original cards are absent from public browsing; previously saved or reviewed cards and personal notes remain accessible in the user's library.
- [ ] Signed-out home introduces the app without personal statistics or learning navigation. Sign in opens the demo account form; Continue as guest opens the dashboard.
- [ ] The welcome sample sliders work without changing progress. Full-lesson access asks for demo sign-in; subject browsing opens guest quick cards.
- [ ] Sign in fills Alex/Sam's fictional credentials; invalid credentials leave Guest active. Successful sign-in opens the personalized dashboard; sign-out returns to the public home.
- [ ] Save progress in Alex, sign out, and verify the original Guest library returns; Sam has separate progress.
- [ ] Reload while signed in and verify the same profile returns. Backup, restore and reset affect only that profile.
- [ ] After loading online, enable airplane mode and test demo sign-in, lesson progress and sign-out.
- [ ] At narrow Android widths, the account dialog scrolls, the keyboard does not hide the focused field, and dark-mode controls remain readable.
- [ ] First installation shows no update prompt; an actual app update offers Later and does not activate until accepted. Export a backup before manual update testing.
- [ ] Use only fictional demo credentials. No real authentication, signup, password recovery or cross-device synchronization is provided.

## Safeguard
- [ ] Export original v0.1 backup before replacing files on GitHub.
- [ ] Keep the **same** GitHub Pages URL and do not clear Chrome site data.
- [ ] After upgrading to v0.3, verify saved quick ideas, custom quick ideas, theme, reviews and prior history survive.
- [ ] Confirm `knowledge-stash-v1` is still present after migration; reloading does not reset progress.
- [ ] Export a v0.3 backup (learning-data format 2) and restore it on a fresh browser profile; compare saved items and results.

## Lessons and assessments
- [ ] All eight full lessons and eight matching quick cards appear. Every short card links to the correct lesson; there are no unmatched public quick cards.
- [ ] All five lesson stages open in order; leave after stage 2, reopen and resume stage 3.
- [ ] Test market sliders: graph, price and quantity change immediately.
- [ ] Test Reynolds, longitude and relativity sliders; try flowchart, scenario choices and timeline.
- [ ] Quiz requires every question answered, marks correct/incorrect with explanations, and calculates score.
- [ ] Finish quiz below 80% → status Completed, not Understood; retry ≥80% → Understood and next-day review.
- [ ] A lesson already completed can be reopened and reread.
- [ ] Review is only accessible when due; passing advances review interval, failing returns to one day.
- [ ] Retention milestone is not granted prematurely.

## Importing AI content
- [ ] Use `docs/EXAMPLE-LESSON-PACK.json` to validate, preview and import.
- [ ] Imported lesson appears in Discover, can be saved, and works offline.
- [ ] Reimport same version → clear rejection; increment version → explicit warning and successful replacement.
- [ ] Invalid answer index, unknown category, unsupported visual, missing source or invalid JSON → reject entire pack; library unchanged.
- [ ] Open `＋` → copy and download official AI prompt. Open Settings → Export publishable pack; confirm it contains lessons but **not progress**.
- [ ] Upload publishable pack as `packs/community.json`; refresh; imported/published duplicates must show only once.

## Android / offline
- [ ] Install/update from GitHub Pages in Chrome; verify home-screen icon and dark mode.
- [ ] With internet, open all resources once, then switch to airplane mode; relaunch from home screen.
- [ ] Lessons, charts, quizzes, imported cards and saved progress work offline; external reference links do not.
- [ ] Update the service worker with a new release; ensure incomplete caching does not erase an existing working cache or local progress.
- [ ] Verify narrow screen (360 px), no horizontal overflow, touch targets, and text contrast.

## Failure handling
- [ ] Corrupted JSON import shows an error without modifying custom lessons.
- [ ] Invalid backup shows a message without replacing local progress.
- [ ] v0.1 JSON backups can restore in v0.3.
- [ ] Clearing **only** the current profile’s data leaves v0.1 storage untouched.
