# 场景胶囊 Schema v1（POC）

本文件定义场景胶囊的**统一机器格式**,目标是:三个人写出来的胶囊能被同一个 parser 可靠解析,
并能与法律 LLM-wiki(`knowledge/wiki/`)对接。

> 设计原则:**对输入宽容,对输出严格**。parser 会尽力容错解析现有 12 个乱格式草稿,
> 但所有胶囊最终都要收敛到本 schema。本文件描述的是"目标格式",不是现状。

---

## 0. 一句话回答三个争议

| 争议 | v1 决定 |
|---|---|
| trigger vs use_when 是否冗余 | **都保留,分工不同**:`triggers`=用户可能怎么*说*(召回);`use_when`=这个胶囊何时*适用*(精筛)。见 §3。 |
| ground 写多细 / 怎么引用法律 | **分层写依据**:`summary`(一句话总体依据)+`legal_basis`(法律依据)+`practice_basis`(实践/NGO 经验依据)+`limits`(边界)。法条与实务经验分开,因为不是所有依据都是法条。`legal_basis` 可选挂 locator 备查。见 §5。 |
| 胶囊之间怎么互引 | 用 `id`(机器标识)互引,**不用中文名、不用树码混指**。见 §1、§6。 |

---

## 1. 文件格式与命名

- 一个胶囊 = 一个文件,**全部结构化字段写在 YAML frontmatter**(顶部 `---` 之间)。
- frontmatter 之下的 markdown 正文**可选**,只作人类备注,parser 忽略。
  - 原因:frontmatter 是单一、无歧义的解析入口,避免"有的用围栏、有的裸写、有的用标题分节"导致抽不全。
- 文件名建议:`<tree_code> <中文名>.md`(沿用现状,便于 Obsidian 浏览)。**文件名不参与解析**,只认 frontmatter 里的 `id`。

---

## 2. 顶层字段总览(required / optional)

```yaml
# ===== 必填(required)=====
id:              # 机器唯一标识,稳定不变。小写,树码即 id。如 n5p / n3a / k1 / n4a1
title:           # 中文显示名。如 "人身安全保护令申请指南"
tree_code:       # 行动树位置码。如 N5p / N3a / K1（大小写保留,供人看）
status:          # draft | review | approved（只有 approved 才正式加载;POC 阶段全是 draft）
triggers:        # list[str] 用户可能怎么说(召回锚点)。见 §3
use_when:        # list[str] 适用语义条件(精筛)。见 §3
do_not_use_when: # list[str] 负向护栏(安全/路由排除)。见 §3
recognize:       # 认知槽 R。见 §4
act:             # 行动槽 A。见 §4
ground:          # 依据槽 G:summary + legal_basis + practice_basis + limits。见 §5

# ===== 选填(optional)=====
scripts:         # list 话术模板。见 §4
safety_note:     # list[str] 安全提示
routing:         # 胶囊互引(用 id)。见 §6
source:          # list 来源元数据(人审用)
ai_stance:       # 该胶囊的特殊立场约束(如 N5d "不替用户决定离婚")
review:          # 审核元数据(reviewer / approved_by / comments)
```

> 现状字段迁移:`fits_any`→并入 `use_when`(N6a 把二者写成一字不差);
> `position_in_tree`→`tree_code`;`capsule_name`→`title`;`【挂起】` 占位字段一律删除。

---

## 3. triggers / use_when / do_not_use_when(§6 Q1 的答案)

三者**职责不同,都要保留**,对应检索两阶段 + 一道护栏:

| 字段 | 回答的问题 | 在 chatflow 里干什么 | 写法 |
|---|---|---|---|
| `triggers` | 用户可能**怎么说** | 召回:LLM-router 的示例话术;以后 embedding 锚点 | 第一人称口语原句 |
| `use_when` | 这个胶囊**何时适用** | 精筛:多个胶囊都召回时,语义判定该不该用 | 抽象适用条件 |
| `do_not_use_when` | 什么时候**绝不能用** | 护栏:命中则排除本胶囊(安全优先/路由别处) | 排除条件,可带→去向 |

