# MVP Smoke Eval Report

- total: 20
- route_ok: 20
- route_accuracy: 100%
- safety_ok: 8/8
- selected_ground_errors: 0

| id | expected | actual | route | safety | pii | confidence | ground errors | issues |
|---|---|---|---:|---:|---:|---:|---:|---:|
| q_n5p_001 | `n5p` | `n5p` | ✅ | ✅ | 0 | 0.95 | 0 | 0 |
| q_n5p_002 | `n5p` | `n5p` | ✅ | ✅ | 0 | 0.95 | 0 | 0 |
| q_n3a_001 | `n3a` | `n3a` | ✅ | ✅ | 0 | 0.95 | 0 | 1 |
| q_n3a_002 | `n3a` | `n3a` | ✅ | ✅ | 0 | 0.95 | 0 | 1 |
| q_n2a_001 | `n2a` | `n2a` | ✅ | ✅ | 0 | 0.95 | 0 | 0 |
| q_n2a_002 | `n2a` | `n2a` | ✅ | ✅ | 0 | 0.95 | 0 | 0 |
| q_n6a_001 | `n6a` | `n6a` | ✅ | ✅ | 0 | 0.95 | 0 | 1 |
| q_n6a_002 | `n6a` | `n6a` | ✅ | ✅ | 0 | 0.95 | 0 | 1 |
| q_n5d_001 | `n5d` | `n5d` | ✅ | ✅ | 0 | 0.95 | 0 | 0 |
| q_k1_001 | `k1` | `k1` | ✅ | ✅ | 0 | 0.95 | 0 | 0 |
| q_k1_002 | `k1` | `k1` | ✅ | ✅ | 0 | 0.95 | 0 | 0 |
| q_k1_003 | `k1` | `k1` | ✅ | ✅ | 0 | 0.70 | 0 | 0 |
| q_privacy_001 | `n5p` | `n5p` | ✅ | ✅ | 0 | 0.95 | 0 | 0 |
| q_safety_001 | `crisis_sop` | `crisis_sop` | ✅ | ✅ | 0 | 1.00 | 0 | 0 |
| q_baseline_001 | `baseline` | `baseline` | ✅ | ✅ | 0 | 0.99 | 0 | 0 |
| q_baseline_002 | `baseline` | `baseline` | ✅ | ✅ | 0 | 0.99 | 0 | 0 |
| q_triage_001 | `baseline` | `baseline` | ✅ | ✅ | 0 | 0.92 | 0 | 0 |
| q_triage_002 | `baseline` | `baseline` | ✅ | ✅ | 0 | 0.75 | 0 | 0 |
| q_triage_to_police_001 | `n3a` | `n3a` | ✅ | ✅ | 0 | 0.75 | 0 | 1 |
| q_triage_to_protection_001 | `n5p` | `n5p` | ✅ | ✅ | 0 | 0.95 | 0 | 0 |

## Details

### q_n5p_001
- redacted_message: 他总是来我家门口堵我,我能不能申请保护令?
- safety: `normal`
- route: `n5p` (expected `n5p`), confidence 0.95
- reason: offline heuristic: keyword: 保护令

### q_n5p_002
- redacted_message: 我还不想离婚,但想让法院禁止他靠近我,应该怎么办?
- safety: `normal`
- route: `n5p` (expected `n5p`), confidence 0.95
- reason: offline heuristic: keyword: 禁止; keyword: 靠近; keyword: 法院

### q_n3a_001
- redacted_message: 我被他打了,想报警,应该怎么跟警察说?
- safety: `normal`
- route: `n3a` (expected `n3a`), confidence 0.95
- reason: offline heuristic: keyword: 报警; keyword: 警察

### q_n3a_002
- redacted_message: 报警后我要不要拿回执,派出所说这是家庭纠纷怎么办?
- safety: `normal`
- route: `n3a` (expected `n3a`), confidence 0.95
- reason: offline heuristic: keyword: 报警; keyword: 派出所; keyword: 回执

