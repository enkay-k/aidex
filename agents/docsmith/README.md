# Documentation Toolkit (Copy/Paste Pack)

This folder contains the current documentation skill + generator scripts from this project, packaged so you can copy them into another repository.

## Documentation philosophy

1. Markdown (`.md`) is for AI and automation workflows (source of truth).
2. Generated HTML (`docs/site/`) is for humans (reading and navigation).
3. Diagrams are for both and should be authored in Mermaid source (`.mmd`) first.
4. Generated HTML links back to Markdown source.
5. Key Markdown pages should include a "Human HTML view" link.

## UI style included in this toolkit

- Top navigation + left navigation docs layout.
- Dark/light theme toggle.
- Responsive mobile/desktop behavior.
- Top-right live date/time display.
- Release metadata badge with hover details (last release and page freshness).

## What is included

- `skills/docs-md-publisher/`
  - `SKILL.md`
  - `agents/openai.yaml`
  - `references/module-doc-format.md`
  - `references/release-doc-checklist.md`
- `utils/docs/build_docs_site.py`
- `utils/docs/scaffold_module_doc.py`
- `docs/utils/templates/module_doc_template.md`
- `docs/utils/documentation_style_v1.md`
- `docs/diagrams/README.md`
- `docs/diagrams/docs_lifecycle.mmd`

## Target structure in another project

Copy these files into the target repo with this structure:

```text
<target-repo>/
  skills/docs-md-publisher/...
  utils/docs/build_docs_site.py
  utils/docs/scaffold_module_doc.py
  docs/utils/templates/module_doc_template.md
```

## Quick install (from this pack)

From inside this `docs-toolkit` folder:

```bash
# Example: replace with your target repo path
TARGET=/absolute/path/to/target-repo

mkdir -p "$TARGET/skills/docs-md-publisher"
mkdir -p "$TARGET/utils/docs"
mkdir -p "$TARGET/docs/utils/templates"
mkdir -p "$TARGET/docs/utils"
mkdir -p "$TARGET/docs/diagrams"

cp -R skills/docs-md-publisher/* "$TARGET/skills/docs-md-publisher/"
cp utils/docs/build_docs_site.py "$TARGET/utils/docs/"
cp utils/docs/scaffold_module_doc.py "$TARGET/utils/docs/"
cp docs/utils/templates/module_doc_template.md "$TARGET/docs/utils/templates/"
cp docs/utils/documentation_style_v1.md "$TARGET/docs/utils/"
cp docs/diagrams/README.md "$TARGET/docs/diagrams/"
cp docs/diagrams/docs_lifecycle.mmd "$TARGET/docs/diagrams/"
```

## How to use in target repo

1. Keep docs in Markdown first (for example under `docs/`).
2. Keep complex diagrams in `docs/diagrams/*.mmd` and update them first.
3. Generate HTML site:

```bash
python3 utils/docs/build_docs_site.py --clean
```

4. Scaffold module documentation for a code file:

```bash
python3 utils/docs/scaffold_module_doc.py --source src/path/to/file.py
```

5. Run the docs workflow skill in your Codex environment:
   - Skill name: `docs-md-publisher`
   - Prompt example: `Use $docs-md-publisher to update docs and rebuild docs/site.`

## Expected conventions

- `docs/site/` is generated output (do not hand-edit).
- `docs/modules/` contains per-file module docs.
- `docs/utils/templates/module_doc_template.md` is used by the scaffold script.
- `docs/**/*.mmd` files are treated as diagram source pages and published to HTML.

## Notes

- `build_docs_site.py` expects to run from within a repo and resolves paths relative to repo root.
- The generator scans:
  - `docs/**/*.md`
  - `docs/**/*.mmd`
  - `src/**/*.md`
  - `tests/**/*.md`
  - `requirements.md`
  - `Readme.md`
