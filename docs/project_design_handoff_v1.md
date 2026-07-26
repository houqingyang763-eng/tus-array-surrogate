# Project Design Handoff v1

```yaml
snapshot_id: tus-array-surrogate-project-design-handoff-v1
snapshot_date: 2026-07-26
audience: Codex
status: current_stage_snapshot
repository_root: C:\Users\HOU\Desktop\tus-array-surrogate
source_concept: docs/project_concept_v7.md
purpose: 单文件恢复当前项目认知、设计接口、证据边界与待决问题
```

## 0. 读取协议

### 0.1 状态枚举

| 状态 | 严格含义 |
|---|---|
| `CONFIRMED` | 用户已明确确认，或当前权威项目文件已记录为稳定共识 |
| `V0_TEMPORARY` | 为推进第一版而固定的工程起点，不代表最优或已通过完整验证 |
| `EXPERIMENT_VERIFIED` | 本仓库实验在其记录条件内直接验证 |
| `ENGINEERING_ESTIMATE` | 计算、外推或工程探针支持，但不是目标条件下的正式实验 |
| `CANDIDATE` | 有来源或物理理由，尚未获准成为最终实现 |
| `UNKNOWN` | 当前缺少用户决定、统一协议或足够证据 |
| `SUPERSEDED` | 历史上曾采用，现已被明确替代 |
| `FROZEN` | 暂停推进；满足解冻条件前不得自行复活 |

禁止把 `V0_TEMPORARY`、`ENGINEERING_ESTIMATE`、`CANDIDATE` 或 `UNKNOWN` 改写为“已经证明”。

### 0.2 权威层级

发生冲突时依次采用：

1. 本快照中带 `CONFIRMED` 的 2026-07-26 用户确认；
2. [project_concept_v7.md](project_concept_v7.md)；
3. [initial_network_design](../experiments/initial_network_design/README.md) 中当前标为 `confirmed` 的组件决定；
4. [decisions.md](decisions.md)；
5. [questions.md](questions.md) 与 [ideas.md](ideas.md)；
6. v1-v6、旧实验方案和历史日志。

本文件是阶段性交接入口；源构想仍是 `docs/project_concept_v7.md`。未来改变当前合同，应新建 handoff 版本并标明替代关系，不静默覆盖本文件。

### 0.3 证据标签

```text
USER      用户明确确认
DOC       当前项目文档
PAPER     论文原文或作者材料
CODE      代码、数据或仓库静态证据
EXPERIMENT 本地运行结果
CALC      计算推导或工程外推
```

## 1. 项目合同

| ID | 状态 | 当前合同 | 依据 | 边界 |
|---|---|---|---|---|
| GOAL-01 | `CONFIRMED` | 建立面向 3D 经颅超声阵列初设计的单阵元 surrogate：预测相对复场与绝对尺度，重建单阵元绝对复场，再在网络外相干叠加。 | USER；DOC:v7/decisions | 不是临床级 full-wave solver 的无条件替代 |
| SCOPE-01 | `CONFIRMED` | 第一阶段固定 MIDA、`500 kHz` 和激励幅值，主要变化量是理想方向性点源的位置与法向。 | USER；DOC:decisions | 位置和法向范围仍为 `UNKNOWN` |
| SCOPE-02 | `CONFIRMED` | 单源网络不以 target focus 为条件。target 仅用于阵元相位/延迟、阵列组合和下游评价。 | USER:2026-07-26 | 延迟与评价公式尚未冻结 |
| SCOPE-03 | `CONFIRMED` | 输出覆盖指定的整个 `144³ mm³` 网络物理域，不采用焦点附近小 ROI 作为主输出。 | USER；DOC:T2/v7 | 不等同于完整全脑或临床安全覆盖 |
| SCOPE-04 | `CONFIRMED` | 当前不使用有限孔径、直径、发射表面、表面点集或圆盘 source mask。 | USER；DOC:A2a | 论文中的有限孔径结果不能迁移成本项目声源定义 |
| SCOPE-05 | `CONFIRMED` | 第一版不用 GAN、CBAM、Dropout、残差块或深监督。 | DOC:initial-network README/A2b | 以后只有出现针对已观察误差的证据才重新评估 |

## 2. 物理与数据合同

