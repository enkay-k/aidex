# Visual Communication & Diagrams Research
## Making Architecture Understandable Fast

**Date:** 2026-02-15
**Purpose:** Learn best practices for diagrams in AIDE X to explain things visually

---

## The C4 Model (Simon Brown)

The most practical, widely-adopted approach to software architecture diagrams.

### Four Zoom Levels

```
Level 1: SYSTEM CONTEXT (highest level)
  "How does our system fit in the world?"
  Shows: System + External people/systems it interacts with
  Audience: Everyone (non-technical stakeholders)

Level 2: CONTAINERS (applications & data stores)
  "What are the major building blocks?"
  Shows: Web apps, APIs, databases, message queues, file systems
  Audience: Technical stakeholders, architects

Level 3: COMPONENTS (internal structure)
  "What's inside each container?"
  Shows: Classes, modules, services within a container
  Audience: Developers, architects

Level 4: CODE (class-level detail)
  "How is this component implemented?"
  Shows: UML class diagrams, entity relationship diagrams
  Audience: Developers (optional — code itself often suffices)
```

### Why C4 Works

1. **Different zoom levels for different audiences** — executives see Level 1, developers see Level 3
2. **Notation-independent** — works with any drawing tool
3. **Lean and practical** — not academic UML heavy
4. **Hierarchical drill-down** — each level zooms into a part of the previous level

---

## Key Principles for AIDE X Diagrams

### 1. Every Project Should Auto-Generate Diagrams
- System Context diagram (always)
- Container diagram (always)
- Component diagram (per module)
- Data flow diagrams (for complex flows)

### 2. Diagrams as Code
- Use tools like Mermaid, PlantUML, Structurizr DSL
- Diagrams live in the repo alongside code
- Version controlled, diff-able, auto-generated

### 3. Architecture Decision Records (ADRs)
- Document WHY decisions were made, not just WHAT
- Include diagrams showing alternatives considered

### 4. Pipeline Visualization
- Show the agent pipeline as a visual flow
- Show data/artifact flow between agents
- Show human decision gates clearly

---

## Recommended Tools

| Tool | Best For | Integration |
|------|----------|-------------|
| **Mermaid** | Quick diagrams in Markdown | GitHub native rendering |
| **PlantUML** | Detailed UML diagrams | CI/CD integration |
| **Structurizr** | C4 model specifically | DSL + workspace |
| **D2** | Modern diagram language | Beautiful defaults |
| **draw.io/diagrams.net** | Manual, collaborative | Web/desktop |

---

## Relevance to AIDE X

### What AIDE X Should Implement

1. **Auto-Generated Architecture Diagrams:** Daedalus (Architect agent) should output C4-style diagrams alongside architecture decisions
2. **Mermaid as Default:** Use Mermaid for all diagrams — renders in GitHub, Markdown, and most tools
3. **Pipeline Visualization:** Every project should have a visual pipeline showing agent flow and decision gates
4. **Live Dashboard Diagrams:** The Niyantran dashboard should render real-time pipeline diagrams
5. **Diagram Per Decision Gate:** When human approval is needed, present a visual summary alongside text

### Proposed AIDE X Diagram Standards

Every AIDE X project should include:

```
/diagrams/
  ├── system-context.mermaid    # Level 1: System in the world
  ├── containers.mermaid         # Level 2: Major building blocks
  ├── components/                # Level 3: Per-container internals
  │   ├── api.mermaid
  │   ├── frontend.mermaid
  │   └── database.mermaid
  ├── data-flow.mermaid          # How data moves through system
  ├── pipeline.mermaid           # AIDE X agent pipeline for this project
  └── decisions/                 # Architecture Decision Records
      ├── 001-database-choice.md
      └── 002-auth-strategy.md
```
