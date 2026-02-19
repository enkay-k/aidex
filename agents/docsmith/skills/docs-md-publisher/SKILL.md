---
name: docs-md-publisher
description: Maintain Rishika documentation with Markdown as the source of truth and generated HTML output. Use when creating or updating docs/README.md, section indexes, per-file module docs in docs/modules, and when publishing docs/site from Markdown after code or requirement changes.
---

# Docs MD Publisher

Keep docs authoritative in Markdown and publish readable HTML consistently.

## Run this workflow

1. Update Mermaid diagram sources (`docs/**/*.mmd`) first when flows change.
2. Update user-facing Markdown docs in `docs/`.
3. Update module docs for each changed code file in `docs/modules/`.
4. Regenerate HTML from Markdown and Mermaid sources.
5. Verify links, diagrams, and command examples.

## Required outputs per task

- `docs/README.md` reflects current architecture and links.
- Relevant section indexes are updated (`docs/frontend`, `docs/api`, `docs/tests`, `docs/utils`).
- Every touched code file has a module doc in `docs/modules`.
- `docs/site/` is regenerated from Markdown.
- Generated HTML pages link back to their Markdown source.
- Key Markdown entry pages include a "Human HTML view" link.

## Commands

```bash
# Generate HTML docs site
python3 utils/docs/build_docs_site.py --clean

# Equivalent shell entrypoint
./rishika.sh docs-build

# Scaffold a new module doc
python3 utils/docs/scaffold_module_doc.py --source <repo-relative-file>
```

## Module doc format

Use the exact section order in `references/module-doc-format.md`.

## Quality checks

Use `references/release-doc-checklist.md` before finalizing.