### 2.1 网络输入与坐标

| ID | 状态 | 接口 | 依据 | 边界 |
|---|---|---|---|---|
| DATA-01 | `CONFIRMED` | 网络介质输入为单通道三维声速场 `c(x,y,z)`，shape=`[B,1,288,288,288]`。 | USER:2026-07-26 | 只约束网络输入；不代表标签求解器只使用声速 |
| DATA-02 | `CONFIRMED` | 点源条件 `g=(x,y,z,nx,ny,nz)`，shape=`[B,6]`。 | USER；DOC:A2a | 不携带目标点、孔径或独立激励相位 |
| DATA-03 | `CONFIRMED` | `(x,y,z)` 按同一全局物理域逐轴缩放至 `[-1,1]`；`(nx,ny,nz)` 是单位法向；介质、源与输出共享全局坐标系。 | DOC:A2a | 坐标原点、轴向和数组索引约定仍须进入正式数据协议 |
| DATA-04 | `UNKNOWN` | 点源允许的位置范围、法向范围、真实最大传播路径和无效几何规则。 | DOC:questions | 关闭条件：用户确认几何范围，并用标签源定义检查可实现性 |
| DATA-05 | `UNKNOWN` | 标签求解器最终使用声速、密度、吸收、剪切或其他参数中的哪些量。 | DOC:questions | 关闭条件：冻结求解器方程、材料参数表和实现版本 |

### 2.2 域、网格与 mask

| ID | 状态 | 接口 | 依据 | 边界 |
|---|---|---|---|---|
| GRID-01 | `V0_TEMPORARY` | 物理域=`144×144×144 mm³`；各向同性 `Δx=Δy=Δz=0.5 mm`；网络网格=`288³`。 | USER；DOC:T2 | 允许推进 V0，不等于绝对相位和界面误差已收敛 |
| GRID-02 | `V0_TEMPORARY` | `500 kHz`、软组织约 `1500 m/s` 时约为 6 PPW。 | PAPER:DeepTFUS；CALC | MIDA 最短有效波长和最终 solver 收敛仍待验证 |
| GRID-03 | `CONFIRMED` | 主网络学习整个网络物理域的相对复场；`brain_eval_mask` 不裁剪网络输出。 | DOC:T2/A4 | 脑内归一化与评价不等于只预测脑内 |
| MASK-01 | `CONFIRMED` | `source.p_mask`=求解器源注入；`sensor.mask`=记录位置；`brain_eval_mask`=尺度、label、重建和脑内指标；`Z`=网络瓶颈。四者不得混用。 | DOC:A4 | mask 的正式生成协议仍为 `UNKNOWN` |
| MASK-02 | `CONFIRMED` | 标签仿真采用域外 PML：`PMLInside=false`。 | DOC:A4 | PML 厚度、材料和离散协议仍须冻结 |
| MASK-03 | `CONFIRMED` | 有效几何要求 `source.p_mask` 不与 `brain_eval_mask` 或 `skull_mask` 重叠。 | DOC:A4 | 不能据此任意排除所有邻近体素 |

### 2.3 绝对标签与相对标签

基础求解器必须保存同一幅值、相位参考和 Pa 单位下的绝对复场：

```text
p_gt(r) = Re_gt(r) + i Im_gt(r)
amp_gt(r) = sqrt(Re_gt(r)^2 + Im_gt(r)^2)

A_gt = max_{r in brain_eval_mask} amp_gt(r)
q_Re_gt(r) = Re_gt(r) / A_gt
q_Im_gt(r) = Im_gt(r) / A_gt
```

| ID | 状态 | 当前合同 | 依据 | 边界 |
|---|---|---|---|---|
| LABEL-01 | `CONFIRMED` | `A_gt` 是 `brain_eval_mask` 内稳态基频复幅值的严格最大值，即 `Pmax_brain`。 | USER；DOC:v7/A4 | 不使用时域 `sensor.record={'p_max'}` 直接代替 |
| LABEL-02 | `CONFIRMED` | A3 label 是逐样本归一化的无量纲 `q_Re_gt/q_Im_gt`。 | USER；DOC:v7/A3/A4 | 不能把 `q` 当绝对 Pa |
| LABEL-03 | `CONFIRMED` | A4 使用训练集统一尺度 `P_ref=max(A_gt over training set)`，`y_gt=A_gt/P_ref`；`P_ref` 写入 checkpoint。 | DOC:A4 | `P_ref` 只由训练集计算，避免数据泄漏 |
| LABEL-04 | `UNKNOWN` | 绝对激励幅值、相位零点、Fourier 正负号、Pa 标定、复幅值提取窗口和 `brain_eval_mask` 版本。 | DOC:v7/questions | 关闭条件：形成版本化数据协议并用确定性示例验收 |

