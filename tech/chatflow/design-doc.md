# 小安 R-A-G 胶囊 + 法律 LLM-wiki Chatflow Design Doc

Status: Draft for review  
Owner: XiaoAn POC  
Scope: Local MVP -> production-ready chatflow architecture  
Last updated: 2026-06-21

## 1. Executive summary

小安的目标不是做一个普通 RAG 问答 bot,而是验证一条更结构化的路径:

```text
用户问题
  -> PII 脱敏
  -> 安全风险判断
  -> 场景胶囊路由
  -> R/A/G 胶囊渲染
  -> 法律 wiki/source ground 注入
  -> LLM 生成支持型回答
  -> 输出安全/法律边界检查
```

核心设计是把“对话策略”和“法律依据”分开:

- **胶囊**负责场景策略:Recognize(认知),Act(行动),Ground(需要哪些依据)。
- **法律 LLM-wiki**负责事实依据:法条、司法解释、实务节点、边界和冲突。
- **chatflow**负责运行时编排:脱敏、安全、路由、ground 解析、上下文、输出。

MVP 要回答的问题:

1. R-A-G 胶囊是否能让回答比普通 RAG 更稳定、更可控?
2. 胶囊只存 locator、运行时从 wiki 拉法律依据是否可行?
3. 胶囊边界按“用户目的”切是否合理?
4. 先脱敏再调用 LLM 的架构是否能支撑连续对话?

Production 要回答的问题:

1. 如何在隐私、安全、法律可靠性、成本、延迟之间做可持续工程化取舍?
2. 如何支持多人维护胶囊/wiki,并用 eval 持续发现漂移、断链、幻觉和边界混淆?

## 2. Goals and non-goals

### Goals

- 提供一个可以本地跑通的 chatflow MVP,用于真实样例测试。
- 在发送给外部 LLM 前完成 PII 脱敏。
- 支持跨轮对话,但只给 LLM 脱敏后的上下文。
- 用胶囊路由决定当前回答策略。
- 用 locator 从 wiki/source 拉取法律依据,避免胶囊内复制法条造成 drift。
- 产出可审计 debug 信息:命中胶囊、使用 locator、ground 断链、路由信心。
- 为未来 production 形态保留清晰接口,避免 POC 代码写死。

### Non-goals for MVP

- 不做 Web UI。
- 不做 Dify。
- 不做向量数据库。
- 不做账号系统/部署/多租户。
- 不做完整法律内容终审。
- 不保证回答可直接构成法律意见。
- 不做长期敏感数据存储。

### Design choice: MVP 先做“可验证链路”,不是“完整产品”

**Choice:** MVP 先做 CLI + OpenAI API + 文件系统胶囊/wiki。  
**Why:** 当前最大风险不是 UI 或部署,而是架构假设本身是否成立。先用最少系统复杂度验证胶囊、路由、ground、脱敏和上下文。  
**Rejected:** 直接做 Web app / Dify / 数据库。这样会过早引入产品和基础设施复杂度,掩盖核心架构问题。

## 3. Requirements

### Functional requirements

| Requirement             | MVP                                               | Production                                    |
| ----------------------- | ------------------------------------------------- | --------------------------------------------- |
| PII redaction           | 接口-only 桩(透传,不做实现)                            | 规则 + NER + 人审配置 + 区域化 PII policy              |
| Safety scan             | 本地关键词 red flag                                    | 多层检测:本地规则 + 小模型/LLM + 风险策略表                   |
| Capsule routing         | LLM-as-router,候选为全部胶囊                             | Hybrid:规则优先级 + embedding recall + LLM rerank  |
| Ground resolution       | node/law/synthesis locator 解析                     | locator lint、版本锁定、source snapshot、引用审计        |
| Conversation continuity | OpenAI Responses `previous_response_id` + 本地最小控制态 | 可插拔 session backend、摘要、TTL、隐私策略               |
| Answer composition      | 单 LLM 生成                                          | 分阶段生成 + output guard + legal citation checker |
| Eval                    | JSONL smoke eval                                  | CI eval、回归集、人工标注、混淆矩阵、风险样本                    |
| Observability           | CLI debug JSON                                    | 结构化日志、指标、trace、隐私过滤                           |

### Privacy requirements

