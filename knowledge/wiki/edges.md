---
type: legal-edge-catalog
title: "法律机制边目录"
source_refs:
  - "knowledge/source/中华人民共和国反家庭暴力法.md"
updated: 2026-06-07
status: draft
---

# 法律机制边目录

本文件记录法律机制树中的边。每条边都应说明：从哪个法律原子节点出发、指向哪个节点、关系类型是什么、依据来自哪条原始法条。

> Obsidian 约定：本表用纯文本（行内代码）引用节点，**不使用** `wikilink`，以免本文件在 graph view 里变成星型 hub。图上的边由各 node 页 `## 机制关系` 里的 node→node `wikilink` 承载，本表只是人/LLM 可读的带标签目录。

## Edge type vocabulary

8 种关系（v0.3，2026-06-07）。v0.2 把 10→6；v0.3 加回**要件层**的 `is_element_of` 与 `proves`——这是律师“请求权基础分析法”的核心,不是冗余。

| Relation | Meaning |
| --- | --- |
| `defines_scope_for` | 定义/条件节点限定另一节点**是否适用、适用范围**（含门槛触发） |
| `is_element_of` | 要件节点（element）是某请求权/救济的**构成要件**（请求权基础） |
| `proves` | 证据节点**证明某个要件**（而不是泛泛支撑某救济） |
| `provides_evidence_for` | 来源节点（机构/义务/程序/支持）产出的记录构成证据 |
| `enables` | 一个节点使另一个节点在实践中**可用或得以执行**（含协助执行裁定） |
| `parallel_support_channel_for` | 支持渠道与另一路径并行，是补充而非替代（求助导航，非法律doctrine） |
| `localizes` | 地方规则细化/落实国家法节点（跨层级） |
| `conflicts_with` | 两个来源的主张看似冲突（标记，不要静默处理） |

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
| `guangdong-implementation` | `localizes` | `domestic-violence-definition` | 广东办法把定义细化到冻饿、禁闭、跟踪骚扰，并将网络手段实施的恐吓/精神侵害纳入家庭暴力。 | 广东省实施办法第2条 | draft |
| `guangdong-implementation` | `localizes` | `public-security-response-duty` | 广东办法细化110接处警、出警记录、告知义务，以及“应当出具告诫书”的情形与24小时时限。 | 广东省实施办法第23条、第25-28条 | draft |
| `guangdong-implementation` | `localizes` | `personal-safety-protection-order` | 广东办法扩展代为/委托申请，增加“远离令”措施并可分批多次作出，细化公安24小时核实与协助执行。 | 广东省实施办法第31-33条 | draft |
| `support-and-legal-aid` | `enables` | `dv-risk-assessment` | 妇联受理家暴投诉后按登记/危险评估/分级处理程序开展危险评估。 | 妇联组织受理家庭暴力投诉工作规程第6-11条 | draft |
| `police-dv-handling-workflow` | `enables` | `dv-risk-assessment` | 警察处警阶段进行危险评估，识别高危信号。 | 预防和制止家庭暴力警察工作手册 | needs-review |

## Open edge gaps

- 需要从 `knowledge/source/公安机关办理伤害案件规定.md` 和 `knowledge/source/预防和制止家庭暴力警察工作手册.md` 中补充公安处置相关边。
- 需要从地方条例中补充“上位法依据 / 地方细化 / 地方差异”边。
- 需要从 `knowledge/source/人身安全保护令实务.md` 中补充保护令申请、证据、执行和违反后果的实践边。

## Schema 校准发现（pilot）

- Schema v0.1 的 `localizes` 只覆盖“地方规则细化国家法”，但司法解释（如法释〔2022〕17号）细化国家法的情况没有专门关系类型。pilot 暂用 `provides_evidence_for` + `needs-review` 表达，待 schema 评审时考虑新增 `interprets`/`refines` 关系。
- 二手实务来源转述一手司法解释时，应统一标记 `needs-review`，并在节点中注明原文待补。
