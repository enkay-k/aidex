# AIDE - AI Driven Engineering Operating System

## Vision

**Can AI build industrial-strength solutions almost autonomously?**

AIDE is an agentic operating system where multiple AI agents work like a human engineering team — each agent has a role, produces observable output, and passes work to the next agent. Humans watch, guide, and approve — AI does the heavy lifting.

**Key Insight:** The problem must be larger than any single context window (100x+). This isn't about code completion — it's about *systematic engineering* by agents.

---

## Full Pipeline: Startup to Deployment

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AIDE FULL PIPELINE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  USER PAIN ──► PROBLEM STATEMENT ──► BUSINESS REQS ──► FEATURES            │
│       │             │                    │                 │                │
│       ▼             ▼                    ▼                 ▼                │
│  ┌─────────┐  ┌──────────┐       ┌───────────┐     ┌──────────┐           │
│  │ Analyst │  │Analyst   │       │Product    │     │Product   │           │
│  │Discovery│  │Problem   │       │Requirements│     │Feature   │           │
│  └────┬────┘  └────┬─────┘       └─────┬─────┘     └────┬─────┘           │
│       │            │                    │                │                 │
│       │        HUMAN DECISION:          │            HUMAN DECISION:       │
│       │        "Is this a real pain?"  │            "Prioritize these?"    │
│       │                                                           │          │
│       ▼                                                           ▼          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    DETAILED ENGINEERING                             │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                       │   │
│  │  ARCHITECTURE ──► UI/UX DESIGN ──► CODE ──► TEST CASES              │   │
│  │       │               │            │            │                    │   │
│  │       ▼               ▼            ▼            ▼                    │   │
│  │  ┌─────────┐    ┌──────────┐ ┌────────┐   ┌────────┐               │   │
│  │  │Blueprint│    │   Muse   │ │ Forge  │   │ Prover │               │   │
│  │  │   Arch  │    │UI/UX Design│ │ Code   │   │ Tests  │               │   │
│  │  └────┬────┘    └────┬─────┘ └───┬────┘   └───┬────┘               │   │
│  │       │              │           │            │                     │   │
│  │       │          HUMAN DECISION │        HUMAN DECISION             │   │
│  │       │          "Love the UI?" │        "Tests pass?"              │   │
│  │       │                          │                                   │   │
│  │       ▼                          ▼                                   │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │                    DEPLOYMENT                                 │  │   │
│  │  ├────────────────────────────────────────────────────────────────┤  │   │
│  │  │                                                                 │  │   │
│  │  │   CI/CD ──► STAGING ──► PRODUCTION ──► MONITORING            │  │   │
│  │  │                          │                   │                 │  │   │
│  │  │                    HUMAN DECISION:                            │  │   │
│  │  │                    "Ready to ship?"                          │  │   │
│  │  │                                                                 │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  │                                                                       │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│              HUMAN DECISION GATES AT EVERY MAJOR STAGE                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Stage-by-Stage Breakdown

| Stage | Agent | AI Does | Human Does |
|-------|-------|---------|------------|
| **1. Discovery** | Analyst | Interviews user, captures pain points | Validate pain is real |
| **2. Problem Statement** | Analyst | Frame problem, market context | Approve problem framing |
| **3. Business Requirements** | Product | ROI, scope, constraints | Approve business case |
| **4. Features** | Product | Feature list, prioritization | Prioritize & approve |
| **5. Architecture** | Blueprint | System design, tech choices | Approve architecture |
| **6. UI/UX Design** | Muse | Wireframes, mockups, flows | Approve design |
| **7. Code** | Forge | Implementation | Review code |
| **8. Tests** | Prover | Test cases, validation | Approve test results |
| **9. Documentation** | DocSmith | Docs, READMEs | Review docs |
| **10. Deployment** | Foreman | CI/CD, infra config | Final go/no-go |
| **11. Monitoring** | Foreman | Alerts, dashboards | Act on alerts |

---

## Agent Roles

| Role | Codename | What They Do |
|------|----------|--------------|
| Coordinator | **Foreman** | Orchestrates pipeline, manages state |
| Architect | **Blueprint** | System design, tech stack |
| Engineer | **Forge** | Code generation |
| Reviewer | **Critic** | Code review, security |
| Tester | **Prover** | Test generation, validation |
| Docs | **DocSmith** | Documentation |
| Product Manager | **Product** | Scope, prioritization, ROI |
| UI/UX Designer | **Muse** | Design, user flows, mocks |
| Business Analyst | **Analyst** | Requirements, feasibility |

---

## Human Decision Gates

| Gate # | Question | Options |
|--------|----------|---------|
| G1 | Is this pain real & worth solving? | Approve / Reject / More Research |
| G2 | Business case valid? | Approve / Modify Scope |
| G3 | Features prioritized correctly? | Approve / Reorder |
| G4 | Architecture sound? | Approve / Redesign |
| G5 | UI/UX acceptable? | Approve / Redesign |
| G6 | Code ready? | Approve / Request Changes |
| G7 | Tests passing? | Approve / Fix / Skip |
| G8 | Ready to deploy? | Deploy / Hold |

---

## Key Realizations

### What AI Can Do Well:
- Generate code from specs
- Write test cases
- Create documentation
- Propose architectures
- Design UI mocks (via tools)
- Run CI/CD pipelines

### What Humans Must Decide:
- Is this problem worth solving?
- What's the business priority?
- Does the design feel right?
- Is this ready for production?
- Any ethical/legal concerns?

### The 100x Context Problem:
- Large startup = 100x context window
- AIDE chunks problems into manageable pieces
- Each chunk flows through the pipeline
- Results synthesized at end

---

## Reference Models

1. **Mission Control HQ** — Dashboard for multi-agent orchestration
2. **OpenClaw** — The underlying agent runtime
3. **AIDE v2** — Previous attempts

---

## Architecture

### Stack
- **Runtime:** OpenClaw
- **Dashboard:** Niyantran (Python FastAPI + HTML/JS)
- **Storage:** SQLite + file artifacts

### Pipeline Engine
- Configurable stages
- Parallel where possible
- Sequential where required
- Rollback on failure

---

## Phases

### Phase 0: Foundation
- Repo structure
- Agent definitions
- Simple pipeline (Code → Test → Deploy)

### Phase 1: Basic Pipeline
- Analyst → Blueprint → Forge → Prover → DocSmith
- Manual human gates
- Basic dashboard

### Phase 2: Full Pipeline
- Add Product, Muse
- All human decision gates
- Rich dashboard

### Phase 3: Scale
- Context chunking
- Concurrent pipelines
- Advanced artifacts

### Phase 4: Production
- Full automation
- Self-healing
- Analytics

---

## Ambitious Goal

**Yes, this can go from user pain to deployment.** But:
- Humans are always in the loop for big decisions
- Each stage produces observable artifacts
- Pipeline can pause at any gate for human input
- AI does the work, humans steer

---

## Open Questions

1. How granular should decision gates be?
2. What's the minimum viable first pipeline?
3. How to handle conflicting agent outputs?
4. What about legal/compliance review?
5. Parallel staging or sequential?

---

*Draft PRD v0.3 — Full Startup-to-Deployment Pipeline*
*Created: 2026-02-14*