- raw user input 不发送给外部 LLM。
- raw user input 不落日志。
- 发给 LLM 的文本必须是 redacted text。
- 日志只允许保存 redacted input、capsule_id、route result、locator、safety labels。
- PII map 只在本地内存中保留,默认不持久化。

### Safety requirements

- red flag 高于 active capsule。
- safety unclear 不直接进入 crisis SOP,避免用户体验变成反复追问“你安全吗”。
- 即时危险、自伤、孩子危险、手机监控等必须触发 safety-first response。
- 普通回答中也可以轻量带安全确认。

## 4. High-level architecture

```text
                ┌────────────────────┐
                │ Raw User Input      │
                └─────────┬──────────┘
                          │ local only
                          v
                ┌────────────────────┐
                │ PII Redaction Gate  │
                │ raw -> redacted     │
                └─────────┬──────────┘
                          │ redacted only
                          v
                ┌────────────────────┐
                │ Safety Scan         │
                └──────┬────────┬────┘
                       │        │
              red flag │        │ normal
                       v        v
              ┌────────────┐  ┌────────────────────┐
              │ Crisis SOP │  │ Capsule Router      │
              └──────┬─────┘  └─────────┬──────────┘
                     │                  │
                     │                  v
                     │        ┌────────────────────┐
                     │        │ Ground Resolver     │
                     │        │ locator -> source   │
                     │        └─────────┬──────────┘
                     │                  │
                     v                  v
              ┌────────────────────────────────────┐
              │ Main Support Agent / Responses API │
              │ redacted history + capsule + ground│
              └─────────────────┬──────────────────┘
                                v
                      ┌────────────────────┐
                      │ Output Guard        │
                      └─────────┬──────────┘
                                v
                      ┌────────────────────┐
                      │ Final Response      │
                      └────────────────────┘
```

### Design choice: 在 LLM 前做 PII 脱敏,而不是只靠 LLM 自律

**Choice:** PII redaction 是 chatflow 的第一步,在本地执行。  
**Why:** 小安处理家暴场景,可能包含地址、姓名、电话、孩子姓名、单位、施暴者身份等高度敏感信息。安全边界必须由系统保证,不能依赖模型“不要泄露”。  
**MVP:** 只保留接口(`redact_pii` 透传桩),不做实际脱敏实现——POC 聚焦验证胶囊路由与 grounding,脱敏留作 prod 工作。pipeline 仍保留这一步的 seam。  
**Prod:** 规则 + NER + policy engine,并对每个字段标注敏感等级和保留策略。

### Design choice: 用 Responses API 做脱敏后的会话连续性,但不把控制权交给 OpenAI session

**Choice:** 对话连续性可以用 OpenAI Responses API 的 `previous_response_id`,但本地仍保存最小 control state。  
**Why:** 
- 不需要每轮传完整历史,降低 prompt 成本和上下文管理复杂度。
- 服务端会话里只有 redacted text,不会有 raw PII。
- 本地 control state 决定 safety override、active capsule、TTL、ground 注入,避免把产品逻辑隐藏在模型历史里。

**Rejected:** 完全 stateless chat completions。它简单,但第二轮“那我怎么说?”会丢失语境。  
**Rejected:** 完全依赖 Assistants/Threads 做状态。它会让业务控制、隐私策略、debug 和 vendor portability 变弱。

## 5. Data flow by stage

### 5.1 PII Redaction Gate

输入:

```text
raw_text = "他现在在上海市XX路XX号我家门口,电话是138...,他说要杀了我"
```

输出:

```json
{
  "redacted_text": "他现在在[ADDRESS]我家门口,电话是[PHONE],他说要杀了我",
  "pii_tags": [
    {"type": "ADDRESS", "placeholder": "[ADDRESS]"},
    {"type": "PHONE", "placeholder": "[PHONE]"}
  ],
  "pii_map": {
    "[ADDRESS]": "上海市XX路XX号",
    "[PHONE]": "138..."
  }
}
```

MVP:

- 本地 regex/rule based。
- 覆盖:
  - 手机号
  - 身份证
  - 微信号/QQ
  - 详细地址关键词
  - 门牌号
  - 姓名弱规则
  - 学校/单位关键词
  - 孩子姓名/施暴者姓名显式模式
- `pii_map` 只在进程内存保留。
- debug 默认不输出 `pii_map`。

Production:

- 增加中文 NER。
- 区分 PII 类型和敏感等级。
- 支持 policy:
  - never send
  - send placeholder only
  - send generalized value,如城市级别
  - allow with consent
