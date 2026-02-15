# AIDE X - AI Driven Engineering X
## PRD v0.4 - Phase 1 (Code Only)

---

## Vision

**Can AI build industrial-strength solutions almost autonomously?**

AIDE X is an agentic operating system where multiple AI agents work like a human engineering team — each agent has a role, produces observable output, and passes work to the next. Humans watch, guide, and approve — AI does the heavy lifting.

**X = Force Multiplier**

---

## Phase 1 Scope: Code Only

**What we build first:**
- Agent pipeline starts at **code generation**
- Input: Feature spec / requirements
- Output: Working code + tests + docs

**What we skip for now:**
- Infrastructure (Docker, Terraform, K8s)
- UI/UX design (Muse)
- Deployment automation
- Product/Analyst (user provides requirements)

**Future (Phase 2+):** Full pipeline including infra, design, deployment

---

## Phase 1 Agent Team (Greek Mythology Names)

| Role | Codename | Description | Phase 1 |
|------|----------|-------------|---------|
| Coordinator | **Hermes** | Orchestrates pipeline | ✅ |
| Architect | **Daedalus** | System design | ✅ |
| Engineer | **Hephaestus** | Code generation | ✅ |
| Reviewer | **Athena** | Code review, security | ✅ |
| Tester | **Cassandra** | Test generation | ✅ |
| Docs | **Calliope** | Documentation | ✅ |
| Product | Apollo | Scope, prioritization | ❌ (Phase 2) |
| UI/UX | Aphrodite | Design | ❌ (Phase 2) |
| Analyst | Oracle | Requirements | ❌ (User provides) |

---

## Phase 1 Pipeline

```
Feature Spec (Human Input)
         │
         ▼
    ┌─────────┐
    │ Hermes  │ ← Coordinator
    └────┬────┘
         │ orchestr
         ▼
    ┌──────────┐
    │ Daedalus │ ← Architect
    └────┬─────┘
         │ design
         ▼
    ┌────────────┐
    │ Hephaestus │ ← Engineer (MAIN AGENT)
    └─────┬──────┘
          │ code
          ▼
    ┌──────────┐
    │  Athena  │ ← Reviewer
    └────┬─────┘
         │ review
         ▼
    ┌──────────┐
    │ Cassandra │ ← Tester
    └────┬─────┘
         │ tests
         ▼
    ┌──────────┐
    │ Calliope  │ ← Docs
    └────┬─────┘
         │ docs
         ▼
    Code + Tests + Docs (Output)
    
    Human Decision Gates at: Design, Code Review, Tests
```

---

## Human Decision Gates (Phase 1)

| Gate | Question | Options |
|------|----------|---------|
| G1 | Architecture sound? | Approve / Redesign |
| G2 | Code ready? | Approve / Request Changes |
| G3 | Tests pass? | Approve / Fix / Skip |

---

## Problem Decomposition

**Key insight:** Break large problems into small, predictable chunks.

Each agent:
- Works on one small thing at a time
- Has clear inputs and outputs
- Can be monitored and validated
- Predictable behavior

**Example:**
```
Large: "Build an e-commerce platform"
    │
    ▼
Chunk 1: User authentication
Chunk 2: Product catalog  
Chunk 3: Shopping cart
Chunk 4: Checkout flow
...
```

Each chunk flows through the pipeline independently.

---

## Context Chunking (The 100x Problem)

For problems 100x larger than context window:

1. **Decompose** → Break into sub-tasks
2. **Solve** → Each sub-task through pipeline
3. **Synthesize** → Combine results

---

## Technical Architecture

### Stack
- **Runtime:** OpenClaw
- **Dashboard:** Niyantran (Python FastAPI + HTML/JS)
- **Storage:** SQLite + file artifacts
- **CI/CD:** GitHub Actions

### File Structure (Phase 1)
```
aidex/
├── src/
│   ├── agents/
│   │   ├── hermes.py      # Coordinator
│   │   ├── daedalus.py    # Architect
│   │   ├── hephaestus.py  # Engineer
│   │   ├── athena.py      # Reviewer
│   │   ├── cassandra.py   # Tester
│   │   └── calliope.py    # Docs
│   ├── pipeline/          # Execution engine
│   ├── dashboard/         # Niyantran UI
│   ├── storage/          # SQLite + artifacts
│   └── utils/
├── tests/
├── docs/
│   ├── PRD.md
│   ├── whitepaper.md
│   ├── naming.md
│   ├── github-actions-analysis.md
│   └── website/
├── scripts/
│   ├── setup.sh
│   └── run.sh
└── README.md
---

## Open Questions

1. Is Greek mythology naming good?
2. Is Phase 1 scope right (code only)?
3. How granular should chunks be?
4. How many parallel pipelines?
5. 

Deployment approach (local first or cloud)?

---

## Next Steps

1. Confirm naming (Greek mythology)
2. Lock Phase 1 scope
3. Start building prototype

---

*PRD v0.4 — Phase 1 Code Only + Greek Names*
*Created: 2026-02-14*
