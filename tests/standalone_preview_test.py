"""Test the generated preview as one real HTML file, with no sibling assets.

Run: python3 tests/standalone_preview_test.py. Builds into a temporary directory,
loads the exact output in an opaque iframe, and blocks every network request.
"""
import html
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class StandalonePreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output_dir = tempfile.TemporaryDirectory(prefix="knowledge-stash-preview-")
        cls.preview_path = Path(cls.output_dir.name) / "preview.html"
        subprocess.run(
            [sys.executable, str(ROOT / "tools/build_preview.py"), "--output", str(cls.preview_path)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        cls.source = cls.preview_path.read_text()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(
            executable_path="/usr/bin/chromium", headless=True, args=["--no-sandbox"]
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.output_dir.cleanup()

    def setUp(self):
        self.context = self.browser.new_context(viewport={"width": 390, "height": 844})
        self.network_requests = []
        self.context.on(
            "request",
            lambda request: self.network_requests.append(request.url)
            if request.url.startswith(("http://", "https://")) else None,
        )
        self.context.route("**/*", lambda route: route.abort())
        self.page = self.context.new_page()
        self.page.set_default_timeout(5000)
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        self.mount_preview()

    def tearDown(self):
        self.context.close()
        self.assertEqual(self.errors, [], "Unexpected preview JavaScript errors")
        self.assertEqual(self.network_requests, [], "Standalone preview must not request sibling/network assets")

    def mount_preview(self):
        # No inlining or preprocessing here: this is the exact generated deliverable.
        self.page.set_content(
            '<iframe title="Standalone Knowledge Stash" sandbox="allow-scripts" '
            'style="width:390px;height:844px;border:0" srcdoc="'
            + html.escape(self.source, quote=True) + '"></iframe>'
        )
        self.app = self.page.frame_locator("iframe")
        self.app.locator('[data-page="welcome"]').wait_for()

    def evaluate(self, expression, arg=None):
        return self.app.locator("html").evaluate(expression, arg)

    def enter_guest(self):
        if self.app.locator('[data-page="welcome"]').is_visible():
            self.app.locator('[data-action="continue-guest"]').click()
        self.app.get_by_text("Grow your mind.").wait_for()

    def sign_in(self):
        if self.app.locator('[data-page="welcome"]').is_visible():
            self.app.locator("#welcome-sign-in").click()
        else:
            self.app.locator("#open-account").click()
        self.app.locator('[data-demo-account="demo-alex"]').click()
        self.app.locator('#login-form button[type="submit"]').click()
        self.app.locator("#account-label").filter(has_text="Alex").wait_for()
        self.app.locator("#login-form").wait_for(state="hidden")

    def test_exact_artifact_has_styles_content_and_no_external_dependencies(self):
        self.assertTrue(self.evaluate("() => window.KS_PREVIEW === true"))
        self.assertEqual(self.app.locator("script[src]").count(), 0)
        self.assertEqual(self.app.locator('link[rel="stylesheet"]').count(), 0)
        self.assertIn("system-ui", self.evaluate("() => getComputedStyle(document.documentElement).fontFamily"))
        self.assertEqual(self.evaluate("() => getComputedStyle(document.body).backgroundColor"), "rgb(247, 247, 251)")
        self.assertEqual(self.evaluate("() => getComputedStyle(document.querySelector('.app-shell')).maxWidth"), "500px")
        self.assertEqual(self.evaluate("() => getComputedStyle(document.querySelector('.welcome-primary')).backgroundColor"), "rgb(101, 88, 217)")
        note = self.app.locator("[data-preview-note]").inner_text().lower()
        self.assertIn("reset", note)
        self.assertIn("reload", note)
        self.app.locator('[data-action="browse-lessons"]').click()
        self.assertEqual(self.app.locator("[data-lesson]").count(), 8)
        self.app.locator('[data-library="Ideas"]').click()
        self.assertEqual(self.app.locator("[data-idea]").count(), 8)

    def test_demo_login_lesson_quiz_import_and_guest_isolation(self):
        self.enter_guest()
        guest_before = self.evaluate("() => localStorage.getItem('knowledge-stash-v2')")
        self.sign_in()
        self.assertIsNone(self.evaluate("() => localStorage.getItem('knowledge-stash-v2:profile:demo-alex')"))
        self.app.locator('[data-tab="discover"]').click()
        self.app.locator('[data-lesson="econ-prices"]').click()
        for stage in range(5):
            self.app.get_by_text(f"Stage {stage + 1} of 5").wait_for()
            if stage == 2:
                self.app.locator('[data-slider="demand"]').fill("14")
                self.assertEqual(self.app.locator("[data-price]").inner_text(), "€67")
            self.app.locator('[data-stage="next"]').click()
        answers = self.evaluate("() => KS_BUILTIN.find(lesson => lesson.id === 'econ-prices').quiz.map(q => q.answer)")
        for index, answer in enumerate(answers):
            self.app.locator(f'input[name="q{index}"][value="{answer}"]').check()
        self.app.locator('#quiz-form button[type="submit"]').click()
        self.app.get_by_text("Understanding demonstrated", exact=True).wait_for()
        self.assertTrue(self.evaluate("() => JSON.parse(localStorage.getItem('knowledge-stash-v2:profile:demo-alex')).lessonProgress['econ-prices'].understood"))
        # Submitted, disabled answers must not trigger a blocked sandbox confirm.
        self.app.locator("#open-account").click()
        self.app.locator('[data-action="sign-out"]').click()
        self.app.locator('[data-page="welcome"]').wait_for()
        self.assertEqual(self.app.locator("#account-label").inner_text(), "Guest")
        self.assertEqual(self.evaluate("() => localStorage.getItem('knowledge-stash-v2')"), guest_before)
        self.sign_in()
        self.app.locator("#open-add").click()
        self.app.locator("#pack-input").fill((ROOT / "docs/EXAMPLE-LESSON-PACK.json").read_text())
        self.app.locator('[data-action="preview-pack"]').click()
        self.app.locator('[data-action="confirm-import"]').click()
        self.assertEqual(self.app.locator('[data-lesson="example-process-bottlenecks"]').count(), 1)
        self.app.locator("#open-account").click()
        self.app.locator('[data-action="sign-out"]').click()
        self.app.locator('[data-page="welcome"]').wait_for()
        self.assertEqual(self.app.locator("#account-label").inner_text(), "Guest")
        self.assertEqual(self.evaluate("() => localStorage.getItem('knowledge-stash-v2')"), guest_before)
        self.assertIsNone(self.evaluate("() => localStorage.getItem('knowledge-stash-demo-session-v1')"))
        self.app.locator('[data-action="browse-lessons"]').click()
        self.assertEqual(self.app.locator("[data-lesson]").count(), 8)

    def test_reopening_preview_discards_only_ephemeral_state(self):
        self.sign_in()
        self.app.locator('[data-tab="discover"]').click()
        self.app.locator('[data-lesson="econ-prices"]').click()
        self.app.locator('[data-save="econ-prices"]').click()
        self.assertIsNotNone(self.evaluate("() => localStorage.getItem('knowledge-stash-v2:profile:demo-alex')"))
        self.mount_preview()
        self.assertTrue(self.app.locator('[data-page="welcome"]').is_visible())
        self.assertEqual(self.app.locator("#account-label").inner_text(), "Guest")
        self.assertIsNone(self.evaluate("() => localStorage.getItem('knowledge-stash-demo-session-v1')"))
        self.assertIsNone(self.evaluate("() => localStorage.getItem('knowledge-stash-v2:profile:demo-alex')"))
        self.assertEqual(self.evaluate("() => KSAuth.getCurrentUser()"), None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
