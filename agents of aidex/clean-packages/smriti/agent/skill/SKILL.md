---
name: smriti-chronicler
description: Keep project documentation aligned to code reality and generate release notes from git changes using Smriti chronology (`.smriti/history/chronicle.json`) and `utils/smriti_engine.py`.
---

# Smriti Chronicler

Use this skill when the user asks to:
- reconcile docs vs code
- create/update release notes
- produce a timestamped change chronicle
- keep requirements/readme/status artifacts in sync with implementation

## Workflow

1. Initialize Smriti if missing.
2. Inspect changed files and current API/runtime behavior.
3. Update docs to reflect actual behavior, not intended behavior.
4. Generate release note markdown from git scope.
5. Append a chronicle entry.
6. Flag unresolved gaps in `data/todo.json` with tags: `open`, `doubtful-change`, and priority.

## Commands

```bash
python3 utils/smriti_engine.py init
python3 utils/smriti_engine.py stamp
python3 utils/smriti_engine.py release-notes --staged --title "Rishika API centralization"
python3 utils/smriti_engine.py promote --env prod
```

## Guardrails

- Treat code as source of truth over stale docs.
- Avoid deleting existing docs unless explicitly requested.
- Keep release notes deterministic: list scope, diff summary, changed files.
- Chronicle entries must include `stamp`, `timestamp`, `env`, `author`, and `release_note`.
