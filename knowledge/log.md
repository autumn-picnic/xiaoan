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

## [2026-06-07] schema-v0.2 | consolidate edge types 10 -> 6

- Audited declared vs used edge relations. Used: provides_evidence_for(6), enables, localizes, defines_scope_for, parallel_support_channel_for, conflicts_with. Unused: triggers, requires, creates_consequence_for, plus stray `limits`.
- Deleted `triggers` (folded into `defines_scope_for`), `requires` (inverse direction), `creates_consequence_for` + `limits` (unused; consequence stays inside node until a consequence node is split out).
- Merged `assists_execution_of` -> `enables` (relabeled 1 edge + 2 node pages).
- Final vocabulary = 6 relations; all 17 edges remap cleanly (provides_evidence_for 6, enables 3, localizes 3, defines_scope_for 2, parallel_support_channel_for 2, conflicts_with 1).
- Updated `knowledge/AGENTS.md` (Edge relations table + label list) and `knowledge/wiki/edges.md` vocabulary.
- Recommendation recorded: if only one edge type can be visualized, use `provides_evidence_for` (connects 6/8 nodes, converges on protection-order; evidence is the highest-leverage DV problem).

## [2026-06-07] schema-v0.3 + synthesis | element layer (请求权基础分析)

- Studied the real 六段式要件清单 from CSlawyer1985/china-lawyer-analyst (请求权基础分析法: 总体情况概述/立案审查/原告诉请/被告抗辩/要件事实/知识图谱).
- Added `element` node_kind and two requirement-layer relations `is_element_of` (element->claim) and `proves` (evidence->element) to knowledge/AGENTS.md (schema v0.3). Documented the lawyer chain: 来源 --provides_evidence_for--> 证据 --proves--> 要件 --is_element_of--> 请求权.
- Created node `protection-order-element-danger` (要件3: 遭受家暴或面临现实危险, needs-review).
- Created synthesis `syntheses/protection-order-six-part-checklist.md`: mimics the six-part framework applied to the protection order, fully source-grounded, with needs-review flags and a reviewer checklist.
- Rewired the protection-order subgraph to route evidence through the element (no longer evidence->remedy directly): evidence proves element; element is_element_of remedy; definition defines_scope_for element. Removed the subsumed duty->remedy evidence shortcut. Edge count stays 17; nodes 8->9.
- Caught a possible citation error to surface for review: practice guide cites "《反家暴法》第八条" for the "对方有过错不影响核发" defense, but 第八条 is about township prevention work — likely a misattributed 审理指南 clause. Flagged in the checklist's review list.

## [2026-06-08] full-ingest | all 32 sources (waves 1-3)

- Rebased onto latest origin/main (source renames: 中国…司法解释, 河北简体). Updated source-registry accordingly.
- Wave 1 (judicial, tier 1): ingested 中国反家庭暴力法律法规与司法解释 (contains 法释〔2022〕17号 + 公通字〔2024〕34号 primary text) and 涉及家庭暴力婚姻案件审理指南.
  - Resolved prior needs-review flags: "较大可能性" standard (法释17号第六条), 11类证据 (第六条), 远离/电话骚扰令 (第十条), 代为申请 (第二条).
  - Resolved the "第八条" citation question: practice guide's "第八条" = 法释〔2022〕17号第八条 (认可家暴但辩称对方有过错不影响作出), not a misattribution; 审理指南第八条 separately states DV is not victim's fault.
  - Added node `warning-letter` (告诫书) from 公通字〔2024〕34号.
- Wave 2 (agency/manual/medical): added node `dv-risk-assessment` (妇联危险预测量表 + police manual, cross-source); enriched `support-and-legal-aid` (妇联 intake procedure) and `injury-appraisal-procedure` (medical evidence collection). Channel directories + NGO case reports registered done without legal nodes (schema: not used to invent duties).
- Wave 3 (18 provincial regulations): created synthesis `local-regulations-comparison` (delta matrix: 网络/经济/冻饿/目睹未成年人/告诫强制/远离令/强制报告/代为申请/热线/信息共享) instead of 18 near-duplicate nodes; kept guangdong-implementation as worked example. All marked done.
- Graph now: 12 nodes, evidence routed through the element layer (请求权基础分析). 2 syntheses filed back.
- Remaining needs-review: police-dv-handling-workflow (pre-2016), local-regulations-comparison (per-province 条号 verification), 法律援助法第32条 primary text not in source.

## [2026-06-08] lint | resolve 法律援助法第32条 (was false "missing")

- Traced the needs-review flag to its origin: `人身安全保护令实务.md` line 405 cites 《法律援助法》第32条 as a secondary claim.
- Found the primary text was ALREADY in the corpus: `中国反家庭暴力法律法规与司法解释.md` §13 (法律援助法) line 325, 第三十二条 — the large compilation's section 13, missed in wave-1 first pass.
- Resolved: added primary source_ref to `support-and-legal-aid` node; corrected scope ("主张相关权益" is broader than the secondary doc's "申请保护令"); checked off the synthesis review item; updated index gaps.
- Lint lesson recorded: large multi-law compilations need per-section verification; first-pass ingest can miss later sections. Flagged in index Open Gaps.

## [2026-06-08] expand | broaden coverage 11 -> 17 nodes

- User chose breadth over depth. Extracted 6 new nodes from existing sources (no new ingest needed):
  - `mandatory-reporting` (duty, 第14/35条 + 山西/重庆): institutional reporting + non-report sanctions.
  - `guardianship-revocation` (remedy, 第21条): revoke guardianship; support duties survive.
  - `temporary-shelter` (support, 第15/18条 + 告诫意见): setup, police-assisted placement, warning-letter voucher.
  - `child-witness-victim` (definition, local regs, needs-review): minors witnessing DV as victims — local extension, not in national law.
  - `special-protection-groups` (definition, 第5条): hub node for minors/elderly/disabled/pregnant/ill.
  - `divorce-and-dv` (procedure, 法释17号第11条 + 审理指南, needs-review): DV as divorce ground, "new circumstances" re-filing, separation violence.
- Added 15 edges; back-links added to existing node pages so Obsidian graph renders them.
- Graph: 17 nodes, 36 edges. defines_scope_for 9, enables 9, provides_evidence_for 6, localizes 6, parallel 3, is_element_of/proves/conflicts_with 1 each.
- Deferred: admonishment-vs-punishment (治安/刑事 vs 告诫) kept inline rather than split, to avoid over-fragmentation.