## 3. 网络合同

### 3.1 总体数据流

```text
c [B,1,288,288,288] -> Encoder -> F [B,128,9,9,9] -----\
                                                           -> A2 Fusion -> Z
g [B,6] -> Linear -> broadcast [B,128,9,9,9] ------------/

Z -> Decoder -> A3 -> q_hat [B,2,288,288,288]
Z -> A4 PMaxHead -> y_hat [B,1] -> A_hat=P_ref*y_hat
```

### 3.2 T2：尺寸、精度与 batch

| ID | 状态 | 设置 | 依据 | 边界 |
|---|---|---|---|---|
| T2-01 | `V0_TEMPORARY` | 网络前向使用 BF16 自动混合精度；数据损失和物理损失转 FP32。 | USER；DOC:T2 | 物理差分不允许默认用 BF16 |
| T2-02 | `V0_TEMPORARY` | native batch=`1`。 | USER；DOC:T2 | 梯度累积尚未冻结 |
| T2-03 | `ENGINEERING_ESTIMATE` | 当前五层候选对 `288³` 的规划峰值为 `18.474 GiB`，含 15% 余量。 | CALC；CODE:t2 probes | 从较小体素数外推，尚无 24 GB GPU 目标尺寸整步实测 |

### 3.3 A1：深度与宽度

```text
下采样次数: 5
通道: 8 -> 16 -> 32 -> 64 -> 128 -> 128
空间: 288 -> 144 -> 72 -> 36 -> 18 -> 9
当前记录参数量: 3,807,426
```

| ID | 状态 | 设置 | 依据 | 边界 |
|---|---|---|---|---|
| A1-01 | `CONFIRMED` | V0 采用上述五次下采样与通道序列。 | USER；DOC:A1 | 不是网络最优性的实验结论 |
| A1-02 | `ENGINEERING_ESTIMATE` | 当前块定义下每轴理论感受野约 `380–412` 体素，超过 `288` 输入边长并被边界截断。 | CALC:A1 | 理论感受野不等于训练后的有效感受野 |
| A1-03 | `UNKNOWN` | 实际源—评价点路径分布、真实最大路径以及模型有效感受野。 | USER:撤回 `82 mm` 已知边界 | 关闭条件：几何协议统计 + 输入梯度或遮挡探针 |

### 3.4 A2a：六维几何瓶颈条件化

```text
F: [B,C_b,D_b,H_b,W_b]
g: [B,6]
 -> Linear(6,C_b,bias=true)
 -> ReLU(inplace=true)
 -> [B,C_b]
 -> reshape/expand [B,C_b,D_b,H_b,W_b]

concat(F,g_feature,dim=channel)
 -> [B,2C_b,D_b,H_b,W_b]
 -> Conv3d(2C_b,C_b,kernel_size=1,bias=false)
 -> GroupNorm(C_b/8,C_b,eps=1e-5,affine=true)
 -> ReLU(inplace=true)
 -> Z
```

当前 `C_b=128`，所以 `Z=[B,128,9,9,9]`、`GroupNorm(16,128)`。

| ID | 状态 | 设置 | 依据 | 边界 |
|---|---|---|---|---|
| A2A-01 | `CONFIRMED` | 使用 `Linear -> broadcast -> concat -> 1×1×1 Conv -> GN -> ReLU`。 | USER；DOC:A2a；PAPER:Jang 为邻近证据 | 融合细节是本项目实现补全，不声称是 Jang 原实现或最优方案 |
| A2A-02 | `CONFIRMED` | Linear 与融合卷积用 ReLU 匹配的 Kaiming normal；Linear bias=0；GN weight=1,bias=0。 | DOC:A2a | 只适用于当前 A2a |

### 3.5 A2b：编码器与解码器块

