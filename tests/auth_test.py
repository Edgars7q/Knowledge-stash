"""Demo-account integration tests. Run: python3 tests/auth_test.py.

Starts its own loopback server and isolated Chromium contexts. No real account,
external service, or existing browser data is used.
"""
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import unittest

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
GUEST_KEY = "knowledge-stash-v2"
OLD_KEY = "knowledge-stash-v1"
SESSION_KEY = "knowledge-stash-demo-session-v1"


def profile_key(user_id):
    return f"{GUEST_KEY}:profile:{user_id}"


def empty_state():
    return {
        "schemaVersion": 2,
        "saved": [],
        "learned": {},
        "reviews": {},
        "history": [],
        "custom": [],
        "theme": "light",
        "customLessons": [],
        "lessonProgress": {},
        "migration": {"from": 0},
    }


class AppHandler(SimpleHTTPRequestHandler):
    """Serve the same checkout at / and a GitHub Pages-style repository path."""

    def do_GET(self):
        if self.path.startswith("/Knowledge-stash/"):
            self.path = self.path[len("/Knowledge-stash"):]
        return super().do_GET()

    def log_message(self, *_args):
        pass


class DemoAccountTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), partial(AppHandler, directory=str(ROOT))
        )
        cls.server_thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"
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
        cls.server_thread.join(timeout=5)

    def setUp(self):
        self.context = self.browser.new_context(
            viewport={"width": 390, "height": 844}, accept_downloads=True
        )
        self.page = self.context.new_page()
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        self.page.on("dialog", lambda dialog: dialog.accept())

    def tearDown(self):
        self.context.close()
        self.assertEqual(self.errors, [], "Unexpected browser JavaScript errors")

    def open_app(self, path="/"):
        self.page.goto(self.base + path, wait_until="networkidle")
        self.page.wait_for_function(
            "window.KSAuth && (document.querySelector('[data-page=welcome]') || document.querySelector('main').textContent.includes('Grow your mind.'))"
        )
        accounts = self.page.evaluate("() => KSAuth.getDemoAccounts()")
        self.assertEqual(len(accounts), 2)
        self.accounts = {account["id"]: account for account in accounts}

    def stored(self, key):
        return self.page.evaluate("key => localStorage.getItem(key)", key)

    def state(self, key):
        raw = self.stored(key)
        return json.loads(raw) if raw else None

    def current_user(self):
        return self.page.evaluate("() => KSAuth.getCurrentUser()")

    def open_sign_in(self):
        if self.page.locator('[data-page="welcome"]').is_visible():
            self.page.locator("#welcome-sign-in").click()
        else:
            self.page.locator("#open-account").click()

    def sign_in(self, user_id):
        account = self.accounts[user_id]
        self.open_sign_in()
        form = self.page.locator("#login-form")
        form.locator('[name="email"]').fill(account["email"])
        form.locator('[name="password"]').fill(account["password"])
        form.locator('[type="submit"]').click()
        self.page.wait_for_function(
            "id => KSAuth.getCurrentUser()?.id === id", arg=user_id
        )
        self.page.wait_for_function(
            "id => JSON.parse(localStorage.getItem('knowledge-stash-demo-session-v1'))?.userId === id",
            arg=user_id,
        )
        self.page.locator("#login-form").wait_for(state="hidden")
        # Successful sign-in may close the dialog or display the account summary.
        close = self.page.locator('#dialog [data-action="close"]')
        if close.is_visible():
            close.click()
        self.assertEqual(
            self.state(SESSION_KEY), {"schemaVersion": 1, "userId": user_id}
        )

    def sign_out(self):
        self.page.locator("#open-account").click()
        self.page.locator('[data-action="sign-out"]').click()
        self.page.wait_for_function("KSAuth.getCurrentUser() === null")
        self.page.wait_for_function(
            "localStorage.getItem('knowledge-stash-demo-session-v1') === null"
        )
        close = self.page.locator('#dialog [data-action="close"]')
        if close.is_visible():
            close.click()
        self.page.locator('[data-page="welcome"]').wait_for()
        self.assertEqual(self.page.locator("#account-label").inner_text(), "Guest")

    def bookmark(self, lesson_id):
        self.page.locator('[data-tab="discover"]').click()
        self.page.locator(f'[data-lesson="{lesson_id}"]').click()
        self.page.locator(f'[data-save="{lesson_id}"]').click()
        self.page.wait_for_function(
            "([key,id]) => JSON.parse(localStorage.getItem(key)).saved.includes(id)",
            arg=[profile_key(self.current_user()["id"]), lesson_id],
        )

    def test_wrong_password_and_session_contents(self):
        self.open_app()
        alex = self.accounts["demo-alex"]
        self.open_sign_in()
        form = self.page.locator("#login-form")
        form.locator('[name="email"]').fill(alex["email"])
        form.locator('[name="password"]').fill("incorrect-demo-password")
        form.locator('[type="submit"]').click()
        # Wait for the provider to reject and make the form usable again.
        self.page.wait_for_function(
            "!document.querySelector('#login-form button[type=submit]').disabled"
        )
        self.assertIsNone(self.stored(SESSION_KEY))
        self.assertIsNone(self.current_user())
        self.assertEqual(self.page.locator("#account-label").inner_text(), "Guest")
        self.page.locator('#dialog [data-action="close"]').click()
        self.sign_in("demo-alex")
        self.page.reload(wait_until="networkidle")
        self.page.wait_for_function("KSAuth.getCurrentUser()?.id === 'demo-alex'")
        self.assertNotEqual(self.page.locator("#account-label").inner_text(), "Guest")
        values = self.page.evaluate("() => Object.values(localStorage)")
        for account in self.accounts.values():
            self.assertFalse(any(account["password"] in value for value in values))
        self.sign_out()

    def test_profiles_preserve_guest_and_scope_backup_reset_restore(self):
        guest = empty_state()
        guest["saved"] = ["e1"]
        guest["theme"] = "dark"
        guest_raw = json.dumps(guest, separators=(",", ":"))
        legacy_raw = json.dumps({"saved": ["p1"], "theme": "light"})
        seed = {GUEST_KEY: guest_raw, OLD_KEY: legacy_raw}
        self.context.add_init_script(
            """(() => {
              const seed = %s;
              for (const [key,value] of Object.entries(seed)) {
                if (localStorage.getItem(key) === null) localStorage.setItem(key,value);
              }
            })();""" % json.dumps(seed)
        )
        self.open_app()
        self.sign_in("demo-alex")
        alex_key = profile_key("demo-alex")
        self.assertNotIn("e1", (self.state(alex_key) or {}).get("saved", []))
        self.bookmark("econ-prices")
        self.page.locator('[data-stage="next"]').click()
        alex_raw = self.stored(alex_key)
        self.sign_out()
        self.assertEqual(self.stored(GUEST_KEY), guest_raw)
        self.assertEqual(self.stored(OLD_KEY), legacy_raw)

        self.sign_in("demo-sam")
        sam_key = profile_key("demo-sam")
        self.assertNotIn("econ-prices", (self.state(sam_key) or {}).get("saved", []))
        self.bookmark("eng-faults")
        self.page.locator("#open-settings").click()
        with self.page.expect_download() as download:
            self.page.locator('[data-action="export"]').click()
        backup = Path(download.value.path()).read_bytes()
        exported = json.loads(backup)
        self.assertEqual(exported["state"]["saved"], ["eng-faults"])
        self.assertNotIn("econ-prices", exported["state"]["saved"])
        sam_before = self.state(sam_key)
        self.page.locator('[data-action="reset"]').click()
        self.page.wait_for_function(
            "key => JSON.parse(localStorage.getItem(key)).saved.length === 0", arg=sam_key
        )
        self.assertEqual(self.stored(alex_key), alex_raw)
        self.assertEqual(self.stored(GUEST_KEY), guest_raw)
        self.page.locator("#open-settings").click()
        self.page.locator("#backup-file").set_input_files(
            {"name": "demo-backup.json", "mimeType": "application/json", "buffer": backup}
        )
        self.page.wait_for_function(
            "key => JSON.parse(localStorage.getItem(key)).saved.includes('eng-faults')",
            arg=sam_key,
        )
        self.assertEqual(self.state(sam_key), sam_before)
        self.assertEqual(self.stored(alex_key), alex_raw)
        self.assertEqual(self.stored(GUEST_KEY), guest_raw)
        self.assertEqual(self.stored(OLD_KEY), legacy_raw)
        self.sign_out()
        self.sign_in("demo-alex")
        self.assertEqual(self.stored(alex_key), alex_raw)
        self.assertEqual(self.state(alex_key)["lessonProgress"]["econ-prices"]["stage"], 1)

    def test_corrupt_guest_recovery_preserves_original_bytes(self):
        corrupt_raw = '{"schemaVersion":2,"saved":["e1"],BROKEN'
        legacy_raw = '{"saved":["p1"],"theme":"dark"}'
        seed = {GUEST_KEY: corrupt_raw, OLD_KEY: legacy_raw}
        self.context.add_init_script(
            """(() => {
              const seed = %s;
              for (const [key,value] of Object.entries(seed)) {
                if (localStorage.getItem(key) === null) localStorage.setItem(key,value);
              }
            })();""" % json.dumps(seed)
        )
        self.open_app()
        self.page.locator("#open-settings").click()
        self.page.locator("#dark-toggle").check()
        self.assertEqual(self.stored(GUEST_KEY), corrupt_raw)
        with self.page.expect_download() as download:
            self.page.locator('[data-action="export"]').click()
        recovery = Path(download.value.path()).read_bytes()
        self.assertEqual(recovery, corrupt_raw.encode("utf-8"))
        self.page.locator('#dialog [data-action="close"]').click()
        self.sign_in("demo-alex")
        self.bookmark("econ-prices")
        self.sign_out()
        self.assertEqual(self.stored(GUEST_KEY), corrupt_raw)
        self.assertEqual(self.stored(OLD_KEY), legacy_raw)
        self.assertIn("econ-prices", self.state(profile_key("demo-alex"))["saved"])

    def test_delayed_backup_aborts_after_profile_switch(self):
        guest = empty_state()
        guest["saved"] = ["e1"]
        guest_raw = json.dumps(guest, separators=(",", ":"))
        self.context.add_init_script(
            """(() => {
              if (localStorage.getItem(%s) === null) localStorage.setItem(%s, %s);
            })();""" % (json.dumps(GUEST_KEY), json.dumps(GUEST_KEY), json.dumps(guest_raw))
        )
        self.open_app()
        self.sign_in("demo-sam")
        self.bookmark("eng-faults")
        sam_key = profile_key("demo-sam")
        sam_raw = self.stored(sam_key)
        candidate = empty_state()
        candidate["saved"] = ["p1"]
        backup = json.dumps({"format": "knowledge-stash-backup", "version": 2, "state": candidate}).encode()
        self.page.evaluate("""() => {
          const originalText = File.prototype.text;
          File.prototype.text = function() {
            return originalText.call(this).then(text => new Promise(resolve => {
              window.finishBackupRead = () => resolve(text);
            }));
          };
        }""")
        self.page.locator("#open-settings").click()
        self.page.locator("#backup-file").set_input_files(
            {"name": "delayed-backup.json", "mimeType": "application/json", "buffer": backup}
        )
        self.page.wait_for_function("typeof window.finishBackupRead === 'function'")
        self.page.locator('#dialog [data-action="close"]').click()
        self.sign_out()
        self.page.evaluate("() => window.finishBackupRead()")
        self.page.wait_for_function("document.querySelector('#toast').textContent.includes('Profile changed')")
        self.assertEqual(self.stored(GUEST_KEY), guest_raw)
        self.assertEqual(self.stored(sam_key), sam_raw)
        self.assertIsNone(self.stored(profile_key("demo-alex")))
        self.sign_in("demo-sam")
        self.assertEqual(self.stored(sam_key), sam_raw)

    def test_cached_accounts_sign_in_offline(self):
        self.open_app()
        self.page.wait_for_function("navigator.serviceWorker.controller !== null", timeout=15000)
        # The first controller change can reload the page; wait for application readiness.
        self.page.wait_for_function("window.KSAuth && document.querySelector('#login-form') === null")
        self.assertEqual(self.page.locator(".update-banner").count(), 0, "First install is not an app update")
        self.context.set_offline(True)
        try:
            self.page.reload(wait_until="networkidle")
            self.page.wait_for_function("window.KSAuth && document.querySelector('#account-label')?.textContent === 'Guest'")
            self.sign_in("demo-alex")
            self.bookmark("econ-prices")
            self.page.reload(wait_until="networkidle")
            self.page.wait_for_function("KSAuth.getCurrentUser()?.id === 'demo-alex'")
            self.assertIn("econ-prices", self.state(profile_key("demo-alex"))["saved"])
            self.sign_out()
        finally:
            self.context.set_offline(False)

    def test_login_under_repository_subpath(self):
        fixture_requests = []
        self.page.on(
            "request",
            lambda request: fixture_requests.append(request.url)
            if "/demo/accounts.json" in request.url else None,
        )
        self.open_app("/Knowledge-stash/")
        self.sign_in("demo-sam")
        self.assertTrue(
            any("/Knowledge-stash/demo/accounts.json" in url for url in fixture_requests),
            "Account fixture should resolve beneath the repository path",
        )
        self.bookmark("eng-faults")
        self.assertIn("eng-faults", self.state(profile_key("demo-sam"))["saved"])
        self.assertTrue(self.page.url.startswith(self.base + "/Knowledge-stash/"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
