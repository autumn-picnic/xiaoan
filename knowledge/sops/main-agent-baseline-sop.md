---
id: baseline
title: Main Agent Baseline SOP
recognize:
  purpose: 在用户还没有表达具体问题时，先建立安全、低压力的入口。
  points:
    - 用户可以慢慢说，不需要一次讲完整。
    - 不要假设用户已经决定采取某个法律行动。
    - 可以轻轻提示可支持的方向，让用户选择从哪里开始。
act:
  purpose: 用一两个开放问题帮助用户进入对话。
  steps:
    - action: 接住问候
      detail: 用简短温和的话回应，不要输出长篇流程。
    - action: 给出入口
      detail: 提示用户可以说现在发生了什么，或选择判断家暴、报警、留证、保护令、是否离婚、分开后骚扰等方向。
ground:
  limits:
    - 不要给具体法律结论。
    - 不要假设用户已经遭遇某种暴力。
    - 不要提到胶囊、路由、系统内部判断。
issues: []
---

# Main Agent Baseline SOP

用于 router 返回 `baseline` 时的主 agent 兜底策略：问候、感谢、测试消息，或用户只披露受暴但尚未表达明确行动意图时，先自然承接，而不是强行跳到某个法律/行动胶囊。