- PII map 加密存储或完全不存储。
- 增加 redaction eval:漏脱敏率比误脱敏率更重要。

### Design choice: redaction 保留风险语义,删除身份定位信息

**Choice:** “他在我家门口拿刀”要保留“门口/拿刀/不安全”,但删除具体地址。  
**Why:** safety scan 需要风险信号;LLM 不需要知道真实地址才能给行动建议。  
**Failure mode:** 过度脱敏可能让模型不知道“家门口”这个风险位置。  
**Mitigation:** PII redactor 只替换具体地址,保留“门口、小区、单位、学校”等场景词。

## 6. Safety scan and crisis routing

MVP:

- 本地关键词 red flag。
- 不调用外部 LLM。
- 覆盖:
  - 正在/刚刚被打
  - 对方在门外/身边
  - 拿刀/杀/威胁
  - 被限制离开
  - 手机被监控
  - 自伤/自杀
  - 孩子危险
- 命中 red flag 时,直接进入 Crisis SOP,不继续 capsule retrieval。

Production:

- 多层 safety:
  1. 本地 hard rule,高精度 red flag。
  2. LLM/small model 判断 ambiguous risk。
  3. 输出 guard 二次检查。
- 支持不同 SOP:
  - immediate danger
  - self harm
  - child danger
  - surveillance/phone monitoring
  - medical emergency
- 引入 safety eval,重点看 false negative。

### Design choice: safety unclear 不直接进入 crisis SOP

**Choice:** 只有 red flag 才强制 crisis path。  
**Why:** 家暴用户经常表达“害怕/不知道怎么办”,如果系统每次都问“你现在安全吗”,会非常烦,并阻断有效帮助。  
**MVP behavior:** 普通回答里轻量加一句安全确认。  
**Prod behavior:** 根据风险分数调节语气和追问强度。

## 7. Capsule retrieval / routing

胶囊的路由输入:

```json
{
  "id": "n5p",
  "title": "人身安全保护令申请指南",
  "triggers": ["怎么让他不能靠近我", "..."],
  "use_when": ["用户想建立物理安全边界", "..."],
  "do_not_use_when": ["用户正在遭遇即时暴力 -> n3a", "..."]
}
```

MVP:

- LLM-as-router。
- 每轮把所有 capsule cards 放进路由 prompt。
- 在 LLM 路由前先跑 deterministic baseline rule:问候、感谢、测试系统、没有具体求助意图时返回 `baseline`,不激活任何胶囊。
- 在 LLM 路由前先跑 deterministic no-match rule:用户只是披露“被打/被家暴”,但没有明确说要报警、留证、申请保护令或离婚时,返回 `baseline`,交给 Main Agent Baseline SOP 自然承接,不直接跳 N5p。
- 返回:
  - `capsule_id`
  - `confidence`
  - `reason`
  - `should_continue_active_capsule`
- 代码层抽象为两个可替换接口:`CapsuleRouter` 与 `SupportAgent`。默认实现是 `LLMRouter` + `LLMSupportAgent`;`--offline` 只是在开发/测试时替换为 `HeuristicTestRouter` + `TemplateTestSupportAgent`,不改变 P0 流程节点。

Production:

- Hybrid retrieval:
  1. 本地规则处理 red flag 和强意图关键词。
  2. embedding recall 取 top K。
  3. LLM rerank 精筛。
  4. do_not_use_when 作为 hard/soft guard。
- 路由结果进入混淆矩阵。
- 对低 confidence 做澄清问题或 baseline support response。

### Design choice: 路由必须有 baseline/no-match 出口

**Choice:** `baseline` 是合法 route,不是错误状态。  
**Why:** 用户可能只是说“你好”、测试系统、感谢、或还没准备好讲具体情况。强行匹配胶囊会让系统过度干预,例如把“你好”匹配到 N3 求助胶囊。  
**MVP behavior:** baseline 是合法策略。在线模式下,baseline strategy + redacted input 仍交给 OpenAI 生成自然回复;离线模式才使用固定支持型回复。baseline 不解析 ground,不设置 `active_capsule_id`。  
**Prod behavior:** baseline 可以是 Main Agent Baseline SOP,必要时自然询问用户想从哪里开始。

### Design choice: “披露被打”不是“申请保护令”意图