```text
每级两次:
Conv3d(k=3,s=1,p=1,dilation=1,groups=1,bias=false,padding_mode=zeros)
-> GroupNorm(每组8通道,eps=1e-5,affine=true)
-> LeakyReLU(negative_slope=0.01,inplace=true)

down: MaxPool3d(k=2,s=2,p=0,dilation=1,ceil_mode=false)
up: ConvTranspose3d(k=2,s=2,p=0,output_padding=0,bias=false)
skip: encoder post-activation/pre-pool -> concat(dim=1) -> 双卷积块
```

| ID | 状态 | 设置 | 依据 | 边界 |
|---|---|---|---|---|
| A2B-01 | `CONFIRMED` | GroupNorm 每组 8 通道：`C=8/16/32/64/128 -> groups=1/2/4/8/16`。 | USER；DOC:A2b | 小 batch 条件下的 V0 选择，不是消融最优 |
| A2B-02 | `CONFIRMED` | 卷积与转置卷积使用 `kaiming_normal_(a=0.01,mode=fan_in,nonlinearity=leaky_relu)`；GN weight=1,bias=0。 | DOC:A2b | 不重复调用网络整体默认初始化 |
| A2B-03 | `CONFIRMED` | 转置卷积后、concat 前无额外激活或归一化；skip 不裁剪、不额外卷积。 | DOC:A2b | 依赖各轴可被 `2^5` 整除 |

### 3.6 A3：相对复场输出头

```text
decoder feature: [B,8,288,288,288]
-> Conv3d(8,2,k=3,s=1,p=1,bias=true)
-> q_hat [B,2,288,288,288]

channel 0 = q_Re
channel 1 = q_Im
```

| ID | 状态 | 设置 | 依据 | 边界 |
|---|---|---|---|---|
| A3-01 | `CONFIRMED` | 共享 U-Net 直接输出两个相对复数分量。 | USER；DOC:A3；PAPER:FEUNet 为邻近证据 | 不采用两个 U-Net 或拆分小头 |
| A3-02 | `CONFIRMED` | 输出层无 normalization/activation；bias=true；Xavier normal gain=1；bias=0。 | DOC:A3 | 输出正负均不受限；归一化属于 label 协议 |

### 3.7 A4：绝对尺度头

```text
Z [B,128,9,9,9]
-> Conv3d(128,128,k=3,s=2,p=1) + GroupNorm(8,128) + ReLU
-> [B,128,5,5,5]
-> Conv3d(128,128,k=3,s=2,p=1) + GroupNorm(8,128) + ReLU
-> [B,128,3,3,3]
-> Flatten [B,3456]
-> Linear: 3456->2048->1024->512->256->128->64->1
-> ReLU after hidden layers; Softplus on scalar
-> y_hat [B,1]
```

| ID | 状态 | 设置 | 依据 | 边界 |
|---|---|---|---|---|
| A4-01 | `CONFIRMED` | A4 从共享条件化瓶颈 `Z` 预测陌生样本的绝对尺度。 | USER；DOC:A4；PAPER:TUSNet 为邻近证据 | A4 不是可删除的附属指标 |
| A4-02 | `V0_TEMPORARY` | 当前约 `10.76M` 参数的大 MLP 暂保留。 | DOC:A4 | 有过拟合风险；只有排除泄漏、划分、学习率和损失问题后才触发轻量头 |
| A4-03 | `CONFIRMED` | `y_hat` 使用正标量 Softplus；`A_hat=P_ref*y_hat`。 | DOC:A4 | 不提供空间或相位信息，不能单独相干叠加 |

## 4. 训练、损失与推理

### 4.1 两阶段训练

| ID | 状态 | 设置 | 依据 | 边界 |
|---|---|---|---|---|
| TRAIN-01 | `CONFIRMED` | 阶段一更新 Encoder、几何投影、A2 Fusion、Decoder/A3；PMaxHead 不参与。 | DOC:A4 | L1 数据损失与 Helmholtz 权重仍为 `UNKNOWN` |
| TRAIN-02 | `CONFIRMED` | 阶段二加载阶段一最佳 checkpoint，冻结并 `eval` 主干，用 `no_grad` 计算 `Z`，只训练 PMaxHead。 | DOC:A4 | 联合微调不是当前合同 |
| TRAIN-03 | `V0_TEMPORARY` | A4 起点：Adam、`2e-4`、20 epochs、ReduceLROnPlateau(`factor=0.1`,`patience=2`)。 | DOC:A4 | 未经消融，不得称为最优 |
| TRAIN-04 | `UNKNOWN` | 主网络 optimizer、learning rate、gradient accumulation、scheduler、early stopping。 | DOC:checklist | 关闭条件：结构与损失固定后的最小学习率/调度比较 |

