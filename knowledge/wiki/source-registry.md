---
type: source-registry
title: "原始法律来源登记表"
updated: 2026-06-07
status: draft
---

# 原始法律来源登记表

本表登记 `knowledge/source/` 中的只读来源，并标注 `source_type`（信任分级见 `knowledge/AGENTS.md`）和当前 ingest 状态。原始文件由用户维护，LLM 只读，不在此处改写来源内容。

`ingest` 状态：`done` 已抽取节点/边；`pilot` 计划用于试验性 ingest；`pending` 待处理。

| Source | source_type | tier | ingest |
| --- | --- | --- | --- |
| `中华人民共和国反家庭暴力法` | national_law | 1 | done |
| `涉及家庭暴力婚姻案件审理指南` | judicial_interpretation | 1 | done |
| `人身安全保护令实务` | practice_guide | 3 | done |
| `中国反家庭暴力法律法规与司法解释` | judicial_interpretation | 1 | done |
| `公安机关办理伤害案件规定` | agency_rule | 2 | done |
| `妇联组织受理家庭暴力投诉工作规程` | agency_rule | 2 | done |
| `预防和制止家庭暴力警察工作手册` | official_manual | 3 | done |
| `预防和制止家庭暴力多部门合作工作手册` | official_manual | 3 | done |
| `如何寻求医院及法医鉴定的帮助` | practice_guide | 3 | done |
| `全国投诉渠道` | channel_directory | 4 | done |
| `各省投诉渠道` | channel_directory | 4 | done |
| `为平七周年_案例` | ngo_report | 4 | done |
| `为平八周年_案例` | ngo_report | 4 | done |
| `云南省反家庭暴力条例` | local_regulation | 2 | pending |
| `吉林省反家庭暴力条例` | local_regulation | 2 | pending |
| `山东省反家庭暴力条例` | local_regulation | 2 | pending |
| `山西省家庭暴力预防和处置办法` | local_regulation | 2 | pending |
| `河北省反家庭暴力条例(2022修订)` | local_regulation | 2 | pending |
| `河南省反家庭暴力条例` | local_regulation | 2 | pending |
| `湖北省反家庭暴力条例` | local_regulation | 2 | pending |
| `甘肃省反家庭暴力条例` | local_regulation | 2 | pending |
| `贵州省反家庭暴力条例` | local_regulation | 2 | pending |
| `辽宁省反家庭暴力条例` | local_regulation | 2 | pending |
| `青海省反家庭暴力条例` | local_regulation | 2 | pending |
| `黑龙江省反家庭暴力条例` | local_regulation | 2 | pending |
| `安徽省实施《中华人民共和国反家庭暴力法》办法` | local_regulation | 2 | pending |
| `广东省实施《中华人民共和国反家庭暴力法》办法` | local_regulation | 2 | done |
| `海南省实施《中华人民共和国反家庭暴力法》办法` | local_regulation | 2 | pending |
| `湖南省实施《中华人民共和国反家庭暴力法》办法` | local_regulation | 2 | pending |
| `重庆市实施《中华人民共和国反家庭暴力法》办法` | local_regulation | 2 | pending |
| `陕西省实施《中华人民共和国反家庭暴力法》办法` | local_regulation | 2 | pending |
| `新疆维吾尔自治区实施《中华人民共和国反家庭暴力法》办法` | local_regulation | 2 | pending |

## Pilot ingest 批次

建议用以下代表性来源先做 pilot ingest，用来校准 schema v0.1，再全量：

1. `中华人民共和国反家庭暴力法`（已部分完成）
2. `人身安全保护令实务`
3. `公安机关办理伤害案件规定`
4. `预防和制止家庭暴力警察工作手册`
5. 一个地方条例，例如 `广东省实施《中华人民共和国反家庭暴力法》办法`

## 说明

- `tier` 与冲突处理规则见 `knowledge/AGENTS.md` 的 “Source types and trust priority”。
- `channel_directory` 与 `ngo_report` 只能支撑 support/context 节点，不能用来推导法律义务。
- 本表只登记来源元数据，不复制来源正文。

## Ingest 说明（wave 2）

- `channel_directory`（全国/各省投诉渠道）与 `ngo_report`（为平案例）按 schema 不创建法律节点：前者是联系方式目录，后者是案例叙事，均不得用来推导法律义务。已登记为 done，内容仅作 support/context 参考。
- `预防和制止家庭暴力多部门合作工作手册`（official_manual）内容与现有协作/转介/危险评估节点重叠，未单独建节点，避免重复；其危险评估部分并入 [[dv-risk-assessment]]。
- `如何寻求医院及法医鉴定的帮助` 的就医取证要点并入 [[injury-appraisal-procedure]]。
