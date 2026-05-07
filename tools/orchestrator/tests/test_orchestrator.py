import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "orchestrator.py"
SPEC = importlib.util.spec_from_file_location("orchestrator", MODULE_PATH)
orchestrator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = orchestrator
SPEC.loader.exec_module(orchestrator)


class OrchestratorTests(unittest.TestCase):
    def test_all_ready_statuses_yield_workflow_ready(self):
        runs = [
            orchestrator.WrapperRun("evidence-validator", True, status="EVIDENCE READY"),
            orchestrator.WrapperRun("github-readiness", True, status="READY FOR REVIEW"),
            orchestrator.WrapperRun("project-closeout", True, status="CLOSEOUT READY"),
        ]

        status, reason = orchestrator.determine_overall_status(runs)

        self.assertEqual(status, "WORKFLOW READY")
        self.assertIn("ready", reason.lower())

    def test_downstream_ready_allows_evidence_organization_warning(self):
        runs = [
            orchestrator.WrapperRun("evidence-validator", True, status="NEEDS ORGANIZATION"),
            orchestrator.WrapperRun("github-readiness", True, status="READY FOR REVIEW"),
            orchestrator.WrapperRun("project-closeout", True, status="CLOSEOUT READY"),
        ]

        status, reason = orchestrator.determine_overall_status(runs)

        self.assertEqual(status, "WORKFLOW READY")
        self.assertIn("warnings", reason.lower())

    def test_missing_wrapper_yields_partial_toolchain(self):
        runs = [
            orchestrator.WrapperRun("evidence-validator", True, status="EVIDENCE READY"),
            orchestrator.WrapperRun("github-readiness", False),
            orchestrator.WrapperRun("project-closeout", True, status="CLOSEOUT READY"),
        ]

        status, _ = orchestrator.determine_overall_status(runs)

        self.assertEqual(status, "PARTIAL TOOLCHAIN")

    def test_blocker_yields_blocked(self):
        runs = [
            orchestrator.WrapperRun("evidence-validator", True, status="EVIDENCE READY"),
            orchestrator.WrapperRun("github-readiness", True, status="READY FOR REVIEW", blockers=["bad ref"]),
            orchestrator.WrapperRun("project-closeout", True, status="CLOSEOUT READY"),
        ]

        status, _ = orchestrator.determine_overall_status(runs)

        self.assertEqual(status, "BLOCKED")

    def test_safe_report_name(self):
        self.assertEqual(orchestrator.safe_report_name("GitHub Readiness", ".md"), "github-readiness.md")


if __name__ == "__main__":
    unittest.main()
