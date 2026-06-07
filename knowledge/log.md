# Knowledge Log

Append-only chronological record of ingests, durable query pages, lint passes, and major wiki maintenance.

## [2026-06-06] ingest | 中华人民共和国反家庭暴力法

- Added initial LLM-wiki schema in `AGENTS.md`.
- Created `knowledge/index.md` as the content catalog.
- Created source summary, legal atoms, legal mechanisms, and one draft scenario capsule derived from `knowledge/source/中华人民共和国反家庭暴力法.md`.
- Open gaps: police implementation details, local rules, social work practice sources, and expert review.

## [2026-06-06] scope-correction | 法律机制树中间层

- Corrected current scope to the legal middle layer only.
- Removed LLM-created source-summary and scenario-capsule pages.
- Added [[legal-mechanism-tree]] as the root node for Obsidian visualization.
- Clarified that `knowledge/source/` is user-maintained and read-only for the LLM.
- Clarified that scenario capsules are future product-layer work and should not be created or edited in this phase.

## [2026-06-07] schema | legal atoms as nodes, mechanisms as edges

- Rebased `copilot/llm-persistent-knowledge-wiki` onto latest `main`.
- Reworked `knowledge/AGENTS.md` so legal atoms are represented as graph nodes and legal mechanisms are represented as sourced edges.
- Moved initial legal atom pages into `knowledge/wiki/nodes/`.
- Added [[edges]] as the mechanism edge catalog.
- Removed separate legal mechanism pages that implied a misleading Legal Atom -> Legal Mechanism layer split.
