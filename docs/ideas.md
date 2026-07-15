# Ideas

本文件记录尚未验证、尚未拍板、但可能值得保留的科研想法。

## 记录原则

1. 只记录对项目可能有用的想法，不记录聊天流水账。
2. 未经验证的内容只能写成想法，不能写成结论。
3. 每条想法尽量说明来源、用途、待验证点。
4. 每条想法必须尽量写明简短依据，方便之后追踪为什么保留。
5. 如果想法已经变成稳定共识，再转写到 `docs/decisions.md`。
6. 如果想法变成近期关注，优先同步到 `docs/memory.md`，不要默认转写到 `docs/research_tasks.md`。

## 建议格式

```markdown
## YYYY-MM-DD：简短标题

来源：

想法：

依据：
- 用户本轮确认：...
- 项目文档：...
- 论文/网页：...
- GitHub/代码：...
- 计算推导：...

可能价值：

待验证点：

当前状态：待验证

## 2026-07-04：低分辨率大区域 pmax baseline 作为第一版

来源：

DeepTFUS 复现阶段 A-D 结束后的迁移判断，以及用户对第一版范围的确认。

想法：

第一版不追求高分辨率 full field，也不继续围绕 DeepTFUS full training 复现推进，而是先做低分辨率大区域 pmax baseline。输出范围不是严格 whole-brain，而是约取上半 / 一半颅骨或脑区覆盖的大区域。模型目标是尽快验证本项目自己的输入输出、label、loss 和指标链路。

依据：

- 用户 2026-07-04 确认：第一版先做低分辨率。
- 用户 2026-07-04 确认：不是严格全脑，而是大区域，差不多切一半。
- 用户 2026-07-04 确认：第一阶段固定频率、阵元尺寸、幅值，优先研究位置 / 法向变化。
- 用户 2026-07-04 确认：pmax 输出必须保留绝对声压标定。
- 运行记录：`docs/deeptfus_run_log.md` 显示本机 8GB GPU 已跑通 DeepTFUS 低分辨率训练链路，但不适合正式 `256^3 batch=4` full training。

可能价值：

1. 比继续复现 DeepTFUS 更直接服务本项目的 MIDA / 阵元问题。
2. 低分辨率大区域输出可先验证数据格式、label 生成、显存压力和指标定义。
3. 保留绝对声压标定后，更适合阵列方案真实强度比较。

待验证点：

1. 大区域具体裁剪边界和坐标系。
2. 第一版分辨率选 `128^3`、`160^3`、`200^3`，还是非立方网格。
3. 低分辨率 pmax 是否足以观察焦点、旁瓣和非目标高压区。
4. 固定 MIDA 下需要多少位置 / 法向 label 才有初步泛化能力。

当前状态：待验证

## 2026-07-04：DeepTFUS 作为工程参考和 baseline，而非最终模型

来源：

DeepTFUS 论文阅读、非官方复现仓库部署、checkpoint eval、低分辨率训练，以及阶段 E 迁移判断。

想法：

DeepTFUS 适合作为 3D pmax surrogate 的工程参考和 baseline：可以借鉴 `3D volume + geometry condition -> 3D field` 的接口、点云式几何编码、weighted loss、最小链路验证、checkpoint/eval/log 结构。但它不应作为本项目最终模型，因为它输出 normalized / log pmax，不输出绝对声压或复声场，也不自然支持可变阵元数量、阵列形状和相干叠加。

依据：

- 代码笔记：`docs/deeptfus_code_notes.md` 记录 DeepTFUS 的标签为 `pressure = log(1 + pmap_resized / max(pmap_resized))`，不是绝对 Pa，也不是复声场。
- 运行记录：`docs/deeptfus_run_log.md` 记录非官方 base checkpoint 能在 CUDA 环境下完成 subset eval，训练链路也能低分辨率跑通。
- 非官方仓库 README / checkpoint README：base reproduction 自报在 `relative_l2` 上接近论文，但 `focal_position_error_mm` 明显差于论文；其硬件目标为 H100/A100 80GB。
- 项目文档：`docs/project_concept_v3.md` 保留大区域 pmax 与单阵元大区域复声场两条候选路线。

可能价值：

1. 为第一版大区域 pmax baseline 提供代码组织、输入输出和 loss 设计参考。
2. 为组会说明“已有 3D TUS surrogate 的边界”提供对照材料。
3. 避免把 DeepTFUS 的 normalized pmax 任务误当作本项目最终目标。

待验证点：

1. 哪些 geometry encoding 方式适合阵元位置 / 法向变化。
2. DeepTFUS weighted loss 思路如何改成绝对声压 pmax 或复声场 loss。
3. baseline 与本项目模型的指标如何公平对照。

当前状态：待验证

## 2026-07-04：单阵元大区域复声场 + 多阵元相干叠加作为后续核心候选

来源：

项目长期路线和 DeepTFUS 迁移判断。

想法：

低分辨率大区域 pmax baseline 可作为第一版，但如果后续要自然支持阵元数量、阵列形状、阵列位置和相位 / 延迟策略变化，更核心的候选仍是单阵元大区域复声场响应预测，再通过多阵元相干叠加得到阵列声场。

依据：

- 项目文档：`docs/project_concept_v3.md` 已保留 single-element large-region complex response field 路线。
- 代码笔记：`docs/deeptfus_code_notes.md` 明确 DeepTFUS 只输出 normalized pmax，不含相位，不能直接用于相干叠加。
- 用户确认：第一阶段固定频率、阵元尺寸、幅值，优先研究位置 / 法向变化；长期仍需支持阵列设计变化。

可能价值：

1. 更自然支持阵元数量变化和阵列形状变化。
2. 保留相位信息，有机会支持相干叠加、延迟校正和阵列方案比较。
3. 可能减少为每个阵列组合单独做 full-wave label 的需求。

待验证点：

1. 单阵元大区域复声场 label 的生成成本和存储成本。
2. 经颅复杂介质中线性相干叠加误差是否可接受。
3. 复声场输出采用 Re/Im、幅相，还是其他稳定表示。
4. 复场路线与低分辨率 pmax baseline 的衔接方式。

当前状态：待验证

## 2026-07-02：DeepTFUS 启发的换能器几何编码与高压区加权 loss

来源：

阅读论文 `A Skull-Adaptive Framework for AI-Based 3D Transcranial Focused Ultrasound Simulation` 及本轮关于公式、坐标编码、loss 和实验结果的讨论。

想法：

DeepTFUS 中把换能器表面表示为 `N × 3` 坐标矩阵，再通过 Fourier positional encoding、MLP 和 attention pooling 得到固定长度的换能器几何表示。这个思路可作为本项目 array geometry encoding 的候选参考。

同时，whole-brain pmax field 的训练不应只依赖普通全场 MSE / L2。可以考虑对焦点、高压区、旁瓣风险区或非目标高压区域加权，使 loss 更贴近阵列设计评价目标。

依据：

- 论文/网页：Srivastav et al., `A Skull-Adaptive Framework for AI-Based 3D Transcranial Focused Ultrasound Simulation`, arXiv:2505.12998；官方仓库 https://github.com/CAMMA-public/TFUScapes 说明 DeepTFUS 从 3D CT volume 和 transducer position 估计 normalized pressure fields，并采用 Fourier-encoded position embeddings、MLP、feature-wise modulation、dynamic convolutions 和 cross-attention。
- 论文实验：weighted loss 将 focal position error 从约 `5.49 mm` 降到 `3.04 mm`，max pressure error 从约 `92.39%` 降到 `22.74%`，但 global relative L2 没有同步改善。
- 论文消融：去掉 Fourier positional encoding 影响有限，说明该编码是候选启发，不是强确定结论。
- 项目文档：`docs/project_concept_v2.md` 已将 array geometry encoding 和 pmax loss 设计列为需要重点查证的问题。

可能价值：

1. 为阵列位置 / 形状变化提供一种非 dense mask 的几何输入方式。
2. 为 whole-brain pmax 训练提供更贴近焦点和旁瓣风险的 loss 设计方向。
3. 帮助后续区分“全场平均误差”和“阵列设计真正关心的焦点 / 峰值 / 旁瓣指标”。

待验证点：

1. Fourier positional encoding 在本项目阵元位置、阵元法向、阵列形状变化更大的情况下是否仍然有效。
2. attention pooling 是否适合可变数量阵元，还是需要 graph / token / element-wise response 结构。
3. 高压区加权 loss 是否会牺牲远场低压区域或旁瓣统计的准确性。
4. 对本项目是否需要同时加入焦点加权、非目标高压区加权和梯度一致性 loss。

当前状态：待验证
```