### 4.2 A4 损失

```text
r = log((y_hat + 1e-8) / (y_gt + 1e-8))
delta = log(1.10)

L_pmax =
    0.5*r^2                              if |r| <= delta
    delta*(|r| - 0.5*delta)              otherwise
```

| ID | 状态 | 设置 | 依据 | 边界 |
|---|---|---|---|---|
| LOSS-A4-01 | `CONFIRMED` | A4 使用上述 log-ratio Huber。 | DOC:A4 | 最终验收阈值仍为 `UNKNOWN` |
| LOSS-DATA-01 | `UNKNOWN` | A3 基础数据损失尚未从 MSE、MAE、相对复数 L2 或组合中确定。 | DOC:checklist | 关闭条件：固定 split 和指标后做最小同协议比较，并由用户冻结 |
| LOSS-PHY-01 | `CANDIDATE` | 三维离散 Helmholtz-PML 残差是核心物理损失候选。 | USER；PAPER:FEUNet/3D Helmholtz schemes | 尚无本项目 3D 方向性点源实现与独立验证 |
| LOSS-PHY-02 | `CONFIRMED` | 若阶段一使用绝对源项，先计算 `p_hat_for_physics=A_gt*(q_Re_hat+i*q_Im_hat)`。 | USER；DOC:v7/A4 | 不得把绝对源项直接作用于无量纲 `q_hat` |
| LOSS-PHY-03 | `UNKNOWN` | 离散格式、变密度/吸收形式、PML、源附近处理、配置点、归一化与权重。 | DOC:questions | 关闭条件：绑定来源、与标签协议一致，并通过已知场和独立求解器验证 |
| LOSS-STRUCT-01 | `CANDIDATE` | 梯度、频谱或区域加权损失只在观察到明确结构性错误后考虑。 | DOC:checklist | 不预先加入第三损失 |

### 4.3 陌生样本绝对复场重建

```text
A_hat = P_ref * y_hat

m_hat = max_{r in brain_eval_mask}
        sqrt(q_Re_hat(r)^2 + q_Im_hat(r)^2)

scale_hat = A_hat / (m_hat + eps_recon)
eps_recon = 1e-8

Re_abs_hat(r) = scale_hat * q_Re_hat(r)
Im_abs_hat(r) = scale_hat * q_Im_hat(r)
p_abs_hat(r) = Re_abs_hat(r) + i Im_abs_hat(r)
```

| ID | 状态 | 当前合同 | 依据 | 边界 |
|---|---|---|---|---|
| RECON-01 | `CONFIRMED` | 同一个正标量缩放整个 `q_Re/q_Im` 场，不是只修改最大点。 | USER；DOC:v7/A4 | 保留预测相位和相对空间分布 |
| RECON-02 | `CONFIRMED` | `m_hat` 应记录验证分布；接近 0 或长期异常表示主网络失败，不能由 A4 掩盖。 | DOC:A4 | 异常阈值仍为 `UNKNOWN` |
| RECON-03 | `CONFIRMED` | 阵列叠加只使用 `p_abs_hat`。 | USER；DOC:v7/A4 | `q_hat` 和 `A_hat` 单独均不足 |

### 4.4 网络外阵列组合

```text
p_array_hat(r) = Σ_j w_j * exp(i*phi_j) * p_abs_hat_j(r)
```