写作约束:
- `triggers` 写**用户的话**,不要写"用户想了解 X"这种第三人称(那是 use_when)。
- `use_when` 写**条件**,不要把法条结论塞进来。
- `do_not_use_when` 优先写**安全红线**;能写明转去哪个胶囊 id 最好。

---

## 4. recognize / act / scripts(R 和 A 两槽)

消除现状"有时扁平字符串、有时 {theme,points}、有时 {key_point,message}"的形状不一,v1 统一如下,parser 对旧格式做归一化。

### recognize(认知槽)
```yaml
recognize:
  purpose: "一句话:这个槽要帮用户建立什么认知"
  points:                 # list,每条一个认知要点
    - "保护令不需要先离婚就能申请"
    - "精神暴力同样受保护,哪怕没有外伤"
```
分组(像 N3/N5d 的 theme)用可选的 `groups`;`points` 与 `groups` 二选一,parser 优先读 `groups`:
```yaml
recognize:
  purpose: "..."
  groups:
    - theme: "说出来的意义"
      points: ["...", "..."]
```

### act(行动槽)
```yaml
act:
  purpose: "一句话:这个槽要把什么拆成可操作步骤"
  steps:                  # list,每条是字符串 或 {action, detail}
    - action: "确认管辖法院"
      detail: "申请人/被申请人居住地或家暴发生地的基层法院,全程免费"
    - "收集证据:能有多少算多少,无需完美"
```

### scripts(可选,话术模板)
```yaml
scripts:
  - scene: "到法院立案窗口"
    say: "我遭受了家庭暴力,我想申请人身安全保护令,请问在哪里办理?"
  - "我不太会写申请书,你能帮我一起写吗?"
```

---

## 5. ground(依据槽):summary + legal_basis + practice_basis + limits(§6 Q2 的答案)

**核心规则:ground 把"为什么这么建议"讲清楚,并按来源区分依据。**
不是所有依据都是法条——有的来自 NGO/妇联/法院的实务经验与实证数据,所以**法律依据和实践依据分开写**。

```yaml
ground:
  summary: >                # 一句话总体依据:为什么这么建议、依据来自哪里、有什么前提
    提供法律依据与实务参考,帮助用户对结果形成合理预期。
  legal_basis:              # list[str] 法律依据:法律/法规/司法解释条文(可带括号说明)
    - "《反家庭暴力法》第二十三条(申请条件:遭受家暴或面临现实危险)"
    - "《反家庭暴力法》第三十四条(违反保护令的法律后果)"
  practice_basis:           # list[str] 实践/经验依据:NGO/妇联/法院实证数据、实务经验(非法条)
    - "上海五年数据(2016—2020):提交两项及以上证据,核发率约 73%(来源:为平《上海市人身安全保护令实施情况研究报告》)"
  limits:                   # list[str] 明确 AI 不能做什么
    - "不能保证法院一定签发(证明标准为'较大可能性')"
```

字段说明:
- `summary`:对依据的一句话总述,给用户"这建议靠不靠谱"的总体判断。
- `legal_basis`(法律依据):写**法律/法规/司法解释**条文,格式建议"《法名》第X条(一句话说明)"。
- `practice_basis`(实践依据):写**不是法条**的依据——NGO/妇联/法院的实证数据、实务经验、地方做法,**必须可溯源**(写明数据来源或出处)。
- `limits`(边界):AI 明确不能承诺/不能做的事,管理用户预期。
- 校验:ground 至少要有 `summary` / `legal_basis` / `practice_basis` 之一,否则报"缺 ground"。

### (可选)给 legal_basis 挂 locator 备查

为可审计、避免法条原文抄错,`legal_basis` 条目**可以**额外挂一个 locator(写在 `basis` 列表里),指向 wiki 节点或 source 法条;
运行时由 chatflow 解析 locator 拉权威原文,与 `legal_basis` 文本互相校对。**这是可选增强,不是必填**——不写 locator 时 `legal_basis` 文本即依据。

