# Research Tasks

> 历史保留文件：从 2026-07-02 起，本文件不再作为 Codex 主动维护的科研任务系统。
>
> 之后的“下一步要干什么 / 什么重要但还没查”优先由 `docs/memory.md` 的近期关注、`docs/questions.md` 的开放问题和 `docs/ideas.md` 的未验证想法综合判断。Codex 不应主动往本文件新增细粒度 task，除非用户明确要求。

本文件保留早期曾整理过的调研任务，主要用于追踪历史判断。

## 记录原则

1. 本文件默认只读、历史保留。
2. 不再要求每轮讨论后整理 task。
3. 不记录“做 PPT / 汇报”等替用户安排的细任务。
4. 如用户明确要求写入任务，只记录用户确认过的近期方向。

## 建议格式

```markdown
## YYYY-MM-DD：任务标题

任务：

目的：

依据：
- ...

产出物：

完成标准：

状态：todo / doing / done / blocked
```

## 2026-07-01：基于 400^3 单通道输入基准继续估算数据量和显存

任务：

以 `400×400×400`、`0.5 mm`、单通道输入体数据为候选基准，继续估算输入、输出、训练标签、显存和数据生成成本。

目的：

为后续判断“全脑输入 + 全脑输出”在现有算力资源下是否可行提供统一计算基准，避免继续使用过度保守或未解释清楚的 `512^3` 默认假设。

依据：

- 用户本轮确认：希望将 `400^3`、`0.5 mm`、单通道输入和低维换能器位置输入整理进记忆，为之后继续估算做准备。
- 项目文档：`docs/project_concept_v2.md` 的第一阶段最小可行任务包括“全脑 pmax 输出的数据量和显存压力”。
- 想法来源：`docs/ideas.md` 已记录 `400^3` 单通道体数据作为全脑输入估算基准。

产出物：

一张估算表，至少包含：

```text
输入体数据大小
换能器低维输入大小
候选输出大小
不同数据类型下的磁盘 / 内存估算
24GB GPU 下的初步风险判断
```

完成标准：

1. 明确区分输入大小、输出标签大小、训练显存和数据生成成本。
2. 明确列出 `float32`、半精度浮点数（fp16 / bf16）等数据类型的影响。
3. 明确说明哪些结论来自代码 / 论文，哪些只是计算假设。

状态：doing

阶段产出：

- 2026-07-01：已形成初步估算文档 `docs/output_data_size_24gb_estimate.md`。当前结论是输出标签本身不一定爆，但 DeepTFUS-like 3D U-Net 的训练显存高风险；仍需后续用本项目最小模型做真实 GPU profiling。

## 2026-07-02：整理 DeepTFUS 对 3D 阵列 surrogate 的借鉴边界

任务：

整理 `A Skull-Adaptive Framework for AI-Based 3D Transcranial Focused Ultrasound Simulation` / DeepTFUS 对本项目的可借鉴内容和不可直接借鉴边界。

目的：

把该论文从“读过”整理成可用于组会 PPT 和技术路线判断的证据材料，尤其服务于 3D IO 设计、array geometry encoding、label 成本和 pmax loss 设计。

依据：

- 论文：DeepTFUS 是 3D transcranial focused ultrasound surrogate 的直接对标工作，输入为 pseudo-CT 3D volume + transducer geometry，输出为 normalized 3D pmax / pressure amplitude field。
- 论文实验：2500 个 3D 仿真消耗超过 750 GPU hours；weighted loss 显著改善焦点定位和最大压力误差。
- 论文限制：单 bowl-shaped transducer、有限几何变化、单频率 `500 kHz`、normalized pmax 输出、不包含复声场相位。
- 项目文档：`docs/project_concept_v2.md` 当前同时关心 whole-brain pmax field 和单阵元复声场叠加路线。

产出物：

一页或一节 Markdown / PPT 提纲，至少包含：

```text
1. DeepTFUS 能偷什么
2. DeepTFUS 不能偷什么
3. 对路线 A：全阵列 -> whole-brain pmax 的启发
4. 对路线 B：单阵元复声场 -> 相干叠加的限制
5. 需要继续验证的问题
```

完成标准：

1. 明确区分 normalized pmax、绝对声压和复声场。
2. 明确说明 label 生成成本对本项目的风险。
3. 明确列出 Fourier geometry encoding、attention pooling、weighted loss 的可借鉴性和待验证边界。
4. 明确说明 DeepTFUS 不支持多阵元数量变化和复声场相干叠加。

状态：todo
