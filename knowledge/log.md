# Knowledge Log

Append-only chronological record of ingests, durable query pages, lint passes, and major wiki maintenance.

## [2026-07-12] maintenance | 最高法典型案例逐案复合锚点

- 将引用 `家暴典型案例.md` 的节点从批次级月份锚点改为 `年份月份/案例编号` 复合锚点，共 46 条逐案引用。
- 将节点正文中的 `2023Nov`、`2023Jun`、`2025案例` 等简称统一为 `YYYY年M月案例N`。
- 扩展 chatflow ground 解析器，使复合锚点限定在父月份章节内，并精确区分 `案例1` 与 `案例10`；新增逐案解析回归测试。

## [2026-07-12] audit-fix | 最高法反家暴典型案例逐案核证

- 以 `source/家暴典型案例.md` 为唯一案例事实基准，逐案核对5批33案与引用该来源的节点。
- 修复重大错配：2025案例3由“受暴者反杀”纠正为施暴者故意杀人未遂；2025案例5移除误植的就业帮扶；2023Nov案例二/四强制报告事实拆分；2025案例4恢复“其他证据相互印证、非孤证定案”边界。
- 收窄过度概括：典型案例不表述为全国法定义务；法院回访、线上平台、一站式联动标明个案/地方实践；同居结束不当然排除保护令，但仍需关系关联、现实危险与证据。
- 拆分程序证明标准：`protection-order-evidence` 仅保留保护令“较大可能性”及证据清单，不再混入离婚和刑事案件的证据评价。
- 新增 `dv-self-defense` 节点，明确“制止正在进行的家暴而正当防卫”与“事后杀害施暴人后量刑从宽”的法律性质差异。
- 新增 `civil-dv-fact-finding` 节点，承接离婚等民事案件中的综合证据评价和职权探知，并与保护令、刑事证明标准明确隔离；2023Jun案例3则归入责任阶梯的刑事案例参照。
- 新增审计报告 `wiki/audits/court-cases-node-audit-2026-07-12.md`；案例型 source_refs 已统一为源文件中可解析的真实批次锚点。

## [2026-06-28] ingest | 家暴典型案例全量 ingest（33案例，wave 4 完整版）

- 補充wave 4 初轮漏处理的 29 个案例（2025年11月8个、2024年11月5个、2023年11月6个、2023年6月10个）。
- Synthesis 节点：新建 `wiki/syntheses/court-cases-collection.md`，33案例按8主题分组（家暴形式扩展/保护令/刑事责任/受暴者反杀/未成年保护/离婚抚养/证据特则/正当防卫）。
- 新建节点2个：
  - `sexual-violence-in-family`（definition, needs-review）：无明显反抗≠同意；未成年被害人陈述特殊采信规则。
  - `dv-survivor-homicide`（consequence, needs-review）：受暴者杀施暴人"情节较轻"从宽处罚；延迟控告合理性。3个案例确立一致先例。
- source_refs 更新：`child-witness-victim`（+7）、`divorce-and-dv`（+3）、`mandatory-reporting`（+2）、`protection-order-evidence`（+1）。
- index.md 新增2个节点条目 + court-cases-collection synthesis 条目。
- Graph: 19 nodes（+2）, edges 结构不变（新节点机制关系已在节点页 wikilink 记录）。

## [2026-06-28] ingest | 最高人民法院反家庭暴力典型案例（2026.3.30）

- Source: `家暴典型案例.md`, source_type: `court_cases`, tier 1（用户决策：最高法典型案例独立分级，高于 ngo_report）。
- 策略：整体 ingest，补充 source_ref 到现有节点，不新建节点。
- 更新节点3个：
  - `domestic-violence-definition`：新增案例一~三 source_ref；增加"最高法典型案例补充认定"表格（语言暴力/限制社交/经济控制三类形式的司法认定要点和法律后果）。
  - `personal-safety-protection-order`：新增案例二~四 source_ref；增加"一站式联动闭环干预机制"说明（案例三的多部门协助执行实践）。
  - `liability-ladder`：新增案例四 source_ref；在违反保护令条款下补充具体案例（拘留15日）。
- 新增 `court_cases`（tier 1）到 AGENTS.md 和 source-registry.md。
- Graph: 17 nodes, 39 edges（结构不变，citations 加强）。

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

## [2026-06-08] refactor | merge Guangdong into comparison; add liability-ladder; schema v0.4