| ID | 状态 | 当前合同 | 依据 | 边界 |
|---|---|---|---|---|
| ARRAY-01 | `CONFIRMED` | 多阵元场采用外部复数幅相加权和。 | USER；DOC:decisions | 依赖线性声学和阵元独立响应近似 |
| ARRAY-02 | `EXPERIMENT_VERIFIED` | 四阵元 k-Wave benchmark 最差复场相对 L2=`5.81e-6`，低于 `1e-4` 验收线。 | EXPERIMENT:elementwise_superposition | 只验证物理重组；不验证网络、非线性、热效应或硬件耦合 |
| ARRAY-03 | `UNKNOWN` | target 复压到相位/延迟的映射、固定频率周期多解、幅值权重和阵列指标定义。 | DOC:questions | 关闭条件：版本化公式、单位测试和独立仿真验收 |

## 5. 验证与验收合同

| ID | 状态 | 必须报告 | 关闭条件 |
|---|---|---|---|
| EVAL-01 | `CONFIRMED` | 相对复场误差、A4 尺度误差、最终绝对复场误差必须分开。 | 每组误差有独立指标与验证分布 |
| EVAL-02 | `UNKNOWN` | 全场复数相对 L2、幅值误差、相位误差、目标点复压误差的具体实现和阈值。 | 固定 mask、零幅值处理、统计方式和接受阈值 |
| EVAL-03 | `UNKNOWN` | `P_target`、`P_peak/pmax`、focus error、side-lobe ratio、脑内最大压力统计。 | 形成版本化指标协议并用确定性场单元测试 |
| EVAL-04 | `UNKNOWN` | 位置插值、位置外推、新法向泛化的数据划分。 | 先冻结采样域，再建立无泄漏 split |
| EVAL-05 | `UNKNOWN` | `0.5 mm` 标签网格收敛。 | 更细网格对照；比较绝对复场、相位、界面与下游指标 |
| EVAL-06 | `UNKNOWN` | `288³/batch1` 在 24 GB GPU 上的完整训练步。 | 前向、FP32 losses、反向和 optimizer step 均成功并记录峰值 |
| EVAL-07 | `UNKNOWN` | A4 是否稳定过拟合及轻量头触发条件。 | 排除泄漏和训练问题后，观察可重复 train-validation gap |

## 6. 证据门禁与路线状态

| ID | 状态 | 路线/证据 | 允许的结论 | 禁止的结论 |
|---|---|---|---|---|
| GATE-01 | `EXPERIMENT_VERIFIED` | elementwise superposition | 当前线性设置下单源复场可高精度重组多源场 | 神经网络已能准确预测单源场 |
| GATE-02 | `FROZEN` | GreenONet 项目适配 | 保留 Green 分解和单源叠加的物理启发 | 无作者实现时自写网络并借 GreenONet 名称裁决路线 |
| GATE-03 | `FROZEN` | 历史 Fourier-SiLU Green V2 | 该自定义配置在当时协议下失败 | Green 数学、INR 或所有 Green 网络均失败 |
| GATE-04 | `FROZEN` | DeepTFUS full training | 可作 3D 工程结构、数据与显存参考 | 已复现或已证明适配当前相对复场+A4任务 |
| GATE-05 | `CANDIDATE` | FEUNet | 支持二维 Re/Im 与监督+Helmholtz 联合训练的邻近方法证据 | 直接证明 3D MIDA+方向性点源+PML 实现 |
| GATE-06 | `CANDIDATE` | Jang et al. 2025 | 支持六维位姿归一化、Dense 映射和瓶颈第二路输入 | 证明 VGG、VAE 或具体瓶颈融合对本项目最优 |
| GATE-07 | `CANDIDATE` | TUSNet | 支持“归一化场+独立尺度”的邻近设计 | 迁移其二维权重、损失权重或标量定义 |

正式仿真、训练或方法可行性实验必须绑定论文作者代码或经审计复现。显存、吞吐、张量形状、文件读写和确定性公式测试可以作为纯工程探针，但不能据此评价科研方法。

## 7. 被替代状态