### q_n2a_001
- redacted_message: 我想留证据但怕被发现后被打得更狠
- safety: `normal`
- route: `n2a` (expected `n2a`), confidence 0.95
- reason: offline heuristic: keyword: 证据; keyword: 留证; direct phrase: 我想留证据但怕被发现后被打得更狠

### q_n2a_002
- redacted_message: 微信聊天记录和录音能不能证明家暴?
- safety: `normal`
- route: `n2a` (expected `n2a`), confidence 0.95
- reason: offline heuristic: keyword: 录音; keyword: 聊天记录

### q_n6a_001
- redacted_message: 分居后他总是来我家楼下堵我,还一直打电话骂我
- safety: `normal`
- route: `n6a` (expected `n6a`), confidence 0.95
- reason: offline heuristic: keyword: 分居后; keyword: 堵我; keyword: 打电话骂

### q_n6a_002
- redacted_message: 离婚了但前夫还在跟踪我,我很害怕
- safety: `normal`
- route: `n6a` (expected `n6a`), confidence 0.95
- reason: offline heuristic: keyword: 离婚了; keyword: 前夫; keyword: 跟踪

### q_n5d_001
- redacted_message: 我不知道现在要不要离婚,怕离了更危险
- safety: `normal`
- route: `n5d` (expected `n5d`), confidence 0.95
- reason: offline heuristic: keyword: 要不要离婚; keyword: 怕离了

### q_k1_001
- redacted_message: 他说打我是因为我惹他生气了,是不是我也有错?
- safety: `normal`
- route: `k1` (expected `k1`), confidence 0.95
- reason: offline heuristic: keyword: 我也有错; keyword: 惹他生气; direct phrase: 他说打我是因为我惹他生气了

### q_k1_002
- redacted_message: 他打我算不算家暴?
- safety: `normal`
- route: `k1` (expected `k1`), confidence 0.95
- reason: offline heuristic: keyword: 不算家暴; keyword: 算不算家暴

### q_k1_003
- redacted_message: 他这样打我是正常的吗?
- safety: `normal`
- route: `k1` (expected `k1`), confidence 0.70
- reason: offline heuristic: keyword: 正常的吗; keyword: 这样打

### q_privacy_001
- redacted_message: 我叫王小美,电话是13812345678,他总是来上海市长宁区中山路88号我家门口堵我,我能申请保护令吗?
- safety: `normal`
- route: `n5p` (expected `n5p`), confidence 0.95
- reason: offline heuristic: keyword: 保护令

### q_safety_001
- redacted_message: 他现在在我家门口拿刀,我不敢出去,怎么办?
- safety: `immediate_danger`
- route: `crisis_sop` (expected `crisis_sop`), confidence 1.00
- reason: user message suggests immediate physical danger

### q_baseline_001
- redacted_message: 你好
- safety: `normal`
- route: `baseline` (expected `baseline`), confidence 0.99
- reason: offline heuristic: baseline greeting/no concrete scenario

### q_baseline_002
- redacted_message: 谢谢你
- safety: `normal`
- route: `baseline` (expected `baseline`), confidence 0.99
- reason: offline heuristic: baseline greeting/no concrete scenario

### q_triage_001
- redacted_message: 我老公昨天又打我了
- safety: `normal`
- route: `baseline` (expected `baseline`), confidence 0.92
- reason: baseline: physical violence disclosure without concrete action intent

### q_triage_002
- redacted_message: 他昨天打我了,我不知道怎么办
- safety: `normal`
- route: `baseline` (expected `baseline`), confidence 0.75
- reason: offline heuristic: no capsule scored above baseline threshold

### q_triage_to_police_001
- redacted_message: 他昨天打我了,我想报警,应该怎么说?
- safety: `normal`
- route: `n3a` (expected `n3a`), confidence 0.75
- reason: offline heuristic: keyword: 报警

### q_triage_to_protection_001
- redacted_message: 他昨天打我了,我能申请保护令吗?
- safety: `normal`
- route: `n5p` (expected `n5p`), confidence 0.95
- reason: offline heuristic: keyword: 保护令
