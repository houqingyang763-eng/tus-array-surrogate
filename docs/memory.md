# Project Memory

本文件是本项目的科研跟进主入口，用于记录完整时间线、当前状态概要和近期重要关注点。

它不替用户设置细粒度 task；它的作用是帮助用户回看：项目为什么走到这里、哪些判断已经变化、下一轮最值得关注什么。

---

## 当前状态摘要

截至 2026-07-02，项目主线调整为：

1. 当前重点是 3D whole-brain intracranial pmax field / 3D time-maximum pressure field surrogate。
2. 输入和输出优先围绕全脑或 `400^3` 级别大区域体数据设计，而不是窄长条传播通道。
3. 单阵元复声场预测 + 多阵元相干叠加路线没有被放弃，但它的候选形式应改为全脑 / 大区域响应预测，而不是“阵元到焦点”的长条形输入和焦点附近小 ROI 输出。
4. `docs/research_tasks.md` 保留为历史文件，不再作为 Codex 主动维护的任务系统。
5. 近期科研推进应从 `memory.md`、`questions.md`、`ideas.md` 和 `decisions.md` 中综合判断，由用户最终决定任务架构。

依据：
- 用户 2026-07-02 明确确认：舍弃“长条形输入 + 入射角特征”路线，当前就做全脑的，而非长条形；但仍然走单阵元叠加，输入和输出都是全脑或 `400^3` 大区域。
- 用户 2026-07-02 明确确认：`research_tasks.md` 功能重复且不符合需求，应保留为历史，不再主动维护；repo 的意义是总结、判断、记录，帮助用户自己定 task。
- 项目文档：`docs/project_concept_v2.md` 已将 whole-brain pmax field 设为主输出之一；`docs/project_concept_v3.md` 进一步把当前路线修正为全脑 / `400^3` 大区域输入输出。

---

## 时间线记录

### 2026-06-30：建立本地科研记忆 repo

建立本地 Markdown repo，用于沉淀经颅超声阵列 surrogate 项目的长期上下文。初始结构包括 `project_concept_v2.md`、`decisions.md`、`questions.md`、`ideas.md` 和 `research_tasks.md`。

当时的想法是把科研输入分类成 idea / question / task / decision，但后来发现 task 文件容易替用户过度设定行动，和真实需求不匹配。

### 2026-06-30：whole-brain pmax field 升为主输出

由于组内新需求要求考虑整个脑内声场，项目从“不优先全脑输出”修正为必须包含 whole-brain intracranial pmax field / 3D time-maximum pressure field。

这一判断仍然有效，是当前项目主线。

### 2026-07-01：形成 `400^3` 单通道输入估算基准

为了避免默认使用过度保守的 `512^3`，项目暂时采用 `400×400×400`、`0.5 mm`、单通道 CT / pseudo-CT 作为全脑输入和显存估算候选基准。

该基准仍需验证：`200 mm` 立方覆盖范围是否够、单通道是否足够、换能器几何如何编码、频率 / 幅值 / 阵元尺寸是否进入输入。

### 2026-07-02：DeepTFUS / TFUScapes 成为核心参考

DeepTFUS 证明了 `3D skull / pseudo-CT volume + transducer geometry -> 3D normalized pmax field` 的 3D TUS surrogate 路线已有公开工作。

它能启发 3D IO 设计、换能器几何编码、weighted loss 和 label 成本估算；但不能直接解决本项目，因为它输出 normalized pmax，不输出绝对声压或复声场，也不覆盖任意阵列形状和阵元数量变化。

### 2026-07-02：舍弃窄长条传播通道路线

用户明确确认：删除 `questions.md` 中的“长条形输入 + 入射角特征”作为活跃问题。当前路线不再围绕窄长方形传播通道，也不以焦点附近小 ROI 作为单阵元路线的主要输出。

新的理解是：如果保留单阵元叠加路线，也应研究全脑 / `400^3` 大区域输入输出下的单阵元响应，而不是长条形局部输入。

### 2026-07-02：科研记忆工作流改为 memory 主入口

用户指出 `research_tasks.md` 设计失败：它和 question / idea 功能重复，也容易产生用户不需要的“做 PPT / 汇报”式任务。

新的工作流是：

```text
memory.md 记录完整时间线、当前状态和近期关注
ideas.md 记录未验证但有价值的想法
questions.md 记录真正开放的问题
decisions.md 记录稳定共识
research_tasks.md 只作历史保留，不再主动维护
```

---

## 近期关注

1. **全脑 / 大区域输出的可行分辨率**
   需要继续判断 whole-brain pmax field 用 `128^3`、`160^3`、`200^3` 还是更高分辨率，才能兼顾旁瓣观察、阵列方案比较和 24GB GPU 训练压力。

