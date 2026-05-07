import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "evidence_validator.py"
SPEC = importlib.util.spec_from_file_location("evidence_validator", MODULE_PATH)
evidence_validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = evidence_validator
SPEC.loader.exec_module(evidence_validator)


class EvidenceValidatorTests(unittest.TestCase):
    def test_cybersecurity_screenshot_terms_are_not_secret_like(self):
        paths = [
            Path("evidence/screenshots/05-pam-login-session-details.png"),
            Path("evidence/screenshots/06-token-event-alert-details.png"),
        ]

        for path in paths:
            with self.subTest(path=str(path)):
                self.assertFalse(evidence_validator.is_secret_like(path))

    def test_real_secret_like_names_are_secret_like(self):
        secret_names = [
            ".env",
            ".env.local",
            "db-secret.txt",
            "admin-password.txt",
            "service-passwd.txt",
            "cloud-credential.json",
            "refresh-token.txt",
            "client-api_key.txt",
            "private.pem",
            "tls.key",
            "cert.pfx",
            "bundle.p12",
        ]

        for name in secret_names:
            with self.subTest(name=name):
                self.assertTrue(evidence_validator.is_secret_like(Path(name)))

    def test_handoff_detection_matches_project_handoff_names(self):
        handoff_names = [
            "HANDOFF.md",
            "SOC_Triage_HANDOFF.md",
            "soc-triage-handoff.md",
        ]

        for name in handoff_names:
            with self.subTest(name=name):
                self.assertTrue(evidence_validator.is_handoff_file(Path(name)))

if __name__ == "__main__":
    unittest.main()