- Q from user exposed an inconsistency: guangdong-implementation was a standalone node while 17 other provinces lived in the comparison synthesis — guangdong was special only because it was done first (historical accident, not design).
- Also found a 0-byte stray `nodes/local-regulations-comparison.md` (auto-created by Obsidian when following the [[link]]); deleted.
- Chose option A: merged Guangdong's specifics into `syntheses/local-regulations-comparison.md` (added as 4th 标志性条款 province), deleted `nodes/guangdong-implementation.md`, rerouted its 3 localizes edges to originate from local-regulations-comparison (now connects definition/public-security/protection-order). 18 provinces now treated uniformly.
- Split out `liability-ladder` (consequence node): 批评教育 → 告诫书(行政指导) → 治安处罚 → 刑事责任, plus protection-order-violation penalties (第34条). Clarifies 告诫 vs 治安/刑事 distinction the user asked about.
- Schema v0.4: re-introduced `creates_consequence_for` now that a real consequence node exists (protection-order --creates_consequence_for--> liability-ladder). Documented in AGENTS.md + edges.md vocab (now 9 relations).
- Graph: 17 nodes (−1 guangdong +1 liability-ladder), 39 edges, all valid, no broken links.
- 2026-07-12 | academic-ingest | 创建 `psychological-violence-concept`（F1）节点：基于 NotebookLM 精神暴力对话并回查蒋月（2016，第7-8页）、郝佳（2016，第59-64页）、但淑华（2025，第138-141页）PDF 原文；新增 `deepens` → `domestic-violence-definition` 边，标记冷暴力、持续性与时效边界。状态：needs-review。
- 2026-07-12 | academic-ingest | 创建 `economic-control-concept`（F1）节点：基于 NotebookLM 经济控制对话并回查王理万（2025，第67-81页）、但淑华（2025，第138-143页）、王丹（2022，第14-15页）、郝佳（2016，第58-64页）PDF 原文；新增 `deepens` → `domestic-violence-definition` 边，区分独立说、涵盖说与一般财务分歧。状态：needs-review。
- 2026-07-12 | academic-ingest | 创建 `dv-scope-extension`（F1）节点：基于 NotebookLM 主体范围对话并回查但淑华（2025，第133-143页）、薛宁兰（2017，第1-7页）、王丹（2022，第11-21页）PDF 原文；新增 `deepens` → `domestic-violence-definition` 边，区分第三十七条、前任关系与《妇女权益保障法》保护令路径。状态：needs-review。
- 2026-07-12 | academic-ingest | 创建 `dv-law-legislative-history`（F2）节点：基于 NotebookLM 立法史对话并回查高莎薇等（2016，第18-20页）、但淑华（2025，第134-135、140页）、郝佳（2016，第58页）、郭夏娟/郑熹（2017，第174-182页）PDF 原文；新增 `traces_legislative_origin_of` → `domestic-violence-definition` 边，并显式记录保护令草案演变和性别中立动机证据不足。状态：needs-review。
- 2026-07-12 | academic-ingest | 创建 `coercive-control-comparative`（F2）节点：基于 NotebookLM 强制性控制对话并回查但淑华（2025）、胡邦彦（2026）、王世洲（2016）、李瀚琰（2017）、薛宁兰（2017）PDF 原文；因现有材料只能证明比较差异、不能证明直接立法来源，采用 `deepens` → `domestic-violence-definition`，未采用设计草案中的 `traces_legislative_origin_of`。状态：needs-review。
- 2026-07-12 | academic-ingest | 创建 `international-human-rights-standards`（F2）节点：基于 NotebookLM 国际标准对话并回查黄列（2002）、但淑华（2025）、陈爱武（2016）、于晶、胡邦彦（2026）PDF 原文；区分条约、一般性建议、结论性意见和软法，对 ICCPR/ICESCR 明确标记论文库证据不足；仅连接 `domestic-violence-definition`，未建立证据不足的责任阶梯边。状态：needs-review。
- 2026-07-12 | academic-ingest | 创建 `judicial-recognition-gap`（F3）节点：基于 NotebookLM 司法认定对话并回查张剑源（2018）、贺欣/肖惠娜（2019）、马忆南/贾雪（2016）、张海/陈爱武（2021）、王丹（2022）PDF 原文；严格区分认定率、赔偿支持率与保护令驳回率，新增三条 `contextualizes_reality_of` 边。状态：needs-review。
- 2026-07-12 | academic-ingest | 创建 `victim-agency-barriers`（F3）节点：基于 NotebookLM 结构性障碍对话并回查吴炜/何进平（2016）、佟新（2000）、彭文华（2022）、吴帆等（2023）PDF 原文；保留受害者能动性，明确习得性无助不是个体诊断，新增一条 `deepens` 和两条 `contextualizes_reality_of` 边。状态：needs-review。
- 2026-07-12 | academic-ingest | 创建 `state-intervention-limits`（F4）节点：基于 NotebookLM 国家干预边界对话并回查黄列（2002）、李洪祥（2020）、纪雅（2025）、王媖娴（2017）、兰孟晗（2021）PDF 原文；新增 `deepens` → `public-security-response-duty` 边，并将「穷尽自治/优先调解」明确标为不得用于高危家暴的争议观点。状态：needs-review。
- 2026-07-12 | academic-ingest | 创建 `constitutional-protection-obligation`（F4）节点：基于 NotebookLM 基本权利保护义务对话并回查胡邦彦（2026，第172-186页）、薛宁兰（2017，第1-2页）、李春斌（2015，第172-174页）PDF 原文；新增 `deepens` → `public-security-response-duty` 与 `liability-ladder` 两条边，明确宪法保护义务是学理框架，不能直接替代部门法诉请。状态：needs-review。
- 2026-07-12 | academic-ingest | 创建 `gender-power-analysis`（F5）节点：基于 NotebookLM 性别权力结构对话并回查佟新（2000）、郭夏娟/郑熹（2017）、黄列（2002）、吴帆/温腾龙/菅苗（2023）PDF 原文；新增 `deepens` → `domestic-violence-definition` 边，保留性别中立框架的保护收益与结构盲点，明确生态谬误、样本边界和非本质主义限制。F5 仅作AI隐性认知底色，不进入胶囊ground。状态：needs-review。
- 2026-07-12 | lint | 完成 academic layer 11节点一致性校验：固定十节与frontmatter齐全，45条本地PDF引用均可解析，16条学术边均在节点机制关系中有wikilink镜像且每个节点至少锚定一个Tier 1-4节点；11项结构测试通过，`git diff --check`通过。同步更新根机制树、索引、来源登记与chatflow的F5边界。
