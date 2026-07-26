# Green 路线实验依据

```text
status: research_complete_route_frozen
as_of: 2026-07-20
purpose: 为后续 Green 复声场实验提供可追踪的论文、代码和结论边界
project_target: 固定 MIDA / 500 kHz / 有限阵元 / 位置与法向变化 / 绝对 Re-Im 复声压
hard_gate: 未列入“准入复现目标”的代码不得用于路线生死判断
```

## 先看结论

1. **未找到原 GreenONet 的官方代码或达到 B 级的第三方复现。**检索覆盖原论文、作者机构页、作者公开 GitHub、学位论文、GitHub 仓库搜索、Zenodo / GitLab / 普通搜索；“未找到”不等于绝对不存在，但当前不能据此启动复现。
2. 同组直接后续只有多级 GreenONet 会议稿 / 摘要；实证仍是 **1D Poisson**，没有 3D、频域复场或声学有限阵元代码。
3. 找到了可原样复现的邻近方法，但**没有一个公开实现同时覆盖**：复数频域、3D 异质介质、有限孔径、可变阵元位置与法向。
4. 因此，当前自写 Fourier-SiLU V2 不能杀死 Green 路线；同样，邻近方法原样复现成功也不能证明项目路线可行。
5. `GreenLearning`、`GF-Net` 和 `SIREN` 的作者示例只在用户明确要求“教育性原样复现”时允许运行；它们不是当前 mission，成功或失败都不能回答项目可行性。项目版复场 V2 仍为 `blocked_by_missing_direct_source`。

## 2026-07-20 路线裁决

- 当前不重做自写 V2，不设计新的 Green 项目网络，不生成新的颅骨训练标签。
- 保留的是固定频率复声压 Green 表示以及“单阵元复响应 + 网络外相干叠加”的物理分解；冻结的是缺少直接来源的 GreenONet 项目适配实现。
- 原样复现邻近低维方法只能用于学习和核查论文代码，不能作为项目路线的替代验证。
- 完整裁决、边界和解冻条件见 `ROUTE_DECISION.md`。

## 来源等级

```text
S: 原论文作者 / 机构官方仓库，论文与仓库互链
A: 同组官方后续，或身份基本可核对但论文未反向链接的作者实现
B: 可核对论文结构、配置、指标和结果的第三方复现
C: 邻近方法的官方实现，只提供迁移依据
X: 缺许可证、缺核心代码、任务不符或来源链不足；不得运行或据此下路线结论
```

## 第一圈：GreenONet 直接证据

