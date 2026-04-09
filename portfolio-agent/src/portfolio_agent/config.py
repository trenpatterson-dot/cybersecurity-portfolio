from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

@dataclass(frozen=True)
class Settings:
    portfolio_root: Path
    output_dir: Path
    max_files_per_project: int
    max_chars_per_file: int
    max_pdf_pages: int
    max_file_size_bytes: int
    allowlist: set[str]
    denylist: set[str]


def _parse_name_list(raw_value: str) -> set[str]:
    return {
        item.strip().lower()
        for item in raw_value.split(",")
        if item.strip()
    }


def get_settings(base_dir: Path) -> Settings:
    load_dotenv(base_dir / ".env")

    portfolio_root = Path(os.getenv("PORTFOLIO_ROOT", str(base_dir.parent))).resolve()
    output_dir = Path(
        os.getenv("OUTPUT_DIR", str(portfolio_root / "agent-output"))
    ).resolve()

    return Settings(
        portfolio_root=portfolio_root,
        output_dir=output_dir,
        max_files_per_project=int(os.getenv("MAX_FILES_PER_PROJECT", "12")),
        max_chars_per_file=int(os.getenv("MAX_CHARS_PER_FILE", "12000")),
        max_pdf_pages=int(os.getenv("MAX_PDF_PAGES", "10")),
        max_file_size_bytes=int(os.getenv("MAX_FILE_SIZE_BYTES", "1048576")),
        allowlist=_parse_name_list(os.getenv("PROJECT_ALLOWLIST", "")),
        denylist=_parse_name_list(os.getenv("PROJECT_DENYLIST", "")),
    )
