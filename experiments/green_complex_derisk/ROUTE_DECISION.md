# Green 路线裁决与后续门禁

```text
as_of: 2026-07-20
physical_green_decomposition: keep
greenonet_project_adaptation: frozen
custom_v2_retraining: forbidden
new_skull_label_generation_for_green: forbidden
next_action: low_cost_evidence_only
```

## 一句话结论

当前不值得继续实施 GreenONet 项目适配；保留“单阵元复响应 + 相干叠加”的物理路线，但不再用自写网络和自建标签给它下生死结论。

## 为什么冻结

1. 原 GreenONet 是物理约束的时域初值算子，数值实验只到 1D / 2D；项目需要固定频率、3D 异质颅骨、有限尺寸阵元、位置 / 法向条件和绝对 `Re/Im` 复声压。这是方法级迁移，不是输出通道适配。
2. 两圈检索未找到原论文官方代码、B 级第三方复现，或同时覆盖项目关键条件的公开实现；同组直接后续仍是 1D Poisson。
3. 原方法虽不需要完整波场 label，但项目监督版需要自建网络与 k-Wave 标签；物理约束版则需要自建 3D 复数 Helmholtz、有限孔径、吸收和 PML 训练。两条路当前都属于原创方法研究。
4. 历史 V2 是 `custom Fourier-SiLU baseline`，训练集复场 L2 约 `42%`；它只能否决该实现。继续调参不会自动产生对 GreenONet 的可信证据。

## 已经成立与尚未成立

已经成立：

- 线性标量声学下，固定频率复声压可以写成复数 Green / Helmholtz 表示。
- 当前 benchmark skull 中，单阵元绝对复场可以准确重组多阵元场；最差复场相对 L2 为 `5.81e-6`。
- 坐标查询的峰值显存可以通过分块控制。

尚未成立：

- 神经网络能在未见位置 / 法向上准确预测有限阵元的 3D 经颅复响应。
- 原 GreenONet 网络可以直接迁移到项目。
- GreenLearning、GF-Net、SIREN 等邻近代码能组合成项目方法。
- 项目需要多少单阵元复场 label，以及这些 label 是否值得生成。

## 当前禁止动作

- 重做或延长历史 V2 训练；
- 自行拼接 GreenLearning、SIREN、Fourier Features、哈希编码或 source encoder；
- 在没有来源的情况下新增复数输出头、损失或物理残差后继续称为 GreenONet 复现；
- 为上述自定义方案生成新的 MIDA / benchmark skull 标签；
- 用邻近低维示例的成功或失败给项目路线下结论。

## 解冻条件

常规项目适配实验需同时满足：

1. 原始或直接邻近的作者实现已经原样复现；
2. 实现至少直接支持固定频率复场与可变源条件，项目修改只属于环境或数据适配；
3. 标签 / 采样协议和资源预算有论文、作者代码或导师批准支撑；
4. 用户重新明确批准实验范围、来源卡、指标和停止条件。

例外：如果导师把它明确批准为原创高风险方法研究，可另立 research mission；必须使用自定义方法名称，并接受结果只评价该改造。

## 证据入口

- 直接与邻近代码审计：`SOURCE_EVIDENCE.md`
- 历史自定义实验边界与结果：`PROVENANCE.md`、`RESULTS.md`
- 理论过渡：`THEORY_GATE.md`
- 物理相干叠加验证：`../elementwise_superposition/RESULTS.md`
- 稳定项目决策：`../../docs/decisions.md`
