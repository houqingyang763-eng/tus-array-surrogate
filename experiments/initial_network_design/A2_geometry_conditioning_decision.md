# A2a 决定：方向性点源坐标在瓶颈处接入

## 状态与范围

状态：`confirmed`

V0 的阵元模型是**有位置和法向的理想点源**，不是有限孔径阵元。点源的位置和法向都是样本变量；允许的变化范围尚未确定。

本文件只记录六维点源条件如何接入网络，不决定 Decoder、损失函数或点源的采样范围。

## 已确认设计

```text
g = (x, y, z, nx, ny, nz)
shape: [B,6]
```

- `(x,y,z)`：点源位置，按同一个全局物理域逐轴缩放到 `[-1,1]`；
- `(nx,ny,nz)`：点源法向，归一化为单位向量；
- 点源、介质体和输出场使用同一个全局坐标系；
- 不输入孔径、直径、表面点集或有限孔径 source mask。

瓶颈通道数统一记为 `C_b`，当前 A1 给出 `C_b=128`：

```text
Encoder 瓶颈 F
[B,C_b,D_b,H_b,W_b]

点源条件 g
[B,6]
-> Linear(6,C_b,bias=true) + ReLU(inplace=true)
-> [B,C_b]
-> reshape / expand
-> [B,C_b,D_b,H_b,W_b]

concat(F,g_feature, dim=channel)
-> [B,2C_b,D_b,H_b,W_b]

Conv3d(2C_b,C_b,kernel_size=1,bias=false)
-> GroupNorm(C_b/8,C_b,eps=1e-5,affine=true)
-> ReLU(inplace=true)
-> 共享瓶颈 Z
```

当前 `C_b=128`，因此具体为 `GroupNorm(16,128)`；与 A2b 统一采用“每组 8 个通道”的规则。

初始化：

- `Linear(6,C_b)` 和融合 `1×1×1 Conv3d` 使用 `kaiming_normal_(mode="fan_in",nonlinearity="relu")`；
- Linear 偏置初始化为 `0`；
- GroupNorm 缩放参数初始化为 `1`，偏移参数初始化为 `0`。

V0 不增加池化、注意力、多尺度重复注入或三维 source mask。

## 依据与边界

- 用户 2026-07-24 明确纠正：当前项目是有朝向的纯点源；位置和法向均会变化，变化范围未定；论文中的有限孔径不迁移到本项目。
- Jang et al. (2025), Section 3.2 / Figure 5：位置和方向经归一化与 Dense 层映射后，作为网络瓶颈的第二路输入。论文未披露具体融合运算。https://doi.org/10.1016/j.engappai.2025.111157
- `Linear -> broadcast -> concat -> 1×1×1 Conv` 是本项目对论文未披露部分的实现补全，不声称是论文原始实现或最优方案。

待确定但不影响本决定：点源位置范围、法向范围、训练/验证外推划分，以及方向性点源在标签求解器和 Helmholtz 源项中的具体数学定义。
