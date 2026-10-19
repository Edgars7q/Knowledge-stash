# Adding lessons later — repeatable process

## The no-code route (recommended)

1. Keep `KNOWLEDGE-STASH-AI-PROMPT.txt` saved somewhere accessible (Google Drive, Notes, or on your phone). The identical prompt is built into the app under **＋ → Copy AI lesson prompt** and **Settings → Download official AI prompt**.
2. Replace `[INSERT TOPIC]` in that prompt with your desired topic and ask any competent AI model to respond **only with the complete JSON object**. Generate one advanced lesson at a time to reduce errors.
3. Read the lesson and check **factual accuracy**, numerical worked examples, answer indices and sources. AI can invent plausible citations or inaccurate statistics, so don't treat validation as independent fact-checking.
4. Open **Knowledge Stash → ＋**, paste the full JSON or load a `.json` file. Tap **Validate & preview**. Fix any reported issues in the AI output, then tap **Import**.
5. Save a private backup from **Settings → Export full backup**. This includes your imported lessons and progress.
6. To make lessons permanent in the GitHub-hosted library, use **Settings → Export publishable lesson pack**, then replace your repository's `packs/community.json` with the exported file. This content pack excludes private progress and bookmarks. Commit changes on `main` and refresh your app online.

## Essential format

The app accepts exactly one JSON object envelope:

```json
{
  "format": "knowledge-stash-lesson-pack",
  "schemaVersion": 2,
  "lessons": [
    {
      "id": "unique-topic-slug",
      "version": 1,
      "title": "Meaningful lesson title",
      "category": "Engineering",
      "model": "system",
      "level": "Intermediate",
      "minutes": 10,
      "hook": "A compelling explanation of why the concept matters.",
      "stages": [
        {"title":"Part one", "paragraphs":["A substantial paragraph with at least 30 characters.", "Another explanation paragraph with at least 30 characters."], "visual":{"type":"sequence","labels":["Start","Observe","Evaluate"]}, "takeaway":"One specific lesson."}
      ],
      "quiz": [
        {"question":"What can you conclude about this concept?", "options":["Valid inference","Incorrect inference","More evidence is needed"], "answer":2, "explanation":"The evidence does not distinguish the possible mechanisms."}
      ],
      "sources":[{"label":"Trustworthy source — title","url":"https://example.org/article"}]
    }
  ]
}
```

**The example above is a partial shape illustration only, not a valid import.** Valid imports need **3–8 stages**, **each with 2–8 substantive paragraphs**, and **5–12 quiz questions** (the official AI prompt requests five stages and six questions). See `docs/EXAMPLE-LESSON-PACK.json` for a complete valid example.

Choose one category exactly: `Psychology`, `Science`, `Engineering`, `Space`, `Philosophy`, `Business`, `Faith & ideas`, `History`. Select a teaching model: `concept`, `system`, `investigation`, `skill`, or `historical`.

Supported `visual.type`: `market`, `memory`, `relativity`, `longitude`, `reynolds`, `flow`, `sequence`, `timing`, `faultcases`, `comparison`, `argument`, `perspectives`, `timeline`. These are **prebuilt** visual components, so choose one only when genuinely relevant. `sequence` should include `labels` (3–7 step labels). `comparison` includes `left` and `right`. Other types use built-in examples and cannot be reconfigured by AI JSON; omit rather than misrepresenting the concept.

Each quiz question uses `answer` **zero-based**: first option `0`, second `1`, third `2`. Quiz pass threshold = **80%**. `sources` requires 1–12 HTTPS links to actual credible references.

## Stable IDs, updates and storage

- Give each different topic a stable lowercase `id` such as `robot-sensors` or `why-currencies-move`. Never reuse it for an unrelated concept.
- For a revised lesson, keep `id`, increase integer `version` (e.g., 1 → 2). Importing the same/older version is rejected to avoid accidental duplicates.
- Replacing a locally imported lesson with a newer version resets that lesson's assessment progress; other lessons are unaffected.
- Built-in lesson IDs (in `lessons/builtin.js`) cannot be overridden via the import screen. Their modifications require an application release.
- After you've published a lesson via `packs/community.json`, the on-phone duplicate is merged into one listing by ID and highest version, so no duplicate card appears.
- If an AI response contains a code fence, remove the opening and closing ``` lines before pasting. Do not paste explanatory text surrounding JSON.
- Keep packs small (in-app JSON file import limit 650 KB); import multiple packs separately and export a combined pack.
- Personal imports **will not** appear automatically on another device unless you restore your full backup or publish the content pack to GitHub. Progress never syncs between devices.

## How to ask AI to improve an existing lesson

> Use the Knowledge Stash official prompt. Update lesson `robot-sensors` from version 1 to version 2. Keep the topic and teaching goal, but correct [specific problem], deepen stage 3, and improve the quiz. Return the complete v0.2 lesson-pack JSON only. Preserve the stable `id`, raise `version` to 2, and do not invent any unsupported visual type.

When generating a new lesson, change the topic, category, teaching model and sources to suit the subject. Do **not** demand the same visual or reasoning style for every category.
