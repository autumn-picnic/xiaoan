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
| `provides_evidence_for` | 一个记录、材料或程序结果可支持后续事实认定 |
| `assists_execution_of` | 一个机构或程序协助另一个救济/裁定执行 |
| `parallel_support_channel_for` | 一个支持渠道与另一路径并行存在，可作为补充 |
| `creates_consequence_for` | 一个行为触发法律责任或后果 |

## Current edges

| From | Relation | To | Claim | Source refs | Status |
| --- | --- | --- | --- | --- | --- |
| [[domestic-violence-definition]] | `defines_scope_for` | [[public-security-response-duty]] | “家庭暴力报案”触发公安机关及时出警、制止、调查取证、协助就医/鉴定伤情等职责。 | 反家暴法第2条、第13条、第15条 | draft |
| [[domestic-violence-definition]] | `defines_scope_for` | [[personal-safety-protection-order]] | 遭受家庭暴力或面临家庭暴力现实危险，是申请人身安全保护令的核心事实基础。 | 反家暴法第2条、第23条、第27条 | draft |
| [[public-security-response-duty]] | `provides_evidence_for` | [[personal-safety-protection-order]] | 公安机关出警记录、告诫书、伤情鉴定意见等可作为法院认定家庭暴力事实的证据来源；保护令相关事实判断可受这些证据支持，但法条第20条并不只限于保护令案件。 | 反家暴法第20条、第23条、第27条 | draft |
| [[public-security-response-duty]] | `assists_execution_of` | [[personal-safety-protection-order]] | 法院作出保护令后，公安机关以及居民委员会、村民委员会等应当协助执行。 | 反家暴法第32条 | draft |
| [[support-and-legal-aid]] | `parallel_support_channel_for` | [[public-security-response-duty]] | 单位、居委会/村委会、妇联等投诉求助渠道与公安报案路径并行，不能替代即时危险时的安全处理。 | 反家暴法第13条 | draft |
| [[support-and-legal-aid]] | `parallel_support_channel_for` | [[personal-safety-protection-order]] | 法律援助和诉讼费用减免可支持受害人使用法院路径，但不等于保证个案结果。 | 反家暴法第19条、第23条 | draft |

## Open edge gaps

- 需要从 `knowledge/source/公安机关办理伤害案件规定.md` 和 `knowledge/source/预防和制止家庭暴力警察工作手册.md` 中补充公安处置相关边。
- 需要从地方条例中补充“上位法依据 / 地方细化 / 地方差异”边。
- 需要从 `knowledge/source/人身安全保护令实务.md` 中补充保护令申请、证据、执行和违反后果的实践边。
