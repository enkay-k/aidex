#!/usr/bin/env python3
"""Build a static HTML docs site from project Markdown files."""

from __future__ import annotations

import argparse
import html
import posixpath
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_ROOT = REPO_ROOT / "docs"
SITE_ROOT = DOCS_ROOT / "site"

SOURCE_GLOBS = [
    "docs/**/*.md",
    "docs/**/*.mmd",
    "src/**/*.md",
    "tests/**/*.md",
    "requirements.md",
    "Readme.md",
]

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
UL_RE = re.compile(r"^\s*[-*]\s+(.*)$")
OL_RE = re.compile(r"^\s*\d+\.\s+(.*)$")
TABLE_DIVIDER_RE = re.compile(r"^\s*\|?(\s*:?-{3,}:?\s*\|)+\s*:?-{3,}:?\s*\|?\s*$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
RELEASE_TAG_RE = re.compile(r"^Release\s+(\d{8}\.\d{3})")
GROUP_ICONS = {
    "Overview": "◉",
    "Frontend": "▣",
    "API": "⬡",
    "Tests": "✓",
    "Utilities": "⚙",
    "Diagrams": "◇",
    "Modules": "☰",
    "Reference": "⌁",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate HTML docs from Markdown files.")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing docs/site output before generating.",
    )
    args = parser.parse_args()

    sources = collect_sources()
    if not sources:
        raise SystemExit("No markdown sources found.")

    source_to_output = {source: map_output_path(source) for source in sources}
    titles = {source: extract_title(source) for source in sources}
    release_context = collect_release_context(sources)
    generator_link_path = Path("docs-toolkit.zip")
    if not (REPO_ROOT / generator_link_path).exists():
        generator_link_path = Path("docs-toolkit/README.md")
    if not (REPO_ROOT / generator_link_path).exists():
        generator_link_path = Path("utils/docs/build_docs_site.py")

    if args.clean and SITE_ROOT.exists():
        shutil.rmtree(SITE_ROOT)
    SITE_ROOT.mkdir(parents=True, exist_ok=True)

    for source in sources:
        output_rel = source_to_output[source]
        output_path = SITE_ROOT / output_rel
        output_path.parent.mkdir(parents=True, exist_ok=True)

        source_text = (REPO_ROOT / source).read_text(encoding="utf-8")
        if source.suffix.lower() == ".mmd":
            content_html = render_mermaid_source(source_text)
            toc_html = ""
        else:
            content_html = render_markdown(source_text, source, output_rel, source_to_output)
            toc_html = build_table_of_contents(source_text)
        navigation_html = build_navigation(source, output_rel, source_to_output, titles)
        top_nav_html = build_top_navigation(source, output_rel, source_to_output)
        source_href = rel_href(Path("docs/site") / output_rel.parent, source)
        home_href = rel_href(output_rel.parent, Path("index.html"))
        generator_href = rel_href(Path("docs/site") / output_rel.parent, generator_link_path)
        release_info = build_release_info(source, release_context)

        page_html = page_template(
            title=titles[source],
            source=source,
            source_href=source_href,
            home_href=home_href,
            generator_href=generator_href,
            top_nav_html=top_nav_html,
            nav_html=navigation_html,
            toc_html=toc_html,
            content_html=content_html,
            release_info=release_info,
        )
        output_path.write_text(page_html, encoding="utf-8")

    print(f"Generated {len(sources)} pages at {SITE_ROOT}")
    print(f"Open {SITE_ROOT / 'index.html'}")
    return 0


def collect_sources() -> List[Path]:
    discovered: Dict[Path, None] = {}
    for pattern in SOURCE_GLOBS:
        for path in REPO_ROOT.glob(pattern):
            if not path.is_file():
                continue
            rel = path.relative_to(REPO_ROOT)
            if rel.parts[:2] == ("docs", "site"):
                continue
            if rel.parts[:3] == ("docs", "utils", "templates"):
                continue
            discovered[rel] = None
    return sorted(discovered)


def map_output_path(source_rel: Path) -> Path:
    if source_rel == Path("docs/README.md"):
        return Path("index.html")

    if source_rel.suffix.lower() == ".mmd":
        if source_rel.parts and source_rel.parts[0] == "docs":
            return Path(*source_rel.parts[1:]).with_suffix(".html")
        return Path("reference") / source_rel.with_suffix(".html")

    if source_rel.parts and source_rel.parts[0] == "docs":
        relative = Path(*source_rel.parts[1:]).with_suffix(".html")
        if relative.name.lower() == "readme.html":
            return relative.with_name("index.html")
        return relative

    return Path("reference") / source_rel.with_suffix(".html")


def extract_title(source_rel: Path) -> str:
    text = (REPO_ROOT / source_rel).read_text(encoding="utf-8")
    if source_rel.suffix.lower() == ".mmd":
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("%%"):
                return stripped.strip("% ").strip() or source_rel.stem.replace("_", " ").replace("-", " ").title()
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return source_rel.stem.replace("_", " ").replace("-", " ").title()


def run_git(args: List[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def parse_git_record(raw: str) -> Optional[Dict[str, object]]:
    if not raw:
        return None
    parts = raw.split("\x1f")
    if len(parts) != 3:
        return None
    commit_hash, date_text, subject = parts
    try:
        at = datetime.fromisoformat(date_text.strip())
    except ValueError:
        return None
    return {
        "hash": commit_hash.strip(),
        "date": date_text.strip(),
        "subject": subject.strip(),
        "at": at,
    }


def collect_release_context(sources: List[Path]) -> Dict[str, object]:
    context: Dict[str, object] = {
        "releases": [],
        "last_release": None,
        "last_release_files": set(),
        "source_changes": {},
    }

    release_rows = run_git([
        "log",
        "--grep",
        "^Release",
        "--date=iso-strict",
        "--pretty=format:%H%x1f%ad%x1f%s",
    ])
    releases: List[Dict[str, object]] = []
    if release_rows:
        for row in release_rows.splitlines():
            record = parse_git_record(row)
            if not record:
                continue
            match = RELEASE_TAG_RE.match(str(record["subject"]))
            if not match:
                continue
            record["tag"] = match.group(1)
            releases.append(record)
    context["releases"] = releases
    context["last_release"] = releases[0] if releases else None

    last_release = context["last_release"]
    if last_release:
        changed = run_git([
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            str(last_release["hash"]),
        ])
        if changed:
            context["last_release_files"] = set(line.strip() for line in changed.splitlines() if line.strip())

    source_changes: Dict[Path, Dict[str, object]] = {}
    for source in sources:
        row = run_git([
            "log",
            "-1",
            "--date=iso-strict",
            "--pretty=format:%H%x1f%ad%x1f%s",
            "--",
            source.as_posix(),
        ])
        record = parse_git_record(row) if row else None
        if record:
            source_changes[source] = record
    context["source_changes"] = source_changes
    return context


def build_release_info(source: Path, context: Dict[str, object]) -> Dict[str, str]:
    fallback = {
        "label": "Release N/A",
        "tooltip": "Last release info unavailable.",
        "page_status": "Unknown",
    }
    last_release = context.get("last_release")
    if not isinstance(last_release, dict):
        return fallback

    releases = context.get("releases", [])
    if not isinstance(releases, list):
        releases = []
    source_changes = context.get("source_changes", {})
    if not isinstance(source_changes, dict):
        source_changes = {}
    last_release_files = context.get("last_release_files", set())
    if not isinstance(last_release_files, set):
        last_release_files = set()

    last_tag = str(last_release.get("tag", "N/A"))
    last_date = str(last_release.get("date", "N/A"))
    page_change = source_changes.get(source)
    page_change_date = "Unknown"
    stale_count = 0
    if isinstance(page_change, dict):
        page_change_date = str(page_change.get("date", "Unknown"))
        page_at = page_change.get("at")
        if isinstance(page_at, datetime):
            stale_count = sum(
                1
                for release in releases
                if isinstance(release, dict)
                and isinstance(release.get("at"), datetime)
                and release["at"] > page_at
            )

    changed_in_last_release = source.as_posix() in last_release_files
    if changed_in_last_release:
        page_status = "Updated in last release"
    elif stale_count > 0:
        page_status = f"Not updated for {stale_count} release(s)"
    else:
        page_status = "Changed after last release"
    tooltip_lines = [
        f"Last release: {last_tag}",
        f"Release timestamp: {last_date}",
        f"This page changed in last release: {'Yes' if changed_in_last_release else 'No'}",
        f"Page last change: {page_change_date}",
        f"Releases since page changed: {stale_count}",
    ]

    return {
        "label": f"Release {last_tag}",
        "tooltip": "\n".join(tooltip_lines),
        "page_status": page_status,
    }


def render_mermaid_source(diagram_text: str) -> str:
    body = diagram_text.strip()
    if not body:
        return "<p>No Mermaid diagram content found.</p>"

    return (
        "<p>Diagram authored as <code>.mmd</code> (source-first).</p>"
        f"<pre class=\"mermaid\">{body}</pre>"
        "<details><summary>View raw diagram source</summary>"
        f"<pre><code>{html.escape(body)}</code></pre>"
        "</details>"
    )


def build_table_of_contents(markdown_text: str) -> str:
    headings: List[Tuple[int, str, str]] = []
    for line in markdown_text.splitlines():
        match = HEADING_RE.match(line.strip())
        if not match:
            continue
        level = len(match.group(1))
        if level not in (2, 3):
            continue
        heading_text = match.group(2).strip()
        headings.append((level, heading_text, slugify(heading_text)))

    if not headings:
        return ""

    items = []
    for level, text, slug in headings:
        css_class = "toc-sub" if level == 3 else "toc-main"
        items.append(
            f"<a class=\"toc-link {css_class}\" href=\"#{html.escape(slug)}\">{html.escape(text)}</a>"
        )
    return "".join(items)


def render_markdown(
    markdown_text: str,
    source_rel: Path,
    output_rel: Path,
    source_to_output: Dict[Path, Path],
) -> str:
    lines = markdown_text.splitlines()
    html_parts: List[str] = []
    list_stack: Optional[str] = None

    def close_list() -> None:
        nonlocal list_stack
        if list_stack:
            html_parts.append(f"</{list_stack}>")
            list_stack = None

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            close_list()
            i += 1
            continue

        if stripped.startswith("```"):
            close_list()
            language = stripped[3:].strip().lower()
            code_lines: List[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1

            code_body = "\n".join(code_lines)
            if language == "mermaid":
                html_parts.append(f"<pre class=\"mermaid\">{code_body}</pre>")
            else:
                class_name = f" class=\"language-{html.escape(language)}\"" if language else ""
                html_parts.append(
                    f"<pre><code{class_name}>{html.escape(code_body)}</code></pre>"
                )
            continue

        heading_match = HEADING_RE.match(stripped)
        if heading_match:
            close_list()
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            slug = slugify(text)
            html_parts.append(f"<h{level} id=\"{slug}\">{render_inline(text, source_rel, output_rel, source_to_output)}</h{level}>")
            i += 1
            continue

        if looks_like_table_header(lines, i):
            close_list()
            table_html, next_index = render_table(lines, i, source_rel, output_rel, source_to_output)
            html_parts.append(table_html)
            i = next_index
            continue

        ul_match = UL_RE.match(line)
        if ul_match:
            if list_stack != "ul":
                close_list()
                list_stack = "ul"
                html_parts.append("<ul>")
            item_text = ul_match.group(1).strip()
            html_parts.append(
                f"<li>{render_inline(item_text, source_rel, output_rel, source_to_output)}</li>"
            )
            i += 1
            continue

        ol_match = OL_RE.match(line)
        if ol_match:
            if list_stack != "ol":
                close_list()
                list_stack = "ol"
                html_parts.append("<ol>")
            item_text = ol_match.group(1).strip()
            html_parts.append(
                f"<li>{render_inline(item_text, source_rel, output_rel, source_to_output)}</li>"
            )
            i += 1
            continue

        close_list()
        paragraph_lines = [stripped]
        i += 1
        while i < len(lines):
            candidate = lines[i].strip()
            if not candidate:
                break
            if candidate.startswith("```"):
                break
            if HEADING_RE.match(candidate):
                break
            if UL_RE.match(lines[i]) or OL_RE.match(lines[i]):
                break
            if looks_like_table_header(lines, i):
                break
            paragraph_lines.append(candidate)
            i += 1

        paragraph_text = " ".join(paragraph_lines)
        html_parts.append(
            f"<p>{render_inline(paragraph_text, source_rel, output_rel, source_to_output)}</p>"
        )

    close_list()
    return "\n".join(html_parts)


def looks_like_table_header(lines: List[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    return "|" in lines[index] and bool(TABLE_DIVIDER_RE.match(lines[index + 1].strip()))


def render_table(
    lines: List[str],
    start: int,
    source_rel: Path,
    output_rel: Path,
    source_to_output: Dict[Path, Path],
) -> Tuple[str, int]:
    header_cells = split_table_row(lines[start])
    i = start + 2
    data_rows: List[List[str]] = []
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or "|" not in stripped:
            break
        if TABLE_DIVIDER_RE.match(stripped):
            i += 1
            continue
        data_rows.append(split_table_row(line))
        i += 1

    head_html = "".join(
        f"<th>{render_inline(cell, source_rel, output_rel, source_to_output)}</th>" for cell in header_cells
    )
    row_html = []
    for row in data_rows:
        cells = "".join(
            f"<td>{render_inline(cell, source_rel, output_rel, source_to_output)}</td>" for cell in row
        )
        row_html.append(f"<tr>{cells}</tr>")

    table_html = "<table><thead><tr>" + head_html + "</tr></thead><tbody>" + "".join(row_html) + "</tbody></table>"
    return table_html, i


def split_table_row(line: str) -> List[str]:
    stripped = line.strip().strip("|")
    return [cell.strip() for cell in stripped.split("|")]


def render_inline(
    text: str,
    source_rel: Path,
    output_rel: Path,
    source_to_output: Dict[Path, Path],
) -> str:
    placeholders: Dict[str, str] = {}

    def stash(value: str) -> str:
        key = f"@@PLACEHOLDER_{len(placeholders)}@@"
        placeholders[key] = value
        return key

    def format_label(value: str) -> str:
        label_placeholders: Dict[str, str] = {}

        def label_stash(fragment: str) -> str:
            key = f"@@LABEL_{len(label_placeholders)}@@"
            label_placeholders[key] = fragment
            return key

        formatted = re.sub(
            r"`([^`]+)`",
            lambda m: label_stash(f"<code>{html.escape(m.group(1))}</code>"),
            value,
        )
        formatted = html.escape(formatted)
        formatted = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", formatted)
        formatted = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", formatted)
        for key, fragment in label_placeholders.items():
            formatted = formatted.replace(key, fragment)
        return formatted

    def link_replacer(match: re.Match[str]) -> str:
        label = format_label(match.group(1).strip())
        href = resolve_link(match.group(2).strip(), source_rel, output_rel, source_to_output)
        return stash(f"<a href=\"{html.escape(href, quote=True)}\">{label}</a>")

    def code_replacer(match: re.Match[str]) -> str:
        return stash(f"<code>{html.escape(match.group(1))}</code>")

    working = LINK_RE.sub(link_replacer, text)
    working = re.sub(r"`([^`]+)`", code_replacer, working)
    working = html.escape(working)
    working = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", working)
    working = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", working)

    for key, value in placeholders.items():
        working = working.replace(key, value)
    return working


def resolve_link(
    target: str,
    source_rel: Path,
    output_rel: Path,
    source_to_output: Dict[Path, Path],
) -> str:
    if not target:
        return target

    if target.startswith(("http://", "https://", "mailto:")):
        return target

    if target.startswith("#"):
        return target

    link_target = target
    anchor = ""
    if "#" in target:
        link_target, anchor_part = target.split("#", 1)
        anchor = f"#{slugify(anchor_part)}" if anchor_part else ""

    source_candidate = resolve_repo_path(link_target, source_rel)
    if source_candidate and source_candidate in source_to_output:
        destination = source_to_output[source_candidate]
        href = rel_href(output_rel.parent, destination)
        return f"{href}{anchor}"

    if source_candidate and source_candidate.suffix.lower() == ".md":
        guessed_destination = map_output_path(source_candidate)
        href = rel_href(output_rel.parent, guessed_destination)
        return f"{href}{anchor}"

    if source_candidate:
        href = rel_href(Path("docs/site") / output_rel.parent, source_candidate)
        return f"{href}{anchor}"

    return target


def resolve_repo_path(raw_target: str, source_rel: Path) -> Optional[Path]:
    if not raw_target:
        return source_rel

    candidate_path: Optional[Path] = None

    if raw_target.startswith(str(REPO_ROOT)):
        candidate_path = Path(raw_target)
    elif raw_target.startswith("/"):
        relative_candidate = raw_target.lstrip("/")
        local = REPO_ROOT / relative_candidate
        if local.exists():
            candidate_path = local
    else:
        candidate_path = (REPO_ROOT / source_rel.parent / raw_target).resolve()

    if not candidate_path:
        return None

    try:
        relative = candidate_path.resolve().relative_to(REPO_ROOT)
    except ValueError:
        return None

    return relative


def rel_href(from_dir: Path, to_file: Path) -> str:
    from_value = from_dir.as_posix() if from_dir.as_posix() else "."
    return posixpath.relpath(to_file.as_posix(), from_value)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "section"


def build_navigation(
    current_source: Path,
    current_output: Path,
    source_to_output: Dict[Path, Path],
    titles: Dict[Path, str],
) -> str:
    grouped: Dict[str, List[Tuple[Path, Path]]] = {
        "Overview": [],
        "Frontend": [],
        "API": [],
        "Tests": [],
        "Utilities": [],
        "Diagrams": [],
        "Modules": [],
        "Reference": [],
    }

    for source, output in sorted(source_to_output.items(), key=lambda item: item[1].as_posix()):
        group_name = nav_group(source)
        grouped.setdefault(group_name, [])
        grouped[group_name].append((source, output))

    current_group = nav_group(current_source)
    sections: List[str] = []
    for group_name, items in grouped.items():
        if not items:
            continue
        links: List[str] = []
        for source, output in items:
            href = rel_href(current_output.parent, output)
            active = " active" if source == current_source else ""
            label = html.escape(titles.get(source, source.stem))
            links.append(
                "<a class=\"nav-link"
                + active
                + f"\" href=\"{href}\">"
                + "<span class=\"nav-link-dot\">•</span>"
                + f"<span class=\"nav-link-text\">{label}</span>"
                + "</a>"
            )

        is_open = group_name == current_group or group_name == "Overview"
        open_class = " open" if is_open else ""
        icon = html.escape(GROUP_ICONS.get(group_name, "•"))
        expanded = "true" if is_open else "false"
        sections.append(
            "<section class=\"nav-group"
            + open_class
            + "\">"
            + f"<button class=\"nav-group-btn\" type=\"button\" aria-expanded=\"{expanded}\">"
            + f"<span class=\"nav-group-icon\">{icon}</span>"
            + f"<span class=\"nav-group-title\">{html.escape(group_name)}</span>"
            + "<span class=\"nav-group-caret\">▾</span>"
            + "</button>"
            + f"<div class=\"nav-group-items\">{''.join(links)}</div>"
            + "</section>"
        )

    return "\n".join(sections)


def build_top_navigation(
    current_source: Path,
    current_output: Path,
    source_to_output: Dict[Path, Path],
) -> str:
    grouped: Dict[str, List[Tuple[Path, Path]]] = {
        "Overview": [],
        "Frontend": [],
        "API": [],
        "Tests": [],
        "Utilities": [],
        "Diagrams": [],
        "Modules": [],
        "Reference": [],
    }
    for source, output in sorted(source_to_output.items(), key=lambda item: item[1].as_posix()):
        grouped.setdefault(nav_group(source), []).append((source, output))

    current_group = nav_group(current_source)
    chips: List[str] = []
    for group_name in ("Overview", "Frontend", "API", "Tests", "Utilities", "Diagrams", "Modules"):
        items = grouped.get(group_name) or []
        if not items:
            continue

        preferred = items[0]
        for source, output in items:
            if output.name == "index.html":
                preferred = (source, output)
                break

        target_source, target_output = preferred
        href = rel_href(current_output.parent, target_output)
        active = " top-link-active" if group_name == current_group else ""
        chips.append(f"<a class=\"top-link{active}\" href=\"{href}\">{html.escape(group_name)}</a>")

    reference_items = grouped.get("Reference") or []
    if reference_items:
        target_source, target_output = reference_items[0]
        href = rel_href(current_output.parent, target_output)
        active = " top-link-active" if current_group == "Reference" else ""
        chips.append(f"<a class=\"top-link{active}\" href=\"{href}\">Reference</a>")

    return "".join(chips)


def nav_group(source: Path) -> str:
    if source == Path("docs/README.md"):
        return "Overview"
    if source.parts[0] != "docs":
        return "Reference"
    if len(source.parts) < 2:
        return "Overview"

    section = source.parts[1]
    mapping = {
        "frontend": "Frontend",
        "api": "API",
        "tests": "Tests",
        "utils": "Utilities",
        "diagrams": "Diagrams",
        "modules": "Modules",
    }
    return mapping.get(section, "Overview")


def page_template(
    title: str,
    source: Path,
    source_href: str,
    home_href: str,
    generator_href: str,
    top_nav_html: str,
    nav_html: str,
    toc_html: str,
    content_html: str,
    release_info: Dict[str, str],
) -> str:
    now_utc = datetime.now(timezone.utc)
    generated_at = now_utc.strftime("%Y-%m-%d %H:%M UTC")
    source_label = html.escape(source.as_posix())
    source_href_escaped = html.escape(source_href, quote=True)
    home_href_escaped = html.escape(home_href, quote=True)
    generator_href_escaped = html.escape(generator_href, quote=True)
    page_title = html.escape(f"{title} | Rishika Docs")
    heading = html.escape(title)
    year = now_utc.year
    release_label = html.escape(release_info.get("label", "Release N/A"))
    release_tooltip = html.escape(release_info.get("tooltip", "Last release info unavailable."), quote=True)
    release_status = html.escape(release_info.get("page_status", "Unknown"))

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{page_title}</title>
  <style>
    :root {{
      --bg: #f2f6fc;
      --surface: #ffffff;
      --surface-2: #f8fbff;
      --ink: #162844;
      --muted: #5d6f8b;
      --border: #d4dfef;
      --link: #0b4fce;
      --code-bg: #eef4ff;
      --active: #e6efff;
      --accent: #0b3fa8;
      --topbar: #ffffffee;
      --topbar-border: #d6e3f5;
      --shadow: rgba(11, 43, 104, 0.08);
      --top-height: 64px;
    }}
    html[data-theme="dark"] {{
      --bg: #0f1420;
      --surface: #121b2a;
      --surface-2: #0f1827;
      --ink: #e7eefc;
      --muted: #95a6c4;
      --border: #243652;
      --link: #7ab6ff;
      --code-bg: #1a263c;
      --active: #1c2c48;
      --accent: #89bfff;
      --topbar: #10192af0;
      --topbar-border: #253958;
      --shadow: rgba(2, 10, 22, 0.45);
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; padding: 0; }}
    body {{
      font-family: "IBM Plex Sans", "Avenir Next", "Segoe UI", ui-sans-serif, system-ui, -apple-system, sans-serif;
      background: radial-gradient(circle at top right, #e8f2ff 0%, var(--bg) 50%);
      color: var(--ink);
    }}
    a {{ color: var(--link); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}

    .topbar {{
      position: sticky;
      top: 0;
      z-index: 50;
      height: var(--top-height);
      background: var(--topbar);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--topbar-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 14px;
    }}
    .top-left {{
      display: flex;
      align-items: center;
      gap: 14px;
      min-width: 0;
    }}
    .menu-btn {{
      display: none;
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--ink);
      border-radius: 10px;
      font-size: 13px;
      font-weight: 600;
      padding: 7px 10px;
      cursor: pointer;
    }}
    .brand {{
      color: var(--ink);
      font-weight: 800;
      letter-spacing: 0.01em;
      font-size: 15px;
      white-space: nowrap;
    }}
    .top-nav {{
      display: flex;
      align-items: center;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 1px;
    }}
    .top-link {{
      display: inline-flex;
      align-items: center;
      height: 30px;
      border-radius: 999px;
      padding: 0 10px;
      color: var(--muted);
      border: 1px solid transparent;
      font-size: 12px;
      font-weight: 600;
      white-space: nowrap;
    }}
    .top-link:hover {{
      color: var(--ink);
      text-decoration: none;
      background: var(--surface);
      border-color: var(--border);
    }}
    .top-link-active {{
      color: var(--accent);
      background: var(--active);
      border-color: var(--border);
    }}
    .top-right {{
      display: flex;
      align-items: center;
      gap: 8px;
      white-space: nowrap;
    }}
    .generated-stamp {{
      color: var(--muted);
      font-size: 12px;
      font-variant-numeric: tabular-nums;
      padding: 0 6px;
    }}
    .release-pill {{
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--ink);
      border-radius: 999px;
      font-size: 12px;
      padding: 6px 10px;
      box-shadow: 0 1px 4px var(--shadow);
      cursor: help;
    }}
    .theme-btn {{
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--ink);
      border-radius: 10px;
      font-size: 12px;
      font-weight: 600;
      padding: 7px 10px;
      cursor: pointer;
    }}
    .layout {{
      display: grid;
      grid-template-columns: 300px minmax(0, 1fr) 240px;
      min-height: calc(100vh - var(--top-height));
    }}
    .sidebar {{
      border-right: 1px solid var(--border);
      background: var(--surface-2);
      padding: 12px 10px 18px;
      position: sticky;
      top: var(--top-height);
      height: calc(100vh - var(--top-height));
      overflow: auto;
    }}
    .sub {{
      color: var(--muted);
      font-size: 12px;
      margin: 0 6px 10px;
    }}
    .nav-group {{
      border: 1px solid var(--border);
      border-radius: 10px;
      background: var(--surface);
      margin-bottom: 8px;
      overflow: hidden;
    }}
    .nav-group-btn {{
      width: 100%;
      border: 0;
      background: transparent;
      color: var(--ink);
      padding: 7px 9px;
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      text-align: left;
    }}
    .nav-group-btn:hover {{
      background: var(--active);
    }}
    .nav-group-icon {{
      width: 16px;
      text-align: center;
      color: var(--accent);
      font-size: 12px;
    }}
    .nav-group-title {{
      flex: 1;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      font-size: 11px;
    }}
    .nav-group-caret {{
      color: var(--muted);
      font-size: 12px;
      transition: transform 0.18s ease;
    }}
    .nav-group.open .nav-group-caret {{
      transform: rotate(0deg);
    }}
    .nav-group:not(.open) .nav-group-caret {{
      transform: rotate(-90deg);
    }}
    .nav-group-items {{
      display: none;
      padding: 0 6px 7px 6px;
      border-top: 1px solid var(--border);
      background: var(--surface-2);
    }}
    .nav-group.open .nav-group-items {{
      display: block;
    }}
    .nav-link {{
      display: flex;
      align-items: center;
      gap: 7px;
      padding: 5px 6px;
      border-radius: 7px;
      color: var(--ink);
      font-size: 12px;
      line-height: 1.3;
    }}
    .nav-link:hover {{
      text-decoration: none;
      background: var(--active);
    }}
    .nav-link-dot {{
      width: 12px;
      text-align: center;
      color: var(--muted);
      font-size: 10px;
      flex: none;
    }}
    .nav-link-text {{
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .nav-link.active {{
      background: var(--active);
      color: var(--accent);
      font-weight: 700;
    }}
    .nav-link.active .nav-link-dot {{
      color: var(--accent);
    }}
    .content-wrap {{ padding: 24px 28px 44px; }}
    .content {{
      max-width: 930px;
      margin: 0 auto;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 26px 30px;
      box-shadow: 0 10px 28px var(--shadow);
    }}
    .meta {{ color: var(--muted); font-size: 12px; margin-bottom: 18px; }}
    .meta-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 14px;
    }}
    .status-pill {{
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 4px 9px;
      background: var(--surface-2);
      color: var(--ink);
      font-size: 11px;
      font-weight: 600;
    }}
    .doc-footer {{
      margin-top: 28px;
      padding-top: 12px;
      border-top: 1px solid var(--border);
      color: var(--muted);
      font-size: 12px;
      text-align: right;
    }}
    .doc-footer a {{
      font-weight: 700;
    }}
    .eyebrow {{ font-size: 11px; letter-spacing: 0.04em; text-transform: uppercase; color: var(--accent); margin-bottom: 8px; font-weight: 700; }}
    h1, h2, h3, h4 {{ color: var(--ink); }}
    h1 {{ margin-top: 0; font-size: 34px; letter-spacing: -0.01em; }}
    h2 {{ margin-top: 28px; font-size: 22px; border-top: 1px solid var(--border); padding-top: 18px; }}
    h3 {{ margin-top: 22px; font-size: 18px; }}
    p, li {{ line-height: 1.62; color: var(--ink); }}
    ul, ol {{ padding-left: 24px; }}
    pre {{ background: #0f172a; color: #e2e8f0; border-radius: 10px; padding: 14px; overflow-x: auto; }}
    pre.mermaid {{ background: var(--surface); border: 1px solid var(--border); color: var(--ink); }}
    code {{ background: var(--code-bg); color: var(--ink); border-radius: 6px; padding: 2px 6px; font-size: 0.92em; }}
    pre code {{ background: transparent; color: inherit; padding: 0; }}
    details {{ margin-top: 14px; }}
    summary {{ cursor: pointer; color: var(--accent); }}
    table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }}
    th, td {{ border: 1px solid var(--border); text-align: left; padding: 9px 10px; vertical-align: top; }}
    th {{ background: var(--surface-2); font-weight: 600; }}
    .toc {{
      border-left: 1px solid var(--border);
      background: var(--surface-2);
      padding: 22px 12px;
      position: sticky;
      top: var(--top-height);
      height: calc(100vh - var(--top-height));
      overflow: auto;
    }}
    .toc h3 {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); margin: 0 0 10px; }}
    .toc-link {{ display: block; color: var(--ink); font-size: 13px; padding: 4px 6px; border-radius: 6px; }}
    .toc-link:hover {{ background: var(--active); text-decoration: none; }}
    .toc-main {{ font-weight: 600; }}
    .toc-sub {{ padding-left: 16px; color: var(--muted); }}
    .toc-empty {{ color: var(--muted); font-size: 12px; }}
    .backdrop {{
      display: none;
      position: fixed;
      inset: var(--top-height) 0 0 0;
      background: rgba(5, 12, 23, 0.42);
      z-index: 35;
    }}
    .backdrop.show {{ display: block; }}
    @media (max-width: 1200px) {{
      .layout {{ grid-template-columns: 280px minmax(0, 1fr); }}
      .toc {{ display: none; }}
    }}
    @media (max-width: 980px) {{
      .menu-btn {{ display: inline-flex; }}
      .top-nav {{ display: none; }}
      .generated-stamp {{ display: none; }}
      .layout {{ grid-template-columns: 1fr; }}
      .sidebar {{
        position: fixed;
        top: var(--top-height);
        left: 0;
        width: min(90vw, 320px);
        transform: translateX(-104%);
        transition: transform 0.22s ease;
        z-index: 40;
        border-right: 1px solid var(--border);
      }}
      .sidebar.open {{ transform: translateX(0); }}
      .content-wrap {{ padding: 12px; }}
      .content {{ padding: 18px; border-radius: 10px; }}
    }}
    @media (max-width: 640px) {{
      .release-pill {{ display: none; }}
      .theme-btn {{ padding: 7px 9px; }}
      .topbar {{ padding: 0 10px; }}
      .content h1 {{ font-size: 30px; }}
    }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
</head>
<body>
  <header class="topbar">
    <div class="top-left">
      <button class="menu-btn" id="menu-toggle" aria-label="Toggle navigation">Menu</button>
      <a class="brand" href="{home_href_escaped}">Rishika Docs</a>
      <nav class="top-nav" aria-label="Top navigation">{top_nav_html}</nav>
    </div>
    <div class="top-right">
      <span class="generated-stamp" title="Generation timestamp">{generated_at}</span>
      <span class="release-pill" title="{release_tooltip}">{release_label}</span>
      <button class="theme-btn" id="theme-toggle" aria-label="Toggle color theme">Dark</button>
    </div>
  </header>
  <div class="layout">
    <aside class="sidebar" id="left-nav" aria-label="Section navigation">
      <div class="sub">Generated from Markdown</div>
      {nav_html}
    </aside>
    <div class="backdrop" id="nav-backdrop"></div>
    <main class="content-wrap">
      <article class="content">
        <div class="eyebrow">Markdown-First Documentation</div>
        <h1>{heading}</h1>
        <div class="meta-row">
          <div class="meta">Source Markdown: <a href="{source_href_escaped}"><code>{source_label}</code></a> · Generated: {generated_at}</div>
          <span class="status-pill" title="{release_tooltip}">{release_status}</span>
        </div>
        {content_html}
        <footer class="doc-footer">(c) {year} <a href="{generator_href_escaped}" title="DocSmith documentation generator">DocSmith</a> documentation generator</footer>
      </article>
    </main>
    <aside class="toc">
      <h3>On This Page</h3>
      {toc_html or '<div class="toc-empty">No section headings on this page.</div>'}
    </aside>
  </div>
  <script>
    (function () {{
      var root = document.documentElement;
      var themeKey = "rishika-docs-theme";
      var menuToggle = document.getElementById("menu-toggle");
      var themeToggle = document.getElementById("theme-toggle");
      var sidebar = document.getElementById("left-nav");
      var backdrop = document.getElementById("nav-backdrop");
      var navGroups = document.querySelectorAll(".nav-group");
      var navGroupButtons = document.querySelectorAll(".nav-group-btn");
      var navLinks = document.querySelectorAll(".nav-link");

      function renderMermaid(theme) {{
        if (!window.mermaid) {{
          return;
        }}
        var nodes = document.querySelectorAll("pre.mermaid");
        for (var i = 0; i < nodes.length; i += 1) {{
          nodes[i].removeAttribute("data-processed");
        }}
        window.mermaid.initialize({{
          startOnLoad: false,
          theme: theme === "dark" ? "dark" : "neutral",
        }});
        window.mermaid.run({{ nodes: nodes }});
      }}

      function setTheme(theme) {{
        root.setAttribute("data-theme", theme);
        themeToggle.textContent = theme === "dark" ? "Light" : "Dark";
        try {{
          localStorage.setItem(themeKey, theme);
        }} catch (err) {{
          // Ignore write failures.
        }}
        renderMermaid(theme);
      }}

      function initTheme() {{
        var stored = null;
        try {{
          stored = localStorage.getItem(themeKey);
        }} catch (err) {{
          stored = null;
        }}
        var preferredDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
        var initial = stored || (preferredDark ? "dark" : "light");
        setTheme(initial);
      }}

      function closeSidebar() {{
        sidebar.classList.remove("open");
        backdrop.classList.remove("show");
      }}

      function setGroupOpen(group, open) {{
        if (!group) {{
          return;
        }}
        group.classList.toggle("open", open);
        var btn = group.querySelector(".nav-group-btn");
        if (btn) {{
          btn.setAttribute("aria-expanded", open ? "true" : "false");
        }}
      }}

      for (var gi = 0; gi < navGroupButtons.length; gi += 1) {{
        navGroupButtons[gi].addEventListener("click", function () {{
          var group = this.closest(".nav-group");
          var shouldOpen = !group.classList.contains("open");
          for (var j = 0; j < navGroups.length; j += 1) {{
            setGroupOpen(navGroups[j], false);
          }}
          setGroupOpen(group, shouldOpen);
        }});
      }}

      if (menuToggle) {{
        menuToggle.addEventListener("click", function () {{
          var open = sidebar.classList.toggle("open");
          backdrop.classList.toggle("show", open);
        }});
      }}
      if (backdrop) {{
        backdrop.addEventListener("click", closeSidebar);
      }}
      window.addEventListener("resize", function () {{
        if (window.innerWidth > 980) {{
          closeSidebar();
        }}
      }});

      for (var li = 0; li < navLinks.length; li += 1) {{
        navLinks[li].addEventListener("click", function () {{
          if (window.innerWidth <= 980) {{
            closeSidebar();
          }}
        }});
      }}

      themeToggle.addEventListener("click", function () {{
        var current = root.getAttribute("data-theme") === "dark" ? "dark" : "light";
        setTheme(current === "dark" ? "light" : "dark");
      }});

      initTheme();
    }})();
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    raise SystemExit(main())
