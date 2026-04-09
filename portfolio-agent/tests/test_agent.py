from __future__ import annotations

import os
from datetime import datetime, timedelta
from pathlib import Path

import pytest

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


def configure_env(
    monkeypatch,
    portfolio_root: Path,
    output_dir: Path,
    denylist: str = "",
    max_file_size_bytes: int = 1048576,
) -> None:
    monkeypatch.setenv("PORTFOLIO_ROOT", str(portfolio_root))
    monkeypatch.setenv("OUTPUT_DIR", str(output_dir))
    monkeypatch.setenv("MAX_FILES_PER_PROJECT", "12")
    monkeypatch.setenv("MAX_CHARS_PER_FILE", "12000")
    monkeypatch.setenv("MAX_PDF_PAGES", "10")
    monkeypatch.setenv("MAX_FILE_SIZE_BYTES", str(max_file_size_bytes))
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


def test_repeated_project_flag_returns_clear_error(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(portfolio_root, "phishing-analysis", {"README.md": ("Phishing project summary.", 0)})
    create_project(portfolio_root, "cyber-deception", {"README.md": ("Cyber deception summary.", 0)})
    configure_env(monkeypatch, portfolio_root, output_dir)

    exit_code = run_agent(
        monkeypatch,
        ["--project", "phishing-analysis", "--project", "cyber-deception"],
    )
    captured = capsys.readouterr().out

    assert exit_code == 1
    assert "ERROR: Repeated --project is not supported yet." in captured
    assert "Use exactly one --project value or run without --project for a full scan." in captured
    assert not output_dir.exists()


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


def test_pick_mode_processes_selected_project_only(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(portfolio_root, "alpha-project", {"README.md": ("Alpha project summary.", 0)})
    create_project(portfolio_root, "beta-project", {"README.md": ("Beta project summary.", 0)})
    configure_env(monkeypatch, portfolio_root, output_dir)
    monkeypatch.setattr("builtins.input", lambda _: "2")

    exit_code = run_agent(monkeypatch, ["--pick"])
    captured = capsys.readouterr().out

    assert exit_code == 0
    assert "Pick a project:" in captured
    assert "1. alpha-project" in captured
    assert "2. beta-project" in captured
    assert "[+] Scanning beta-project" in captured
    assert "[+] Scanning alpha-project" not in captured
    assert (output_dir / "beta-project").is_dir()
    assert not (output_dir / "alpha-project").exists()


def test_pick_mode_with_recent_days_filters_the_list_first(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(portfolio_root, "recent-project", {"README.md": ("Recent project summary.", 1)})
    create_project(portfolio_root, "stale-project", {"README.md": ("Old project summary.", 20)})
    configure_env(monkeypatch, portfolio_root, output_dir)
    monkeypatch.setattr("builtins.input", lambda _: "1")

    exit_code = run_agent(monkeypatch, ["--pick", "--recent-days", "7"])
    captured = capsys.readouterr().out

    assert exit_code == 0
    assert "Pick a project:" in captured
    assert "1. recent-project" in captured
    assert "stale-project" not in captured.split("Pick a project:")[-1]
    assert "[+] Scanning recent-project" in captured
    assert not (output_dir / "stale-project").exists()


def test_pick_and_project_flags_together_return_clear_error(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(portfolio_root, "phishing-analysis", {"README.md": ("Phishing project summary.", 0)})
    configure_env(monkeypatch, portfolio_root, output_dir)

    exit_code = run_agent(monkeypatch, ["--pick", "--project", "phishing-analysis"])
    captured = capsys.readouterr().out

    assert exit_code == 1
    assert "ERROR: Use only one of --pick or --project." in captured


def test_secret_like_files_are_excluded_from_sources_and_outputs(tmp_path, monkeypatch):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(
        portfolio_root,
        "safe-project",
        {
            "README.md": ("Safe project summary.", 0),
            "api.txt": ("API_KEY=super-secret-value", 0),
            ".env": ("OPENAI_API_KEY=super-secret-value", 0),
            "notes.txt": ("Visible project notes.", 0),
        },
    )
    configure_env(monkeypatch, portfolio_root, output_dir)

    exit_code = run_agent(monkeypatch, ["--project", "safe-project"])

    assert exit_code == 0
    sources_content = (output_dir / "safe-project" / "sources.md").read_text(encoding="utf-8")
    assert "README.md" in sources_content
    assert "notes.txt" in sources_content
    assert "api.txt" not in sources_content
    assert ".env" not in sources_content


def test_project_with_only_secret_like_files_is_skipped(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(
        portfolio_root,
        "secret-only-project",
        {
            "api.txt": ("API_KEY=super-secret-value", 0),
            ".env": ("OPENAI_API_KEY=super-secret-value", 0),
            "private.key": ("super-secret-key-material", 0),
        },
    )
    configure_env(monkeypatch, portfolio_root, output_dir)

    exit_code = run_agent(monkeypatch, [])
    captured = capsys.readouterr().out

    assert exit_code == 1
    assert "No eligible project folders were found after discovery rules were applied." in captured
    assert not (output_dir / "secret-only-project").exists()


def test_public_mode_sanitizes_outputs_and_source_listing(tmp_path, monkeypatch):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(
        portfolio_root,
        "phishing-analysis",
        {
            "README.md": (
                "This project documents phishing analysis steps. "
                "OPENAI_API_KEY=super-secret-value "
                "Internal-only path C:\\Users\\tester\\secret\\note.txt "
                "and internal-only notes should not be published.",
                0,
            ),
            "docs/internal-notes.md": (
                "Internal-only observation with token=abc123secret and private troubleshooting detail.",
                0,
            ),
        },
    )
    configure_env(monkeypatch, portfolio_root, output_dir)

    exit_code = run_agent(monkeypatch, ["--project", "phishing-analysis", "--public"])

    assert exit_code == 0
    project_output = output_dir / "phishing-analysis"
    technical = (project_output / "technical-summary.md").read_text(encoding="utf-8")
    github_update = (project_output / "github-update.md").read_text(encoding="utf-8")
    linkedin = (project_output / "linkedin-post.md").read_text(encoding="utf-8")
    onenote = (project_output / "onenote-notes.md").read_text(encoding="utf-8")
    sources = (project_output / "sources.md").read_text(encoding="utf-8")

    for content in [technical, github_update, linkedin, onenote]:
        assert "super-secret-value" not in content
        assert "C:\\Users\\tester\\secret\\note.txt" not in content
        assert "internal-only" not in content.lower()

    assert "Public mode" in technical
    assert "README.md" in sources
    assert "internal-notes.md" in sources
    assert "docs/internal-notes.md" not in sources
    assert "Only safe source filenames are shown in public mode." in sources


def test_oversized_supported_files_are_skipped(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    large_text = "A" * 5000
    create_project(
        portfolio_root,
        "size-limited-project",
        {
            "README.md": ("Visible summary.", 0),
            "large-notes.txt": (large_text, 0),
        },
    )
    configure_env(monkeypatch, portfolio_root, output_dir, max_file_size_bytes=128)

    exit_code = run_agent(monkeypatch, ["--project", "size-limited-project"])
    captured = capsys.readouterr().out

    assert exit_code == 0
    assert "[+] Scanning size-limited-project" in captured
    sources = (output_dir / "size-limited-project" / "sources.md").read_text(encoding="utf-8")
    assert "README.md" in sources
    assert "large-notes.txt" not in sources


def test_binary_text_file_is_skipped(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    project_dir = portfolio_root / "binary-project"
    project_dir.mkdir(parents=True, exist_ok=True)
    write_project_file(project_dir / "README.md", "Visible summary.", 0)
    binary_path = project_dir / "capture.txt"
    binary_path.write_bytes(b"\x00\x01\x02\x03binary")
    configure_env(monkeypatch, portfolio_root, output_dir)

    exit_code = run_agent(monkeypatch, ["--project", "binary-project"])
    captured = capsys.readouterr().out

    assert exit_code == 0
    assert "[+] Scanning binary-project" in captured
    sources = (output_dir / "binary-project" / "sources.md").read_text(encoding="utf-8")
    assert "README.md" in sources
    assert "capture.txt" not in sources


def test_symlinked_project_pointing_outside_root_is_skipped(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    outside_dir = tmp_path / "outside-project"
    outside_dir.mkdir(parents=True, exist_ok=True)
    write_project_file(outside_dir / "README.md", "Outside summary.", 0)
    link_path = portfolio_root / "linked-project"
    portfolio_root.mkdir(parents=True, exist_ok=True)

    try:
        link_path.symlink_to(outside_dir, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("Symlink creation is not available in this environment.")

    configure_env(monkeypatch, portfolio_root, output_dir)
    exit_code = run_agent(monkeypatch, [])
    captured = capsys.readouterr().out

    assert exit_code == 1
    assert "linked-project (linked or out-of-root folder)" in captured
    assert not (output_dir / "linked-project").exists()


def test_dry_run_shows_planned_projects_and_sources_without_writing_files(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(
        portfolio_root,
        "phishing-analysis",
        {"README.md": ("Phishing summary.", 0), "notes.txt": ("Extra notes.", 0)},
    )
    configure_env(monkeypatch, portfolio_root, output_dir)

    exit_code = run_agent(monkeypatch, ["--project", "phishing-analysis", "--dry-run"])
    captured = capsys.readouterr().out

    assert exit_code == 0
    assert "[DRY-RUN] Would process phishing-analysis" in captured
    assert "README.md" in captured
    assert "notes.txt" in captured
    assert "Run index      : not written in dry-run mode" in captured
    assert not output_dir.exists()


def test_dry_run_with_open_prints_clear_no_write_message(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(portfolio_root, "phishing-analysis", {"README.md": ("Phishing summary.", 0)})
    configure_env(monkeypatch, portfolio_root, output_dir)

    exit_code = run_agent(monkeypatch, ["--project", "phishing-analysis", "--dry-run", "--open"])
    captured = capsys.readouterr().out

    assert exit_code == 0
    assert "Quick-access files: no output files were written because --dry-run was used." in captured
    assert not output_dir.exists()


def test_pick_mode_works_with_dry_run(tmp_path, monkeypatch, capsys):
    portfolio_root = tmp_path / "portfolio"
    output_dir = tmp_path / "agent-output"
    create_project(portfolio_root, "alpha-project", {"README.md": ("Alpha project summary.", 0)})
    create_project(portfolio_root, "beta-project", {"README.md": ("Beta project summary.", 0)})
    configure_env(monkeypatch, portfolio_root, output_dir)
    monkeypatch.setattr("builtins.input", lambda _: "1")

    exit_code = run_agent(monkeypatch, ["--pick", "--dry-run"])
    captured = capsys.readouterr().out

    assert exit_code == 0
    assert "Pick a project:" in captured
    assert "[DRY-RUN] Would process alpha-project" in captured
    assert not output_dir.exists()
