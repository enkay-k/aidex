Ribhu's E2E Master Playbook: PRD to Industrial WBS

This document defines the sequential workflow Ribhu follows to translate a raw PRD and UX design into an industrial-strength Work Breakdown Structure (WBS) using the Aidex Protocol.

By dynamically loading these skills, Ribhu avoids context pollution and maintains production-grade engineering rigor.

STAGE 1: Intake & Problem Shaping

Goal: Deconstruct the human ideas (Docs, UX) into strict technical boundaries.

prd-decomposer: Breaks vague goals into 10+ granular technical requirements. Highlights race conditions and edge cases.

ux-ui-state-mapper: Maps visual flow into a Component Hierarchy and defines frontend Data State.

tech-stack-assessor: Uses MCP to check live docs and select safe LTS versions.

STAGE 2: Architectural Blueprinting

Goal: Design the system securely, efficiently, and visually.
4. system-design-architect: Designs microservices, message queues, databases, and OpenTelemetry hooks.
5. finops-cloud-optimizer: Strips out cloud waste; implements semantic routing.
6. mcp-integration-specialist: Defines secure external tool interactions (GitHub, Core Banking APIs).
7. 3d-architecture-visualizer: Outputs the finalized architecture as a multi-dimensional spatial JSON/Mermaid payload.

STAGE 3: Agentic Logic & Orchestration

Goal: Decide what gets coded by humans vs. what gets automated by AI.
8. agentic-workflow-orchestrator: Routes features to Deterministic APIs or Agentic loops. Sets up data contracts between agents.

STAGE 4: The Factory Floor (WBS Generation)

Goal: Create the actionable execution plan.
9. ai-native-clean-code: Sets coding standards (Pydantic, deterministic testing).
10. aidex-wbs-generator: Compiles all context into the final SDLC Execution Plan ([ENG], [REV], [TEST], [BUG]).

The Output

Once Stage 4 completes, Ribhu writes the ADR_LOG.md, updates MEMORY.md, and delivers the final WBS.