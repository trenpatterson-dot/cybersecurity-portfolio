from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from .scanner import ProjectScan


TOOL_KEYWORDS = {
    "nmap": "Nmap",
    "wireshark": "Wireshark",
    "wazuh": "Wazuh",
    "splunk": "Splunk",
    "suricata": "Suricata",
    "zeek": "Zeek",
    "rita": "RITA",
    "metasploit": "Metasploit",
    "burp": "Burp Suite",
    "kali": "Kali Linux",
    "linux": "Linux",
    "windows": "Windows",
    "python": "Python",
    "elastic": "Elastic Stack",
    "ssh": "SSH",
    "hydra": "Hydra",
    "dns": "DNS",
    "tcp": "TCP/IP",
}

TOPIC_KEYWORDS = {
    "network": "network-security",
    "phishing": "phishing-analysis",
    "wazuh": "threat-hunting",
    "splunk": "siem",
    "suricata": "intrusion-detection",
    "zeek": "network-telemetry",
    "metasploit": "penetration-testing",
    "web": "web-security",
    "owasp": "owasp",
    "active directory": "active-directory",
    "brute force": "brute-force-detection",
    "dns": "dns-analysis",
    "ssh": "ssh-monitoring",
}

STOPWORDS = {
    "about",
    "after",
    "also",
    "and",
    "been",
    "from",
    "into",
    "that",
    "this",
    "were",
    "with",
    "your",
    "readme",
    "project",
    "using",
    "used",
    "user",
    "lab",
}


@dataclass
class ProjectAnalysis:
    project_title: str
    project_slug: str
    sources_reviewed: list[str]
    headings: list[str]
    tools: list[str]
    topics: list[str]
    summary_sentences: list[str]
    keyword_highlights: list[str]


def analyze_project(scan: ProjectScan) -> ProjectAnalysis:
    combined_text = "\n\n".join(source.content for source in scan.sources)
    headings = _extract_headings(scan)
    tools = _extract_tools(combined_text)
    topics = _extract_topics(combined_text)
    summary_sentences = _extract_summary_sentences(combined_text)
    keyword_highlights = _extract_keyword_highlights(combined_text)

    return ProjectAnalysis(
        project_title=_humanize_name(scan.project_name),
        project_slug=_slugify(scan.project_name),
        sources_reviewed=[source.relative_path for source in scan.sources],
        headings=headings,
        tools=tools,
        topics=topics,
        summary_sentences=summary_sentences,
        keyword_highlights=keyword_highlights,
    )


def write_project_outputs(scan: ProjectScan, output_root: Path) -> Path:
    analysis = analyze_project(scan)
    project_output_dir = output_root / analysis.project_slug
    project_output_dir.mkdir(parents=True, exist_ok=True)

    _clear_existing_output_files(project_output_dir)

    files = {
        "eli10.md": build_eli10_summary(analysis, scan),
        "technical-summary.md": build_technical_summary(analysis, scan),
        "github-update.md": build_github_readme_update(analysis, scan),
        "linkedin-post.md": build_linkedin_post(analysis, scan),
        "onenote-notes.md": build_onenote_notes(analysis, scan),
        "sources.md": build_source_manifest(analysis, scan),
    }

    for filename, content in files.items():
        (project_output_dir / filename).write_text(content, encoding="utf-8")

    return project_output_dir


def build_eli10_summary(analysis: ProjectAnalysis, scan: ProjectScan) -> str:
    intro = (
        f"# ELI10 Summary: {analysis.project_title}\n\n"
        f"This project is like a safety check for a digital building. "
        f"The goal was to look for signs of trouble, understand what was happening, "
        f"and explain why it matters in simple language.\n\n"
    )
    body = [
        *_limited_source_notice(scan),
        "## In Plain English",
        f"- The project folder was reviewed locally using notes and write-ups already inside `{scan.project_path.name}`.",
        f"- Main idea: {_sentence_or_default(analysis.summary_sentences, 0, 'The project focuses on identifying, documenting, and explaining a cybersecurity task or lab.')}",
        f"- Why it matters: {_sentence_or_default(analysis.summary_sentences, 1, 'It helps show how defenders or analysts notice problems, investigate them, and learn from them.')}",
        f"- Tools involved: {', '.join(analysis.tools) if analysis.tools else 'The written notes did not clearly name tools, but the project still documents a real workflow.'}",
        "- Big takeaway: cybersecurity work is often about collecting clues, checking evidence, and turning technical steps into clear decisions.",
    ]
    return intro + "\n".join(body) + "\n"