| ID | 状态 | 历史内容 | 当前替代 |
|---|---|---|---|
| OLD-01 | `SUPERSEDED` | 低分辨率大区域 pmax 作为主网络输出 | 相对复场+A4尺度+绝对复场重建 |
| OLD-02 | `SUPERSEDED` | 主 U-Net 直接预测绝对 Re/Im | 主 U-Net 预测 `q_Re/q_Im`，A4 恢复尺度 |
| OLD-03 | `SUPERSEDED` | A4 是可删的 pmax 辅助指标 | A4 是绝对复场重建必需分支 |
| OLD-04 | `SUPERSEDED` | 有限孔径、圆盘或表面点集作为当前声源 | 六维条件的理想方向性点源 |
| OLD-05 | `SUPERSEDED` | `108×108×40 mm³` slab、`224×224×80`、native batch 2 | `144³ mm³`、`288³`、native batch 1 |
| OLD-06 | `SUPERSEDED` | `400³` 单通道作为当前网格合同 | 仅保留历史数据量估算 |
| OLD-07 | `SUPERSEDED` | 已知最大源—焦点路径为 `82 mm` | 最大路径为 `UNKNOWN`；五层结构仍是当前 V0 |
| OLD-08 | `SUPERSEDED` | target focus 是否进入网络保持未定 | target 只在网络外下游使用 |

## 8. 开放问题关闭顺序

未来 Codex 按以下依赖顺序提问或调研，不得跳过上游协议直接冻结下游超参数：

1. `Q-PHY-01`：标签求解器方程、介质参数、方向性点源数学定义、幅相和边界协议。
2. `Q-GEO-01`：点源位置/法向范围、无效几何、真实路径统计和数据 split。
3. `Q-DATA-01`：绝对复数标签、mask、单位、相位、Fourier 符号和版本化存储协议。
4. `Q-NUM-01`：0.5 mm 网格收敛与网络/标签/Helmholtz 网格一致性。
5. `Q-LOSS-01`：L1 数据损失 baseline。
6. `Q-PHYLOSS-01`：3D Helmholtz-PML 离散、独立验证、配置点和权重。
7. `Q-TRAIN-01`：主网络 optimizer、学习率、累积、调度与停止条件。
8. `Q-EVAL-01`：相对场、尺度、绝对场和阵列下游指标及阈值。
9. `Q-ARRAY-01`：target 相位/延迟、周期多解、幅值权重和阵列指标。

## 9. Repo 证据索引

### 当前入口

- [根 README](../README.md)
- [项目规则](../AGENTS.md)
- [当前源构想 v7](project_concept_v7.md)
- [稳定决定](decisions.md)
- [开放问题](questions.md)
- [项目记忆](memory.md)

### 第一版网络

- [initial_network_design README](../experiments/initial_network_design/README.md)
- [T2：网格、显存与 batch](../experiments/initial_network_design/T2_grid_memory_batch.md)
- [A1：深度与宽度](../experiments/initial_network_design/A1_depth_width.md)
- [A2a：几何条件](../experiments/initial_network_design/A2_geometry_conditioning_decision.md)
- [A2b：层结构](../experiments/initial_network_design/A2b_layer_design.md)
- [A3：相对复场头](../experiments/initial_network_design/A3_reim_output_head_decision.md)
- [A4：绝对尺度头](../experiments/initial_network_design/A4_pmax_auxiliary_head_decision.md)
- [待确定问题清单](../experiments/initial_network_design/question_checklist.md)

### 实验与路线门禁

- [四阵元叠加结果](../experiments/elementwise_superposition/RESULTS.md)
- [FEUNet 复现审计](../experiments/feunet_repro_audit/AUDIT_LOG.md)
- [Green 路线裁决](../experiments/green_complex_derisk/ROUTE_DECISION.md)
- [Green 来源证据](../experiments/green_complex_derisk/SOURCE_EVIDENCE.md)
- [DeepTFUS 运行日志](deeptfus_run_log.md)

## 10. Codex 查询接口

把本文件单独提供给 Codex 后，可直接询问：

```text
1. 列出所有 CONFIRMED 接口及对应 shape。
2. 列出实现第一版网络前仍阻塞的 UNKNOWN，按依赖排序。
3. 对某条 ID 给出状态、依据、边界和 repo 证据入口。
4. 判断一个新想法应进入 CONFIRMED、CANDIDATE、UNKNOWN 还是 FROZEN。
5. 检查某段新设计是否复活了 SUPERSEDED 路线。
6. 区分论文证明、代码/数据事实、本地实验事实和工程外推。
7. 生成实现清单时只展开 CONFIRMED 与明确标为 V0_TEMPORARY 的设置。
```

若 Codex 无法从本文件回答，应返回对应 `UNKNOWN` ID 和所需证据，不得补造项目参数。
