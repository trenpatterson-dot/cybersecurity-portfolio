import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "github_readiness.py"
SPEC = importlib.util.spec_from_file_location("github_readiness", MODULE_PATH)
github_readiness = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = github_readiness
SPEC.loader.exec_module(github_readiness)


class GitHubReadinessTests(unittest.TestCase):
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
                self.assertTrue(github_readiness.is_secret_like(Path(name)))

    def test_cybersecurity_screenshot_name_is_not_secret_like(self):
        path = Path("evidence/screenshots/05-pam-login-session-details.png")

        self.assertFalse(github_readiness.is_secret_like(path))

    def test_readme_image_refs_are_parsed(self):
        text = """
# Test
![One](evidence/screenshots-public/one.png)
<img src="evidence/screenshots-public/two.png">
"""

        self.assertEqual(
            github_readiness.parse_readme_image_refs(text),
            ["evidence/screenshots-public/one.png", "evidence/screenshots-public/two.png"],
        )

    def test_credentialed_remote_detection(self):
        line = "origin\thttps://user:secret@example.com/repo.git (fetch)"

        self.assertRegex(line, github_readiness.CREDENTIALED_REMOTE_RE)


if __name__ == "__main__":
    unittest.main()
