## P0 架构图

```
User Input
    |
    v
[PII Tagging / Redaction Gate]
    |
    v
[Safety Scan]
    |
    +-- Red Flag Detected
    |       |
    |       v
    |   [Crisis SOP]
    |       |
    |       v
    |   [Crisis Response]
    |
    +-- No Red Flag
            |
            v
    [Capsule Retrieval]
            |
    +-------+----------------------+
    |                              |
    v                              v
[Capsule Match or                [No Match]
 Active Capsule Continue]           |
    |                              v
    v                      [Main Agent Baseline SOP]
[Capsule Render Policy]             |
    |                              |
    v                              |
[Main Support Agent                 |
 + selected slots]                  |
    |                              |
    +--------------+---------------+
                   |
                   v
            [Output Guard]
                   |
                   v
            Final Response
```

## 1.信息脱敏

A. PII Tagging

先识别：
```
姓名
电话
身份证
详细地址
单位
学校
具体门牌号
微信号
车牌
孩子姓名
施暴者姓名
```
然后打标签：
```
[NAME]
[PHONE]
[ADDRESS]
[ID_NUMBER]
```
B. Safety Scan 用什么文本？

如果 Safety Scan 是本地规则 / 自己后端模型

可以用原文做内存内扫描，但不要落日志。

如果 Safety Scan 调外部 LLM/API

应该用 redacted text：
```
原文：他现在在我家门口，地址是上海市XX路XX号，他拿着刀。
脱敏后：他现在在我家门口，[ADDRESS]，他拿着刀。
```
这样仍然保留风险信号：
```
在门口
拿着刀
威胁
不安全
```
但不暴露具体地址。

日志里存什么？

只存脱敏版。
raw input: 不落库
redacted input: 可落日志
safety labels: 可落日志
capsule_id: 可落日志
route: 可落日志

## 2.安全确认
Safety unclear 不应该一律走 Crisis SOP
如果 safety unclear 就直接走 Crisis SOP，会导致产品很烦：系统反复问“你现在安全吗？你现在安全吗？你现在安全吗？”，用户体验会崩。

我建议 P0 不要设一个独立的 safety_unclear → crisis 路径，而是这样：

P0 安全规则
默认假设用户当前可继续对话。
只有检测到 red flag 时，才进入 safety-first / crisis 分支。
Red flag 包括
```
正在被打
刚刚被打
对方在门外 / 身边 / 正在威胁
用户说不方便说话
手机被监控
被限制离开
有刀 / 杀 / 自杀 / 孩子危险
严重受伤 / 流血
```
如果只是信息不足
例如：
```
我不知道怎么办
我好害怕
他又这样了
```
不要直接 Crisis SOP。

可以在正常回复里轻轻带一个安全确认（/或者在聊天的最开始强制安全确认）：

我先陪你慢一点。你现在方便继续打字吗？如果你现在人是安全的，我们可以一起把下一步拆小。

这不是 Crisis 分支，只是 Main Agent 的安全感知表达。

## 3.Capsule match 应该有跨轮次延续性

有，而且必须有。不然用户第二轮说“那我具体怎么说？”系统会不知道“那”指什么。

P0 最小状态可以这样存：
```
conversation_state:
  active_capsule_id: police_pushback_family_matter
  active_capsule_confidence: high
  last_rendered_slots:
    - recognize
    - act.default_steps
    - ground.short
  last_user_intent: ask_what_to_do
  ttl_turns: 3
```
每轮处理逻辑

1. 先做 Safety Scan
   高危永远覆盖 active capsule。

2. 如果用户明显是在追问上一轮：
   继续使用 active capsule。

3. 如果用户明显换话题：
   重新检索 capsule。

4. 如果不确定：
   让 Main Agent 自然承接，不强行切换。

什么时候延续 active capsule？

延续条件：
```
用户说“那我怎么说？”
用户说“这个以后有用吗？”
用户说“凭什么他们要管？”
用户说“如果他们还是不处理呢？”
```
这些都应该继续用上一轮胶囊。

什么时候切换？

切换条件：
```
用户从“警察不管”转到“我想申请保护令”
用户从“报警记录”转到“孩子抚养权”
用户突然说“他现在在门外”
```
最后一个不是切换胶囊，而是直接被 Safety Scan 覆盖。