**Choice:** “我老公昨天又打我了”这类暴力事件披露,如果没有明确行动意图,归入 `baseline`/no-match,由 Main Agent Baseline SOP 自然承接。  
**Why:** 这类输入的用户意图还不明确,直接给保护令流程跨度太大;但单独造一个伪胶囊会让实现偏离 P0 架构图。  
**MVP behavior:** baseline 是合法策略,不解析 ground,不设置 `active_capsule_id`。用户明确说“想报警/怎么报警”时转 N3a;明确说“能不能申请保护令”时转 N5p。  
**Prod behavior:** 如果后续确认“事件后分流”需要稳定内容资产,再把它做成正式 N0/NC 胶囊,而不是 chatflow 私有伪路由。

### Design choice: MVP 先 LLM-as-router,不上向量库

**Choice:** 12 个胶囊规模下,直接把 candidates 放进 prompt。  
**Why:** 简单、可解释、零基础设施,更快暴露 schema 和边界问题。  
**When to change:** 胶囊超过 50-100 个、路由成本变高、或混淆矩阵显示召回不足时,引入 embedding recall。

### Design choice: triggers 和 use_when 都保留

**Choice:** `triggers` 用于用户怎么说,`use_when` 用于什么时候适用。  
**Why:** 一个是 recall anchor,一个是 semantic precision filter。合并会让作者不知道是在写口语样例还是适用条件。  
**Prod benefit:** embedding 可以吃 triggers,LLM reranker 可以吃 use_when/do_not_use_when。

## 8. Capsule schema and R-A-G rendering

胶囊 v1 required fields:

- `id`
- `title`
- `tree_code`
- `status`
- `triggers`
- `use_when`
- `do_not_use_when`
- `recognize`
- `act`
- `ground`

MVP:

- Parser 容错读取旧格式。
- N5p 已作为 v1 样板。
- 旧胶囊仍可加载,但 report 会标出缺字段/legacy ground。
- Answer composer 使用:
  - recognize points
  - act steps
  - ground:summary + legal_basis + practice_basis(+可选 resolved citations)
  - safety note
  - limits

Production:

- 胶囊必须通过 schema lint 才能进入 runtime。
- `status=approved` 才能公开启用。
- 胶囊版本化:
  - schema_version
  - content_version
  - reviewer
  - approved_at
  - source_snapshot
- 支持 capsule boundary eval:
  - always confused -> merge/rewrite
  - never selected -> trigger/use_when 不足或胶囊无用
  - selected but answer poor -> R/A/G 内容问题

### Design choice: 胶囊按用户目的切,不是按法律章节切

**Choice:** N5p 是“用户想申请保护令/建立安全边界”,不是“反家暴法第 23-34 条”。  
**Why:** 用户不是按法律章节提问,而是按处境和目的提问。法律章节属于 ground,不属于路由主轴。  
**Validation:** 用 eval 混淆矩阵验证是否过宽/过细。

## 9. Ground resolver and legal wiki integration

Locator v1:

```text
node:<node_id>
node:<node_id>#<法律文件名>/第X条
law:<source_file>#第X条
synthesis:<name>
```

例:

```text
node:personal-safety-protection-order#中华人民共和国反家庭暴力法/第二十三条
```

MVP:

- `node:<node_id>` 返回 wiki node 的“原子结论”。
- `node:<node_id>#<法律文件名>/第X条`:
  1. 找到 `knowledge/wiki/nodes/<node_id>.md`
  2. 检查 node frontmatter 的 `source_refs`
  3. 要求存在 `knowledge/source/<法律文件名>.md#第X条`
  4. 从 source 文件抽取该条原文
- 断链进入 normalization report/debug warnings。

Production:

- locator lint 作为 CI。
- source 文件版本锁定。
- 支持 source snapshot export。
- 支持法条变更 diff。
- 回答中的引用必须来自 resolved ground,不能模型自己编。

### Design choice: locator 必须带法律文件名

**Choice:** 不允许 `node:<node_id>#第X条`,必须写 `node:<node_id>#<法律文件名>/第X条`。  
**Why:** 一个 node 可能引用多部法律,不同法律都有“第二十三条”。只写条号无法定位源文件。  
**Tradeoff:** locator 更长。  
**Why acceptable:** 零 alias 维护成本,parser 简单,断链清晰。以后如果维护 source alias 表,可以在不改变 runtime 语义的情况下加 syntactic sugar。