## 2026-07-01：用 400^3 单通道体数据作为全脑输入估算基准

来源：

基于 DeepTFUS / TFUScapes 的输入形式、whole-skull 仿真尺寸调研，以及当前项目对“全脑输入 + 全脑输出”数据量估算的讨论。

想法：

后续进行输入数据量和显存估算时，暂时不默认使用 `512^3`。可以先采用一个候选输入基准：

```text
输入体数据尺寸：400 × 400 × 400 voxels
体素物理间距：0.5 mm
对应物理范围：约 200 mm × 200 mm × 200 mm
输入体数据通道数：1 channel
```

这里的 `1 channel` 暂时参考 DeepTFUS / TFUScapes 的公开数据形式，即输入一个 CT / pseudo-CT 风格的三维体数据，而不是一开始就输入声速、密度、衰减三个独立体数据。

换能器信息仍然是输入，但不作为大体积 dense volume 处理，而是作为低维几何信息输入，例如：

```text
单阵元位置：x, y, z
单阵元法向：nx, ny, nz
```

或类似 DeepTFUS 的换能器表面点坐标。其数据量相对 `400^3` 三维体数据很小，通常不是输入数据量瓶颈。

依据：

- 用户本轮确认：输入拟用 `400×400×400` 体素、`0.5 mm` 间距、`1 channel` 信息；换能器位置也是输入，但不怎么占用数据空间。
- 项目文档：`docs/project_concept_v2.md` 将 `3D skull acoustic volume`、阵列 / 阵元位置和法向列为候选输入。
- GitHub/代码：DeepTFUS / TFUScapes 公开样本采用单通道 `ct` 输入和 `tr_coords` 换能器点坐标，来源：https://github.com/CAMMA-public/TFUScapes
- 计算推导：`400 × 0.5 mm = 200 mm`，约对应 `200 mm × 200 mm × 200 mm` 覆盖范围；`400^3 = 64,000,000` 体素。

可能价值：

1. `400^3` 对应约 200 mm 立方体，比 `512^3` 更接近“覆盖全脑并留一定边界”的初步估算，而不是过度保守。
2. 单通道输入更接近 DeepTFUS 的公开数据结构，便于和已有 3D TUS surrogate 工作对比。
3. 将换能器位置作为低维几何输入，有助于避免把换能器信息误建模成额外的大体积通道。
4. 该基准可作为后续估算输入磁盘大小、输出标签大小、训练显存和数据生成成本的统一起点。

待验证点：

1. `200 mm × 200 mm × 200 mm` 是否足够覆盖目标所需的全脑、颅骨和必要传播空间。
2. 第一版输入到底采用 CT / pseudo-CT 单通道，还是声速、密度、衰减三通道。
3. 换能器输入应采用单点位置 + 法向，还是类似 DeepTFUS 的表面点坐标。
4. 是否还需要把目标焦点位置、频率、幅值、阵元尺寸等作为输入。
5. 该输入基准与输出设置结合后，在 24GB GPU 上是否可训练。

当前状态：待验证
