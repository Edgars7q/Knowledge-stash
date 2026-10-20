# Knowledge Stash development

Preserve the existing free, static, mobile-first application and user learning data. Do not introduce a backend or replace working components without a requested feature that needs it.

## User-facing previews

The user has requested the self-contained preview method for every preview update because the chat's multi-file Index visualization repeatedly failed.

- Run `python3 tools/build_preview.py --share` after the final source changes. Deliver the generated HTML in `previews/`, whose filename changes with its contents. Do not send `index.html` or reuse an older preview link as the user-facing standalone preview.
- Provide the new HTML link in its own paragraph. Include the companion ZIP as a fallback that can be downloaded, extracted, and opened in a normal browser if the embedded viewer fails.
- Run `python3 tests/standalone_preview_test.py` for affected preview changes. Validate the generated artifact itself with networking blocked; do not hide missing assets by assembling them in the test harness.
- Keep the maintained app modular. Generated previews embed its actual styles, scripts, lesson content, and fictional demo fixtures. Their storage is disposable and must never read or overwrite the user's saved app data.
- Distinguish observed browser-test success from the chat viewer's status. Do not claim to have restarted or fixed that viewer unless directly verified. Do not invent a public preview URL.

Generated HTML and ZIP files are ignored outputs. Rebuild them from `tools/build_preview.py` rather than editing them by hand.
