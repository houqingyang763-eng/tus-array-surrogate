# TUS Array Surrogate Research Workspace

这是一个面向“3D 经颅超声阵列设计 / 声场预测 / 神经网络 surrogate model”的个人科研工作区。

仓库的目标不是堆积聊天笔记，而是让用户与 Codex 围绕同一套项目状态、证据规则和自主研究任务持续协作。

## 开始工作

用 Codex 打开本目录后，优先读取：

1. `AGENTS.md`：项目规则与边界；
2. `docs/project_design_handoff_v1.md`：2026-07-26 面向 Codex 的阶段性项目设计快照；
3. `docs/project_concept_v7.md`：当前项目源构想；
4. `docs/memory.md`：最新状态、近期关注和时间线；
5. `docs/decisions.md`：稳定共识；
6. `docs/questions.md`：开放问题；
7. `docs/research_tasks.md`：已获用户批准的自主研究 mission。

## 四层工作流

```text
稳定知识层
project_concept / memory / decisions / ideas / questions
        ↓
任务合同层
research_tasks.md 中 1-3 个用户批准的 Research Mission
        ↓
执行与证据层
主 Agent + 可选子 Agent + Worktree，产物进入 docs/agent_runs/
        ↓
人工验收层
用户学习、批注、批准后，再更新核心记忆
```

## 当前技术主线

第一阶段固定 MIDA、频率和激励幅值，网络介质输入固定为单通道三维声速场，优先研究理想方向性点源的位置 / 法向变化。target focus 不进入单源网络，只用于下游相位 / 延迟、阵列组合和评价。主 U-Net 预测逐样本归一化的相对复声场 `q_Re/q_Im`，A4 预测脑内绝对峰值尺度，二者共同重建指定三维域内的单阵元绝对复声场。

当前核心路线是“相对复场预测 + 独立绝对尺度预测 + 单阵元绝对复场重建 + 网络外多阵元相干叠加”。三维离散 Helmholtz 残差仍是全场预测的核心物理约束候选，但训练时必须先把相对预测恢复到绝对量纲。

## Git 使用方式

- `main`：用户认可的稳定状态；
- `codex/*` 或 Worktree：Codex 的后台研究与改造；
- commit：阶段性可回滚快照；
- 大型数据、外部仓库、模型权重和运行产物默认不进入 Git。

个人研究阶段不强制使用 Issue 或 Pull Request。

论文阅读默认不使用多 Agent：Codex 先给简洁导读，用户自己精读，再围绕具体问题讨论。
