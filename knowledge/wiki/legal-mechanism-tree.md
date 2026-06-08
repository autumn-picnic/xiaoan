---
type: legal-mechanism-tree
title: "反家庭暴力法律机制树"
source_refs:
  - "knowledge/source/中华人民共和国反家庭暴力法.md"
updated: 2026-06-07
status: draft
---

# 反家庭暴力法律机制树

这是 XiaoAn 的法律中间层：把只读原始法条整理成可引用、可审计、可继续扩展的法律机制图。它不直接写用户话术，也不维护场景胶囊。

当前约定：

- Legal atoms 是图里的节点，存放在 [[domestic-violence-definition]] 这类 node page 中。
- Legal mechanisms 是节点之间的边/关系，集中记录在 [[edges]]，并在节点页里用 Obsidian links 表达。
- 原始法条只读；LLM 只维护 `knowledge/wiki/`、`knowledge/index.md`、`knowledge/log.md` 和本 schema。

## 只读来源

- [[中华人民共和国反家庭暴力法]]

## 当前节点

- [[domestic-violence-definition]]：家庭暴力定义、特殊保护对象、共同生活者参照适用。
- [[public-security-response-duty]]：报案渠道、公安处置、告诫书、记录和证据价值。
- [[personal-safety-protection-order]]：保护令申请条件、申请人、管辖、时限、措施、执行和违反后果。
- [[warning-letter]]：家庭暴力告诫书——出具条件、证据条件、送达、查访监督。
- [[protection-order-element-danger]]：保护令核心要件——遭受家暴或面临现实危险（第27条要件3）。
- [[protection-order-evidence]]：保护令证明标准与证据类型（需法律核对）。
- [[injury-appraisal-procedure]]：伤情鉴定与公安受案处置、调解边界。
- [[police-dv-handling-workflow]]：警察处理家暴五阶段工作流程（实务，需核对）。
- [[guangdong-implementation]]：广东省实施办法的地方细化（仅适用广东）。
- [[support-and-legal-aid]]：投诉求助渠道、临时庇护、法律援助、诉讼费用减免、监护撤销和组织支持。

## 综合分析（filed back）

- 六段式要件清单：`syntheses/protection-order-six-part-checklist.md`（请求权基础分析法应用于保护令，needs-review）。

## 当前机制边

详见 [[edges]]。当前已表达的机制包括：

- 家暴定义如何限定公安响应，并界定保护令“遭受家暴”要件的含义。
- 律师推理链：证据来源 → 证据 → 要件（遭受家暴/现实危险）→ 保护令请求权。
- 人身安全保护令作出后，公安机关、居委会、村委会如何协助执行。
- 投诉求助、临时庇护、法律援助与报警/法院路径如何构成并行支持渠道。

## 维护边界

- 原始法条由用户添加和维护，LLM 永远不改写。
- 法律机制树由 LLM 维护：可以新增、拆分、合并、重命名节点，并新增、修正、删除边。
- 场景胶囊是未来 product layer，由用户和 LLM 共同更新；当前不创建、不编辑。
- 每个节点和边必须保留来源依据和适用边界，不能把法律机制写成确定性的个案建议。
