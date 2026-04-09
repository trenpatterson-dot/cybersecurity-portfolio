from __future__ import annotations

import os
from datetime import datetime, timedelta
from pathlib import Path

from portfolio_agent.main import main


EXPECTED_OUTPUT_FILES = {
    "eli10.md",
    "technical-summary.md",
    "github-update.md",
    "linkedin-post.md",
    "onenote-notes.md",
    "sources.md",
}


def write_project_file(path: Path, content: str, days_ago: int = 0) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    modified_at = datetime.now() - timedelta(days=days_ago)
    timestamp = modified_at.timestamp()
    os.utime(path, (timestamp, timestamp))


def create_project(root: Path, name: str, files: dict[str, tuple[str, int]]) -> Path:
    project_dir = root / name
    project_dir.mkdir(parents=True, exist_ok=True)
    for relative_path, (content, days_ago) in files.items():
        write_project_file(project_dir / relative_path, content, days_ago=days_ago)
    return project_dir


def configure_env(monkeypatch, portfolio_root: Path, output_dir: Path, denylist: str = "") -> None:
    monkeypatch.setenv("PORTFOLIO_ROOT", str(portfolio_root))
    monkeypatch.setenv("OUTPUT_DIR", str(output_dir))
    monkeypatch.setenv("MAX_FILES_PER_PROJECT", "12")
    monkeypatch.setenv("MAX_CHARS_PER_FILE", "12000")
    monkeypatch.setenv("MAX_PDF_PAGES", "10")
    monkeypatch.setenv("PROJECT_ALLOWLIST", "")
    monkeypatch.setenv("PROJECT_DENYLIST", denylist)


def run_agent(monkeypatch, args: list[str]) -> int:
    monkeypatch.setattr("sys.argv", ["agent.py", *args])
    return main()


def test_full_scan_mode_processes_all_eligible_projects(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(portfolio_root, "alpha-project", {"README.md": ("Alpha project summary.", 0)})
    create_project(portfolio_root, "beta-project", {"README.md": ("Beta project summary.", 0)})
    configure_env(monkeypatch, portfolio_root, output_dir)

    exit_code = run_agent(monkeypatch, [])
    captured = capsys.readouterr().out

    assert exit_code == 0
    assert "[+] Scanning alpha-project" in captured
    assert "[+] Scanning beta-project" in captured
    assert (output_dir / "alpha-project").is_dir()
    assert (output_dir / "beta-project").is_dir()


def test_single_project_mode_only_processes_named_project(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(portfolio_root, "alpha-project", {"README.md": ("Alpha project summary.", 0)})
    create_project(portfolio_root, "beta-project", {"README.md": ("Beta project summary.", 0)})
    configure_env(monkeypatch, portfolio_root, output_dir)

    exit_code = run_agent(monkeypatch, ["--project", "beta-project"])
    captured = capsys.readouterr().out

    assert exit_code == 0
    assert "[+] Scanning beta-project" in captured
    assert "[+] Scanning alpha-project" not in captured
    assert (output_dir / "beta-project").is_dir()
    assert not (output_dir / "alpha-project").exists()


def test_recent_days_mode_only_processes_recent_projects(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(portfolio_root, "recent-project", {"README.md": ("Recent project summary.", 1)})
    create_project(portfolio_root, "stale-project", {"README.md": ("Old project summary.", 20)})
    configure_env(monkeypatch, portfolio_root, output_dir)

    exit_code = run_agent(monkeypatch, ["--recent-days", "7"])
    captured = capsys.readouterr().out

    assert exit_code == 0
    assert "[+] Scanning recent-project" in captured
    assert "[+] Scanning stale-project" not in captured
    assert "stale-project (no supported files modified in the last 7 day(s))" in captured
    assert (output_dir / "recent-project").is_dir()
    assert not (output_dir / "stale-project").exists()


def test_project_and_recent_days_can_be_combined(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(portfolio_root, "phishing-analysis", {"README.md": ("Recent phishing notes.", 2)})
    create_project(portfolio_root, "other-project", {"README.md": ("Other project summary.", 1)})
    configure_env(monkeypatch, portfolio_root, output_dir)

    exit_code = run_agent(monkeypatch, ["--project", "phishing-analysis", "--recent-days", "7"])
    captured = capsys.readouterr().out

    assert exit_code == 0
    assert "[+] Scanning phishing-analysis" in captured
    assert "[+] Scanning other-project" not in captured
    assert (output_dir / "phishing-analysis").is_dir()
    assert not (output_dir / "other-project").exists()


def test_denylisted_project_returns_clear_error(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(portfolio_root, "journal", {"README.md": ("Journal entry.", 0)})
    configure_env(monkeypatch, portfolio_root, output_dir, denylist="journal")

    exit_code = run_agent(monkeypatch, ["--project", "journal"])
    captured = capsys.readouterr().out

    assert exit_code == 1
    assert "ERROR: Project folder 'journal' was found but skipped: denylisted or meta folder" in captured


def test_missing_project_returns_clear_error(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(portfolio_root, "alpha-project", {"README.md": ("Alpha project summary.", 0)})
    configure_env(monkeypatch, portfolio_root, output_dir)

    exit_code = run_agent(monkeypatch, ["--project", "missing-project"])
    captured = capsys.readouterr().out

    assert exit_code == 1
    assert f"ERROR: Project folder 'missing-project' does not exist in {portfolio_root}" in captured


def test_standardized_output_filenames_are_created(tmp_path, monkeypatch):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(
        portfolio_root,
        "phishing-analysis",
        {"README.md": ("Phishing project summary.", 0), "notes.txt": ("Extra note.", 0)},
    )
    configure_env(monkeypatch, portfolio_root, output_dir)

    exit_code = run_agent(monkeypatch, ["--project", "phishing-analysis"])

    assert exit_code == 0
    project_output = output_dir / "phishing-analysis"
    assert project_output.is_dir()
    assert {path.name for path in project_output.iterdir() if path.is_file()} == EXPECTED_OUTPUT_FILES
    sources_content = (project_output / "sources.md").read_text(encoding="utf-8")
    assert "README.md" in sources_content
    assert "notes.txt" in sources_content


def test_open_flag_prints_quick_access_paths_for_single_project(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(
        portfolio_root,
        "phishing-analysis",
        {"README.md": ("Phishing project summary.", 0)},
    )
    configure_env(monkeypatch, portfolio_root, output_dir)

    exit_code = run_agent(monkeypatch, ["--project", "phishing-analysis", "--open"])
    captured = capsys.readouterr().out
    project_output = output_dir / "phishing-analysis"

    assert exit_code == 0
    assert "Quick-access files:" in captured
    assert f"github-update.md : {project_output / 'github-update.md'}" in captured
    assert f"linkedin-post.md : {project_output / 'linkedin-post.md'}" in captured
    assert f"onenote-notes.md : {project_output / 'onenote-notes.md'}" in captured
