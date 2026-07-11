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
| [[liability-ladder]] | consequence | DV liability ladder: criticism → warning letter → public-security penalty → criminal liability; protection-order violation. | 第16、33、34条 |
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
- **学术论文层（wave 5）**：81篇唯一论文已上传 NotebookLM（`b14e6843`；本地82个PDF含1组重复版本）。11个 concept-depth 节点已全部创建；规范见 [[academic-layer]]。

## 學術論文層節點（Tier 5，无法律强制力）

节点清单（参见 `knowledge/wiki/academic-layer.md` 中的抽取规则和 NotebookLM 查询模板）：

| 节点 | 功能 | 核心问题 |
| --- | --- | --- |
| [[psychological-violence-concept]] | F1 定义纵深 | 精神暴力的边界、冷暴力争议、认定困境（已创建，needs-review） |
| [[economic-control-concept]] | F1 定义纵深 | 经济控制定义、立法空白、学界分歧（已创建，needs-review） |
| [[dv-scope-extension]] | F1 定义纵深 | 准家庭成员、前任伴侣的认定边界（已创建，needs-review） |
| [[dv-law-legislative-history]] | F2 立法溯源 | 反家暴法为何如此立法、立法博弈（已创建，needs-review） |
| [[coercive-control-comparative]] | F2 比较法纵深 | 强制性控制行为模式、英国制度与保护令工具比较（已创建，needs-review） |
| [[international-human-rights-standards]] | F2 国际标准纵深 | CEDAW、CRC、国际政策文件与中国现行法边界（已创建，needs-review） |
| [[judicial-recognition-gap]] | F3 司法现实 | 样本口径、证据审查与法官组织行为（已创建，needs-review） |
| [[victim-agency-barriers]] | F3 司法现实 | 求助与离开的结构性障碍、受害者能动性（已创建，needs-review） |
| [[state-intervention-limits]] | F4 法哲学 | 公私领域、家庭自治与国家干预边界（已创建，needs-review） |
| [[constitutional-protection-obligation]] | F4 法哲学 | 基本权利保护义务、国家积极义务与保护不足审查（已创建，needs-review） |
| [[gender-power-analysis]] | F5 倡导框架 | 性别权力与资源结构分析（已创建，AI 隐性底色，needs-review） |