2. **`400^3` 单通道输入基准的边界**
   需要确认 `200 mm` 立方覆盖范围、CT / pseudo-CT 单通道是否足够、换能器几何编码方式，以及目标点 / 频率 / 幅值 / 阵元尺寸是否进入输入。

3. **DeepTFUS 可借鉴边界**
   重点不是复述论文，而是明确它对本项目能偷什么、不能偷什么：geometry encoding、weighted loss、label 成本、normalized pmax 的局限。

4. **高质量 3D label 成本**
   DeepTFUS 的 2500 个 3D 仿真已消耗超过 750 GPU hours。本项目如果位置、阵元数量、阵列形状变化更大，label 生成可能成为首要瓶颈。

5. **normalized pmax 与绝对声压 / 指标输出**
   需要判断只预测 normalized pmax 是否足够支持阵列方案比较，还是必须同时保留绝对幅值、`P_target`、`P_peak`、`side_lobe_ratio` 等指标。

---

## 已舍弃 / 已降级路线

### 窄长条传播通道输入

状态：已舍弃为当前主线。

原思路：

```text
阵元 -> 颅骨 -> 焦点
```

只截取一条长条形传播通道作为输入，并输出焦点附近小 ROI 复声场。

舍弃原因：
- 用户 2026-07-02 明确确认当前“就做全脑的，而非长条形”。
- 当前项目需要 whole-brain pmax field / 大区域声场，窄长条输入可能无法覆盖远场旁瓣和全脑高压风险。

保留价值：
- 入射角、颅骨厚度、路径声速统计量仍可作为全脑 / 大区域模型的低维物理先验候选特征。

### `research_tasks.md` 作为主动任务系统

状态：已废弃维护。

舍弃原因：
- 用户 2026-07-02 明确确认 task 文件功能重复，且容易生成不符合需求的细任务。
- 当前 repo 的职责不是替用户设定 task，而是总结、判断、记录，方便用户自己定 task。

保留方式：
- 文件仍保留为历史记录。
- 新的“下一步”只在 `memory.md` 中以 3-5 个近期关注方向记录。

---

## 2026-07-04：DeepTFUS 复现收束，转入迁移判断

状态更新：

1. DeepTFUS 非官方复现阶段 A-D 暂告一段落，不继续做 `96^3` / `128^3` 显存探针，也不在笔记本上尝试 full training。
2. 本轮复现已经完成工程链路验证：`local_verify.py`、base checkpoint subset eval、`64^3` 低分辨率从零短训练、checkpoint 保存和后验 eval 均已跑通。
3. 当前项目第一版方向调整为：低分辨率、大区域输出，约取上半 / 一半颅骨或脑区覆盖，而不是严格 whole-brain 全域输出。
4. 第一阶段固定频率、阵元尺寸和幅值，优先研究阵元位置 / 法向变化。
5. pmax 输出必须保留绝对声压标定；normalized pmax 只能作为辅助表示或 DeepTFUS 对照。

依据：

- 用户 2026-07-04 明确确认：无需再做探针，停止复现，先做迁移判断。
- 用户 2026-07-04 明确确认：不是严格全脑，而是大区域，差不多切一半。
- 用户 2026-07-04 明确确认：第一阶段固定频率、阵元尺寸、幅值，只研究位置 / 法向变化。
- 用户 2026-07-04 明确确认：pmax 输出必须保留绝对声压标定。
- 运行记录：`docs/deeptfus_run_log.md` 已记录阶段 A/C/D 跑通结果；阶段 D 在 `64^3`、tiny model、batch size 1 下峰值显存约 `0.222 GiB`。
- 代码笔记：`docs/deeptfus_code_notes.md` 已记录 DeepTFUS 输出为 normalized / log pmax，不是绝对声压，也不是复声场。

近期关注更新：

1. **低分辨率第一版大区域 pmax baseline**
   第一版优先验证低分辨率、大区域 pmax 预测链路；具体分辨率候选保留为 `128^3`、`160^3`、`200^3` 或非立方大区域网格。

2. **大区域裁剪范围**
   当前方向已从严格 whole-brain 修正为大区域，约取上半 / 一半区域；仍需确定具体裁剪边界、坐标系和是否覆盖颅骨、脑组织及必要传播空间。

3. **绝对声压标定与指标输出**
   normalized pmax 不足以支持真实强度比较；第一版 pmax 输出需要保留绝对声压标定，并继续关注 `P_target`、`P_peak`、`focus_error`、`side_lobe_ratio` 等指标。

4. **MIDA 固定 skull 下的位置 / 法向采样**
   第一阶段固定 MIDA、频率、阵元尺寸和幅值后，核心数据问题变为需要多少位置 / 法向 label 才能支撑初步 surrogate。

5. **单阵元大区域复声场候选路线**
   DeepTFUS pmax baseline 可作为对照；支持阵元数量和阵列形状变化的长期候选仍是单阵元大区域复声场响应 + 多阵元相干叠加。
