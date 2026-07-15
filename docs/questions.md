# Questions

本文件记录需要问师兄、查论文或做实验验证的开放问题。

记录问题时尽量写明来源或依据，方便之后知道这个问题为什么产生。

注意：已被舍弃或降级的旧路线不再放在这里作为活跃问题；历史变化见 `docs/memory.md`。

## 2026-07-04：大区域输入输出边界（由 2026-07-01 问题更新）

问题：

当前第一版已确认不是严格 whole-brain，而是大区域输出，约取上半 / 一半颅骨或脑区覆盖。此前 `400×400×400`、`0.5 mm`、单通道体数据仍可作为估算参考，但边界问题需要改为验证大区域裁剪条件：

1. 大区域具体裁剪范围如何定义，是否采用上半颅骨 / 上半脑区 / 其他物理坐标边界？
2. 第一版输入用 CT / pseudo-CT 单通道是否足够，还是必须显式输入声速、密度、衰减三通道？
3. 换能器位置只用单点位置 + 法向是否足够，还是需要类似 DeepTFUS 的换能器表面点坐标？
4. 低分辨率第一版应选 `128^3`、`160^3`、`200^3`，还是采用非立方大区域网格？

依据：

- 用户确认：输入拟用 `400×400×400` 体素、`0.5 mm` 间距、`1 channel` 信息，并将换能器位置作为输入。
- 用户 2026-07-04 确认：不是严格全脑，而是大区域，差不多切一半；第一版先做低分辨率。
- 项目文档：`docs/project_concept_v4.md` 已将第一版明确为低分辨率大区域绝对 pmax 输出。
- GitHub/代码：DeepTFUS / TFUScapes 公开样本采用单通道 `ct` 和 `tr_coords`，但它是 `256^3 crop`，不能直接证明 `400^3` 全脑输入一定合理，来源：https://github.com/CAMMA-public/TFUScapes

当前状态：待查 / 待验证

## 2026-07-02：阵元小且位置多时，高质量 3D label 成本是否不可承受

问题：

DeepTFUS 只有 `125` 个 subject、每个 subject `20` 个 transducer placements、总计 `2500` 个 3D 仿真，已经消耗超过 `750 GPU hours`，并生成超过 `200 GB` 数据。本项目阵元更小，候选空间位置可能远超 20 个，甚至可能超过 1000 个位置。如果每个位置都做 full-wave label，训练数据生成成本可能成为主要瓶颈。

需要验证：

1. 本项目在固定 MIDA skull、频率、阵元尺寸和幅值后，单阵元位置 / 法向采样最少需要多少个 3D full-wave label。
2. 是否可以通过单阵元大区域复声场响应、低分辨率大区域 pmax、稀疏位置采样、物理先验或主动采样降低 label 成本。
3. 换能器位置按 100、500、1000 个候选位置采样时，label 生成时间、磁盘数据和训练收益如何权衡。

依据：

- 论文：DeepTFUS / TFUScapes 报告 2500 个仿真、超过 750 GPU hours、超过 200 GB 数据。
- 用户确认：本项目阵元更小，需要考虑的空间位置肯定不止 20 个，可能超过 1000 个位置。
- 用户 2026-07-04 确认：第一阶段固定频率、阵元尺寸、幅值，只研究位置 / 法向变化。
- 项目文档：`docs/project_concept_v4.md` 保留单阵元大区域复声场叠加路线。

当前状态：待查 / 待验证

## 2026-07-02：只预测 normalized pmax 是否足够支持阵列方案比较

问题：

DeepTFUS 预测的是 normalized peak pressure amplitude / normalized pmax field。论文训练时还对 pressure map 先除以 max pressure，再做 `log(1+x)`。这种输出适合看相对声场形状和焦点位置，但不直接给绝对 `P_target`、`P_peak` 或安全阈值判断，也不包含相位，不能直接用于单阵元复声场相干叠加。

需要验证：

1. 绝对声压标定如何在 label、网络输出、loss 和 eval metrics 中保留。
2. 是否需要同时保存 normalized pmax 作为辅助训练目标或 DeepTFUS 对照。
3. 是否需要额外输出 `P_target`、`P_peak`、`side_lobe_ratio` 等 scalar metrics，还是从预测场后处理得到。
4. normalized pmax 在早期阵列方案相对比较中是否会误导真实强度对比。

依据：

- 论文：DeepTFUS 将输出定义为 normalized peak pressure amplitude pmax，并在训练中对 pressure map 做 max normalization 和 `log(1+x)`。
- 讨论结论：DeepTFUS 输出不是绝对声压、不是时间声压，也不是复声场。
- 用户 2026-07-04 确认：pmax 输出必须保留绝对声压标定。
- 项目文档：`docs/project_concept_v4.md` 将大区域绝对 pmax field 和 `P_target`、`P_peak`、`focus_error`、`side_lobe_ratio` 列为第一版输出。

当前状态：待查 / 待验证

## 2026-07-02：单频率 3D surrogate 是否会限制阵列设计泛化

问题：

DeepTFUS / TFUScapes 只在 `500 kHz` 下训练和验证。若本项目需要比较不同频率、阵元尺寸、幅值或相位策略，单频率模型无法直接覆盖更广泛的阵列设计空间。

需要验证：

1. 第一版固定频率、阵元尺寸和幅值后，模型能否可靠泛化到未见过的位置 / 法向组合。
2. 第二阶段是否需要把频率、幅值、阵元尺寸作为输入条件。
3. 多频率 label 成本会增加多少，是否会进一步放大数据生成瓶颈。

依据：

- 论文：DeepTFUS / TFUScapes 采用固定 `500 kHz` continuous-wave source。
- 用户总结：单频率受限，大模型不能做到非常广泛的适用。
- 用户 2026-07-04 确认：第一阶段固定频率、阵元尺寸、幅值，只研究位置 / 法向变化。
- 项目文档：`docs/project_concept_v4.md` 固定第一版频率、阵元尺寸和幅值，后续是否扩展仍待验证。

当前状态：待查 / 待验证
