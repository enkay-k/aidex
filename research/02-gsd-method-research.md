# GSD Method Research
## Get Shit Done — Meta-Prompting System for AI Development

**Date:** 2026-02-15
**Purpose:** Understand GSD to inform AIDE X execution model

---

## What Is GSD?

GSD (Get Shit Done) is a meta-prompting, context engineering, and spec-driven development system for AI-driven software development. Created by Lex Christopherson, it has 8.5k+ GitHub stars and is the #1 Claude Code framework.

**Core Insight:** Claude is brilliant, but without structure it drifts. Context rots. Sessions become "ping-pong hell." The answer: fresh contexts for each task, not one long degrading session.

---

## The Core Problem: Context Rot

Context rot = progressive degradation of AI accuracy as tokens accumulate.

- After thousands of lines, AI forgets initial specs
- Generates inconsistent code, loses track of logic
- Tokens at front of context window more effective than those at end
- **Solution:** Spawn fresh Claude instances per task, each with clean 200k context window loaded with precisely needed info

---

## Core Workflow Pattern

```
IDEA → ROADMAP → PHASE PLAN → ATOMIC EXECUTION

Detailed:
1. Dream Extraction (/gsd:new-project)
   - Ask questions to extract requirements, goals, constraints

2. Roadmap Creation
   - Divide into phases based on requirements

3. Phase Planning
   - Each phase → structured plans

4. Sub-Plan Creation
   - Each plan → 2-3 ATOMIC tasks
   - Each task fits ~50% of fresh context window

5. Parallel Wave Execution
   - Independent tasks run in parallel
   - Dependent tasks wait for previous wave

6. Fresh Context Execution
   - Each task runs in own fresh 200k token subagent

7. Atomic Commits
   - Each task = one atomic, traceable git commit

8. Verification Loop
   - Discuss → Research/Plan → Execute → Human Verify
```

---

## Key Architecture: The Lean Orchestrator Pattern

```
ORCHESTRATOR (thin, 30-40% context)
    │
    ├── Spawns → PLANNING AGENT (fresh context)
    │              └── Gap analysis, prioritized TODOs
    │
    ├── Spawns → BUILDING AGENT 1 (fresh context)
    │              └── Implement, test, commit
    │
    ├── Spawns → BUILDING AGENT 2 (fresh context)
    │              └── Implement, test, commit
    │
    └── Collects results, routes to next step

KEY: Orchestrator NEVER does heavy lifting
     Each subagent gets clean 200k tokens
     Task 50 runs with same clarity as Task 1
```

---

## Key Principles

### 1. Aggressive Atomicity
- 2-3 tasks per plan maximum
- Each plan fits ~50% of fresh context window
- No single task big enough to degrade quality

### 2. Git-Centric Workflow
- Each task = separate atomic commit
- Git bisect finds exact failing task
- Easy rollback without losing other work
- Commits are "surgical, traceable, meaningful"

### 3. Requirements Traceability
```
Requirements → Phases → Plans → Commits
Everything connected. Everything verifiable.
```

### 4. Goal-Backward Verification
- Ask "what must be TRUE for this to work?"
- NOT "what tasks did we do?"

### 5. State Management
- `.planning/` directory tracks: project vision, requirements, roadmap, execution state, historical decisions

---

## Real-World Results

- Engineers at Amazon, Google, Shopify, Webflow use GSD
- Solo developer: **100,000 lines of code in 2 weeks**
- 23-plan development projects completed successfully
- Claims of **100x faster shipping**

---

## Resources

- **GitHub:** github.com/glittercowboy/get-shit-done (8.5k+ stars)
- **Website:** gsd.build
- **Tutorial:** ccforeveryone.com/gsd (free, 45-60 min)
- **Install:** `npx get-shit-done-cc --claude --global`

---

## Relevance to AIDE X

### What AIDE X Can Learn from GSD

1. **Fresh Context Per Task:** Design agent execution to use fresh contexts, not accumulate token debt
2. **Aggressive Atomicity:** Break work into tiny, atomic tasks that fit in context windows
3. **Lean Orchestrator:** Foreman (coordinator) should be thin — spawn agents, collect results, never do heavy work
4. **Parallel Wave Execution:** Independent tasks run in parallel, dependent tasks wait
5. **Git-Centric Everything:** Every agent output = atomic commit. Full traceability
6. **State Directory Pattern:** `.planning/` directory concept for tracking project state
7. **Goal-Backward Verification:** Verify by checking "what must be true" not "what did we do"
8. **Anti-Context-Rot Design:** The fundamental architecture must prevent degradation over time

### Where AIDE X Differs/Can Improve

1. GSD is primarily for Claude Code — AIDE X aims to be platform-agnostic
2. GSD focuses on execution — AIDE X covers full lifecycle (vision to marketing)
3. AIDE X has richer agent taxonomy (17 vs GSD's 3-4 agent types)
4. AIDE X needs GSD's execution rigor combined with its broader scope
5. AIDE X can add human decision gates that GSD doesn't emphasize as strongly
