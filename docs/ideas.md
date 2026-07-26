# Ideas

> **当前口径（2026-07-25）：** 主 U-Net 预测逐样本归一化的相对复场 `q_Re/q_Im`，A4 预测脑内绝对峰值尺度，二者共同重建绝对 `Re/Im`。下文旧条目中“主网络直接输出绝对复场”或有限孔径相关表述仅保留为历史想法，除非条目另有更新。

本文件记录尚未验证、尚未拍板、但可能值得保留的科研想法。

> 当前边界（2026-07-24）：项目已改为位置、法向均可变化的理想方向性点源。下文涉及有限孔径、表面点集或圆盘积分的内容只保留为历史 idea，不是当前项目候选。

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
```

## 2026-07-22：直接介质输入与阵元多尺度条件化的比较框架

来源：

精读 Jang et al. (2025) 的逐切片 VGG19—ADNet—PPNet 流程，并与当前固定 MIDA、可变有限孔径位置 / 法向、绝对 `Re/Im` 任务对照。

想法：

不要预设逐切片 VGG19 或瓶颈低维位姿是唯一表示。后续若进入网络选型，可在同一仿真标签、同一训练 / 测试划分和同一复场指标下，分层比较：

```text
介质上下文：
A. 固定 MIDA 隐含在模型参数中
B. 直接输入三维声速 / 密度场
C. 三维介质编码器特征（保留空间层级并可缓存）

