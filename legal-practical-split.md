# legal_basis / practice_basis 分离设计

**背景**：capsule 的 `ground` 字段需要区分法律依据（法条/司法解释）和实践依据（NGO 经验/实务流程），以便不同团队独立维护，并让 chatflow 在渲染时能按用户意图区分引用方式。

---

## 现状盘点

### capsule 层（knowledge/capsules/）

`capsules.json` 中每个 capsule 的 `ground` 字段**已经包含三个子字段**：

```json
"ground": {
  "legal_basis":    ["《反家庭暴力法》第X条（说明）", ...],
  "practice_basis": ["源众《自我保护手册》（2025版）", ...],
  "nodes":          ["personal-safety-protection-order", ...]
}
```

`legal_basis` / `practice_basis` 的数据分离**已经存在**。

当前 gap：`ground.py` 只读 `nodes` 字段，`legal_basis` / `practice_basis` 字符串列表目前未被 chatflow 使用。

### wiki nodes 层（knowledge/wiki/nodes/）

全部 21 个节点的 `type` 字段均为 `legal-node`，但 `node_kind` 已隐含两类：

| node_kind | 数量 | 实际性质 |
|---|---|---|
| definition / duty / remedy / condition / consequence / element | 15 | 法律性：法条直接推导 |
| procedure / support | 6 | 实务性：流程、资源、手册 |
| evidence | 2 | 视内容而定（见下方待确认项） |

---

## 三个独立问题（成本差很远）

### P0：分开维护约定（现在就能做）

数据分离已经存在，只需确立工作约定：

- **法律团队** → 只改各 capsule 文件的 `## legal_basis` 段落  
- **实务团队** → 只改各 capsule 文件的 `## practice_basis` 段落  
- 两者互不干扰，parser 已能分别解析

**改动量：0 行代码。**

---

### P1：wiki nodes 加 `type: procedure-node`（30 分钟，本周可做）

目的：在 schema 层明确"procedure-node 只能放进 `practice_basis`，不能放进 `legal_basis`"，防止作者写 locator 时归类错误。

需要改的文件（`node_kind: procedure` 或 `node_kind: support`）：

```
police-dv-handling-workflow.md   → procedure-node
injury-appraisal-procedure.md    → procedure-node
dv-risk-assessment.md            → procedure-node（待确认）
support-and-legal-aid.md         → procedure-node
temporary-shelter.md             → procedure-node
```

同时更新 `tech/chatflow/capsule-schema.md` §5，补充：

```
procedure-node:
  - 只能放在 practice_basis，不能放在 legal_basis
  - ground resolver 回传时加标注：⚠️ 实务参考来源
  - LLM 须用「实务中通常…」「根据 XX 手册…」等非法定性语言
  - 注明来源 updated 日期，提示核实时效
```

**改动量：5-6 个文件的 frontmatter 字段 + 一处文档更新。不影响运行时。**

---

### P2：chatflow 渲染区分（POC 评测后再做）

目前 `ground.py` 把所有 wiki 内容平铺给 LLM，LLM 自行决定引用哪部分。POC 阶段这已经够用。

评测后如需精细化，需要：

1. **ground.py**：`GroundItem` 增加 `basis_type: "legal" | "practice"` 字段，在 `resolve_node_context()` 里根据节点 `type` 打标
2. **render_policy.py**：根据用户意图调整 ground 渲染顺序

```python
# ground.py 改动示意
@dataclass
class GroundItem:
    ...
    basis_type: str = "legal"   # "legal" | "practice"

def resolve_node_context(node_id, note=""):
    node_type = extract_frontmatter_field(node_text, "type")  # legal-node / procedure-node
    basis_type = "practice" if node_type == "procedure-node" else "legal"
    ...
```

```python
# render_policy.py 改动示意（intent 分类）
LEGAL_INTENT_TERMS  = ["权利", "合法", "法律规定", "法条", "依据"]
PRACTICE_INTENT_TERMS = ["怎么做", "怎么说", "具体步骤", "流程", "材料"]
```

**改动量：ground.py + render_policy.py，2 个文件，约 40-60 行。**

---

## 优先级总表

| 优先级 | 动作 | 负责方 | 成本 | 前置条件 |
|---|---|---|---|---|
| P0 | 确立分工约定，法律/实务团队各守一个字段 | 全员 | 0 | 无 |
| P1 | wiki nodes 加 `type: procedure-node` | 开发 | 30 min | 确认 evidence 类节点归属 |
| P2 | ground.py + render_policy.py 差异化渲染 | 开发 | 1-2 天 | POC 评测完成后 |

---

## 待确认项

- `protection-order-evidence.md`（node_kind: evidence）：内容以法条为核还是以实务经验为核？决定归 `legal-node` 还是 `procedure-node`
- `dv-risk-assessment.md`（node_kind: evidence）：同上

---

_更新日期：2026-07-12_
