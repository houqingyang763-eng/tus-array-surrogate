# AGENTS.md

## 项目定位

本仓库用于“3D 经颅超声阵列设计 / 声场预测 / 神经网络 surrogate model”科研训练。

用户当前目标不是泛泛学习深度学习，而是围绕：

1. 前期论文阅读；
2. 3D 技术路线判断；
3. 阵列位置、阵列形状、阵元数量变化下的声场快速预测；
4. whole-brain intracranial pmax field / 3D time-maximum pressure field；
5. 单阵元全脑 / 大区域复声场响应预测 + 多阵元相干叠加；
6. 初步验证实验；
7. 后续组会材料。

默认中文回答。先判断，再展开。不要泛泛科普。

---

## 工作前优先读取

每次处理本项目任务前，优先读取：

1. `docs/project_concept_v3.md`：当前项目源构想；
2. `docs/decisions.md`：已经沉淀的当前共识；
3. `docs/questions.md`：待问师兄、待查论文、待验证问题；
4. 科研记忆整理 / 归档任务再读取 `docs/memory.md`、`docs/memory_workflow.md`、`docs/ideas.md`；
5. 论文任务再读取 `docs/literature/paper_summary_skill.md` 和 `docs/literature/paper_categories.md`。

如果存在 `docs/project_concept_v3.md`，优先读取 v3 作为当前项目源构想。`project_concept_v2.md` 和 `project_concept_v1.md` 作为历史来源；必须注意 v1 中“不优先全脑输出”的判断已经被组内新需求修正，v2 中“长条形传播通道 / 焦点 ROI”相关候选已被 v3 修正。

---

## 当前主线

项目从 TUSNet 等经颅超声神经网络声场预测工作出发，但不局限于 2D proof-of-concept。

当前目标面向 3D：

输入：

- 3D skull acoustic volume，例如声速 / 密度 / 衰减体数据；
- bowl array geometry / element coordinates / element mask；
- target focus position；
- 可选：阵元法向、阵元尺寸、贴附距离、入射角、颅骨厚度、路径声速统计量。

输出：

- 主输出：whole-brain intracranial pmax field / 3D time-maximum pressure field；
- 指标输出：P_target、P_peak、focus_error、side_lobe_ratio、脑内最大压力统计；
- 候选扩展：single-element whole-brain / large-region complex response；
- 候选扩展：phase / delay correction。

---

## 重要技术判断

1. 不要默认“整阵列黑箱网络”是唯一方案。
2. 保留“单阵元全脑 / 大区域复声场预测 + 多阵元相干叠加”作为支持阵列位置、形状、阵元数量变化的核心候选路线。
3. 组内新需求要求整个脑内声场，因此 whole-brain pmax field 必须作为主输出之一。
4. 只输出单阵元 Pmax 不适合相干叠加，因为会丢失相位 / 时间信息。
5. 相干叠加依赖线性声学近似；涉及非线性传播、热效应或阵元硬件耦合时必须重新评估。
6. 当前阶段优先判断路线可行性和风险，不急着追求大规模完整实现。
7. 当前已舍弃“长条形传播通道输入 + 焦点附近小 ROI 输出”作为主线；入射角、颅骨厚度等特征只作为大区域模型的候选物理先验。

---

## 文档维护规则

1. 修改项目构想时，新建版本文件，不要覆盖旧版本。
2. `docs/memory.md` 是科研跟进主入口，记录完整时间线、当前状态、近期 3-5 个关注方向和已舍弃 / 已降级路线。
3. 稳定结论写入 `docs/decisions.md`。
4. 未验证但可能有价值的想法写入 `docs/ideas.md`。
5. 未解决问题写入 `docs/questions.md`。
6. `docs/research_tasks.md` 是历史保留文件，不再由 Codex 主动维护；不要主动往里面新增细粒度 task，除非用户明确要求。
7. 日常科研笔记先按 `docs/memory_workflow.md` 分类并反问确认，再写入文件。
8. 当前简化阶段暂不主动建立 `docs/literature/summaries/`、`docs/experiments/`、`docs/meeting/`，除非用户明确要求。
9. 不要把聊天流水账写进核心文档，只写稳定共识、可追踪想法、待解决问题、时间线摘要和近期关注。
10. 修改文件后必须输出修改摘要，并指出需要人工确认的风险点。

---

## 论文阅读规则

阅读论文时使用 `docs/literature/paper_summary_skill.md` 的结构。

每篇论文必须回答：

- 对本项目有没有用；
- 能偷什么；
- 不能偷什么；
- 输入输出是什么；
- 网络结构是什么；
- 数据怎么来；
- 是否支持 3D；
- 是否支持阵列位置变化；
- 是否支持阵列形状变化；
- 是否支持 whole-brain pmax field；
- 是否适合“单阵元全脑 / 大区域响应预测 + 叠加”；
- 适合放进组会 PPT 哪一页。

不要只翻译摘要。

---

## 初步实验规则

写实验代码前，先说明实验目的和最小验证问题。

优先做小实验：

1. 单源复场是否能叠加成多源场；
2. Pmax 输出为何不能直接相干叠加；
3. whole-brain low-resolution pmax baseline 的显存和数据量压力；
4. 单阵元全脑 / 大区域响应路线和整阵列黑箱路线的泛化差异；
5. normalized pmax 与绝对声压 / scalar metrics 的差异。

每个实验必须记录：输入、输出、label、loss、指标、结论、失败原因。

---

## 禁止事项

1. 不要把 0.5 mm 仿真 grid 默认当真实独立 delay 通道。
2. 不要在没有论据时声称某网络一定适合 3D 经颅超声。
3. 不要把相位延迟矫正单独带偏成主线；它应服务于声场预测和阵列设计。
4. 不要删除历史版本文档。
5. 不要大规模改动仓库结构而不说明理由。
6. 不要把 AGENTS.md 写成百科全书；细节放入 docs 或 skills。
