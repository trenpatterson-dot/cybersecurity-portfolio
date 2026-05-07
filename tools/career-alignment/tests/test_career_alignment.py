import importlib.util
import json
import shutil
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "career_alignment.py"
SPEC = importlib.util.spec_from_file_location("career_alignment", MODULE_PATH)
career_alignment = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = career_alignment
SPEC.loader.exec_module(career_alignment)


class CareerAlignmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(__file__).resolve().parent / "_tmp"
        if self.tmp.exists():
            shutil.rmtree(self.tmp)
        self.tmp.mkdir(parents=True)

    def tearDown(self):
        if self.tmp.exists():
            shutil.rmtree(self.tmp)

    def make_lab(self, name: str, readme: str, with_evidence: bool = True):
        lab = self.tmp / "blue-team-labs" / name
        (lab / "docs").mkdir(parents=True)
        (lab / "queries").mkdir()
        (lab / "README.md").write_text(readme, encoding="utf-8")
        (lab / "docs" / "project-closeout-report.md").write_text("SOC closeout with evidence handling.", encoding="utf-8")
        (lab / "docs" / "github-readiness-report.md").write_text("GitHub readiness and privacy review complete.", encoding="utf-8")
        (lab / "queries" / "event-queries.txt").write_text("Event ID 4625 failed login query", encoding="utf-8")
        if with_evidence:
            (lab / "evidence" / "screenshots-public").mkdir(parents=True)
            (lab / "evidence" / "screenshots-public" / "failed-login-alert.png").write_bytes(b"\x89PNG\r\n\x1a\n")
        return lab

    def test_secret_like_files_are_skipped_without_content_read(self):
        lab = self.make_lab("windows-failed-login", "# Windows Failed Login\n\nWazuh SIEM Event ID 4625 failed login triage.")
        (lab / ".env").write_text("SHOULD_NOT_BE_READ=wazuh malware yara sigma", encoding="utf-8")

        report = career_alignment.build_report(self.tmp)

        self.assertIn("blue-team-labs/windows-failed-login/.env", report.secret_like_paths_skipped)
        self.assertEqual(report.skill_map["Malware analysis"]["status"], "MISSING")
        self.assertEqual(report.skill_map["YARA/Sigma"]["status"], "MISSING")

    def test_build_report_classifies_soc_ready_or_developing_with_evidence(self):
        self.make_lab(
            "windows-failed-login",
            "# Windows Failed Login Investigation\n\nWazuh SIEM Event ID 4625 failed login SOC triage with evidence screenshots.",
        )
        self.make_lab(
            "soc-alert-triage",
            "# SOC Alert Triage\n\nIncident response alert investigation, privacy review, GitHub workflow, and Python automation.",
        )

        report = career_alignment.build_report(self.tmp)

        self.assertIn(report.readiness_level, career_alignment.READINESS_LEVELS)
        self.assertIn(report.skill_map["Wazuh"]["status"], {"PARTIAL", "PROVEN"})
        self.assertIn(report.skill_map["Evidence handling"]["status"], {"PARTIAL", "PROVEN"})
        self.assertTrue(report.strongest_projects)

    def test_json_output_contains_expected_sections(self):
        self.make_lab(
            "soc-alert-triage",
            "# SOC Alert Triage\n\nSOC operations, incident response, evidence handling, and GitHub readiness.",
        )

        report = career_alignment.build_report(self.tmp)
        data = career_alignment.as_dict(report)

        self.assertIn("readiness_level", data)
        self.assertIn("skill_map", data)
        self.assertIn("suggested_next_labs", data)
        self.assertIn("suggested_github_pin_order", data)
        json.dumps(data)

    def test_output_directory_writes_markdown_and_json(self):
        self.make_lab("soc-alert-triage", "# SOC Alert Triage\n\nSOC operations and evidence handling.")
        report = career_alignment.build_report(self.tmp)
        output_paths = career_alignment.write_outputs(report, self.tmp / "reports")

        self.assertEqual(len(output_paths), 2)
        self.assertTrue((self.tmp / "reports" / "career-alignment.md").exists())
        self.assertTrue((self.tmp / "reports" / "career-alignment.json").exists())


if __name__ == "__main__":
    unittest.main()