### Design choice: ground 分法律依据与实践依据,默认写文本、可选挂 locator

**Choice:** 胶囊 ground 分 `summary`(总述)+ `legal_basis`(法律依据文本)+ `practice_basis`(NGO/实务经验,可溯源)+ `limits`(边界)。`legal_basis` 可选挂 locator 指向 wiki/source 备查。  
**Why:** 不是所有依据都是法条——很多是 NGO/妇联/法院的实证数据与实务经验,强行塞进"法条 locator"会丢掉这部分依据,也不符合作者写作习惯。法律与实践分开,作者好写、用户好读。  
**Tradeoff:** `legal_basis` 文本可能与 wiki 法条漂移。  
**Mitigation:** 提供可选 `basis` locator,运行时解析权威原文与 `legal_basis` 文本互校;Production 用 citation checker 校验法条引用,用来源标注校验 `practice_basis`。

## 10. Conversation continuity and OpenAI API usage

### Target MVP v1 approach

使用 OpenAI Responses API:

```text
turn 1:
  input = redacted_user_text + selected_capsule + resolved_ground
  response_id = resp.id

turn 2:
  input = redacted_user_text + selected/continued_capsule + newly_resolved_ground
  previous_response_id = response_id
  response_id = resp.id
```

本地保存:

```yaml
conversation_control_state:
  previous_response_id: resp_xxx
  active_capsule_id: n5p
  active_capsule_confidence: 0.91
  ttl_turns: 3
  last_rendered_slots:
    - recognize
    - act.steps
    - ground.short
  safety_level: normal
```

不保存或默认不持久化:

```yaml
raw_user_input: no
pii_map: memory only
full_raw_conversation: no
```

Current MVP:

- PII redaction gate 为接口-only 桩(`redact_pii` 透传,无 tag);router/composer 仍走 `redacted_text` seam,便于 prod 接入真实脱敏。
- 已加入 `ConversationState`,保存 `previous_response_id`、`active_capsule_id`、TTL 和 safety level。
- 已加入 redacted recent-turn control context,供 stateless router 判断含糊追问是否延续上一轮。
- OpenAI runtime 优先使用 Responses API + `previous_response_id`;若 SDK 不支持 `client.responses`,回退到 Chat Completions。
- 在线模式下 baseline 也会调用 OpenAI 生成用户可见回答;离线模式才使用本地模板。red flag 直接进入 Crisis SOP,绕过 capsule router。
- raw input 不落盘;PII redaction 与 output guard 在 POC 为接口-only 桩(透传),debug 中 redaction 显示透传文本、无 PII tag;safety scan 为真实实现。

Production:

- 封装 `LLMClient` 接口,不要让业务逻辑直接依赖 OpenAI SDK。
- 可切换:
  - OpenAI Responses
  - 自托管模型
  - 其他 vendor
- session backend 可插拔:
  - dev: memory
  - staging/prod: encrypted store with TTL
- 对 vendor-side retained context 做策略:
  - 只发 redacted text
  - 高危/高敏场景可禁用 previous_response_id,改为本地摘要
  - 支持用户请求清除会话

### Design choice: 本地 state 是 control state,不是完整 memory

**Choice:** 本地只保存控制状态,不保存完整敏感历史。  
**Why:** 我们需要控制 safety override、active capsule、TTL、ground 注入;但不需要把 raw 对话持久化。  
**Key distinction:** “不用本地保存完整上下文”不等于“完全无本地状态”。Production 需要少量控制态来保证可解释和可测试。

## 11. Prompt composition

MVP prompt payload:

```json
{
  "redacted_user_message": "...",
  "capsule": {
    "id": "n5p",
    "recognize": "...",
    "act": "...",
    "ground": {
      "summary": "...",
      "legal_basis": ["《反家庭暴力法》第二十三条 ..."],
      "practice_basis": ["上海五年数据:核发率约 73% ..."],
      "limits": ["..."]
    }
  },
  "resolved_law_text": [
    {
      "locator": "...",
      "source_ref": "...",
      "text": "第二十三条 ..."
    }
  ],
  "safety_signal": "normal"
}
```

Production:

- Prompt 分层:
  - global system:小安语气、安全边界、禁止编法条、**AI 立场声明**（见下）
  - developer/system policy:只基于 resolved ground 说法律依据
  - dynamic capsule slots
  - dynamic resolved ground
  - redacted conversation context

