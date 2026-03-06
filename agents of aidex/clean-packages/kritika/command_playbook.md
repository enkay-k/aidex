# Aidex Agent Command Playbook

Use this as the canonical prompt map for each agent.

## Ribhu (Tech Architect)

- Ask me: "Ribhu, design architecture and WBS for [problem]."
- Command examples:
  - `ribhu plan all`
  - `ribhu design module [name]`
  - `ribhu wbs task [epic]`

## Kritika (Lead Creative Architect)

- Ask me: "Kritika, turn this brief/prototype into layered specs."
- Command examples:
  - `kritika spec all`
  - `kritika journeys stage [stage-name]`
  - `kritika stories epic [epic-name]`

## Smriti (Chronicler)

- Ask me: "Smriti, reconcile docs and produce release trace for this change."
- Command examples:
  - `smriti reconcile all`
  - `smriti release-notes scope [scope]`
  - `smriti chronicle task [task-id]`

## Shilpi (Builder)

- Ask me: "Shilpi, implement this scoped change and certify it."
- Command examples:
  - `shilpi build task [eng-id]`
  - `shilpi test scope [scope]`
  - `shilpi certify task [eng-id]`

## Docsmith (Documentation)

- Ask me: "Docsmith, update current-state docs for this implementation."
- Command examples:
  - `docsmith docs update [scope]`
  - `docsmith adr update [adr-id]`
  - `docsmith publish docs`

## Parikshak (Testing & QA)

- Ask me: "Parikshak, I can do QA and functional testing for you. Do you have code for me to eat? :-)"
- Command examples:
  - `parikshak go test code all`
  - `parikshak go test code module [module-name]`
  - `parikshak go test code file [path]`
  - `parikshak go test code function [symbol]`
- What happens by default:
  1. Runs baseline tests.
  2. Generates additional tagged tests with `PARIKSHAK_CASE`.
  3. Generates verification-focused test data (edge/negative/boundary/stress) for stronger coverage.
  4. Runs generated tests separately.
  5. Opens/updates GitHub issues for bugs and suggestions.
  6. Produces English-readable report + Smriti/Docsmith handoff.
- Antigravity frontend runbook + GitHub issue template mapping:
  - `.aidex/agents/parikshak/antigravity_quickstart.md`

## Test Data Ownership (Cross-Agent)

- Ribhu: test strategy architecture and quality gates.
- Shilpi: implementation-aligned fixtures/baseline data.
- Parikshak: verification-focused test data generation and deep case expansion.
- Smriti/Docsmith: evidence and documentation, not data generation.
