import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "recruiter_portfolio.py"
SPEC = importlib.util.spec_from_file_location("recruiter_portfolio", MODULE_PATH)
recruiter_portfolio = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = recruiter_portfolio
SPEC.loader.exec_module(recruiter_portfolio)

TEST_TMP = Path(__file__).resolve().parent / "_tmp"


class RecruiterPortfolioTests(unittest.TestCase):
    def test_secret_like_names_are_detected_without_contents(self):
        for name in [".env", ".env.local", "api_key.txt", "service-token.json", "private.pem"]:
            with self.subTest(name=name):
                self.assertTrue(recruiter_portfolio.is_secret_like(Path(name)))

    def test_status_workflow_ready(self):
        root = TEST_TMP / "workflow-ready"
        project = root / "lab"
        (project / "docs").mkdir(parents=True, exist_ok=True)
        (project / "evidence" / "screenshots-public").mkdir(parents=True, exist_ok=True)
        (project / "README.md").write_text("# Lab\n", encoding="utf-8")
        (project / "docs" / "github-readiness-report.md").write_text("READY", encoding="utf-8")
        (project / "docs" / "project-closeout-report.md").write_text("READY", encoding="utf-8")

        self.assertEqual(recruiter_portfolio.status_for(project), "WORKFLOW READY")

    def test_skill_tags_infer_windows_event_logs(self):
        root = TEST_TMP / "skill-tags"
        project = root / "windows-failed-login"
        project.mkdir(parents=True, exist_ok=True)
        (project / "README.md").write_text("Event ID 4625 in Windows Event Viewer", encoding="utf-8")

        tags = recruiter_portfolio.infer_skill_tags(project, root)

        self.assertIn("Windows Event Logs", tags)
        self.assertIn("SOC Operations", tags)

    def test_project_dict_contains_presentation_flags(self):
        project = recruiter_portfolio.ProjectCard(
            name="lab",
            path="blue-team-labs/lab",
            status="WORKFLOW READY",
            headline="Lab",
            github_pin_candidate=True,
            linkedin_feature_candidate=True,
        )

        data = recruiter_portfolio.project_to_dict(project)

        self.assertTrue(data["github_pin_candidate"])
        self.assertTrue(data["linkedin_feature_candidate"])

    def test_write_outputs_creates_markdown_and_json(self):
        target = TEST_TMP / "reports"
        portfolio = recruiter_portfolio.RecruiterPortfolio(
            repo_path=str(TEST_TMP),
            reviewed_at="2026-05-07T00:00:00+00:00",
            story_summary="SOC story",
            featured_projects=[],
            github_pin_candidates=[],
            linkedin_feature_candidates=[],
            cleanup_warnings=[],
            skill_map={},
            all_projects=[],
        )

        paths = recruiter_portfolio.write_outputs(portfolio, target)

        self.assertEqual(len(paths), 2)
        self.assertTrue((target / "recruiter-portfolio.md").exists())
        self.assertTrue((target / "recruiter-portfolio.json").exists())


if __name__ == "__main__":
    unittest.main()