**AI 立场声明（待补充）**：global system prompt 需要明确写入以下立场，作为所有回答的基础语调：
- 受害者遭受家暴不是她的错，是施暴者的责任
- 受害者留下来/不举报的原因是结构性困境（经济依赖、人身控制、社会压力），不是个人软弱
- 不使用任何暗示受害者应该早点离开或早点举报的语言
- 解释受害者行为时优先使用结构性语言，而非个人归因

> 上述立场来源于 `knowledge/wiki/nodes/gender-power-analysis.md`（已建立，Tier 5 F5 节点）。该节点内容**不经由 ground resolver / capsule locator 注入**，而是在 system prompt 撰写阶段由人工提炼并固化为立场声明。
- 生成后进入 output guard:
  - 是否泄露 PII placeholder map
  - 是否声称保证结果
  - 是否编造未提供法条
  - 是否忽略 red flag
  - 是否泄露内部路由/胶囊/系统思考语言

### Design choice: Ground 是 evidence,不是让模型自由检索

**Choice:** 模型只看到 resolver 提供的 ground,不让模型自己在回答时“想起”法条。  
**Why:** 法律回答需要可审计。模型自由引用会产生看似权威但不可追溯的幻觉。  
**Prod extension:** Citation checker 校验每个法条引用是否在 resolved_ground 中。

## 12. Output guard

MVP:

- 接口-only 桩:`guard_output` 原样返回回答(`passed=True`、无 warning),**不做实际输出检查实现**。
- POC 聚焦验证胶囊路由与 grounding;输出护栏留作 prod 工作。
- pipeline 仍保留 output guard 这一步的 seam(`GuardResult` 接口不变),便于 prod 接入真实实现。
- 真实 prod 行为预期(尚未实现)覆盖:
  - 是否出现“保证法院一定会...”
  - 是否出现 raw PII
  - 是否建议危险行为,如“你直接去找他谈”
  - red flag 时是否包含报警/避险优先
  - 是否出现 `胶囊`、`route`、`crisis_sop` 等内部实现词
- 失败时重新生成或附加修正提示。

Production:

- 两层 guard:
  1. Deterministic rules:PII、禁止词、citation presence。
  2. LLM judge:safety/legal boundary review。
- 对高风险回答强制降级:
  - 更短
  - 更安全
  - 更少法律结论
  - 更多现实求助路径

### Design choice: output guard 不替代上游安全

**Choice:** Safety scan 在前,output guard 在后。  
**Why:** 只靠输出后检查太晚;模型可能已经在错误上下文下生成。前置 safety 决定路径,后置 guard 防漏。

## 13. Storage, logging, and observability

MVP:

- 不落 raw input。
- CLI debug 显示:
  - safety level
  - route decision
  - selected capsule
  - resolved locators
  - ground warnings
  - capsule issues
- 生成:
  - `capsules.json`
  - `capsule-normalization-report.md`
  - `eval/smoke-report.md`

Production:

- 结构化日志:
  - session_id
  - turn_id
  - redacted_input_hash
  - safety_label
  - capsule_id
  - route_confidence
  - locator_ids
  - output_guard_result
  - latency/cost
- 不记录:
  - raw input
  - pii_map
  - full model output if policy forbids
- 指标:
  - route accuracy
  - ground resolution success rate
  - output guard failure rate
  - safety red flag rate
  - avg latency/cost per turn

### Design choice: debug 信息要可审计,但默认脱敏

**Choice:** debug 是产品和法律审核的必要工具,但只能包含 redacted data 和 ids。  
**Why:** 没有 debug 就无法验证胶囊是否有效;有 raw debug 又会制造隐私风险。

## 14. Evaluation strategy

MVP:

- JSONL 测试集:
  - message
  - expected_capsule_id
  - tags
- 评测:
  - route accuracy
  - selected ground errors
  - capsule issue count
- 当前 smoke eval 的目标是验证链路,不是证明产品可上线。

Production:

- 多维 eval:
  - Routing:top-1/top-3 accuracy,confusion matrix
  - Ground:locator resolution,引用覆盖,断链率
  - Safety:false negative,red flag handling
  - Legal:是否超出依据,是否过度承诺
  - UX:是否人话、是否温和、是否可执行
  - Privacy:PII leakage tests
- 样本来源:
  - synthetic adversarial
  - volunteer-written realistic prompts
  - lawyer-reviewed legal edge cases
  - red-team safety cases

