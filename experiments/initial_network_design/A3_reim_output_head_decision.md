# A3 决定：相对复声场双通道输出头

状态：`confirmed`

## 1. 输出组织

采用一个共享 3D U-Net，最后直接输出两个通道：

```text
decoder feature: [B,8,288,288,288]
        |
Conv3d(
    in_channels=8,
    out_channels=2,
    kernel_size=3,
    stride=1,
    padding=1,
    dilation=1,
    groups=1,
    bias=True,
    padding_mode="zeros"
)
        |
q_hat: [B,2,288,288,288]
```

通道语义固定为：

```text
channel 0 = q_Re
channel 1 = q_Im
```

`q_Re/q_Im` 是逐样本归一化的相对复声场，不是绝对 Pa。绝对复场由 A4 预测的尺度统一乘回。

## 2. 末层设置

- 不使用 GroupNorm、BatchNorm 或 InstanceNorm；
- 不使用 ReLU、LeakyReLU、Sigmoid、Tanh 或 Softplus；
- `bias=True`，因为该层后没有归一化层吸收偏置；
- 权重使用 `xavier_normal_(gain=1.0)`；
- 偏置初始化为 `0`；
- 网络前向可使用 BF16 自动混合精度，进入数据损失与物理损失前转为 FP32。

线性输出不限制正负值，允许两个复数分量在零点两侧取值。归一化发生在 label 协议中，不由输出层 activation 完成。

## 3. 选择依据与边界

- FEUNet 的复波场代码采用共享 U-Net 和末层 `8 -> 2` 的 `3×3` 卷积，支持“同一主干直接输出 Re/Im 两通道”；
- 本项目不复制 FEUNet 末层 LeakyReLU，因为带负半轴斜率的输出会对负值引入不对称映射；
- 不采用两个独立 U-Net，也不采用分离的 Re/Im 小头；V0 先让两分量共享同一空间表征，减少参数和额外变量；
- A3 只冻结输出头结构与语义，不决定 L1 数据损失、A4 误差权重或最终训练日程。
