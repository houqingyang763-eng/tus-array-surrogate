# TUS Array Surrogate Starter Repo

这是一个用于“3D 经颅超声阵列设计 / 声场预测 / 神经网络 surrogate model”科研训练的本地 Codex app 项目模板。

## 推荐使用方式

1. 解压本项目文件夹；
2. 用 Codex app 打开 `tus-array-surrogate/`；
3. 先阅读 `AGENTS.md`；
4. 在 Codex app 中尝试输入：

```text
阅读 AGENTS.md、docs/project_concept_v2.md、docs/decisions.md、docs/questions.md。请总结当前项目状态，并告诉我下一步应该先完善哪个文件。不要改文件。
```

## 核心文件

- `AGENTS.md`：给 Codex 的总规则；
- `docs/project_concept_v1.md`：历史构想；
- `docs/project_concept_v2.md`：当前项目源构想；
- `docs/decisions.md`：稳定共识；
- `docs/ideas.md`：尚未验证但值得保留的科研想法；
- `docs/questions.md`：待问 / 待查 / 待验证问题；
- `docs/research_tasks.md`：明确要执行且有产出物的调研任务；
- `docs/memory_workflow.md`：自然语言科研输入的归档工作流；
- `docs/literature/`：论文阅读材料；
- `skills/`：可复用任务工作流。

## 当前重点

组内新需求要求输出整个脑内声场，因此 v2 将 whole-brain intracranial pmax field / 3D time-maximum pressure field 设为主输出之一。

同时，保留“单阵元复声场预测 + 多阵元相干叠加”路线，用于支持阵列位置、阵列形状和阵元数量变化。
