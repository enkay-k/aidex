# Documentation Style v1

Human HTML view: [`../site/utils/documentation_style_v1.html`](../site/utils/documentation_style_v1.html)

This is the writing and publishing contract for Rishika docs.

## Core Rules

1. Markdown (`.md`) is the canonical source and is updated first.
2. Generated HTML (`docs/site/`) is for human reading and navigation.
3. Diagrams are mandatory for architecture and flow pages.
4. Standalone diagrams are authored in Mermaid source files (`.mmd`) first.
5. HTML must link back to source Markdown.
6. Markdown should include a "Human HTML view" link near the top.
7. Links must be relative and portable.

## HTML Experience Rules

1. Use both top navigation and left navigation in generated HTML.
2. Support dark mode and light mode in generated HTML.
3. Pages must remain responsive for desktop and mobile widths.
4. Show current date/time in the top-right area.
5. Show release metadata in top-right with hover details:
   - Last release tag/date.
   - Whether this page changed in the last release.
   - How many releases have passed since this page changed.

## Writing Guidance

- Prefer short sections with clear headings.
- Keep one main idea per section.
- Use tables only for structured comparison.
- Keep command examples executable.
- Keep wording product/system focused, not only implementation detail.

## Diagram Policy

- Diagram source location: [`../diagrams/`](../diagrams/)
- For complex flows, create/update `.mmd` file first.
- Mirror the same flow in Markdown where helpful for AI context.
- Rebuild HTML after diagram updates.

## Publishing Flow

1. Update Markdown and `.mmd` source.
2. Update related module docs.
3. Generate HTML with `python3 utils/docs/build_docs_site.py --clean`.
4. Verify links in Markdown and HTML.

## Definition of Done

- Markdown reflects latest behavior.
- HTML regenerated from current Markdown.
- Diagram sources and rendered diagrams match.
- Module docs updated for changed files.
