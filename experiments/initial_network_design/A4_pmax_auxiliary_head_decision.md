# A4 决定：绝对声压尺度头

## 状态与角色

状态：`confirmed`

A4 预测陌生样本的脑内绝对峰值尺度。它不是可删的辅助指标，而是把 A3 的相对复声场恢复为绝对复声场所必需的第二分支。

```text
medium -> Encoder -> F --------\
                                -> A2 Fusion -> Z -> Decoder -> q_Re/q_Im
g=(x,y,z,nx,ny,nz) ------------/             \-> PMaxHead -> A_hat
```

两个分支分别学习：

- A3：无量纲复声场的空间形状、相对幅值和相位；
- A4：该样本的绝对声压尺度。

## 1. 输入与几何边界

PMaxHead 只读取介质特征与六维点源条件融合后的瓶颈 `Z`：

```text
Z: [B,128,9,9,9]
```

V0 不把脑区 mask 乘到 `Z`，也不把 mask 作为额外网络输入。以下对象必须分开：

| 对象 | 作用 |
|---|---|
| `source.p_mask` | 标签求解器中的声源注入位置 |
| `sensor.mask` | 标签求解器中的记录位置 |
| `brain_eval_mask` | 定义归一化尺度、label 和脑内指标 |
| `Z` | 条件化后的低分辨率网络特征 |

标签仿真使用域外 PML：

```text
'PMLInside', false
```

每个几何样本必须满足：

```text
nnz(source.p_mask & brain_eval_mask) == 0
nnz(source.p_mask & skull_mask)      == 0
```

## 2. V0 网络结构

```text
输入 Z
[B,128,9,9,9]

Conv3d(128,128,kernel=3,stride=2,padding=1)
GroupNorm(8,128)
ReLU
-> [B,128,5,5,5]

Conv3d(128,128,kernel=3,stride=2,padding=1)
GroupNorm(8,128)
ReLU
-> [B,128,3,3,3]

Flatten
-> [B,3456]

Linear(3456,2048) + ReLU
Linear(2048,1024) + ReLU
Linear(1024,512)  + ReLU
Linear(512,256)   + ReLU
Linear(256,128)   + ReLU
Linear(128,64)    + ReLU
Linear(64,1)      + Softplus
-> [B,1]
```

该头约 `10.76 M` 参数，存在过拟合风险。V0 暂保留 TUSNet 式“卷积压缩—Flatten—多层全连接—正标量”结构；若验证集出现稳定的 train-validation gap，再换成已记录的轻量池化头，而不是继续加宽。

## 3. 训练 label 与主网络归一化

从同一样本、稳态基频的绝对复声场标签计算：

```text
amp_gt(r) = sqrt(Re_gt(r)^2 + Im_gt(r)^2)
A_gt      = max_{r in brain_eval_mask} amp_gt(r)

q_Re_gt(r) = Re_gt(r) / A_gt
q_Im_gt(r) = Im_gt(r) / A_gt
```

`A_gt` 即严格的 `Pmax_brain`。主网络以 `q_Re_gt/q_Im_gt` 为监督目标。

A4 使用只由训练集计算、写入 checkpoint 的全局常数：

```text
P_ref = max(A_gt over training set)
y_gt  = A_gt / P_ref
```

这里有两种不同归一化，不得混淆：

- `Re_gt/Im_gt ÷ A_gt`：逐样本归一化，用来形成主网络相对复场 label；
- `A_gt ÷ P_ref`：训练集统一的标量缩放，用来训练 A4。

不要直接把 k-Wave 的时域 `sensor.record={'p_max'}` 当作 `A_gt`。`A_gt` 必须从稳态 500 kHz 复幅值 `Re_gt/Im_gt` 在 `brain_eval_mask` 内计算。

## 4. A4 损失

```text
y_hat = Softplus(PMaxHead(Z))
r = log((y_hat + epsilon) / (y_gt + epsilon))

                 0.5*r^2,                         |r| <= delta
L_pmax(r) = {
                 delta*(|r| - 0.5*delta),          |r| > delta

epsilon = 1e-8
delta   = log(1.10)
```

推理得到：

```text
A_hat = P_ref * y_hat
```

## 5. 两阶段训练

### 阶段一：训练相对复声场