### Design choice: 用 eval 回答胶囊边界问题

**Choice:** 不靠主观争论决定“这个胶囊该合并还是拆分”,用混淆矩阵和回答质量判断。  
**Why:** 胶囊边界本质是产品/语言行为问题,不是纯 schema 问题。  
**Example:** 如果 N6a 和 N5p 总是被一起召回,说明“分开后骚扰”和“保护令”需要更清晰的 routing 或合并策略。

## 15. Failure modes and mitigations

| Failure mode | Risk | MVP mitigation | Production mitigation |
|---|---|---|---|
| PII 漏脱敏 | 高 | regex + no raw logs | NER + redaction eval + policy engine |
| red flag 漏检 | 高 | hard keywords | multi-layer safety + red team |
| 胶囊路由错 | 中 | debug + eval | hybrid retrieval + confusion matrix |
| locator 断链 | 中 | normalization report | CI lint + source versioning |
| 模型编造法条 | 高 | prompt 禁止 + resolved ground | citation checker + output guard |
| 过度法律承诺 | 高 | limits 注入 | LLM/legal guard + lawyer-reviewed templates |
| 上下文污染 | 中 | redacted previous_response_id | session TTL + reset + topic shift detection |
| 成本/延迟高 | 中 | 12 capsule prompt | embedding recall + caching + model tiering |
| 胶囊内容多人写漂移 | 中 | schema v1 + report | review workflow + approved status |

## 16. Implementation plan

### MVP v1 tasks

1. Add `pii_redactor.py`. ✅
2. Change runtime input from raw text to redacted text after redaction gate. ✅
3. Add local `config.py` command for model/API key. ✅
4. Replace direct `chat.completions.create` with Responses API where available. ✅
5. Store `previous_response_id` and `active_capsule_id` in in-memory control state. ✅
6. Add `state.py` for control state, not full raw memory. ✅
7. Add basic output guard. ✅
8. Extend smoke eval with:
   - PII leakage cases
   - red flag override cases
   - route/ground regression cases

### Production track

1. Web server / API backend with session lifecycle and TTL.
2. Web/mobile client calls backend; client never talks directly to OpenAI.
3. Encrypted/redacted logging pipeline.
4. Capsule/wiki authoring workflow:
   - lint
   - review
   - approval
   - changelog
5. Eval CI.
6. Safety/legal review workflow.
7. Model/vendor abstraction.
8. Deployment and monitoring.

## 17. Open questions for review

1. Redaction policy:
   - 哪些信息永远不发给 LLM?
   - 城市级别/省份级别是否可以保留?
2. OpenAI session strategy:
   - MVP 是否直接切 Responses API + `previous_response_id`?
   - 高敏场景是否禁用 remote session continuity?
3. Capsule activation:
   - 低 confidence 时是问澄清问题,还是走 baseline support agent?
4. N5p 样板:
   - 当前 schema 是否足够让三位作者稳定复写?
5. Legal review:
   - 哪些胶囊必须先经过律师审才能进入 user-facing MVP?
6. Logging:
   - 本地 MVP 是否允许保存 redacted transcript 方便 review?
7. Crisis SOP:
   - MVP 是否要先接入固定 crisis response 模板,还是只做 safety-first 提醒?

## 18. Appendix: current repo state

当前已实现的 POC 文件:

- `tech/chatflow/capsule-schema.md`
- `knowledge/capsules/N5p 人身安全保护令申请指南.md`
- `tech/chatflow/poc/capsule_loader.py`
- `tech/chatflow/poc/config.py`
- `tech/chatflow/poc/settings.py`
- `tech/chatflow/poc/pii_redactor.py`
- `tech/chatflow/poc/state.py`
- `tech/chatflow/poc/ground.py`
- `tech/chatflow/poc/router.py`
- `tech/chatflow/poc/safety.py`
- `tech/chatflow/poc/output_guard.py`
- `tech/chatflow/poc/compose.py`
- `tech/chatflow/poc/app.py`
- `tech/chatflow/poc/eval_runner.py`

当前已知缺口:

- 除 N5p 外,多数胶囊仍是 legacy ground。
- 法律内容尚未专家终审。
- 还没有 production web server;当前仍是本地 CLI MVP。
- Responses API 分支已写入,但需要真实 OpenAI SDK/key 做 live verification。
