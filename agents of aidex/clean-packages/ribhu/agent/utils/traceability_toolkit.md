# Ribhu Traceability Toolkit (Reusable)

This toolkit standardizes how we connect PRD-level business requirements to engineering execution in GitHub.

## Model

- `BR` = Business Requirement from PRD
- `ERS` = Engineering Feature that satisfies one or more BRs
- `ENG` = Implementable engineering task

Relationship:

- `BR -> ERS -> ENG`

## Why this helps

- Keeps product intent visible during implementation
- Makes status reporting accurate (`which BR is blocked?`)
- Reduces orchestration overhead for future coding agents

## Required issue conventions

- IDs in title:
  - `BR-###: ...`
  - `ERS-###: ...`
  - `ENG-###: ...`
- Labels:
  - `br`, `ers`, `eng-task`
  - `br:BR-xx` and `ers:ERS-xx` on ENG issues
- Issue body fields:
  - `BR_ID`, `ERS_ID`, `Epic_Ref`, `Screen`, `Depends_On`, `Acceptance`

## Import tools

### 1) Import BR/ERS requirements

```bash
python3 .aidex/ribhu/utils/create_github_issues_from_csv.py \
  --csv .aidex/ribhu/requirements_br_ers_seed.csv \
  --execute
```

### 2) Import ENG task backlog

```bash
python3 .aidex/ribhu/utils/create_github_issues_from_csv.py \
  --csv .aidex/ribhu/github_task_backlog.csv \
  --execute
```

## Audit checklist

- Every `ENG-*` has exactly one `ERS_ID`
- Every `ERS-*` maps to at least one `BR_ID`
- No issue missing `Acceptance`
- No issue missing `Status` in GitHub Project

## Suggested GitHub Project fields

- `BR_ID`, `ERS_ID`, `Epic`, `Screen`
- `Estimate_points`, `Push_Cadence`
- `Risk`, `Depends_On`, `DoR`, `DoD`, `Status`

## Notes for future users

- Script is resilient to transient GitHub 5xx errors (retries built in)
- Script skips duplicate titles by default
- If labels fail due API instability, it retries issue creation without labels
- Never paste PAT tokens into chat or docs