更新 Encoder、几何投影、A2 Fusion 和 Decoder；PMaxHead 不参与。

数据目标为 `q_Re_gt/q_Im_gt`。若加入 Helmholtz 物理损失，必须先用该训练样本已知的 `A_gt` 重建绝对预测：

```text
p_hat_for_physics = A_gt * (q_Re_hat + i*q_Im_hat)
```

再与绝对源项计算残差。不得把绝对源项直接作用在无量纲 `q_hat` 上。

### 阶段二：训练绝对尺度头

加载阶段一最佳 checkpoint，冻结 Encoder、几何投影、A2 Fusion 和 Decoder，并设为 `eval`。用 `no_grad` 计算固定的 `Z`，只让 `L_pmax` 更新 PMaxHead。

当前训练起点仍为：

```text
optimizer: Adam
learning rate: 2e-4
epochs: 20
scheduler: ReduceLROnPlateau(factor=0.1, patience=2)
```

这些训练超参数属于 A4 的 V0 起点，不是经消融证明的最优值。

## 6. 陌生样本的绝对复场重建

面对没有标签的新输入：

```text
m_hat = max_{r in brain_eval_mask}
        sqrt(q_Re_hat(r)^2 + q_Im_hat(r)^2)

scale_hat = A_hat / (m_hat + eps_recon)

Re_abs_hat(r) = scale_hat * q_Re_hat(r)
Im_abs_hat(r) = scale_hat * q_Im_hat(r)

eps_recon = 1e-8
```

这就是“把绝对声压赋到相对声压最大点上”的严格实现：不是只修改最大点，而是用同一个正标量缩放整个复场。这样保持所有体素之间的相对幅值以及 `Re/Im` 所表达的相位。

`m_hat` 理想情况下接近 1；显式除以 `m_hat` 可消除主网络输出未严格达到单位峰值造成的整体尺度漂移。必须记录 `m_hat` 的验证分布；若它长期接近 0 或明显异常，说明主网络失败，不能依靠 A4 掩盖。

多阵元相干叠加只使用重建后的：

```text
p_abs_hat = Re_abs_hat + i*Im_abs_hat
```

单独的 `A_hat` 没有空间与相位信息，不能相干叠加；单独的 `q_hat` 没有绝对尺度，也不能用于绝对阵列声压。

## 7. 过拟合纠错与暂存 idea

若大 MLP 在排除数据泄漏、划分、学习率和损失实现问题后仍出现稳定过拟合，改用：

```text
[B,128,3,3,3]
AdaptiveAvgPool3d(1) -> [B,128]
AdaptiveMaxPool3d(1) -> [B,128]
concat                -> [B,256]
Linear(256,128) + ReLU
Linear(128,64)  + ReLU
Linear(64,1)    + Softplus
```

“最高 500 个体素平均”只保留为 `P_high_tail` idea，不替代严格 `A_gt=Pmax_brain`。

## 8. 依据与边界

- 用户 2026-07-25 明确确认：主网络一直预测逐样本归一化的相对复场；A4 必须保留并用于恢复陌生样本的绝对声压。
- TUSNet：Naftchi-Ardebili et al., *A deep-learning model for one-shot transcranial ultrasound simulation and phase aberration correction*, https://doi.org/10.1002/mp.70259；其“归一化场 + 独立压力尺度”提供邻近方法证据。
- TUSNet PressureDecoder：https://github.com/kbp-lab/TUSNet/blob/main/src/tusnet/PressureDecoder.py 。
- 当前结构入口：`A1_depth_width.md`、`A2_geometry_conditioning_decision.md`、`A2b_layer_design.md`、`A3_reim_output_head_decision.md`。

边界：

1. TUSNet 的二维权重不能迁移；本项目预测三维复场，并用同一个尺度同时重建 `Re/Im`。
2. A4 的误差会等比例进入整个绝对复场；必须分别报告相对场误差、A4 尺度误差和最终绝对复场误差。
3. 当前 `A_gt` 域为 `brain_eval_mask`；更换为整个颅内或其他域将改变 label 和重建协议，必须新建版本。
4. 主网络归一化只改变学习参数化，不改变底层仿真标签仍需保存绝对 Pa 与统一相位参考的要求。
