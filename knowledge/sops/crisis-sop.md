---
id: crisis_sop
title: Crisis SOP
message: |
  我先把安全放在第一位：{safety_message}

  如果你现在能安全地做，请先离开对方能接触到你的位置，去有人的地方、邻居家、便利店、物业或警务室等更安全的地方。

  如果存在即时人身危险，请直接拨打 110；如果你担心自己会伤害自己，请立刻联系身边可信的人或当地危机干预热线。现在不用解释完整经过，先让现实中的人介入保护你。
ground:
  limits:
    - 不询问细节拖延即时安全动作。
    - 不要求用户先收集证据。
    - 不输出复杂法律流程。
---

# Crisis SOP

用于 safety scan 命中即时危险或自伤风险时的短路回复。该 SOP 绕过 capsule router 和 support agent，直接进入 output guard。

编辑 `message` 时保留 `{safety_message}` 占位符；运行时会替换为 safety scan 给出的具体安全提示。
