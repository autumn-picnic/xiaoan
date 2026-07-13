---
type: legal-edge-catalog
title: "法律机制边目录"
source_refs:
  - "knowledge/source/中华人民共和国反家庭暴力法.md"
updated: 2026-07-12
status: draft
---

# 法律机制边目录

本文件记录法律机制树中的边。每条边都应说明：从哪个法律原子节点出发、指向哪个节点、关系类型是什么、依据来自哪条原始法条。

> Obsidian 约定：本表用纯文本（行内代码）引用节点，**不使用** `wikilink`，以免本文件在 graph view 里变成星型 hub。图上的边由各 node 页 `## 机制关系` 里的 node→node `wikilink` 承载，本表只是人/LLM 可读的带标签目录。

## Edge type vocabulary

12 种关系（v0.5，2026-07-11）。v0.2 把 10→6；v0.3 加回**要件层** `is_element_of`/`proves`；v0.4 因出现真实 consequence 节点（[[liability-ladder]]）加回 `creates_consequence_for`；v0.5 正式加入**学术层**三个边类型（`deepens`、`traces_legislative_origin_of`、`contextualizes_reality_of`）。

| Relation | Meaning |
| --- | --- |
| `defines_scope_for` | 定义/条件节点限定另一节点**是否适用、适用范围**（含门槛触发） |
| `is_element_of` | 要件节点（element）是某请求权/救济的**构成要件**（请求权基础） |
| `proves` | 证据节点**证明某个要件**（而不是泛泛支撑某救济） |
| `provides_evidence_for` | 来源节点（机构/义务/程序/支持）产出的记录构成证据 |
| `enables` | 一个节点使另一个节点在实践中**可用或得以执行**（含协助执行裁定） |
| `creates_consequence_for` | 一个行为/违反触发法律责任或后果节点 |
| `parallel_support_channel_for` | 支持渠道与另一路径并行，是补充而非替代（求助导航，非法律doctrine） |
| `localizes` | 地方规则细化/落实国家法节点（跨层级） |
| `conflicts_with` | 两个来源的主张看似冲突（标记，不要静默处理） |
| `deepens` | `concept-depth`（Tier 5）节点为 Tier 1–4 节点补充语义深度。非约束性；AI 引用须标注学术框架。 |
| `traces_legislative_origin_of` | `concept-depth` 节点说明某 Tier 1–4 概念的域外立法来源或立法历史。 |
| `contextualizes_reality_of` | `concept-depth`（F3 司法现实）节点解释某法律机制在实践中为何失灵或低效。 |

### 律师的推理链（请求权基础分析）

证据**永远不直接连救济**，而是经由要件：

```
来源（机构/义务/程序/支持）
   --provides_evidence_for-->  证据（evidence）
   --proves-->                 要件（element）
   --is_element_of-->          请求权/救济（remedy）
定义（definition）--defines_scope_for--> 要件（element）   # 定义界定要件含义
```

已删除的关系（v0.2 起）：`triggers`（并入 `defines_scope_for`）、`assists_execution_of`（并入 `enables`）、`requires`（反向，用 From→To 表达）、`creates_consequence_for`/`limits`（零使用，违反后果暂留 node 内部）。

完整 schema（节点类型、边类型、source_type 信任分级、ingest 粒度、禁止项）见 `knowledge/AGENTS.md`。

## Current edges

