"""Signed-out landing, Guest access and demo-dashboard transitions.

Run: python3 tests/welcome_test.py. Starts its own local server and uses isolated
Chromium contexts; no user data or external services are accessed.
"""
from functools import partial
from http.server import ThreadingHTTPServer
import json
from threading import Thread
import unittest

from playwright.sync_api import sync_playwright

from auth_test import AppHandler, GUEST_KEY, OLD_KEY, ROOT, SESSION_KEY, empty_state


class WelcomeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), partial(AppHandler, directory=str(ROOT))
        )
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}/"
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

    def setUp(self):
        self.context = self.browser.new_context(viewport={"width": 390, "height": 844})
        self.page = self.context.new_page()
        self.page.set_default_timeout(5000)
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))

    def tearDown(self):
        self.context.close()
        self.assertEqual(self.errors, [], "Unexpected browser JavaScript errors")

    def open_welcome(self):
        self.page.goto(self.base, wait_until="networkidle")
        self.page.locator('[data-page="welcome"]').wait_for()

    def seed_guest(self):
        guest = empty_state()
        guest["saved"] = ["e1"]
        guest["history"] = [{"day": "2026-10-01", "type": "learn"}]
        guest_raw = json.dumps(guest, separators=(",", ":"))
        legacy_raw = '{"saved":["p1"],"theme":"light"}'
        seed = {GUEST_KEY: guest_raw, OLD_KEY: legacy_raw}
        self.context.add_init_script(
            """(() => {for (const [key,value] of Object.entries(%s)) {
              if (localStorage.getItem(key) === null) localStorage.setItem(key,value);
            }})();""" % json.dumps(seed)
        )
        return guest_raw, legacy_raw

    def stored(self, key):
        return self.page.evaluate("key => localStorage.getItem(key)", key)

    def test_signed_out_page_introduces_learning_without_personal_dashboard(self):
        guest_raw, legacy_raw = self.seed_guest()
        self.open_welcome()
        self.assertEqual(" ".join(self.page.locator("h1").inner_text().split()), "Turn curiosity into understanding.")
        self.assertFalse(self.page.locator("#bottom-nav").is_visible())
        self.assertFalse(self.page.locator("#open-add").is_visible())
        self.assertFalse(self.page.locator(".account-strip").is_visible())
        self.assertTrue(self.page.locator("#welcome-sign-in").is_visible())
        self.assertEqual(self.page.locator("main .stat-row, main .resume").count(), 0)
        self.assertEqual(self.stored(GUEST_KEY), guest_raw)
        self.assertEqual(self.stored(OLD_KEY), legacy_raw)
        self.assertIsNone(self.stored(SESSION_KEY))

    def test_sign_in_reload_sign_out_and_guest_data_preservation(self):
        guest_raw, legacy_raw = self.seed_guest()
        self.open_welcome()
        self.page.locator('[data-action="sign-in"]').first.click()
        self.page.locator('[data-demo-account="demo-alex"]').click()
        self.page.locator('#login-form button[type="submit"]').click()
        self.page.get_by_text("Grow your mind.", exact=True).wait_for()
        self.assertEqual(self.page.locator('[data-page="welcome"]').count(), 0)
        self.assertIn("Welcome, Alex", self.page.locator("main").text_content())
        self.assertTrue(self.page.locator("#bottom-nav").is_visible())
        self.assertTrue(self.page.locator(".stat-row").is_visible())
        self.assertEqual(self.stored(GUEST_KEY), guest_raw)
        # A remembered account goes straight to its dashboard even without a hash.
        self.page.goto(self.base, wait_until="networkidle")
        self.page.get_by_text("Grow your mind.", exact=True).wait_for()
        self.assertEqual(self.page.locator("#account-label").inner_text(), "Alex")
        self.page.goto(self.base + "#welcome", wait_until="networkidle")
        self.page.get_by_text("Grow your mind.", exact=True).wait_for()
        self.assertEqual(self.page.locator('[data-page="welcome"]').count(), 0)
        self.page.locator("#open-account").click()
        self.page.locator('[data-action="sign-out"]').click()
        self.page.locator('[data-page="welcome"]').wait_for()
        self.assertFalse(self.page.locator("#bottom-nav").is_visible())
        self.assertIsNone(self.stored(SESSION_KEY))
        self.assertEqual(self.stored(GUEST_KEY), guest_raw)
        self.assertEqual(self.stored(OLD_KEY), legacy_raw)
        self.page.locator('[data-action="continue-guest"]').click()
        self.page.get_by_text("Grow your mind.", exact=True).wait_for()
        self.page.locator('[data-tab="stash"]').click()
        self.assertEqual(self.page.locator('[data-idea="e1"]').count(), 1)

    def test_guest_can_read_quick_cards_and_browse_without_signing_in(self):
        self.open_welcome()
        self.page.locator('[data-page="welcome"] [data-idea]').first.click()
        self.page.locator("#dialog [data-explore-lesson]").wait_for()
        self.assertIsNone(self.stored(SESSION_KEY))
        self.page.locator("#dialog [data-explore-lesson]").click()
        self.page.locator("#login-form").wait_for()
        self.assertEqual(self.page.locator('[data-stage]').count(), 0)
        self.page.locator('[data-action="close"]').click()
        self.page.locator(".brand").click()
        self.page.locator('[data-page="welcome"]').wait_for()
        self.page.locator('[data-action="browse-quick"]').first.click()
        self.assertEqual(self.page.locator("#results [data-idea]").count(), 8)
        self.page.locator('[data-tab="today"]').click()
        self.page.get_by_text("Grow your mind.", exact=True).wait_for()
        self.assertTrue(self.page.locator("#bottom-nav").is_visible())

    def test_guest_deep_links_stay_accessible(self):
        self.page.goto(self.base + "#discover", wait_until="networkidle")
        self.assertEqual(self.page.locator("[data-lesson]").count(), 8)
        self.assertEqual(self.page.locator('[data-page="welcome"]').count(), 0)
        self.page.goto(self.base + "#lesson/econ-prices", wait_until="networkidle")
        self.page.locator('[data-page="lesson-gate"]').wait_for()
        self.assertEqual(self.page.locator('[data-stage], #quiz-form').count(), 0)
        self.assertIsNone(self.stored(SESSION_KEY))
        self.page.goto(self.base + "#not-a-page", wait_until="networkidle")
        self.page.locator('[data-page="welcome"]').wait_for()
        self.assertFalse(self.page.locator("#bottom-nav").is_visible())

    def test_landing_remains_usable_on_narrow_screens_and_dark_theme(self):
        self.open_welcome()
        for width in (320, 360, 390):
            self.page.set_viewport_size({"width": width, "height": 844})
            with self.subTest(width=width):
                self.assertLessEqual(
                    self.page.evaluate("document.documentElement.scrollWidth"), width
                )
                self.assertTrue(self.page.locator('[data-action="continue-guest"]').is_visible())
        self.page.locator("#open-settings").click()
        self.page.locator("#dark-toggle").check()
        self.page.locator('[data-action="close"]').click()
        self.assertEqual(self.page.locator("html").get_attribute("class"), "dark")
        self.assertTrue(self.page.locator('[data-page="welcome"]').is_visible())
        self.assertLessEqual(self.page.evaluate("document.documentElement.scrollWidth"), 390)


if __name__ == "__main__":
    unittest.main(verbosity=2)
