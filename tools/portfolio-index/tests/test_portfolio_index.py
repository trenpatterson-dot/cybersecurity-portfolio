import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "portfolio_index.py"
SPEC = importlib.util.spec_from_file_location("portfolio_index", MODULE_PATH)
portfolio_index = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = portfolio_index
SPEC.loader.exec_module(portfolio_index)

TEST_TMP = Path(__file__).resolve().parent / "_tmp"


class PortfolioIndexTests(unittest.TestCase):
    def test_secret_like_names_are_detected_without_contents(self):
        for name in [".env", ".env.local", "api_key.txt", "service-token.json", "private.pem"]:
            with self.subTest(name=name):
                self.assertTrue(portfolio_index.is_secret_like(Path(name)))

    def test_classify_workflow_ready(self):
        status = portfolio_index.classify_project(
            has_readme=True,
            has_docs=True,
            has_evidence=True,
            has_screenshots_public=True,
            has_queries=True,
            has_github_readiness=True,
            has_closeout_report=True,
            has_outputs=True,
            has_handoff=True,
            is_tool=False,
        )

        self.assertEqual(status, "WORKFLOW READY")

    def test_classify_local_only_without_readme(self):
        status = portfolio_index.classify_project(
            has_readme=False,
            has_docs=False,
            has_evidence=False,
            has_screenshots_public=False,
            has_queries=False,
            has_github_readiness=False,
            has_closeout_report=False,
            has_outputs=True,
            has_handoff=False,
            is_tool=False,
        )

        self.assertEqual(status, "LOCAL ONLY")

    def test_skill_tags_infer_windows_event_logs(self):
        root = TEST_TMP / "skill-tags"
        project = root / "windows-failed-login"
        project.mkdir(parents=True, exist_ok=True)
        (project / "README.md").write_text("Event ID 4625 in Windows Event Viewer", encoding="utf-8")

        tags = portfolio_index.infer_skill_tags(project, root)

        self.assertIn("Windows Event Logs", tags)
        self.assertIn("SOC Operations", tags)

    def test_write_outputs_creates_markdown_and_json(self):
        target = TEST_TMP / "reports"
        index = portfolio_index.PortfolioIndex(
            repo_path=str(TEST_TMP),
            reviewed_at="2026-05-07T00:00:00+00:00",
            projects=[],
        )

        paths = portfolio_index.write_outputs(index, target)

        self.assertEqual(len(paths), 2)
        self.assertTrue((target / "portfolio-index.md").exists())
        self.assertTrue((target / "portfolio-index.json").exists())


if __name__ == "__main__":
    unittest.main()