def build_technical_summary(analysis: ProjectAnalysis, scan: ProjectScan) -> str:
    lines = [
        f"# Technical Summary: {analysis.project_title}",
        "",
        *_limited_source_notice(scan),
        "## Overview",
        f"- Project folder: `{scan.project_path.name}`",
        f"- Sources reviewed: {len(scan.sources)}",
        f"- Focus areas: {', '.join(analysis.topics) if analysis.topics else 'cybersecurity documentation, analysis, and lab execution'}",
        "",
        "## What The Project Appears To Cover",
    ]
    if analysis.summary_sentences:
        lines.extend(f"- {sentence}" for sentence in analysis.summary_sentences[:5])
    else:
        lines.append("- The available files describe a hands-on cybersecurity project, but there was limited extractable text to summarize.")

    lines.extend(
        [
            "",
            "## Tools And Technologies Detected",
            f"- {', '.join(analysis.tools) if analysis.tools else 'No specific tools were confidently detected from the available text.'}",
            "",
            "## Skills Demonstrated",
            "- Reading and documenting technical evidence",
            "- Converting lab activity into a structured portfolio artifact",
            "- Explaining security work in both simple and technical language",
        ]
    )
    if analysis.keyword_highlights:
        lines.append(f"- Repeated technical signals: {', '.join(analysis.keyword_highlights[:8])}")

    lines.extend(
        [
            "",
            "## Suggested Portfolio Framing",
            "- State the lab objective in one sentence.",
            "- List the tools used and why they were chosen.",
            "- Summarize the workflow from setup to findings.",
            "- End with what was learned and how it maps to analyst skills.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_github_readme_update(analysis: ProjectAnalysis, scan: ProjectScan) -> str:
    lines = [
        f"# GitHub-Ready README Text: {analysis.project_title}",
        "",
        *_limited_source_notice(scan),
        "## Project Summary",
        f"{analysis.project_title} is a cybersecurity portfolio project that documents a hands-on exercise focused on {', '.join(analysis.topics) if analysis.topics else 'security analysis and lab documentation'}. The project was reviewed locally from the existing files in this folder and rewritten into a cleaner portfolio format.",
        "",
        "## Objectives",
        f"- Document the purpose of `{scan.project_path.name}` in a way that is easy for recruiters and hiring managers to understand.",
        "- Highlight the workflow, findings, and analyst mindset used during the project.",
        "- Preserve the technical value while keeping the write-up easy to scan on GitHub.",
        "",
        "## Tools Used",
        f"- {', '.join(analysis.tools) if analysis.tools else 'Add the main tools used in the project here.'}",
        "",
        "## Key Takeaways",
    ]
    if analysis.summary_sentences:
        lines.extend(f"- {sentence}" for sentence in analysis.summary_sentences[:4])
    else:
        lines.append("- Add a short list of the most important findings, outcomes, or lessons learned.")

    lines.extend(
        [
            "",
            "## Skills Demonstrated",
            "- Security analysis",
            "- Technical documentation",
            "- Evidence review and summarization",
            "- Communication for mixed technical and non-technical audiences",
        ]
    )
    return "\n".join(lines) + "\n"


def build_linkedin_post(analysis: ProjectAnalysis, scan: ProjectScan) -> str:
    hook = f"Turned another cybersecurity lab into a portfolio-ready write-up: {analysis.project_title}."
    lesson_one = _sentence_or_default(
        analysis.summary_sentences,
        0,
        "This project reinforced how important clear documentation is during technical investigations.",
    )
    lesson_two = _sentence_or_default(
        analysis.summary_sentences,
        1,
        "It also showed how much value comes from connecting tools, findings, and analyst thinking in one place.",
    )
    hashtags = " ".join(f"#{topic.replace('-', '')}" for topic in analysis.topics[:4]) or "#Cybersecurity #SOCAnalyst #BlueTeam #Homelab"
    limited_notice = "\n".join(_limited_source_notice(scan))
    if limited_notice:
        limited_notice = limited_notice + "\n"

    return (
        f"# LinkedIn Post Draft: {analysis.project_title}\n\n"
        f"{limited_notice}"
        f"{hook}\n\n"
        f"Two things this project helped me practice:\n"
        f"- {lesson_one}\n"
        f"- {lesson_two}\n\n"
        f"I also used the project notes inside `{scan.project_path.name}` to turn raw lab material into a cleaner, recruiter-friendly summary.\n\n"
        f"What is one cybersecurity skill you think becomes more valuable when it is documented clearly?\n\n"
        f"{hashtags}\n"
    )


def build_onenote_notes(analysis: ProjectAnalysis, scan: ProjectScan) -> str:
    lines = [
        f"# OneNote Notes: {analysis.project_title}",
        "",
        *_limited_source_notice(scan),
        "## Snapshot",
        f"- Project folder: `{scan.project_path.name}`",
        f"- Sources reviewed: {len(scan.sources)}",
        f"- Primary topics: {', '.join(analysis.topics) if analysis.topics else 'security analysis and documentation'}",
        "",
        "## Main Points",
    ]
    if analysis.summary_sentences:
        lines.extend(f"- {sentence}" for sentence in analysis.summary_sentences[:6])
    else:
        lines.append("- The project contains limited extractable text, so review screenshots or source documents manually if needed.")

    lines.extend(
        [
            "",
            "## Tools",
            f"- {', '.join(analysis.tools) if analysis.tools else 'Add the confirmed tools here after a manual review.'}",
            "",
            "## Headings Found In Notes",
        ]
    )
    if analysis.headings:
        lines.extend(f"- {heading}" for heading in analysis.headings[:10])
    else:
        lines.append("- No markdown headings were detected in the reviewed files.")

    lines.extend(
        [
            "",
            "## Follow-Up Ideas",
            "- Add a short timeline of the work performed.",
            "- Add screenshots or command snippets if they strengthen the evidence.",
            "- Convert the strongest takeaway into a resume bullet or interview story.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_source_manifest(analysis: ProjectAnalysis, scan: ProjectScan) -> str:
    lines = [
        f"# Sources: {analysis.project_title}",
        "",
        "These are the files the local agent reviewed while generating the output.",
        "",
    ]
    if not scan.sources:
        lines.append("- No supported text sources were available.")
    else:
        for source in scan.sources:
            lines.append(f"- `{source.relative_path}` ({source.source_type})")
    return "\n".join(lines) + "\n"


def _clear_existing_output_files(project_output_dir: Path) -> None:
    for child in project_output_dir.iterdir():
        if child.is_file():
            child.unlink()


def _limited_source_notice(scan: ProjectScan) -> list[str]:
    if len(scan.sources) == 0:
        return [
            "> Limited source material: no supported text files were available. This file was created with placeholder guidance so the output structure stays consistent.",
            "",
        ]
    if len(scan.sources) <= 2:
        return [
            f"> Limited source material: this summary is based on only {len(scan.sources)} source file(s), so some sections may need manual refinement.",
            "",
        ]
    return []


def _extract_headings(scan: ProjectScan) -> list[str]:
    headings: list[str] = []
    for source in scan.sources:
        for line in source.content.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                headings.append(stripped.lstrip("#").strip())
    return _dedupe_preserve_order(headings)


def _extract_tools(text: str) -> list[str]:
    lowered = text.lower()
    detected = [label for keyword, label in TOOL_KEYWORDS.items() if keyword in lowered]
    return detected


def _extract_topics(text: str) -> list[str]:
    lowered = text.lower()
    topics = [label for keyword, label in TOPIC_KEYWORDS.items() if keyword in lowered]
    return topics


def _extract_summary_sentences(text: str) -> list[str]:
    cleaned = _normalize_source_text(text)
    raw_sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    selected = []
    for sentence in raw_sentences:
        sentence = re.sub(r"^[^A-Za-z0-9]+", "", sentence.strip(" -#>"))
        if len(sentence) < 60 or len(sentence) > 220:
            continue
        if sentence.lower().startswith(("copyright", "license", "image", "http")):
            continue
        selected.append(sentence)
        if len(selected) == 8:
            break
    return selected


def _extract_keyword_highlights(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z\-]{3,}", _normalize_source_text(text).lower())
    counts = Counter(word for word in words if word not in STOPWORDS)
    return [word for word, _ in counts.most_common(12)]


def _dedupe_preserve_order(items: list[str]) -> list[str]:
    seen = set()
    ordered = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def _humanize_name(name: str) -> str:
    return re.sub(r"[-_]+", " ", name).strip().title()


def _slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _sentence_or_default(sentences: list[str], index: int, default: str) -> str:
    if index < len(sentences):
        return sentences[index]
    return default


def _normalize_source_text(text: str) -> str:
    cleaned = text
    cleaned = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    cleaned = re.sub(r"`{1,3}", "", cleaned)
    cleaned = re.sub(r"^#{1,6}\s*", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^\s*[-*_]{3,}\s*$", " ", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()
