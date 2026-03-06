---
name: smriti-gh-review-sync
description: Update GitHub ENG issues and project status to Ready for review after validated task completion certificates, including acceptance evidence comments and architect traceability fields.
---

# Smriti GH Review Sync

Use this skill after each ENG task completion certificate is generated.

## Inputs
- `task_id` (example: `ENG-012`)
- `issue_number` (GitHub issue number)
- `status` (`completed|blocked|partial`)
- `certificate_path` (JSON certificate file)
- Optional:
  - `project_id` (GitHub Project V2 id)
  - `status_field_id` (Project field id for status)
  - `ready_option_id` (Option id for "Ready for review")

## Behavior
1. Validate certificate exists and parse key fields.
2. If `status != completed`, add comment only and do **not** set Ready for review.
3. For `completed`:
- Ensure acceptance checks are all `pass` or `na`.
- Post issue comment with:
  - task id, traceability (`BR_ID`, `ERS_ID`, `Epic_Ref`, `Screen`)
  - commands + exit codes
  - key evidence snippets
- Add label `status:ready-for-review`.
- Optionally set project field `Status` to Ready for review when project metadata env vars are provided.
4. Print final sync summary for logs.

## Commands
```bash
python .aidex/agents/smriti/skill/smriti-gh-review-sync/scripts/gh_issue_sync.py \
  --task ENG-012 \
  --issue 12 \
  --status completed \
  --certificate docs/certificates/ENG-012.json
```

## Guardrails
- Never mark review-ready when acceptance checks include failures.
- Never overwrite blocked/partial status with ready label.
- Include architect note if present (`architect_clarification_note`).
- Keep issue comments deterministic and concise for fast reviewer scan.
