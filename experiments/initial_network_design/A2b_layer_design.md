# A2b：每层结构状态

状态：`confirmed`

## 已确认

```text
每级使用两次普通 3×3×3 Conv。

每次卷积均采用：
Conv3d -> GroupNorm -> LeakyReLU

Conv3d:
kernel_size=3, stride=1, padding=1, dilation=1
groups=1, bias=false, padding_mode=zeros

GroupNorm 固定每组 8 个通道：
C=8   -> GroupNorm(1,8)
C=16  -> GroupNorm(2,16)
C=32  -> GroupNorm(4,32)
C=64  -> GroupNorm(8,64)
C=128 -> GroupNorm(16,128)
eps=1e-5, affine=true

LeakyReLU:
negative_slope=0.01, inplace=true
```

本文件不承担长篇调研、解释或论证。具体参数清单、依据、用户质疑和讨论均在对话中完成；只有经用户确认后的简洁决定再写入本目录。

## 已有相关决定

- A1：5 次下采样，通道为 `8 -> 16 -> 32 -> 64 -> 128 -> 128`。
- 下采样：每一级统一使用 `MaxPool3d(kernel_size=2,stride=2,padding=0,dilation=1,return_indices=false,ceil_mode=false)`。
- 上采样：`ConvTranspose3d(kernel_size=2,stride=2,padding=0,output_padding=0,dilation=1,groups=1,bias=false,padding_mode="zeros")`。
- 跳跃连接采用通道拼接（`concat`）：
  1. 保存 Encoder 每级第二次 `LeakyReLU` 后、`MaxPool3d` 前的特征；
  2. Decoder 先执行 `ConvTranspose3d`；
  3. 与同分辨率 Encoder 特征执行 `concat(dim=1)`；
  4. 拼接结果再进入双卷积块。
- `ConvTranspose3d` 后、`concat` 前不额外使用归一化或激活；skip 不裁剪、不额外卷积。
- V0 不使用 CBAM 或其他注意力模块。
- V0 不使用 Dropout、残差块或深监督。

## 初始化

- `Conv3d` 与 `ConvTranspose3d`：`kaiming_normal_(a=0.01,mode="fan_in",nonlinearity="leaky_relu")`；
- GroupNorm：缩放参数初始化为 `1`，偏移参数初始化为 `0`；
- 不对网络整体重复调用 PyTorch 默认初始化。

## 边界

- A2a 输入仍是位置和法向均可变化的理想方向性点源，不含孔径、直径、表面点集或有限孔径 mask。
- 主 `Re/Im` 输出头及其偏置/初始化归入 A3，不在 A2b 内冻结。
- 随机种子、确定性计算和训练期梯度策略归入 T，不属于 A2。
