"""Smoke tests for the current app.main startup flow."""

from __future__ import annotations

from pathlib import Path

from app import main as main_module


def test_main_starts_successfully_with_temp_database(monkeypatch, tmp_path, capsys):
    """Proves the current main entry point can start cleanly with test settings."""

    database_path = tmp_path / "agent.db"

    monkeypatch.setattr("app.config._load_local_dotenv", lambda: None)
    monkeypatch.setenv("AMAZON_ASSOCIATE_TAG", "yourtag-20")
    monkeypatch.setenv("DATABASE_PATH", str(database_path))
    monkeypatch.setenv("DRY_RUN", "true")

    result = main_module.main()
    captured = capsys.readouterr()

    assert result == 0
    assert "Workflow Summary" in captured.out
    assert database_path.exists()


def test_main_falls_back_to_mock_when_creators_api_is_selected_but_incomplete(
    monkeypatch, tmp_path, capsys
):
    """Proves the app stays usable when real-provider config is not ready yet."""

    database_path = tmp_path / "agent.db"

    monkeypatch.setattr("app.config._load_local_dotenv", lambda: None)
    monkeypatch.setenv("AMAZON_ASSOCIATE_TAG", "yourtag-20")
    monkeypatch.setenv("DATABASE_PATH", str(database_path))
    monkeypatch.setenv("DRY_RUN", "true")
    monkeypatch.setenv("PRODUCT_SOURCE_PROVIDER", "creators_api")

    result = main_module.main()
    captured = capsys.readouterr()

    assert result == 0
    assert "Workflow Summary" in captured.out
    assert database_path.exists()


def test_main_returns_error_when_config_is_incomplete(monkeypatch, capsys):
    """Proves startup exits cleanly with a friendly config error."""

    monkeypatch.setattr("app.config._load_local_dotenv", lambda: None)
    monkeypatch.delenv("AMAZON_ASSOCIATE_TAG", raising=False)

    result = main_module.main()
    captured = capsys.readouterr()

    assert result == 1
    assert "Configuration is incomplete" in captured.out
