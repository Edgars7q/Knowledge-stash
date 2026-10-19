# Knowledge Stash v0.2 release checklist

## Safeguard
- [ ] Export original v0.1 backup before replacing files on GitHub.
- [ ] Keep the **same** GitHub Pages URL and do not clear Chrome site data.
- [ ] After first v0.2 opening, verify saved quick ideas, custom quick ideas, theme, reviews and prior history survive.
- [ ] Confirm `knowledge-stash-v1` is still present after migration; reloading does not reset progress.
- [ ] Export v0.2 backup and restore it on a fresh browser profile; compare saved items and results.

## Lessons and assessments
- [ ] All eight deep lessons appear; all 32 short ideas remain visible under Discover → Quick ideas.
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
- [ ] v0.1 JSON backup can restore into v0.2.
- [ ] Clearing **only** v0.2 data leaves v0.1 storage untouched.
