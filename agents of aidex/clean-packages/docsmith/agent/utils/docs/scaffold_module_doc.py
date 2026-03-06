#!/usr/bin/env python3
"""Create a module doc markdown file from the project template."""

from __future__ import annotations

import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = REPO_ROOT / "docs/utils/templates/module_doc_template.md"
MODULE_DOCS_DIR = REPO_ROOT / "docs/modules"


def slug_from_source(source_rel: Path) -> str:
    value = source_rel.as_posix().replace("/", "-").replace(".", "_")
    return f"{value}.md"


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a docs/modules markdown file for a source file.")
    parser.add_argument("--source", required=True, help="Repo-relative source file path, for example src/api/main.py")
    parser.add_argument("--force", action="store_true", help="Overwrite existing module doc if present")
    args = parser.parse_args()

    source_rel = Path(args.source)
    source_abs = REPO_ROOT / source_rel
    if not source_abs.exists():
        raise SystemExit(f"Source file not found: {source_rel}")

    if not TEMPLATE_PATH.exists():
        raise SystemExit(f"Template not found: {TEMPLATE_PATH}")

    output_path = MODULE_DOCS_DIR / slug_from_source(source_rel)
    if output_path.exists() and not args.force:
        raise SystemExit(f"Module doc already exists: {output_path}. Use --force to overwrite.")

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    module_doc_html = slug_from_source(source_rel).replace(".md", ".html")
    output = template.replace("<repo-relative-path>", source_rel.as_posix())
    output = output.replace("<module>", source_rel.stem)
    output = output.replace("<module-doc-html>", module_doc_html)

    MODULE_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    print(f"Created {output_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