阵元条件：
1. 仅用 (x,y,z,nx,ny,nz) 在瓶颈注入
2. 与网格对齐的有限孔径 source mask
3. 低维位姿 + source mask
4. 在多个编码 / 解码尺度注入位姿条件
5. 加入相对距离场、方向场或局部阵元坐标
```

网络比较先以确定性 3D 基线为参照；VAE只作为“潜在空间正则化是否改善位置 / 法向插值泛化”的对照，不预设为最佳。GAN、CycleGAN、VQ-VAE 等只有出现与绝对复声场直接相关的来源后再提高优先级。

依据：

- 论文：Jang et al. (2025)，https://doi.org/10.1016/j.engappai.2025.111157；VAE仅在 `[315,512]` VGG特征、瓶颈位姿和归一化最大压力场任务中排名第一。
- 论文方法缺口：未比较直接 CT / 声速 / 密度体输入；未充分说明瓶颈处位姿是拼接、相加还是其他融合。
- 项目文档：`docs/project_concept_v5.md` 要求阵元有限孔径在网络输入、标签仿真和 Helmholtz 源项中保持同一物理含义，并输出绝对 `Re/Im`。
- 物理考虑：固定介质和确定源条件对应唯一复声场；VAE随机潜在变量与 KL 正则可能提供泛化，也可能平滑幅值 / 相位细节，不能脱离复场指标判断。

可能价值：

1. 把“介质是否显式输入”和“阵元如何条件化”拆成两个可审计因素，避免一次更换整个架构后无法归因。
2. source mask 或相对几何场可显式建立阵元与局部介质的空间关系；低维位姿继续提供精确连续坐标，二者可能互补。
3. 固定 MIDA 编码可缓存，避免每个样本重复处理同一个大体积，同时为以后多颅骨扩展保留接口。
4. 公平比较确定性基线与 VAE，能回答正则化收益是否超过复相位平滑风险。

待验证点：

1. 固定 MIDA 下显式介质输入是否提供超过“模型参数已记住介质”的实际收益；未来多颅骨时结论是否变化。
2. source mask 的离散化、旋转、总激励幅值和相位参考如何与标签求解器、Helmholtz源项严格一致。
3. 位姿只在瓶颈、在多尺度重复注入、与 source mask 组合，谁对未见位置 / 法向的复场幅相误差更好。
4. 比较指标必须至少包含全场复数相对 L2、幅值误差、相位误差、目标点复压误差和多阵元叠加后误差。
5. 是否存在直接针对三维异质介质、可变有限源和复声场的公开架构 / 代码，可作为正式实验来源。

当前状态：待来源调研和实验协议设计；未批准直接实现。

## 2026-07-21：Helmholtz 配置点分层抽样

来源：

FEUNet 采用随机配置点计算 PDE error；用户指出曾在另一篇论文中见过分层抽样，并批准把该方法列入后续调研。

想法：

三维 Helmholtz 物理损失不一定只做全域均匀随机抽样。可以按物理区域分层，再从各层抽取配置点：

```text
普通介质内部
颅骨 / 介质界面附近
阵元 / 声源附近
目标焦点附近
PML / 外边界相关区域
```

分层的目的不是简单增加点数，而是避免体素数量巨大的平滑内部区域淹没界面、源和边界等关键但占比很小的区域。

依据：

- FEUNet：https://doi.org/10.1121/10.0025391；说明可通过抽取少量配置点计算离散 Helmholtz PDE loss，但其示例不是本项目所需的三维分层方案。
- 用户 2026-07-21 确认：分层抽样值得研究，并准备继续阅读见过该方法的论文。

可能价值：

1. 在固定配置点预算下提高介质界面、源附近和 PML 区域进入物理损失的概率。
2. 可以分别观察不同物理区域的残差，避免一个全局平均值掩盖局部失败。
3. 为后续高残差自适应采样提供清晰的初始分区。

待验证点：

1. 分层规则、每层比例和每个 batch 是否动态重采样。
2. 源附近奇异性 / 高斯源区域是否应排除、降权或单独建层。
3. 界面点应按材料标签、声速梯度还是密度梯度定义。
4. 与均匀随机抽样进行同点数消融后，是否真正改善全场复数误差、界面误差和焦点 / 旁瓣指标。
5. 用户随后提供的论文能否给出可迁移的抽样依据。

当前状态：已批准调研；尚未证明优于均匀随机抽样，也未批准为最终实现。

## 2026-07-19：Green 有效阵元响应 + 隐式神经表示（INR）

> **2026-07-20 状态更新：保留但冻结。** 以下内容只是一组论文启发，不是已批准架构。未找到直接支持项目任务的作者实现前，不得拼接 GreenLearning、SIREN、Fourier Features、哈希编码或自写 source encoder 后继续做路线生死实验。

来源：

Green 复声场 V2 排雷结果、用户与 ChatGPT 关于 GreenONet 后续表示方式的讨论，以及 SIREN、Fourier Features、Instant-NGP 原始论文。

想法：

项目不必把“GreenONet 原论文的网络结构”当作唯一实现。更合理的候选是保留 Green 的物理分解和阵元级复响应，再用适合连续坐标场的隐式神经表示（Implicit Neural Representation, INR）学习有限孔径、方向性和固定介质造成的复数修正：

```text
显式自由传播载波 (1/r) exp(ikr)
+ 阵元局部坐标中的有限孔径修正
+ 固定 MIDA 全局坐标中的颅骨传播修正
-> 单阵元大区域绝对复声压
```

候选表示按优先级分为：

1. 历史 `SiLU MLP + Fourier Features` 只作为自定义失败记录，不再是获准重训的基线；
2. SIREN（正弦激活网络）只作为高频连续场的论文启发，不能自动升级为条件 Green 算子；
3. 多分辨率哈希编码作为固定 MIDA 下的速度 / 空间细节候选，暂不默认用于跨头颅泛化；
4. KAN 暂不列为主候选，直到找到直接支持高频三维波场或条件算子学习的可靠证据。

这里的 INR 不是替代 Green 思想，而是替代或增强“用什么网络表示查询坐标到复响应”的部分。网络仍然输出 `Re/Im` 或等价的复数修正，阵列仍在网络外相干叠加。

依据：

- 代码 / 实验：`experiments/green_complex_derisk/green_model.py` 已显式计算自由传播载波，V2 网络不是从零学习 `cos(kr)` / `sin(kr)`；`experiments/green_complex_derisk/RESULTS.md` 显示当前600步方案训练集复场 L2 仍约 `42%`，尚不能区分训练不足、坐标表示不足和架构不足。
- 计算审计：在相同随机查询上，32点圆盘积分相对512点参考的复场 L2 约 `13.5%–13.6%`；512点相对2048点约 `0.95%`。原 V2 的32点教师不足以支撑物理误差 `<2%` 的解释，重做前应先提高教师积分精度。
- 论文：Sitzmann et al., `Implicit Neural Representations with Periodic Activation Functions`, NeurIPS 2020，https://arxiv.org/abs/2006.09661；论文展示 SIREN 表示波场并处理 Helmholtz / wave equation，但未验证本项目的三维经颅条件算子。
- 论文：Tancik et al., `Fourier Features Let Networks Learn High Frequency Functions in Low Dimensional Domains`, NeurIPS 2020，https://arxiv.org/abs/2006.10739；说明普通坐标 MLP 的频谱偏置及 Fourier 输入映射的改善作用。
- 论文：Müller et al., `Instant Neural Graphics Primitives with a Multiresolution Hash Encoding`, ACM TOG 2022，https://arxiv.org/abs/2201.05989；支持哈希编码提高坐标网络训练 / 查询效率和细节表示，但研究对象不是声学算子。
- 用户本轮确认：该组合观点打开了项目思路，值得先作为 idea 保留，再通过分层实验决定是否升级。

可能价值：

1. 把 Green 的物理可叠加性与 INR 的连续坐标查询能力分工，避免把原 GreenONet 的具体 MLP 当成路线本身。
2. 允许查询点分块，继续保持 V1 已验证的低峰值显存特性。
3. 阵元局部坐标可显式表达轴向距离、径向距离和离轴角，减少网络自己学习平移 / 旋转对称性的负担。
4. 固定 MIDA 时，可把全局颅骨影响留给位置相关分支或可训练空间编码，同时让有限孔径分支保持可复用。

待验证点（只有解除来源门禁后才进入实验）：

1. 当前 V2 失败究竟来自仅600步训练、采样 / 损失，还是当前 Fourier-SiLU 表示能力不足。
2. 自由传播载波已经显式移除后，剩余复修正是否仍需要 SIREN，还是普通 MLP + 物理局部坐标已经足够。
3. SIREN、可调 Fourier Features 和哈希编码在同参数量、同训练时间、同查询吞吐下，谁能先通过单姿态和多姿态解析场测试。
4. INR 常用于拟合一个固定信号；本项目需要从阵元位置 / 法向条件化到一族声场，必须验证 source embedding、FiLM、hypernetwork 或局部 / 全局双分支是否能形成真正的条件算子，而不是每个阵元单独训练一个网络。
5. 多分辨率哈希编码是否只会记住固定 MIDA 的绝对空间，导致未见阵元位置、法向或未来多头颅泛化变差。
6. 新表示能否继续输出绝对 Pa 的 `Re/Im`，并在多阵元相干叠加时控制相位误差累积。

当前状态：保留但冻结（`blocked_by_missing_direct_source`）；不属于当前实验任务。

## 2026-07-04：低分辨率大区域 pmax baseline 作为第一版（已被替代）

> **2026-07-21 状态更新：** 用户明确删除该路线。以下内容仅保留为历史想法，不再作为当前 baseline、任务或分辨率选择依据。

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

当前状态：已被 `docs/project_concept_v5.md` 替代，不再活跃。

## 2026-07-04：DeepTFUS 作为工程参考和 baseline，而非最终模型

来源：

DeepTFUS 论文阅读、非官方复现仓库部署、checkpoint eval、低分辨率训练，以及阶段 E 迁移判断。

想法：

DeepTFUS 仍可作为 3D 网络工程参考：可以借鉴 `3D volume + geometry condition -> 3D field` 的接口、点云式几何编码、weighted loss、最小链路验证、checkpoint/eval/log 结构。但它不再是当前输出任务的 baseline，因为它输出 normalized / log pmax，不输出绝对复声压，也不自然支持单阵元复场相干叠加。

依据：

- 代码笔记：`docs/deeptfus_code_notes.md` 记录 DeepTFUS 的标签为 `pressure = log(1 + pmap_resized / max(pmap_resized))`，不是绝对 Pa，也不是复声场。
- 运行记录：`docs/deeptfus_run_log.md` 记录非官方 base checkpoint 能在 CUDA 环境下完成 subset eval，训练链路也能低分辨率跑通。
- 非官方仓库 README / checkpoint README：base reproduction 自报在 `relative_l2` 上接近论文，但 `focal_position_error_mm` 明显差于论文；其硬件目标为 H100/A100 80GB。
- 项目文档：`docs/project_concept_v5.md` 已将单阵元三维绝对复声场确立为当前路线，DeepTFUS 只保留工程参考价值。

可能价值：

1. 为三维条件网络提供代码组织、几何编码、训练日志和评估流水线参考。
2. 为组会说明“已有 3D TUS surrogate 的边界”提供对照材料。
3. 避免把 DeepTFUS 的 normalized pmax 任务误当作本项目最终目标。

待验证点：

1. 哪些 geometry encoding 方式适合阵元位置 / 法向变化。
2. DeepTFUS weighted loss 思路能否改成对绝对 `Re/Im`、焦点和非目标高压区域的辅助加权。
3. baseline 与本项目模型的指标如何公平对照。

当前状态：降级为工程参考；不作为当前复声场路线的直接方法证据或输出 baseline。

## 2026-07-04：单阵元大区域复声场 + 多阵元相干叠加（已升级为当前主线）

来源：

项目长期路线和 DeepTFUS 迁移判断。

想法：

在固定 MIDA、频率、阵元尺寸和激励幅值下，根据阵元位置与法向预测指定三维域内的单阵元绝对复声场，再通过多阵元相干叠加得到阵列声场。该想法已由 2026-07-21 用户确认升级为当前主线。

依据：

- 项目文档：`docs/project_concept_v5.md` 已将 single-element 3D absolute complex pressure field 写为当前主输出。
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
4. 复场相位误差在大量阵元叠加后如何累积，并应采用什么阵列级验收阈值。

当前状态：已升级为 `docs/project_concept_v5.md` 当前路线；具体网络、标签和损失设计仍待验证。

## 2026-07-02：DeepTFUS 启发的换能器几何编码与高压区加权 loss

来源：

阅读论文 `A Skull-Adaptive Framework for AI-Based 3D Transcranial Focused Ultrasound Simulation` 及本轮关于公式、坐标编码、loss 和实验结果的讨论。

想法：

DeepTFUS 中把换能器表面表示为 `N × 3` 坐标矩阵，再通过 Fourier positional encoding、MLP 和 attention pooling 得到固定长度的换能器几何表示。这个思路可作为本项目 array geometry encoding 的候选参考。

同时，绝对复声场训练不一定只依赖普通全场 MSE / L2。可以研究对焦点、高压区、旁瓣风险区或非目标高压区域增加辅助权重，但不能因此忽略低幅值区域的相位和全场 Helmholtz 一致性。

依据：

- 论文/网页：Srivastav et al., `A Skull-Adaptive Framework for AI-Based 3D Transcranial Focused Ultrasound Simulation`, arXiv:2505.12998；官方仓库 https://github.com/CAMMA-public/TFUScapes 说明 DeepTFUS 从 3D CT volume 和 transducer position 估计 normalized pressure fields，并采用 Fourier-encoded position embeddings、MLP、feature-wise modulation、dynamic convolutions 和 cross-attention。
- 论文实验：weighted loss 将 focal position error 从约 `5.49 mm` 降到 `3.04 mm`，max pressure error 从约 `92.39%` 降到 `22.74%`，但 global relative L2 没有同步改善。
- 论文消融：去掉 Fourier positional encoding 影响有限，说明该编码是候选启发，不是强确定结论。
- 项目文档：`docs/project_concept_v5.md` 将 geometry encoding、绝对 `Re/Im` label / loss 和阵列指标设计列为当前问题。

可能价值：

1. 为单阵元位置、法向和有限孔径提供一种非 dense mask 的几何输入方式。
2. 为绝对复声场训练提供更贴近焦点和旁瓣风险的辅助 loss 设计方向。
3. 帮助后续区分“全场平均误差”和“阵列设计真正关心的焦点 / 峰值 / 旁瓣指标”。

待验证点：

1. Fourier positional encoding 在本项目阵元位置、阵元法向、阵列形状变化更大的情况下是否仍然有效。
2. 对单阵元有限孔径，attention pooling 是否比低维位置 / 法向或三维源 mask 更合适。
3. 高压区加权 loss 是否会牺牲远场低压区域或旁瓣统计的准确性。
4. 对本项目是否需要同时加入焦点加权、非目标高压区加权和梯度一致性 loss。

当前状态：待验证

## 2026-07-01：用 400^3 单通道体数据作为全脑输入估算基准（历史估算）

> **2026-07-21 状态更新：** `400^3 × 0.5 mm` 只保留为历史数据量估算，不再预先决定当前模型的分辨率或介质通道。当前网格由固定频率、最短波长和收敛实验确定；介质通道另行调研。

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
- 历史项目文档：`docs/project_concept_v4.md` 曾将 `3D skull acoustic volume`、阵元位置和法向列为第一版候选输入；当前路线见 `docs/project_concept_v5.md`。
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

当前状态：历史估算参考；不得据此直接确定当前网格或单通道输入。
