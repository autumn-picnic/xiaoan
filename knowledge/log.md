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
- Added `legal-mechanism-tree` as the root node for Obsidian visualization.
- Clarified that `knowledge/source/` is user-maintained and read-only for the LLM.
- Clarified that scenario capsules are future product-layer work and should not be created or edited in this phase.

## [2026-06-07] schema | legal atoms as nodes, mechanisms as edges

- Rebased `copilot/llm-persistent-knowledge-wiki` onto latest `main`.
- Reworked `knowledge/AGENTS.md` so legal atoms are represented as graph nodes and legal mechanisms are represented as sourced edges.
- Moved initial legal atom pages into `knowledge/wiki/nodes/`.
- Added `edges` as the mechanism edge catalog.
- Removed separate legal mechanism pages that implied a misleading Legal Atom -> Legal Mechanism layer split.

## [2026-06-07] schema-v0.1 | node/edge/source-type taxonomy

- Added Schema v0.1 to `knowledge/AGENTS.md`: node kinds, edge relations, `source_type` trust tiers, ingest granularity, and out-of-scope rules.
- Aligned `knowledge/wiki/edges.md` edge vocabulary with the schema.
- Added `source-registry` cataloging all `knowledge/source/` files with `source_type`, tier, and ingest status, plus a pilot ingest batch.
- Status conventions: new legal claims default to `draft`; cross-source/interpretive claims default to `needs-review`; legal-reviewer-confirmed claims become `reviewed`.

## [2026-06-07] pilot-ingest | 4 sources, schema v0.1 frozen

- Froze schema v0.1 and ran pilot ingest on 4 sources.
- ingest | 人身安全保护令实务 (practice_guide): added `protection-order-evidence` node; enriched `personal-safety-protection-order` with judicial-interpretation refinements (needs-review); enriched `support-and-legal-aid` (legal aid not limited by hardship, needs-review).
- ingest | 公安机关办理伤害案件规定 (agency_rule): added `injury-appraisal-procedure` node (appraisal commission/timelines, mediation limits).
- ingest | 预防和制止家庭暴力警察工作手册 (official_manual): added `police-dv-handling-workflow` node (5-stage workflow, risk assessment); flagged conflicts_with current law (predates 2016, no 告诫书) -> needs-review.
- ingest | 广东省实施反家暴法办法 (local_regulation): added `guangdong-implementation` local-rule node with 3 `localizes` edges.
- Schema gaps found: (1) no relation for judicial-interpretation refining national law (used provides_evidence_for + needs-review; consider adding `interprets`/`refines`); (2) existing protection-order node bundles remedy+procedure+condition+consequence, may need splitting; (3) secondary sources citing primary judicial interpretations should consistently be needs-review with "原文待补".
- Next: legal reviewer to check needs-review nodes/edges; then ingest remaining sources per `source-registry`.

## [2026-06-07] graph-cleanup | make Obsidian graph match node/edge structure

- Root cause: Obsidian renders one node per file and one edge per `wikilink`; `edges.md` and `source-registry.md` were becoming star hubs because they linked to every node/source.
- Converted all `wikilinks` in `edges.md` (34) and `source-registry.md` (37) to plain inline code.
- Changed node pages' "详见 `edges`" (8) to plain `edges.md`.
- Verified all 17 edges are mirrored as node-to-node `wikilinks` in node pages, so no graph edges were lost.
- Added an Obsidian graph convention to `knowledge/AGENTS.md`: node-to-node wikilinks are the graph edge source of truth; catalogs use plain text; use Graph filter `path:nodes` for a pure node view.