| ID | 论文 / 证据 | 代码结论 | 能证明什么 | 不能证明什么 |
|---|---|---|---|---|
| D01 | [原 GreenONet](https://arxiv.org/abs/2307.13902), Aldirany et al., 2023/2024 | 原文无代码链接；精确标题、arXiv ID、方法名及作者入口均未找到可核对实现 | 物理约束 FNN 学 `G(x,t,ξ)`，对初始位移积分；实验仅 1D/2D、均匀/异质时域波动 | 不能证明固定频率复声压、3D、有限阵元或位置/法向泛化 |
| D02 | [多级 GreenONet 会议稿](https://www.scipedia.com/wd/images/a/aa/Draft_Sanchez_Pinedo_111518280130.pdf), Aldirany et al., WCCM 2024 | 未找到代码、数据、环境或权重 | 多级残差修正可在 1D Poisson 降低误差 | 不能证明已经跨到波动方程；作者明确说朴素逐级修正会在小尺度过拟合，需要很大的训练函数族 |
| D03 | [PolyPublie 博士论文](https://publications.polymtl.ca/58312/), Aldirany, 2024 | 全文及附件未发现代码声明或仓库入口 | 汇总原 GreenONet 与多级方法；把多级 GreenONet 定位为未来扩展基础 | 不是 3D / 复声场实现证据 |
| D04 | [DTE/AICOMAS 2025 摘要](https://dte_aicomas_2025.iacm.info/event/contribution/c3f844ea-970a-11ef-ba01-000c29ddfc0c) / [CMS 2025 摘要](https://www2.cms.math.ca/Events/summer25/res/pdf/caf-cb.pdf) | 只有摘要，未找到新增代码或新实验 | 作者组仍在讨论多级 GreenONet | 未提供超出 1D Poisson 的实证 |
| D05 | 第三方复现 | 未找到达到 B 级的复现 | 当前没有可审计的直接替代实现 | 不能用相似自写网络冒充原论文复现 |

### 对后续实验最尖锐的原文约束

- 原论文只报告一、二维数值实验，并非“理论写了 `d=1,2,3` 就已经验证 3D”。
- 多级后续使用每级 `5000 Adam + 300–400 L-BFGS`，并为每一级使用 `5000` 个训练函数；这与旧 V2 的 `600 steps` 不是同一训练强度。
- 多级后续原文报告：直接用连续 Green 修正会因小尺度泛化需要极大的训练函数族而过拟合；高频修正不是免费收益。

## 第二圈：可获得实现与排除理由

| ID | 方法 / 固定版本 | 等级 / 许可证 | 原任务与代码完整性 | 项目价值 | 致命缺口 / 处置 |
|---|---|---|---|---|---|
| N01 | [论文](https://www.nature.com/articles/s41598-022-08745-5) / [GreenLearning 代码](https://github.com/NBoulle/greenlearning), `v1.0` / `6659df915b56cb5d320f07b4f3f46286fca4060d` | S / Apache-2.0 | 作者论文互链；包、训练、数据生成、数据、文档、Zenodo 齐全；1D/2D 实数线性 PDE | 最干净的“从输入—输出对学习 Green 核”复现起点 | 1D Helmholtz 示例是实数 ODE；无 3D、复数、源姿态和有限孔径 |
| N02 | [论文](https://proceedings.mlr.press/v190/teng22a.html) / [GF-Net 代码](https://github.com/sloooWTYK/GF-Net), `e81e04e1c91df919ebeeff9df58e70711efc02fc` | S / MIT | PMLR 与仓库互链；模型、训练、测试、网格齐全；2D Poisson / reaction-diffusion，域分解 + 物理损失 | 审查奇异点、边界和域分解的来源实现 | 训练命令为 `20000 Adam + 10000 L-BFGS`；无环境锁定、权重和复数 Helmholtz |
| N03 | [GreenMGNet](https://github.com/linye-boli/GreenMgNet), `8f3d2b2c4db801b51cfb2631e98c5c130ccb7b01` | A* / MIT | 代码、脚本、notebook、结果和论文问题高度一致 | 分段核 + MLMI 可审查 Green 奇异性和积分成本 | 论文未反向链接仓库、账户身份未完全核实；仅 1D/2D 椭圆问题，暂不进入准入名单 |
| N04 | [论文](https://arxiv.org/abs/2006.09661) / [SIREN 代码](https://github.com/vsitzmann/siren), `4df34baee3f0f9c8f351630992c1fe1f69114b5f` | C / MIT | 作者官方代码；含 Helmholtz 与 wave equation 脚本、环境和论文数据 | 给“Green + INR”中的高频坐标表示提供原样复现依据 | 它拟合单个场 / 解 PDE，不学习阵元条件化 Green 算子，也不是复数 3D 经颅模型 |
| N05 | [论文与代码声明](https://repository.kaust.edu.sa/items/06d3ef00-5dcc-4450-8a82-954f7263155e) / [Gabor wavefield 代码](https://github.com/summerwine668/PINNbasedgabor), `cba3a7329ff0b5121c4fe7df507b01721717537d` | C / MIT | 作者机构页反向链接；2D 高频 Helmholtz、环境、训练和数据入口齐全 | 直接支持“波友好基函数比普通 MLP 更值得审查” | 作者实验使用 A6000；单实例 PINN，不是 Green 算子或有限阵元 surrogate，暂不列首轮目标 |
| N06 | [GreensONet](https://github.com/hangjianggu/GreensONet), `3428d05af23fcaf318978edc2e6ad2eb64d7acba` | X / 无许可证 | 有 3D 四面体网格、训练、推理、数据和权重；Poisson / 热 / Stokes | 证明另一团队做过 3D Green 积分架构 | 无许可证；无波动、复数和源姿态，禁止运行 |
| N07 | [Neural Green's Functions](https://github.com/KAIST-Visual-AI-Group/NGF), `c8029bde9f800e65d740e5a60fad7b796dc1bb6d` | X / 无许可证 | NeurIPS 2025 官方实现；3D Poisson / 热、点云几何、权重和 150 GB 数据 | 证明 3D 几何条件 Green-inspired operator 并非空想 | 训练区仍标 WIP，README/TODO 不一致；无许可证、无波动复场，禁止运行 |
| N08 | [Neural Green's Operators](https://github.com/JoostHMPrins/ngo), `6276932b51382a5510a662bb8a510822f35561f3` | X / 仅版权声明 | 参数化 Green 表示、扩散示例、训练 notebook | 可启发“介质参数 → Green 算子” | `license` 无使用许可条款；无 Helmholtz 复场，禁止运行 |
| N09 | [DeepGreen](https://github.com/sheadan/DeepGreen), `ec0d0568a4f0e0177f558eac7f2bb01a57d4711e` | X / 无许可证 | 论文反向链接；非线性 BVP 的双自编码器、数据和脚本 | 说明 Green 思想可与潜空间线性化结合 | 任务、表示与项目均不同，且无许可证，禁止运行 |
| N10 | [PIBI 声场重建](https://github.com/steDamiano/pibi-sfr), `3a8bf60271611656eaa78ef49296a06f8011556d` | X / MIT | 2D/3D Helmholtz 边界积分、声压场、完整环境和脚本 | 提供复数声压 / Helmholtz 边界积分的实现证据 | 是“麦克风测量 → 声场”的逆重建，不是“源几何 → 场”的 forward surrogate；按范围排除 |
| N11 | [BI-GreenNet](https://arxiv.org/abs/2204.13247) / [Deep Generalized Green's Function](https://arxiv.org/abs/2306.02925) | X / 未找到代码 | 论文分别处理已知奇异部分和广义 Green 函数 | 是奇异性处理的论文证据 | 无可审计公开训练实现，不得补写替代代码 |

## 历史准入复现目标（当前冻结）

这些目标曾通过来源审计，但当前没有活跃 mission。只有用户重新明确要求教育性原样复现时才可运行；尚未授权项目数据适配、复数输出头或网络拼接。

| 优先级 | 固定来源 | 首个原样示例 | 能验证什么 | 不能验证什么 | 状态 |
|---:|---|---|---|---|---|
| 1 | GreenLearning `v1.0` / `6659df91` | 官方 1D Helmholtz 示例 | 官方 Green 核学习是否能在本机复现；训练曲线和 Rational NN 的效果 | 项目复场、3D、姿态泛化；成功或失败都不能给项目路线下生死状 | dormant_user_approval_required |
| 2 | GF-Net `e81e04e` | README 的 2D square Poisson 最小训练 / 测试 | 物理损失、域分解和 Green 公式链路是否可复现 | 复数 Helmholtz、有限孔径、MIDA；资源过大时可在运行前停 | dormant_user_approval_required |
| 3 | SIREN `4df34bae` | 官方 `train_helmholtz.py`，随后才是 `train_wave_equation.py` | 高频坐标表示的作者结果与本机训练行为 | 不是 Green 算子，不验证阵元位置/法向条件化 | dormant_user_approval_required |

### 可直接复制的来源卡

```text
# R1 GreenLearning Helmholtz
method_source: https://doi.org/10.1038/s41598-022-08745-5
implementation_source: https://github.com/NBoulle/greenlearning
source_commit_or_release: 6659df915b56cb5d320f07b4f3f46286fca4060d
reproduction_level: unchanged
changes_from_source: none; only paths and device may change
claim_boundary: official 1D real Helmholtz Green-learning reproduction only

# R2 GF-Net square Poisson
method_source: https://proceedings.mlr.press/v190/teng22a.html
implementation_source: https://github.com/sloooWTYK/GF-Net
source_commit_or_release: e81e04e1c91df919ebeeff9df58e70711efc02fc
reproduction_level: unchanged
changes_from_source: none; environment repair must be relabeled environment_port
claim_boundary: official 2D real elliptic Green-function reproduction only

# R3 SIREN Helmholtz
method_source: https://arxiv.org/abs/2006.09661
implementation_source: https://github.com/vsitzmann/siren
source_commit_or_release: 4df34baee3f0f9c8f351630992c1fe1f69114b5f
reproduction_level: unchanged
changes_from_source: none; environment repair must be relabeled environment_port
claim_boundary: official single-wavefield INR reproduction; not a Green operator test
```

### 首轮最重要的基准事实

GreenLearning 官方 Helmholtz 示例默认使用 `1000 Adam + 最多 50000 L-BFGS-B`，Rational NN 报告 Green 函数相对误差 `0.9%`，ReLU 为 `5.3%`。这说明旧 V2 的 `600 steps` 只能评价其短预算自写实现，不能据此声称有限孔径 Green 映射不可学习。

## 项目 V2 的当前门禁

```text
project_v2_status: blocked_by_missing_direct_source
reason:
  没有找到可原样复现、同时支持复数频域 + 3D异质介质
  + 有限孔径 + 可变位置/法向的公开 Green / 单源响应实现。
forbidden:
  将 GreenLearning、SIREN、Gabor 或自写源编码器拼接后，
  继续以论文复现名义给 Green 路线下生死结论。
```

若以后要解除门禁，至少满足其一：

1. 找到直接覆盖上述任务的作者代码 / 合格复现；
2. 用户明确批准“基于已复现组件的自定义改造”，并接受它只能评价该改造，不能单独判死 Green 数学路线；
3. 先原样复现一个 Green 核方法和一个官方波场 INR，再由新的论文依据定义唯一改动项，逐层验证，禁止一次拼出新架构。

## 每次运行必须复制的来源字段

```text
method_source:
implementation_source:
source_commit_or_release:
reproduction_level: unchanged | environment_port | data_adapter | custom
changes_from_source:
claim_boundary:
```

`custom` 只能做工程探索，必须使用自定义名称，不能用于论文方法或 Green 路线的生死判断。

## 检索完成说明

- 入口一：论文 / 学位论文 / 会议材料 → 代码与数据声明 → 作者 / 机构主页。
- 入口二：精确标题、arXiv ID、方法名、作者名 → GitHub / Zenodo / GitLab / 普通网页与仓库搜索。
- 第二轮没有产生新的 GreenONet 直接高等级候选；邻近实现控制为 11 项。
- 本轮未克隆仓库、未安装依赖、未运行训练，也未修改 `docs/decisions.md`。
