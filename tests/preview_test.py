"""Exercise an embedded HTML preview without an origin, storage, or HTTP server.

Run: python3 tests/preview_test.py. All assets are inlined from this checkout;
no app source is changed and no existing browser data is read.
"""
import html
from pathlib import Path
import re
import unittest

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def inline_preview():
    source = (ROOT / "index.html").read_text()
    source = re.sub(
        r'<script\b[^>]*\bsrc="\./([^"?]+)[^"]*"[^>]*>\s*</script>',
        lambda match: "<script>" + (ROOT / match[1]).read_text() + "</script>",
        source,
    )
    source = re.sub(r'<link\b[^>]*>', '', source)
    return source.replace("</head>", "<style>" + (ROOT / "style.css").read_text() + "</style></head>")


class EmbeddedPreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(
            executable_path="/usr/bin/chromium", headless=True, args=["--no-sandbox"]
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context(viewport={"width": 390, "height": 844})
        self.page = self.context.new_page()
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        self.page.set_default_timeout(5000)
        self.page.set_content(
            '<iframe title="Knowledge Stash preview" sandbox="allow-scripts" '
            'style="width:390px;height:844px;border:0" srcdoc="'
            + html.escape(inline_preview(), quote=True) + '"></iframe>'
        )
        self.app = self.page.frame_locator('iframe')
        self.app.locator('[data-page="welcome"]').wait_for()

    def tearDown(self):
        self.context.close()
        self.assertEqual(self.errors, [], 'Unexpected preview JavaScript errors')

    def test_public_navigation_and_sign_in_gate_in_opaque_preview(self):
        self.app.locator('[data-action="continue-guest"]').click()
        self.app.get_by_text('Grow your mind.').wait_for()
        self.app.locator('[data-tab="discover"]').click()
        self.app.locator('[data-lesson="econ-prices"]').wait_for()
        self.assertEqual(self.app.locator('[data-lesson]').count(), 8)
        self.app.locator('[data-library="Ideas"]').click()
        self.app.locator('[data-idea="quick-prices"]').click()
        self.app.locator('[data-explore-lesson="econ-prices"]').wait_for()
        self.app.locator('[data-explore-lesson="econ-prices"]').click()
        self.app.locator('#login-form').wait_for()
        self.assertEqual(self.app.locator('[data-stage]').count(), 0)
        self.app.locator('[data-action="close"]').click()
        self.app.locator('[data-tab="stash"]').click()
        self.app.get_by_text('My Stash.', exact=True).wait_for()
        self.app.locator('[data-tab="today"]').click()
        self.app.get_by_text('Grow your mind.').wait_for()

    def test_dialogs_and_clear_demo_fallback(self):
        self.app.locator('#welcome-sign-in').click()
        self.app.locator('#login-form').wait_for()
        self.assertIn('Demo accounts are unavailable', self.app.locator('#dialog').inner_text())
        self.app.locator('[data-action="close"]').click()
        self.app.locator('#open-settings').click()
        self.app.locator('#dark-toggle').check()
        self.app.locator('[data-action="close"]').click()
        self.app.locator('[data-page="welcome"]').wait_for()


if __name__ == '__main__':
    unittest.main(verbosity=2)
