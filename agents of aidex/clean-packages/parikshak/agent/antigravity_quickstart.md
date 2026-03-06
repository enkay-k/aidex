# Parikshak Antigravity Quickstart

This quickstart intentionally excludes model presets.

## Scope

- Frontend/browser testing runbook in Antigravity.
- GitHub issue template mapping for bugs and suggestions.
- Test data ownership clarity across Aidex agents.

## Frontend Testing Runbook (Antigravity)

1. Confirm scope:
   - `all` | `module` | `file` | `function`
2. Run baseline tests first (existing suites only).
3. Run browser exploration in Antigravity browser subagent:
   - happy path
   - one negative path
   - one edge path
4. Generate additional tests under `tests/` or `test/` only.
5. Store generated datasets under `tests/testdata/parikshak/` following the convention guide.
6. Tag every generated test with `PARIKSHAK_CASE`.
7. Re-run generated tests separately from baseline tests.
8. Produce report in two sections:
   - Baseline/Shilpi tests
   - Parikshak-generated tests
9. For each failure or significant QA finding, open/update GitHub issue.
10. Handoff evidence summary to Smriti and generated-test documentation notes to Docsmith.

## GitHub Issue Template Mapping

### Bug Issue Template

- Title: `[BUG][PARIKSHAK][scope] concise failure summary`
- Labels (recommended): `bug`, `testing`, `parikshak`
- Body fields:
  - Context
  - Reproduction command
  - Expected behavior
  - Actual behavior
  - Impact/Risk
  - Evidence (logs/screenshots/test output)
  - Related test IDs (include `PARIKSHAK_CASE` names when applicable)

### Suggestion Issue Template

- Title: `[SUGGESTION][PARIKSHAK][quality] concise improvement summary`
- Labels (recommended): `enhancement`, `quality`, `parikshak`
- Body fields:
  - Observation
  - Why it matters
  - Suggested change
  - Safety/compatibility note
  - Evidence and affected files/tests

## Test Data Ownership (Who Does What)

- Ribhu owns test strategy architecture:
  - test layers, risk priorities, acceptance strategy.
- Shilpi owns implementation-aligned fixtures/data setup needed for feature delivery.
- Parikshak owns verification data generation for testing depth:
  - edge cases,
  - negative cases,
  - boundary values,
  - fuzz-like or stress-oriented sample sets,
  - all tagged and traceable.
- Smriti does not generate test data; Smriti documents outcomes and traceability.
- Docsmith does not generate test data; Docsmith documents generated test assets and rationale.

## Boundary Rules

- Parikshak must not modify `src/` during testing missions.
- Parikshak may create/update only testing assets in `tests/` or `test/`.
- Issue system for this workflow is GitHub Issues only.

## Reusability Guide

- `tests/testdata/parikshak/README.md`
