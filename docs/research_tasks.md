# Autonomous Research Missions

本文件只记录 1-3 个用户明确批准、可以交给 Codex 自主推进的任务合同，不保存普通 todo。

## 当前队列

当前没有活跃 mission。

| ID | Mission | 状态 | 说明 |
|---|---|---|---|
| R001 | 多 Agent 论文精读与 taste 校准试点 | stopped / workflow_replaced | 用户确认耗时和 token 成本过高，停止后续论文 |

状态含义：

```text
draft：尚未批准
approved：已批准，可以执行
running：正在执行
review：等待用户验收
accepted：用户已验收
blocked：达到合同停止条件
stopped：用户主动终止或工作流已被替代
```

---

## R001：多 Agent 论文精读试点（已停止）

状态：`stopped / workflow_replaced`

### 原目标

通过三个 Agent 对同一篇论文分别进行证据、技术和反方审查，再由用户批注形成 research taste。

### 实际结果

第一篇 FDE-UNet 论文已完成，但：

1. 耗时和 token 成本过高；
2. 相比单 Agent 没有产生显著额外价值；
3. 主报告与子报告大量重复；
4. 输出比论文更长，不符合用户真实阅读习惯。

### 用户决策

1. 放弃多 Agent 论文精读和三篇 taste 校准计划；
2. 第二、第三篇不按 R001 合同启动；
3. 论文精读主体仍是用户；
4. Codex 默认改为单 Agent 论文导读：结构地图、最多 5 个审计问题、理论分块和阅读路线。

### 保留材料

- 默认入口：`docs/agent_runs/R001/paper1_guide.md`；
- 旧的多 Agent 报告作为失败试点证据保留，但不得默认加载；
- 不继续要求用户填写 `paper1_user_review.md`，不生成 `taste_v0`。

### 依据

- 用户 2026-07-15 对第一篇试点的明确反馈和终止决定。

---

## 新 Mission 模板

```markdown
## Rxxx：标题

状态：draft
研究问题：
允许范围：
禁止事项：
证据标准：
交付物：
完成标准：
资源预算：
停止条件：
依据：
```