```yaml
ground:
  summary: "……"
  legal_basis:
    - "《反家庭暴力法》第二十三条(申请条件)"
  basis:                    # 可选:legal_basis 的机读 locator(供校对/取原文)
    - locator: "node:personal-safety-protection-order#中华人民共和国反家庭暴力法/第二十三条"
      note: "申请条件"
```

locator 语法(仅在使用可选 `basis` 时需要):

| 形式 | 含义 | 解析结果 |
|---|---|---|
| `node:<node_id>` | 一个 wiki 节点 | 该节点"原子结论"段 |
| `node:<node_id>#<法律文件名>/第X条` | 节点 + 指定某部法的某条 | 拼成 `source/<法律文件名>.md#第X条`,必须命中该节点 `source_refs` 里的某一条,再取 source 原文 |
| `law:<source_file>#第X条` | 直连 source 法条(逃生通道) | source 文件里该条原文 |
| `synthesis:<name>` | syntheses/ 下的综述 | 该综述全文 |

约定:
- **优先用 `node:`**,让 wiki 当中间层(可复用、单点维护)。
- 条文锚点必须带「哪部法」:写成 `#<法律文件名>/第X条`,因为一个节点常引用多部法律,只写 `#第X条` 无法定位源文件,会歧义。
- 校验:把 `<法律文件名>/第X条` 拼成 `knowledge/source/<法律文件名>.md#第X条`,必须等于该节点 `source_refs` 里的某一条;否则报断链。

### 现有 wiki 节点 id(locator 目标)
```
domestic-violence-definition      public-security-response-duty
personal-safety-protection-order  warning-letter
protection-order-element-danger   protection-order-evidence
injury-appraisal-procedure        dv-risk-assessment
police-dv-handling-workflow       support-and-legal-aid
mandatory-reporting               guardianship-revocation
temporary-shelter                 child-witness-victim
special-protection-groups         divorce-and-dv
liability-ladder
```
(syntheses: `local-regulations-comparison`、`protection-order-six-part-checklist`)

#### 学术层节点（Tier 5，concept-depth）

以下节点可作为 locator 目标，但**只能放在 `practice_basis`，不能放在 `legal_basis`**。
ground resolver 回传时会包含节点顶部的 `⚠️ 学术来源` 警告，LLM 须使用「学界通说认为」等非约束性语言。

```
psychological-violence-concept    economic-control-concept
dv-scope-extension                dv-law-legislative-history
coercive-control-comparative      international-human-rights-standards
judicial-recognition-gap          victim-agency-barriers
state-intervention-limits         constitutional-protection-obligation
```

以上 F1–F4 节点均已建立。F5 `gender-power-analysis` 仅作为 system prompt 的 AI 隐性认知底色，**不得**作为 locator 目标，也不得进入 `ground`、`legal_basis` 或 `practice_basis`。

---

## 6. routing(胶囊互引,§6 Q3 相关)

```yaml
routing:
  exit_to:
    - to: n4              # 必须是某个胶囊的 id
      when: "用户证据不足 / 不知如何举证"
    - to: n5p
      when: "用户面临即时危险 / 担心诉讼期间被报复"
  related: [n3a, n5d]     # 可选,平级相关胶囊
```

规则:
- `to` / `related` 一律填 **胶囊 id**,**禁止**填中文名("报警胶囊")或裸树码混指。
- parser 校验所有路由目标 id 是否存在;指向不存在的胶囊 → "悬空路由"。
- 当前只有 12 个胶囊,N1/N2/N6/NC/危机干预/K3 等树枝未实现 → 这些目标暂时悬空属预期,报告会列"待建胶囊"清单。

---

## 7. 胶囊边界原则(§6 Q3:按场景还是按用户目的)

- **主切法 = 用户目的/意图**(贴近用户怎么问),不是按法条章节或暴力阶段。
- 同一目的下的不同**场景**作为胶囊**内部变体**(用 triggers 不同条目 + act.steps 覆盖),不拆成一堆过细小胶囊。
- 哪些该合并/拆分,**用 POC 的检索混淆矩阵实证**(总被一起召回 = 边界不清),不拍脑袋。