| From | Relation | To | Claim | Source refs | Status |
| --- | --- | --- | --- | --- | --- |
| `domestic-violence-definition` | `defines_scope_for` | `public-security-response-duty` | “家庭暴力报案”触发公安机关及时出警、制止、调查取证、协助就医/鉴定伤情等职责。 | 反家暴法第2条、第13条、第15条 | draft |
| `protection-order-element-danger` | `is_element_of` | `personal-safety-protection-order` | “遭受家暴或面临现实危险”是保护令请求权的核心权利发生要件（第27条三要件之一）。 | 反家暴法第27条、第23条 | draft |
| `domestic-violence-definition` | `defines_scope_for` | `protection-order-element-danger` | 家暴定义界定“遭受家暴”这一要件的含义（身体与精神侵害）。 | 反家暴法第2条、第27条 | draft |
| `public-security-response-duty` | `enables` | `personal-safety-protection-order` | 法院作出保护令后，公安机关以及居民委员会、村民委员会等应当协助执行。 | 反家暴法第32条 | draft |
| `support-and-legal-aid` | `parallel_support_channel_for` | `public-security-response-duty` | 单位、居委会/村委会、妇联等投诉求助渠道与公安报案路径并行，不能替代即时危险时的安全处理。 | 反家暴法第13条 | draft |
| `support-and-legal-aid` | `parallel_support_channel_for` | `personal-safety-protection-order` | 法律援助和诉讼费用减免可支持受害人使用法院路径，但不等于保证个案结果。 | 反家暴法第19条、第23条 | draft |
| `protection-order-evidence` | `proves` | `protection-order-element-danger` | 11类证据（陈述、告诫书、出警记录、视听资料、电子数据、医疗记录、求助记录、证人证言、伤情鉴定等）用于证明“遭受家暴或面临现实危险”要件；证明标准为“较大可能性”。 | 法释〔2022〕17号第六条（一手）；反家暴法第20条 | draft |
| `public-security-response-duty` | `provides_evidence_for` | `protection-order-evidence` | 告诫书、出警记录、报警回执、询问/讯问笔录等公安记录是保护令证据的重要组成。 | 反家暴法第16-17条、第20条；法释〔2022〕17号第六条 | draft |
| `support-and-legal-aid` | `provides_evidence_for` | `protection-order-evidence` | 单位、民政、居委会、村委会、妇联、救助机构等收到投诉/反映/求助的记录可作为证据之一。 | 法释〔2022〕17号第六条第(八)项 | draft |
| `domestic-violence-definition` | `defines_scope_for` | `warning-letter` | 家暴事实的认定界定是否对加害人出具告诫书。 | 反家暴法第16条；公通字〔2024〕34号第三至六条 | draft |
| `public-security-response-duty` | `enables` | `warning-letter` | 公安机关对情节较轻的家暴出具、送达告诫书并查访监督。 | 反家暴法第16-17条；公通字〔2024〕34号 | draft |
| `warning-letter` | `provides_evidence_for` | `protection-order-evidence` | 家庭暴力告诫书是法释〔2022〕17号列举的保护令证据之一。 | 法释〔2022〕17号第六条第(二)项；反家暴法第20条 | draft |
| `public-security-response-duty` | `enables` | `injury-appraisal-procedure` | 公安机关协助受害人就医、鉴定伤情，并按规定开具伤情鉴定委托书、规范现场处置。 | 反家暴法第15条；公安机关办理伤害案件规定第11-12条、第18-19条 | draft |
| `injury-appraisal-procedure` | `provides_evidence_for` | `protection-order-evidence` | 伤情鉴定意见是保护令及后续认定家暴事实的重要证据来源。 | 公安机关办理伤害案件规定第18-19条；反家暴法第20条 | draft |
| `police-dv-handling-workflow` | `enables` | `public-security-response-duty` | 警察五阶段工作流程把法定出警/处置职责落成可操作的现场流程。 | 预防和制止家庭暴力警察工作手册 | needs-review |
| `police-dv-handling-workflow` | `provides_evidence_for` | `protection-order-evidence` | 处警阶段的现场处置与收集固定证据，为后续证据链提供来源。 | 预防和制止家庭暴力警察工作手册 | needs-review |
| `police-dv-handling-workflow` | `conflicts_with` | `public-security-response-duty` | 手册成文较早，使用旧“保护裁定”表述且缺少告诫书制度，与现行反家暴法不完全一致，需核对。 | 预防和制止家庭暴力警察工作手册；反家暴法第16-17条、第23条 | needs-review |
| `local-regulations-comparison` | `localizes` | `domestic-violence-definition` | 地方条例普遍扩展定义：网络手段、冻饿、禁闭、经济控制、跟踪骚扰等（广东第2条、重庆第2条、甘肃/黑龙江第3条等）。 | 18省条例定义条款 | draft |
| `local-regulations-comparison` | `localizes` | `public-security-response-duty` | 地方条例细化110接处警、出警记录、告知义务，以及“应当出具告诫书”的情形与24小时时限（广东第23/25-28条等）。 | 广东、山东、重庆等条例 | draft |
| `local-regulations-comparison` | `localizes` | `personal-safety-protection-order` | 地方条例扩展代为/委托申请，增加“远离令”并可分批多次作出，细化公安24小时核实与协助执行（广东第31-33条等）。 | 广东、云南、重庆等条例 | draft |
| `support-and-legal-aid` | `enables` | `dv-risk-assessment` | 妇联受理家暴投诉后按登记/危险评估/分级处理程序开展危险评估。 | 妇联组织受理家庭暴力投诉工作规程第6-11条 | draft |
| `police-dv-handling-workflow` | `enables` | `dv-risk-assessment` | 警察处警阶段进行危险评估，识别高危信号。 | 预防和制止家庭暴力警察工作手册 | needs-review |
| `domestic-violence-definition` | `defines_scope_for` | `mandatory-reporting` | 家暴/疑似家暴的认定界定机构强制报告义务的触发。 | 反家暴法第14条 | draft |
| `mandatory-reporting` | `enables` | `public-security-response-duty` | 机构强制报案触发公安出警与处置。 | 反家暴法第14条 | draft |
| `local-regulations-comparison` | `localizes` | `mandatory-reporting` | 地方条例扩展报告对象并禁止打击报复报告人。 | 山西办法第13条；重庆办法 | draft |
| `domestic-violence-definition` | `defines_scope_for` | `guardianship-revocation` | 家暴严重侵害被监护人权益的认定界定撤销监护资格的适用。 | 反家暴法第21条 | draft |
| `special-protection-groups` | `defines_scope_for` | `guardianship-revocation` | 被监护人多为特殊保护群体，触发撤销监护与另行指定。 | 反家暴法第5条、第21条 | draft |
| `special-protection-groups` | `defines_scope_for` | `mandatory-reporting` | 强制报告对象多为无/限制民事行为能力的特殊群体。 | 反家暴法第5条、第14条 | draft |
| `local-regulations-comparison` | `localizes` | `special-protection-groups` | 地方条例扩展特殊保护对象（如终止妊娠六个月内妇女、目睹家暴未成年人）。 | 重庆/甘肃等条例 | needs-review |
| `public-security-response-duty` | `enables` | `temporary-shelter` | 公安协助将危险状态的无/限制民事行为能力人安置到临时庇护场所。 | 反家暴法第15条、第18条 | draft |
| `warning-letter` | `enables` | `temporary-shelter` | 告诫书可作为受害人主动申请临时庇护的书面凭证。 | 告诫制度意见 | draft |
| `temporary-shelter` | `parallel_support_channel_for` | `personal-safety-protection-order` | 临时庇护与法院保护令路径并行，是临时生活帮助而非替代。 | 反家暴法第18条 | draft |
| `domestic-violence-definition` | `defines_scope_for` | `child-witness-victim` | 地方层面把目睹家暴的未成年人纳入受害人范围。 | 重庆/甘肃/黑龙江条例 | needs-review |
| `local-regulations-comparison` | `localizes` | `child-witness-victim` | 目睹家暴未成年人为地方扩展概念，国家法无明文。 | 重庆/甘肃/黑龙江条例 | needs-review |
| `domestic-violence-definition` | `defines_scope_for` | `divorce-and-dv` | 家暴认定界定离婚法定理由与损害赔偿依据。 | 民法典婚姻家庭编；审理指南第17条 | needs-review |
| `personal-safety-protection-order` | `provides_evidence_for` | `divorce-and-dv` | 保护令及违反情形可作为离婚/再诉中综合认定家暴事实的依据之一。 | 法释〔2022〕17号第十一条 | draft |
| `domestic-violence-definition` | `defines_scope_for` | `liability-ladder` | 家暴认定是适用批评教育/告诫/治安/刑事各层责任的前提。 | 反家暴法第16、33条 | draft |
| `warning-letter` | `defines_scope_for` | `liability-ladder` | 告诫对应“情节较轻、不予治安处罚”一层，与治安/刑事处罚层互斥。 | 反家暴法第16条；公通字〔2024〕34号第一条 | draft |
| `personal-safety-protection-order` | `creates_consequence_for` | `liability-ladder` | 违反保护令触发训诫、1000元以下罚款、15日以下拘留或刑事责任。 | 反家暴法第34条 | draft |
| `domestic-violence-definition` | `defines_scope_for` | `sexual-violence-in-family` | 既有家暴形成的恐惧与控制情境，会影响家庭成员或共同生活、照护关系中性侵案件的意志判断与证据审查；无明显反抗不等于同意。 | 家暴典型案例2025案例2、4 | needs-review |
| `special-protection-groups` | `defines_scope_for` | `sexual-violence-in-family` | 未成年被害人的身心特点、陈述形成环境及是否受干扰，是审查其陈述证明力的重要因素。 | 家暴典型案例2025案例2、4 | needs-review |
| `domestic-violence-definition` | `defines_scope_for` | `dv-survivor-homicide` | 长期严重家暴史及其对受暴者的影响，是判断杀害施暴人案件起因、动机、被害人过错和是否属于故意杀人“情节较轻”的重要事实。 | 家暴典型案例2024案例二、2023Jun案例2 | needs-review |
| `domestic-violence-definition` | `defines_scope_for` | `dv-self-defense` | 正在进行的家庭暴力属于正当防卫所针对的不法侵害；是否成立防卫及是否过当仍须结合行为目的、时机和限度判断。 | 家暴典型案例2023Jun案例4 | needs-review |
| `civil-dv-fact-finding` | `enables` | `divorce-and-dv` | 离婚等民事案件可结合当事人陈述、报警和医疗材料、鉴定、未成年子女证言及对方解释能力综合认定家暴，并加强职权探知；不得与保护令或刑事证明标准混同。 | 家暴典型案例2023Jun案例8、9 | needs-review |
| `psychological-violence-concept` | `deepens` | `domestic-violence-definition` | 学术研究补充精神暴力的控制目的、人格利益侵害、行为类型及冷暴力边界争议；非约束性，不能替代法律认定。 | 蒋月（2016）第7-8页；郝佳（2016）第59-64页；但淑华（2025）第138-141页 | needs-review |
| `economic-control-concept` | `deepens` | `domestic-violence-definition` | 学术研究补充经济控制的经济自主侵害、依附后果、四类行为及独立说/涵盖说分歧；非约束性，不能替代法律认定。 | 王理万（2025）第67-81页；但淑华（2025）第138-143页；王丹（2022）第14-15页；郝佳（2016）第58-64页 | needs-review |
| `dv-scope-extension` | `deepens` | `domestic-violence-definition` | 学术研究补充「家庭成员以外共同生活的人」的关系类型、共同生活判断及前任伴侣边界；非约束性，保护令资格不等同于全面纳入家暴定义。 | 但淑华（2025）第133-143页；薛宁兰（2017）第1-7页；王丹（2022）第11-21页 | needs-review |
| `dv-law-legislative-history` | `traces_legislative_origin_of` | `domestic-violence-definition` | 学术资料解释主体范围与精神暴力的草案演变、性暴力和经济控制未独立列举的取舍；立法动机区分同期陈述、学者解释与事后批评。 | 高莎薇等（2016）第18-20页；但淑华（2025）第134-135、140页；郝佳（2016）第58页 | needs-review |
| `coercive-control-comparative` | `deepens` | `domestic-violence-definition` | 比较研究以持续、反复的控制行为模式补充按侵害客体划分的家暴类型，并记录两种分类维度的争议；现有证据不足以建立直接立法来源关系。 | 但淑华（2025）第133、140-141页；胡邦彦（2026）第180页；王世洲（2016）第92-101页 | needs-review |
| `international-human-rights-standards` | `deepens` | `domestic-violence-definition` | 学术研究以 CEDAW、CRC、国际政策文件和区域性比较标准补充家暴范围与国家保护视角；条约、解释材料、结论性意见和软法效力必须区分。 | 黄列（2002）PDF第2-7页；但淑华（2025）第132-134页；陈爱武（2016）第128-130页；于晶第108-109页；胡邦彦（2026）第179-180页 | needs-review |
| `judicial-recognition-gap` | `contextualizes_reality_of` | `protection-order-evidence` | 实证研究解释家暴证据形成、评价、公安定性依赖及证明标准被主观抬高的问题；统计口径不可外推。 | 张剑源（2018）第103-111页；张海/陈爱武（2021）第185-200页 | needs-review |
| `judicial-recognition-gap` | `contextualizes_reality_of` | `divorce-and-dv` | 实证研究解释调解、是否判离、抚养财产平衡、二审和安全压力如何影响家暴事实书写与认定。 | 贺欣/肖惠娜（2019）第5-20页；张剑源（2018）第103-111页 | needs-review |
| `judicial-recognition-gap` | `contextualizes_reality_of` | `personal-safety-protection-order` | 对驳回裁定和历史统计的研究揭示证明责任、主体范围、保证书与法官顾虑等实践障碍；不等于全国驳回原因分布。 | 张海/陈爱武（2021）第185-200页；王丹（2022）第11-21页 | needs-review |
| `victim-agency-barriers` | `deepens` | `domestic-violence-definition` | 结构性研究补充经济、住房、照护、安全、社会支持与制度回应如何压缩受害者选择空间；继续关系不等于同意暴力。 | 吴炜/何进平（2016）第88-91页；佟新（2000）第102-111页 | needs-review |
| `victim-agency-barriers` | `contextualizes_reality_of` | `protection-order-evidence` | 求助失败、资源不足、报复风险和机构回应可能使证据延迟形成、不完整或中断，不能据缺失反推暴力不存在。 | 吴炜/何进平（2016）第88-91页；彭文华（2022）第66-77页 | needs-review |
| `victim-agency-barriers` | `contextualizes_reality_of` | `judicial-recognition-gap` | 理想化的立即报警、立即离开模型可能误读受害者的生存策略并放大司法认定鸿沟。 | 佟新（2000）第102-111页；吴帆等（2023）第65-79页 | needs-review |
| `state-intervention-limits` | `deepens` | `public-security-response-duty` | 法理研究解释公私领域二分、国家介入正当性、家庭自治边界及警务「家务事」观念；自治和调解不得削弱高危处置与现行职责。 | 黄列（2002）PDF第5-7页；李洪祥（2020）第141-152页；王媖娴（2017）第67-72页；兰孟晗（2021）第37-45页 | needs-review |
| `constitutional-protection-obligation` | `deepens` | `public-security-response-duty` | 基本权利国家保护义务解释国家为何须积极保护家暴受害人，公安具体职责仍须由现行部门法确定。 | 胡邦彦（2026）第172-186页；薛宁兰（2017）第1-2页 | needs-review |
| `constitutional-protection-obligation` | `deepens` | `liability-ladder` | 禁止保护不足与风险预防视角可用于学理审视责任层级是否有效，但不改变现行责任条件。 | 胡邦彦（2026）第174-176、181-186页 | needs-review |
| `gender-power-analysis` | `deepens` | `domestic-violence-definition` | 性别权力与资源结构分析补充家暴发生、持续和求助障碍的解释，并防止受害者归责；F5 只作AI隐性认知底色，不进入胶囊ground或个案事实认定。 | 佟新（2000）第102-111页；郭夏娟、郑熹（2017）第174-183页；黄列（2002）PDF第5-10页；吴帆等（2023）第65-79页 | needs-review |

## Open edge gaps

- 需要从 `knowledge/source/公安机关办理伤害案件规定.md` 和 `knowledge/source/预防和制止家庭暴力警察工作手册.md` 中补充公安处置相关边。
- 需要从地方条例中补充“上位法依据 / 地方细化 / 地方差异”边。
- 需要从 `knowledge/source/人身安全保护令实务.md` 中补充保护令申请、证据、执行和违反后果的实践边。

## Schema 校准发现（pilot）

- Schema v0.1 的 `localizes` 只覆盖“地方规则细化国家法”，但司法解释（如法释〔2022〕17号）细化国家法的情况没有专门关系类型。pilot 暂用 `provides_evidence_for` + `needs-review` 表达，待 schema 评审时考虑新增 `interprets`/`refines` 关系。
- 二手实务来源转述一手司法解释时，应统一标记 `needs-review`，并在节点中注明原文待补。
