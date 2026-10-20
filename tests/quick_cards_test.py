"""Public quick-card hooks, full-lesson links, and historical-card preservation.

Run: python3 tests/quick_cards_test.py. Uses isolated Chromium contexts and a
local temporary HTTP server; the standalone case blocks every network request.
"""
from functools import partial
from http.server import ThreadingHTTPServer
import html
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from threading import Thread
import unittest

from playwright.sync_api import sync_playwright

from auth_test import AppHandler, GUEST_KEY, OLD_KEY, ROOT, SESSION_KEY, empty_state, profile_key


class QuickCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), partial(AppHandler, directory=str(ROOT))
        )
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}/"
        cls.output = tempfile.TemporaryDirectory(prefix="knowledge-stash-quick-preview-")
        cls.preview_path = Path(cls.output.name) / "preview.html"
        subprocess.run(
            [sys.executable, str(ROOT / "tools/build_preview.py"), "--output", str(cls.preview_path)],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(
            executable_path="/usr/bin/chromium", headless=True, args=["--no-sandbox"]
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)
        cls.output.cleanup()

    def setUp(self):
        self.context = self.browser.new_context(viewport={"width": 390, "height": 844})
        self.page = self.context.new_page()
        self.page.set_default_timeout(5000)
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        self.page.on("dialog", lambda dialog: dialog.accept())

    def tearDown(self):
        self.context.close()
        self.assertEqual(self.errors, [], "Unexpected browser JavaScript errors")

    def open_welcome(self):
        self.page.goto(self.base, wait_until="networkidle")
        self.page.locator('[data-page="welcome"]').wait_for()

    def stored(self, key):
        return self.page.evaluate("key => localStorage.getItem(key)", key)

    def browse_quick(self):
        self.page.locator('[data-action="browse-quick"]').first.click()
        self.page.locator('[data-library="Ideas"]').wait_for()
        self.page.wait_for_function("document.querySelectorAll('#results [data-idea]').length === 8")

    def test_public_quick_cards_have_one_valid_full_lesson_each(self):
        self.open_welcome()
        cards = self.page.evaluate("() => STARTER_IDEAS")
        lessons = self.page.evaluate("() => KS_BUILTIN.map(({id,category}) => ({id,category}))")
        full = {lesson["id"]: lesson for lesson in lessons}
        self.assertEqual(len(cards), 8)
        self.assertEqual(len({card["id"] for card in cards}), 8)
        self.assertEqual({card["lessonId"] for card in cards}, set(full))
        for card in cards:
            with self.subTest(card=card["id"]):
                self.assertEqual(card["category"], full[card["lessonId"]]["category"])
                for field in ("title", "hook", "body", "example", "takeaway", "question"):
                    self.assertTrue(card[field].strip(), field)
        self.assertGreater(self.page.locator('[data-page="welcome"] [data-idea]').count(), 0)
        self.assertIsNone(self.stored(SESSION_KEY))

    def test_every_public_card_requires_sign_in_then_opens_its_correct_full_lesson(self):
        self.open_welcome()
        cards = self.page.evaluate("() => STARTER_IDEAS")
        for card in cards:
            with self.subTest(card=card["id"]):
                self.browse_quick()
                before = self.stored(GUEST_KEY)
                self.page.locator(f'#results [data-idea="{card["id"]}"]').click()
                self.page.locator("#dialog").wait_for()
                self.assertIn(card["title"], self.page.locator("#dialog").text_content())
                self.assertEqual(self.stored(GUEST_KEY), before, "Reading a quick card must not mark learning progress")
                self.assertIsNone(self.stored(SESSION_KEY))
                save = self.page.locator(f'#dialog [data-save="{card["id"]}"]')
                save.click()
                self.assertIn("Saved", save.inner_text())
                self.assertIn(card["id"], json.loads(self.stored(GUEST_KEY))["saved"])
                save.click()
                self.assertIn("Save card", save.inner_text())
                self.assertNotIn(card["id"], json.loads(self.stored(GUEST_KEY))["saved"])
                self.assertEqual(json.loads(self.stored(GUEST_KEY))["lessonProgress"], {})
                before = self.stored(GUEST_KEY)
                self.page.locator(f'[data-explore-lesson="{card["lessonId"]}"]').click()
                self.page.locator("#login-form").wait_for()
                self.assertEqual(self.page.locator('[data-stage]').count(), 0)
                self.assertEqual(self.stored(GUEST_KEY), before)
                self.assertIsNone(self.stored(SESSION_KEY))
                self.page.locator('[data-demo-account="demo-alex"]').click()
                self.page.locator('#login-form button[type="submit"]').click()
                self.page.get_by_text("Stage 1 of 5", exact=True).wait_for()
                self.assertTrue(self.page.locator("#overlay").is_hidden())
                self.assertEqual(self.page.evaluate("location.hash"), f'#lesson/{card["lessonId"]}')
                self.assertEqual(self.stored(GUEST_KEY), before)
                self.page.locator("#open-account").click()
                self.page.locator('[data-action="sign-out"]').click()
                self.page.locator('[data-page="welcome"]').wait_for()

    def test_direct_full_lesson_and_review_links_are_gated_without_progress_writes(self):
        for route in ("#lesson/econ-prices", "#lesson/econ-prices/review"):
            with self.subTest(route=route):
                self.page.goto(self.base + route, wait_until="networkidle")
                self.page.locator('[data-page="lesson-gate"]').wait_for()
                self.assertEqual(self.page.locator('[data-stage], #quiz-form').count(), 0)
                self.assertIsNone(self.stored(GUEST_KEY))
                self.assertIsNone(self.stored(SESSION_KEY))
                self.assertTrue(self.page.locator('[data-sign-in-lesson="econ-prices"]').is_visible())

    def test_direct_lesson_gate_sign_in_resumes_the_selected_full_lesson(self):
        self.open_welcome()
        card = self.page.evaluate("() => STARTER_IDEAS[0]")
        before = self.stored(GUEST_KEY)
        self.page.goto(self.base + f'#lesson/{card["lessonId"]}', wait_until="networkidle")
        self.page.locator('[data-page="lesson-gate"]').wait_for()
        self.page.locator(f'[data-sign-in-lesson="{card["lessonId"]}"]').click()
        self.page.locator('[data-demo-account="demo-alex"]').click()
        self.page.locator('#login-form [name="password"]').fill("incorrect-demo-password")
        self.page.locator('#login-form button[type="submit"]').click()
        self.page.locator('#dialog [role="alert"]').wait_for()
        self.assertIsNone(self.stored(SESSION_KEY))
        self.assertEqual(self.stored(GUEST_KEY), before)
        self.page.locator('[data-demo-account="demo-alex"]').click()
        self.page.locator('#login-form button[type="submit"]').click()
        self.page.get_by_text("Stage 1 of 5", exact=True).wait_for()
        self.assertEqual(self.page.evaluate("location.hash"), f'#lesson/{card["lessonId"]}')
        self.assertEqual(self.page.locator("#account-label").inner_text(), "Alex")
        self.assertEqual(self.stored(GUEST_KEY), before)
        self.assertTrue(self.page.locator("#overlay").is_hidden())
        profile = json.loads(self.stored(profile_key("demo-alex")))
        self.assertIn(card["lessonId"], profile["lessonProgress"])

    def test_cancelled_card_sign_in_does_not_redirect_a_later_normal_sign_in(self):
        self.open_welcome()
        self.browse_quick()
        self.page.locator('#results [data-idea="quick-prices"]').click()
        self.page.locator('[data-explore-lesson="econ-prices"]').click()
        self.page.locator("#login-form").wait_for()
        self.page.locator('[data-action="close"]').click()
        self.page.locator("#open-account").click()
        self.page.locator('[data-demo-account="demo-sam"]').click()
        self.page.locator('#login-form button[type="submit"]').click()
        self.page.locator('[data-page="dashboard"]').wait_for()
        self.assertEqual(self.page.locator("#account-label").inner_text(), "Sam")
        self.assertEqual(self.page.locator('[data-stage]').count(), 0)
        self.assertEqual(self.page.evaluate("location.hash"), "#today")
        self.assertIsNone(self.stored(GUEST_KEY))
        self.assertIsNone(self.stored(profile_key("demo-sam")))

    def test_saved_legacy_and_personal_cards_stay_readable_outside_public_quick_library(self):
        guest = empty_state()
        guest["saved"] = ["p1", "own-personal-1"]
        guest["learned"] = {"p1": "2026-01-01"}
        guest["reviews"] = {"p1": {"step": 1, "due": "2000-01-01"}}
        guest["custom"] = [{
            "id": "own-personal-1", "title": "My personal note", "category": "Science",
            "hook": "Keep my original note", "body": "A personal explanation that must survive the catalogue update.",
            "takeaway": "Preserve personal content", "example": "My own example", "question": "What did I learn?",
        }]
        guest_raw = json.dumps(guest, separators=(",", ":"))
        legacy_raw = '{"saved":["p1"],"theme":"light"}'
        seed = {GUEST_KEY: guest_raw, OLD_KEY: legacy_raw}
        self.context.add_init_script(
            """(() => {for (const [key,value] of Object.entries(%s)) {
              if (localStorage.getItem(key) === null) localStorage.setItem(key,value);
            }})();""" % json.dumps(seed)
        )
        self.open_welcome()
        self.browse_quick()
        self.assertEqual(self.page.locator('#results [data-idea="p1"]').count(), 0)
        self.assertEqual(self.page.locator('#results [data-idea="own-personal-1"]').count(), 0)
        self.page.locator('[data-tab="stash"]').click()
        for card_id in ("p1", "own-personal-1"):
            self.page.locator(f'[data-idea="{card_id}"]').click()
            self.assertTrue(self.page.locator("#dialog").is_visible())
            self.assertEqual(self.page.locator("#dialog [data-explore-lesson]").count(), 0)
            self.page.locator('[data-action="close"]').click()
        self.page.locator('[data-tab="review"]').click()
        self.assertEqual(self.page.locator('[data-idea="p1"]').count(), 1)
        self.assertEqual(self.stored(GUEST_KEY), guest_raw)
        self.assertEqual(self.stored(OLD_KEY), legacy_raw)

    def test_unavailable_full_lesson_is_not_offered_as_a_quick_card(self):
        self.open_welcome()
        removed = self.page.evaluate("""() => {
          const card = STARTER_IDEAS[0];
          KS_BUILTIN.splice(KS_BUILTIN.findIndex(lesson => lesson.id === card.lessonId), 1);
          return card.id;
        }""")
        self.page.locator(".brand").click()
        self.page.locator('[data-action="browse-quick"]').first.click()
        self.assertEqual(self.page.locator("#results [data-idea]").count(), 7)
        self.assertEqual(self.page.locator(f'#results [data-idea="{removed}"]').count(), 0)
        self.assertEqual(self.page.locator('[data-explore-lesson="missing-lesson"]').count(), 0)

    def test_standalone_explore_more_signs_in_and_closes_dialog_for_full_lesson(self):
        requests = []
        self.context.on("request", lambda request: requests.append(request.url)
                        if request.url.startswith(("http://", "https://")) else None)
        self.context.route("**/*", lambda route: route.abort())
        source = self.preview_path.read_text()
        self.page.set_content(
            '<iframe sandbox="allow-scripts" style="width:390px;height:844px;border:0" srcdoc="'
            + html.escape(source, quote=True) + '"></iframe>'
        )
        app = self.page.frame_locator("iframe")
        app.locator('[data-page="welcome"]').wait_for()
        app.locator('[data-action="browse-quick"]').first.click()
        app.locator('#results [data-idea="quick-prices"]').click()
        app.locator('[data-explore-lesson="econ-prices"]').click()
        app.locator("#login-form").wait_for()
        self.assertEqual(app.locator('[data-stage]').count(), 0)
        self.assertIsNone(app.locator("html").evaluate("() => localStorage.getItem('knowledge-stash-demo-session-v1')"))
        app.locator('[data-demo-account="demo-alex"]').click()
        app.locator('#login-form button[type="submit"]').click()
        app.get_by_text("Stage 1 of 5", exact=True).wait_for()
        self.assertTrue(app.locator("#overlay").is_hidden())
        session = app.locator("html").evaluate("() => JSON.parse(localStorage.getItem('knowledge-stash-demo-session-v1'))")
        self.assertEqual(session["userId"], "demo-alex")
        self.assertEqual(requests, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