---

## 8. 标准样板:N5p(人身安全保护令)

下面是按 v1 写出的完整示例,作为三人对齐的参照模板。
(ground 分 summary / legal_basis / practice_basis / limits;legal_basis 可选挂 locator 备查。)

```yaml
---
id: n5p
title: 人身安全保护令申请指南
tree_code: N5p
status: draft
triggers:
  - "他老来找我,我能不能申请保护令?"
  - "怎么让法院禁止他靠近我?"
  - "我还没离婚能申请人身保护令吗?"
  - "申请保护令需要什么材料?"
use_when:
  - 用户想用法律手段阻止加害人接近/骚扰/继续施暴
  - 用户面临持续或潜在的人身危险,需要事前防护
do_not_use_when:
  - 用户正处于即时暴力/生命危险中 → 先走 nc(危机求助)/报警
  - 用户只想了解如何报警 → n3a
recognize:
  purpose: 让用户知道保护令是独立、免费、不必先离婚的事前保护手段
  points:
    - 申请保护令不需要先起诉离婚,可单独申请
    - 精神威胁、骚扰、跟踪也可作为申请依据,不限于身体伤害
    - 证明标准是"较大可能性",低于刑事的"排除合理怀疑"
act:
  purpose: 把申请流程拆成可操作步骤
  steps:
    - action: 确定管辖法院
      detail: 申请人/被申请人居住地或家暴发生地基层法院,申请免费
    - action: 准备申请书与证据
      detail: 写明申请人、被申请人、具体请求和事实理由;证据能收多少收多少
    - action: 提交申请
      detail: 情况紧急可口头申请;法院一般 72 小时内、紧急 24 小时内作出裁定
ground:
  purpose: 说明法律依据与预期边界
  basis:
    - locator: "node:personal-safety-protection-order#中华人民共和国反家庭暴力法/第二十三条"
      note: 当事人可向法院申请人身安全保护令
    - locator: "node:personal-safety-protection-order#中华人民共和国反家庭暴力法/第二十八条"
      note: 法院作出裁定的时限
    - locator: "node:liability-ladder#中华人民共和国反家庭暴力法/第三十四条"
      note: 违反保护令的法律后果
  limits:
    - 不能保证法院必然签发,取决于证据与"较大可能性"判断
    - AI 不能代写具有法律效力的文书,只能协助梳理
routing:
  exit_to:
    - to: n5d
      when: 用户在咨询中表露想离婚/对婚姻去留犹豫
    - to: n3a
      when: 用户当前需要的是报警而非保护令
  related: [n6a]
safety_note:
  - 若用户描述即时危险,优先引导报警/危机求助,不要停留在流程讲解
---
```

---

## 9. parser 合约(Phase 1 capsule_loader 依据本节实现)

输入:`knowledge/capsules/*.md`。对每个文件:

1. **只解析 frontmatter**(首个 `---`…`---`)。无 frontmatter → 报"无法解析",跳过。
2. **容错归一化**:
   - `fits_any`→`use_when`;`position_in_tree`→`tree_code`;`capsule_name`→`title`。
   - recognize/act 的扁平 list 或 {theme,points}/{key_point,message} → 统一成 §4 结构。
   - 删除值为 `【挂起】`/`暂缺`/模板说明文字的字段。
3. **校验**(进规范化报告,不中断):
   - required 字段缺失。
   - 每个 ground.basis.locator 能否解析(节点存在 + 条文可匹配)→ 断链清单。
   - 每个 routing 目标 id 是否存在 → 悬空路由清单 + 待建胶囊清单。
   - `id` 是否全局唯一。
4. **输出**:`capsules.json`(供 chatflow)+ `capsule-normalization-report.md`(给三位作者的回填清单)。

> 本合约对应计划 Phase 1。Phase 3 的混淆矩阵结果可能回头修订本 schema(Phase 4)。

---

_版本: schema v1 (POC)。后续依 POC 评测结果迭代。_
