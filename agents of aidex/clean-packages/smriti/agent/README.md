# Smriti Agent Bundle

## ⚠️ Migration Notice

Canonical runtime workspace path migrated to:

- `.aidex/workspaces/smriti/`

Legacy workspace path is removed.

Copied from `<source-project>` on 2026-03-03 for reuse in sample-project.

## Included

- `agent_contract.v0.02.yaml` (active wrapper contract)
- `skill/SKILL.md`
- `skill/agents/openai.yaml`
- `skill/scripts/smriti_engine.py` (wrapper)
- `utils/smriti_engine.py` (engine)
- `config/smriti.config.template.json`
- `.aidex/workspaces/smriti/AGENTS.md`
- `.aidex/workspaces/smriti/SOUL.md`
- `.aidex/workspaces/smriti/session_starter.md`

## Not included

- Runtime history (`.smriti/history/chronicle.json`) was intentionally not copied.

## Next integration options

- Use as reference-only bundle under `.aidex`.
- Or wire into sample-project by placing engine in `utils/smriti_engine.py` and initializing `.smriti/` in repo root.

## Contract First

Load order for active operation:

1. `agent_contract.v0.02.yaml`
2. `.aidex/workspaces/smriti/AGENTS.md`
3. `.aidex/workspaces/smriti/SOUL.md`
4. `skill/SKILL.md`

## Agent Awareness & Polite Handoff

Smriti is aware of sibling agent responsibilities:

- Ribhu: architecture and planning.
- Kritika: product/design specification.
- Shilpi: implementation and validation execution.
- Parikshak: testing and QA defect discovery.
- Docsmith: structured documentation authoring and publishing.

If the user request is outside Smriti's role, Smriti should politely redirect:

- "This is best handled by [agent]. I can document and trace the result once done, or you can ask [agent]: '[recommended prompt]'."
