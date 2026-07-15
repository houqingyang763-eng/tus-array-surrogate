# TUS Array Surrogate Research Workspace

这是一个面向“3D 经颅超声阵列设计 / 声场预测 / 神经网络 surrogate model”的个人科研工作区。

仓库的目标不是堆积聊天笔记，而是让用户与 Codex 围绕同一套项目状态、证据规则和自主研究任务持续协作。

## 开始工作

用 Codex 打开本目录后，优先读取：

1. `AGENTS.md`：项目规则与边界；
2. `docs/project_concept_v4.md`：当前项目源构想；
3. `docs/memory.md`：最新状态、近期关注和时间线；
4. `docs/decisions.md`：稳定共识；
5. `docs/questions.md`：开放问题；
6. `docs/research_tasks.md`：已获用户批准的自主研究 mission。

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

第一版固定 MIDA、频率、阵元尺寸和幅值，优先研究阵元位置 / 法向变化，输出低分辨率大区域绝对 pmax field 与关键指标。

长期保留“单阵元大区域复声场预测 + 多阵元相干叠加”路线，用于支持阵元数量、阵列形状和相位策略变化。

## Git 使用方式

- `main`：用户认可的稳定状态；
- `codex/*` 或 Worktree：Codex 的后台研究与改造；
- commit：阶段性可回滚快照；
- 大型数据、外部仓库、模型权重和运行产物默认不进入 Git。

个人研究阶段不强制使用 Issue 或 Pull Request。

论文阅读默认不使用多 Agent：Codex 先给简洁导读，用户自己精读，再围绕具体问题讨论。
