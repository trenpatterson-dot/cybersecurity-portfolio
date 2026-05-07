import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "project_closeout.py"
SPEC = importlib.util.spec_from_file_location("project_closeout", MODULE_PATH)
project_closeout = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = project_closeout
SPEC.loader.exec_module(project_closeout)


class ProjectCloseoutTests(unittest.TestCase):
    def test_secret_like_names_are_detected_without_contents(self):
        secret_names = [
            ".env",
            ".env.local",
            "api_key.txt",
            "db-password.txt",
            "service-token.json",
            "private.pem",
            "tls.key",
            "bundle.p12",
            "cert.pfx",
        ]

        for name in secret_names:
            with self.subTest(name=name):
                self.assertTrue(project_closeout.is_secret_like(Path(name)))

    def test_cybersecurity_screenshot_name_is_not_secret_like(self):
        path = Path("evidence/screenshots/05-pam-login-session-details.png")

        self.assertFalse(project_closeout.is_secret_like(path))

    def test_extract_status_finds_closeout_decision(self):
        text = "# Project Closeout Report\n\n- Status: CLOSEOUT READY\n"

        self.assertEqual(
            project_closeout.extract_status(text, project_closeout.DECISIONS),
            "CLOSEOUT READY",
        )

    def test_closeout_ready_yields_ready_decision(self):
        status, reason = project_closeout.determine_status([], [], [], [])

        self.assertEqual(status, "CLOSEOUT READY")
        self.assertIn("human approval", reason)

    def test_security_blocker_takes_priority(self):
        status, reason = project_closeout.determine_status(
            ["secret-like filename found"],
            ["raw screenshot is not ignored/local-only"],
            [],
            [],
        )

        self.assertEqual(status, "SECURITY BLOCKED")
        self.assertEqual(reason, "secret-like filename found")


if __name__ == "__main__":
    unittest.main()
