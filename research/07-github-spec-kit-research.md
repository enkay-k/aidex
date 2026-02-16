# GitHub Spec Kit Research
## Spec-Driven Development — Specs as Executable Artifacts

**Date:** 2026-02-15
**Purpose:** Understand GitHub's Spec Kit to inform AIDE X methodology
**Source Video:** VS Code "Let it Cook" Episode 13 — Den Delimarsky (GitHub DevRel)

---

## What Is Spec Kit?

Spec Kit is an open-source toolkit from **GitHub** enabling **Spec-Driven Development (SDD)** — a methodology where detailed specifications directly generate working code implementations, rather than just serving as documentation.

**Core Insight:** "Specifications become executable, directly generating working implementations rather than just guiding them."

**Key Quote:** Specs become "unit tests for English" — validation mechanisms ensuring requirements are complete and internally consistent before implementation begins.

---

## The Workflow (6 Steps)

```
Step 1: INSTALL
  └── uv tool install specify-cli

Step 2: ESTABLISH PRINCIPLES (/speckit.constitution)
  └── Project governance, non-negotiable development guidelines
  └── Like a constitution for your codebase

Step 3: DEFINE REQUIREMENTS (/speckit.specify)
  └── Describe WHAT to build (user needs, not implementation)
  └── Focus on intent, not how

Step 4: PLAN IMPLEMENTATION (/speckit.plan)
  └── Specify tech stack, architecture, constraints
  └── Technical design document

Step 5: BREAK INTO TASKS (/speckit.tasks)
  └── Generate actionable implementation work items
  └── User stories with acceptance criteria

Step 6: EXECUTE (/speckit.implement)
  └── AI agents build features per the complete spec
```

---

## Key Concepts

### 1. Constitution
A `constitution.md` file establishing non-negotiable project principles. Ensures consistency across all generated code and design decisions. Think: guardrails that no agent can violate.

### 2. Multi-Step Refinement
Not single-prompt code generation. Progressive specification development with optional validation steps:
- `/speckit.clarify` — resolve ambiguities
- `/speckit.analyze` — analyze for completeness
- `/speckit.checklist` — validate against criteria

### 3. Artifact-Driven Development
Development revolves around interconnected documents:
```
Constitution → Specifications → Plans → Task Lists → Implementation
     ↑                                                      │
     └────────── Each artifact informs the next ────────────┘
```

### 4. Tool Independence
Specs remain constant while AI tools evolve. You can switch between AI assistants while maintaining quality standards. Works with 16+ agents: Claude Code, GitHub Copilot, Cursor, Gemini/Jules, Windsurf, Amazon Q, etc.

---

## Development Phases Supported

| Phase | Description |
|-------|-------------|
| **0-to-1 (Greenfield)** | Generate complete applications from specifications |
| **Creative Exploration** | Generate parallel implementations with different tech stacks |
| **Iterative Enhancement (Brownfield)** | Add features to existing systems incrementally |

---

## File Structure

```
project/
├── .speckit/                  # Specification artifacts
│   ├── constitution.md        # Project principles & guardrails
│   ├── specifications/        # What to build
│   ├── plans/                 # How to build it
│   └── tasks/                 # Work items
├── features/                  # Feature-based organization
├── src/                       # Generated source code
└── ...
```

---

## Why This Matters (From the Video)

### The Problem: "Vibe Coding"
- Ad-hoc AI code generation without planning
- Unpredictable results
- No repeatability
- Can't switch AI tools without starting over

### The Solution: Spec-Driven Development
- Specs remain your source of truth
- Quality of AI output correlates directly with spec detail/clarity
- Repeatable, verifiable workflow
- Enterprise-ready structure
- AI tools are interchangeable — specs are permanent

### Key Shift
```
TRADITIONAL:
  Requirements → Design → Manual Coding → Testing

SPEC-DRIVEN:
  Requirements → Detailed Specification → AI Generation → Validation
```

---

## Industry Validation

- **Thoughtworks** identified SDD as one of 2025's key new AI-assisted engineering practices
- **Martin Fowler** wrote analysis: "Understanding Spec-Driven Development: Kiro, spec-kit, and Tessl"
- **GitHub** made it official with open-source release
- **VS Code team** integrates it into their development process
- Works across Claude Code, Copilot, Cursor, and 13+ other AI agents

---

## Relevance to AIDE X

### What AIDE X MUST Adopt from Spec Kit

1. **Constitution Pattern:** Every AIDE X project should have a `constitution.md` — non-negotiable principles, allowed libraries, security requirements, performance budgets. Agents CANNOT violate the constitution.

2. **Spec → Plan → Tasks → Implement Pipeline:** This IS the core of what AIDE X should orchestrate. The agents in AIDE X map directly:
   - Apollo (PM) + Oracle (BA) → `/speckit.specify` (requirements)
   - Daedalus (Architect) → `/speckit.plan` (architecture/design)
   - Foreman (Coordinator) → `/speckit.tasks` (work breakdown)
   - Hephaestus (Engineer) → `/speckit.implement` (execution)

3. **Multi-Step Refinement:** Don't jump to code. Clarify → Analyze → Checklist → Then build. AIDE X's human decision gates align perfectly with this.

4. **Tool Independence:** Design AIDE X specs in a format that ANY AI agent can consume. Don't lock into one provider.

5. **"Unit Tests for English":** Specs should be validatable. Before implementation, verify specs are complete, consistent, and unambiguous.

### How Spec Kit Validates AIDE X's Direction

| Spec Kit Concept | AIDE X Equivalent | Status |
|------------------|-------------------|--------|
| Constitution | Project guardrails | Not yet implemented |
| Specify (requirements) | Apollo + Oracle agents | Defined, not built |
| Plan (architecture) | Daedalus agent | Defined, not built |
| Tasks (work breakdown) | Foreman orchestration | Defined, not built |
| Implement (code) | Hephaestus agent | Defined, not built |
| Clarify/Analyze/Checklist | Human decision gates | Conceptualized |

### Where AIDE X Goes Beyond Spec Kit

1. Spec Kit stops at code generation — AIDE X continues through testing, security, DevOps, VaPT, performance, docs, and deployment
2. Spec Kit is developer-centric — AIDE X targets non-developers too
3. Spec Kit has no dashboard/UI — AIDE X has Niyantran
4. Spec Kit has no cost estimation — AIDE X has Plutus
5. Spec Kit doesn't auto-generate diagrams — AIDE X should (with C4 model)

---

## Updated Force Multiplier Formula

```
AIDE X = Spec Kit's Spec-Driven Foundation
       × BMAD's Agent Persona Depth
       × GSD's Fresh-Context Execution
       × C4's Visual Communication
       × VS Code's Multi-Agent Orchestration
       × Human Decision Gates (AIDE X original)

= Industrial-Strength AI-Driven Engineering
```

---

## Sources

- [GitHub Spec Kit Repository](https://github.com/github/spec-kit)
- [VS Code "Let it Cook" Episode 13](https://www.youtube.com/watch?v=TXcL-te7ByY)
- [Diving Into Spec-Driven Development With GitHub Spec Kit - Microsoft](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)
- [What's The Deal With GitHub Spec Kit — Den Delimarsky](https://den.dev/blog/github-spec-kit/)
- [Spec-Driven Development — Thoughtworks](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [Understanding SDD: Kiro, spec-kit, and Tessl — Martin Fowler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
