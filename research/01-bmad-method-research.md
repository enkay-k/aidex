# BMAD Method Research
## Breakthrough Method for Agile AI-Driven Development

**Date:** 2026-02-15
**Purpose:** Understand BMAD to inform AIDE X evolution

---

## What Is BMAD?

BMAD stands for **Breakthrough Method for Agile AI-Driven Development**. It's an open-source framework (8k+ stars) that transforms chaotic "vibe coding" with AI into a structured, predictable software development process.

**Core Insight:** The real problem isn't AI capability — it's the lack of structure around AI. Without process, AI drifts, context degrades, and outputs become unpredictable.

---

## Core Philosophy

1. **Spec-Driven Development (SDD):** Specifications become first-class executable artifacts. You write the spec first, then AI generates code respecting that contract.
2. **Human-in-the-Loop Governance:** AI proposes, humans decide. Control manifests set guardrails (allowed libraries, performance budgets, code exclusion zones).
3. **Agentic Planning + Context-Engineered Development:** Two-phase process where agents plan comprehensively first, then development stories carry complete context.

---

## Agent Roles (21 Agents)

| Agent | Responsibility |
|-------|---------------|
| **Analyst** | Explores idea space, surfaces constraints, produces project brief |
| **Product Owner** | Aligns documents, runs Master Checklist, ensures PRD/Architecture/UX are synced |
| **Product Manager** | Turns brief into comprehensive PRD with FRs and NFRs |
| **Architect** | Full stack view, component maps, data flows, integration strategies |
| **Scrum Master** | Drafts hyper-detailed stories embedding full context and architectural guidance |
| **Developer** | Implements stories with tests on a branch, guided by control manifest |
| **QA/Test Architect** | Testing frameworks, test strategy, validates against requirements |
| **Orchestrator** | Coordinates agent interactions, manages dependencies, prevents bottlenecks |

Plus 13 additional supporting agents for specific domains.

---

## Workflow Pipeline

```
Phase 1: AGENTIC PLANNING
  Analyst → Project Brief
  PM → PRD (FRs + NFRs)
  Architect → System Architecture
  [Human Review Gates at Each Step]

Phase 2: CONTEXT-ENGINEERED DEVELOPMENT
  Scrum Master → Hyper-Detailed Stories (complete context per story)
  Developer → Implementation (per story, per branch)
  QA → Validation against original requirements
  [Human Review at PR Level]

Phase 3: DELIVERY
  Merge → Deploy → Monitor
```

---

## Key Technical Details

### Agents as Code
- Agent definitions are **Markdown persona files** (structured system prompts)
- Each defines: role, expertise, personality, style, commands, dependencies
- Templates are **interactive workflows** with structure, processing logic, and validation rules

### YAML-Based Workflows
- Workflows are YAML blueprints orchestrating task sequences
- Define specific steps, dependencies, and handoff points between agents

### "Party Mode"
- All agents operate in one session with orchestrator picking relevant agent per message
- Agents respond in character, agree, disagree, build on ideas — simulates live team meeting

### Token Efficiency
- V6 achieves **74-90% reduction** in token consumption
- Comprehensive artifacts created once, reused throughout development
- Fresh context per task prevents degradation

---

## Key Metrics Claimed

| Metric | Traditional | BMAD |
|--------|------------|------|
| Speed | Months | 10x faster |
| Token Usage | High (repeated context) | 74-90% reduction |
| Quality | Post-hoc fixes | Integrated validation |
| Governance | Limited audit | Continuous compliance ledger |

---

## Resources

- **GitHub:** github.com/bmad-code-org/BMAD-METHOD
- **Docs:** docs.bmad-method.org
- **Website:** bmadcodes.com
- **npm:** `npx bmad-method install`
- **Guide:** bmadmethodguide.com

---

## Relevance to AIDE X

### What AIDE X Can Learn from BMAD

1. **Spec-Driven Development:** AIDE X should make specs/PRDs executable artifacts, not just documents
2. **Context Engineering:** Stories/tasks should carry ALL context needed — no assumptions
3. **Control Manifests:** Each project should have guardrails that agents cannot violate
4. **Agent Persona Files:** Define agents as structured Markdown — portable, versionable, shareable
5. **Master Checklist Pattern:** Ensure all artifacts (PRD, Architecture, UX) stay aligned
6. **Token Efficiency:** Design for fresh contexts per task, not one long degrading session
7. **Party Mode Concept:** Allow agents to "discuss" solutions before implementing
8. **YAML Workflows:** Standardize pipeline definitions as code

### Where AIDE X Differs/Can Improve

1. AIDE X has broader scope (17 agents vs BMAD's 21, but AIDE X includes DevOps, VaPT, Performance, Marketing, Cost)
2. AIDE X targets enterprise-scale systems specifically (payments, DeFi, agentic engines)
3. AIDE X needs to implement BMAD-level execution rigor (currently at vision/whitepaper stage)
4. AIDE X can combine BMAD's planning depth with GSD's execution efficiency
