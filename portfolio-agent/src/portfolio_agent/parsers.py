from __future__ import annotations

from pathlib import Path


def read_text_file(path: Path, max_chars: int) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:max_chars]
    except OSError:
        return ""


def read_docx_file(path: Path, max_chars: int) -> str:
    try:
        from docx import Document  # type: ignore
    except ImportError:
        return ""

    try:
        document = Document(str(path))
    except Exception:
        return ""

    lines = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
    return "\n".join(lines)[:max_chars]


def read_pdf_file(path: Path, max_chars: int, max_pages: int) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
    except ImportError:
        return ""

    try:
        reader = PdfReader(str(path))
    except Exception:
        return ""

    chunks = []
    for page in reader.pages[:max_pages]:
        try:
            page_text = page.extract_text() or ""
        except Exception:
            page_text = ""
        if page_text.strip():
            chunks.append(page_text.strip())

    return "\n".join(chunks)[:max_chars]


def read_supported_file(path: Path, max_chars: int, max_pdf_pages: int) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return read_text_file(path, max_chars)
    if suffix == ".docx":
        return read_docx_file(path, max_chars)
    if suffix == ".pdf":
        return read_pdf_file(path, max_chars, max_pdf_pages)
    return ""
