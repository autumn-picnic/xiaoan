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

## Edge type vocabulary

| Relation | Meaning |
| --- | --- |
| `defines_scope_for` | 一个定义节点限定另一个制度/义务/救济节点的适用范围 |
| `triggers` | 一个事实或条件触发某项义务、程序或救济 |
| `requires` | 一个救济/程序需要某个条件或前置输入 |
| `enables` | 一个节点使另一个节点在实践中可用 |
| `provides_evidence_for` | 一个记录、材料或程序结果可支持后续事实认定 |
| `assists_execution_of` | 一个机构或程序协助另一个救济/裁定执行 |
| `parallel_support_channel_for` | 一个支持渠道与另一路径并行存在，可作为补充 |
| `creates_consequence_for` | 一个行为触发法律责任或后果 |
| `localizes` | 地方规则细化/落实国家法节点 |
| `conflicts_with` | 两个来源的主张看似冲突（标记，不要静默处理） |

完整 schema v0.1（节点类型、边类型、source_type 信任分级、ingest 粒度、禁止项）见 `knowledge/AGENTS.md`。

## Current edges

| From | Relation | To | Claim | Source refs | Status |
| --- | --- | --- | --- | --- | --- |
| [[domestic-violence-definition]] | `defines_scope_for` | [[public-security-response-duty]] | “家庭暴力报案”触发公安机关及时出警、制止、调查取证、协助就医/鉴定伤情等职责。 | 反家暴法第2条、第13条、第15条 | draft |
| [[domestic-violence-definition]] | `defines_scope_for` | [[personal-safety-protection-order]] | 遭受家庭暴力或面临家庭暴力现实危险，是申请人身安全保护令的核心事实基础。 | 反家暴法第2条、第23条、第27条 | draft |
| [[public-security-response-duty]] | `provides_evidence_for` | [[personal-safety-protection-order]] | 公安机关出警记录、告诫书、伤情鉴定意见等可作为法院认定家庭暴力事实的证据来源；保护令相关事实判断可受这些证据支持，但法条第20条并不只限于保护令案件。 | 反家暴法第20条、第23条、第27条 | draft |
| [[public-security-response-duty]] | `assists_execution_of` | [[personal-safety-protection-order]] | 法院作出保护令后，公安机关以及居民委员会、村民委员会等应当协助执行。 | 反家暴法第32条 | draft |
| [[support-and-legal-aid]] | `parallel_support_channel_for` | [[public-security-response-duty]] | 单位、居委会/村委会、妇联等投诉求助渠道与公安报案路径并行，不能替代即时危险时的安全处理。 | 反家暴法第13条 | draft |
| [[support-and-legal-aid]] | `parallel_support_channel_for` | [[personal-safety-protection-order]] | 法律援助和诉讼费用减免可支持受害人使用法院路径，但不等于保证个案结果。 | 反家暴法第19条、第23条 | draft |
| [[protection-order-evidence]] | `provides_evidence_for` | [[personal-safety-protection-order]] | 多类证据（陈述、告诫书、出警记录、医疗记录、证人证言、伤情鉴定等）可用于支持保护令申请；证明标准为“较大可能性”。 | 人身安全保护令实务（转述法释〔2022〕17号第6条）；反家暴法第20条 | needs-review |
| [[public-security-response-duty]] | `provides_evidence_for` | [[protection-order-evidence]] | 告诫书、出警记录、报警回执等公安记录是保护令证据的重要组成。 | 反家暴法第16-17条、第20条；人身安全保护令实务 | needs-review |
| [[support-and-legal-aid]] | `provides_evidence_for` | [[protection-order-evidence]] | 妇联、居委会、救助机构收到投诉/求助的记录可作为保护令证据之一。 | 人身安全保护令实务（转述法释〔2022〕17号第6条） | needs-review |
| [[public-security-response-duty]] | `enables` | [[injury-appraisal-procedure]] | 公安机关协助受害人就医、鉴定伤情，并按规定开具伤情鉴定委托书、规范现场处置。 | 反家暴法第15条；公安机关办理伤害案件规定第11-12条、第18-19条 | draft |
| [[injury-appraisal-procedure]] | `provides_evidence_for` | [[protection-order-evidence]] | 伤情鉴定意见是保护令及后续认定家暴事实的重要证据来源。 | 公安机关办理伤害案件规定第18-19条；反家暴法第20条 | draft |
| [[police-dv-handling-workflow]] | `enables` | [[public-security-response-duty]] | 警察五阶段工作流程把法定出警/处置职责落成可操作的现场流程。 | 预防和制止家庭暴力警察工作手册 | needs-review |
| [[police-dv-handling-workflow]] | `provides_evidence_for` | [[protection-order-evidence]] | 处警阶段的现场处置与收集固定证据，为后续证据链提供来源。 | 预防和制止家庭暴力警察工作手册 | needs-review |
| [[police-dv-handling-workflow]] | `conflicts_with` | [[public-security-response-duty]] | 手册成文较早，使用旧“保护裁定”表述且缺少告诫书制度，与现行反家暴法不完全一致，需核对。 | 预防和制止家庭暴力警察工作手册；反家暴法第16-17条、第23条 | needs-review |
| [[guangdong-implementation]] | `localizes` | [[domestic-violence-definition]] | 广东办法把定义细化到冻饿、禁闭、跟踪骚扰，并将网络手段实施的恐吓/精神侵害纳入家庭暴力。 | 广东省实施办法第2条 | draft |
| [[guangdong-implementation]] | `localizes` | [[public-security-response-duty]] | 广东办法细化110接处警、出警记录、告知义务，以及“应当出具告诫书”的情形与24小时时限。 | 广东省实施办法第23条、第25-28条 | draft |
| [[guangdong-implementation]] | `localizes` | [[personal-safety-protection-order]] | 广东办法扩展代为/委托申请，增加“远离令”措施并可分批多次作出，细化公安24小时核实与协助执行。 | 广东省实施办法第31-33条 | draft |

## Open edge gaps

- 需要从 `knowledge/source/公安机关办理伤害案件规定.md` 和 `knowledge/source/预防和制止家庭暴力警察工作手册.md` 中补充公安处置相关边。
- 需要从地方条例中补充“上位法依据 / 地方细化 / 地方差异”边。
- 需要从 `knowledge/source/人身安全保护令实务.md` 中补充保护令申请、证据、执行和违反后果的实践边。

## Schema 校准发现（pilot）

- Schema v0.1 的 `localizes` 只覆盖“地方规则细化国家法”，但司法解释（如法释〔2022〕17号）细化国家法的情况没有专门关系类型。pilot 暂用 `provides_evidence_for` + `needs-review` 表达，待 schema 评审时考虑新增 `interprets`/`refines` 关系。
- 二手实务来源转述一手司法解释时，应统一标记 `needs-review`，并在节点中注明原文待补。
