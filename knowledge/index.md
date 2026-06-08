# Knowledge Index

This is the content-oriented catalog for XiaoAn's LLM-maintained legal mechanism tree. Read this first when searching the legal middle layer, then open the relevant node pages and [[edges]].

## Tree Root

| Page | Summary |
| --- | --- |
| [[legal-mechanism-tree]] | Root page for the legal middle layer: raw legal sources -> legal atom nodes + legal mechanism edges. |
| [[edges]] | Edge catalog where legal mechanisms are represented as sourced relationships between nodes. |
| [[source-registry]] | Registry of raw sources with `source_type`, trust tier, and ingest status. |

## Read-only Raw Legal Sources

| Source | Notes |
| --- | --- |
| [[中华人民共和国反家庭暴力法]] | User-maintained raw legal source. Do not edit. |
| [[中国反家庭暴力法律法规与司法解释]] | 一手法规汇编：含法释〔2022〕17号、公通字〔2024〕34号等全文。Do not edit. |

## Legal Atom Nodes

| Page | Node kind | Summary | Key source refs |
| --- | --- | --- | --- |
| [[domestic-violence-definition]] | definition | Legal definition of domestic violence and groups requiring special protection. | 第2条、第5条、第37条 |
| [[public-security-response-duty]] | duty | Public security duties after a domestic-violence report: dispatch, stop violence, investigate evidence, assist medical care/appraisal. | 第13-17条、第20条 |
| [[personal-safety-protection-order]] | remedy | Protection order eligibility, applicants, jurisdiction, timing, measures, duration, execution, and consequences of violation. | 第23-34条 |
| [[warning-letter]] | remedy | Police warning letter (告诫书): issuance conditions, evidence conditions, service, follow-up. | 第16-17条；公通字〔2024〕34号 |
| [[guardianship-revocation]] | remedy | Revocation of guardianship for severe DV against a ward; support duties survive. | 第21条 |
| [[special-protection-groups]] | definition | Minors, elderly, disabled, pregnant/nursing women, seriously ill — special protection. | 第5条 |
| [[child-witness-victim]] | definition | Minors who witness DV treated as victims (local regulations; not in national law). | 重庆/甘肃/黑龙江条例 |
| [[mandatory-reporting]] | duty | Mandatory reporting by institutions for DV against persons lacking/with limited capacity. | 第14、35条；地方 |
| [[temporary-shelter]] | support | Temporary shelter setup, police-assisted placement, warning-letter as entry voucher. | 第15、18条；告诫意见 |
| [[divorce-and-dv]] | procedure | DV in divorce litigation: ground for divorce, "new circumstances" re-filing, separation violence. | 法释17号第11条；审理指南 |
| [[protection-order-element-danger]] | element | Core constitutive element of the protection-order claim: suffered DV or facing real danger (第27条要件3). | 第27条、第2条、第23条 |
| [[protection-order-evidence]] | evidence | Protection-order proof standard ("larger possibility") and evidence types; needs legal review (secondary source). | 人身安全保护令实务、第20条 |
| [[injury-appraisal-procedure]] | procedure | Injury-appraisal commission/timelines and police case handling; mediation limits. | 公安机关办理伤害案件规定第11-39条 |
| [[dv-risk-assessment]] | procedure | DV risk/lethality assessment and graded handling (妇联 scale + police manual). | 妇联规程；警察工作手册 |
| [[police-dv-handling-workflow]] | procedure | Five-stage police DV workflow and risk assessment; predates 2016 law, needs review. | 预防和制止家庭暴力警察工作手册 |
| [[guangdong-implementation]] | local-rule | Guangdong implementation specifics (online harassment as DV, mandatory warning-letter triggers, stay-away order). Guangdong only. | 广东省实施办法第2/23/25-33条 |
| [[support-and-legal-aid]] | support | Complaint channels, temporary shelter, legal aid, fee relief, and organization support. | 第13条、第18-22条 |

## Legal Mechanism Edges

See [[edges]] for the current sourced relationship table.

## Syntheses (legal analyses filed back into the wiki)

| Page | Method | Summary | Status |
| --- | --- | --- | --- |
| [[protection-order-six-part-checklist]] | 请求权基础分析法（六段式审判框架） | Six-part element checklist for the personal-safety protection order: overview, filing review, applicant claims, respondent defenses, element facts, knowledge graph. | draft |
| [[local-regulations-comparison]] | 上位法—下位法对照（localizes） | Cross-province comparison of 18 local DV regulations: definition/economic/online/witnessing-children deltas, mandatory warning letters, mandatory reporting, stay-away orders. | needs-review |

## Open Gaps

- All 32 sources in `knowledge/source/` are ingested (see [[source-registry]]). Pilot + full ingest complete.
- 18 省条例已做横向对比 [[local-regulations-comparison]]（needs-review，待逐省条号复核）。
- 旧《审理指南》（2008，“保护裁定”）多被现行法取代，是否单独建 superseded 节点待定。
- Lint 教训：大型法规汇编（如 `中国反家庭暴力法律法规与司法解释.md`，含 14+ 节）首轮 ingest 易只覆盖前部；需逐节核查。`法律援助法第32条` 即属此情形（原已在第13节，曾误判为缺失）。
- Scenario capsules are intentionally out of scope for the current phase.
