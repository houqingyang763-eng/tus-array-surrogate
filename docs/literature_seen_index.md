# 已知论文与方向检索清单

初始核对：2026-10-08；专题增量核查：2026-10-09—10。用途：讨论或检索新方向前先查重；允许重访和借鉴，但应明确说出“已有方向 + 本次新增内容”。

## 给 GPT / Codex 的使用规则

1. 提出“新论文 / 新道路”前，先查本文件的题名、简称、DOI 和方法关键词；同题、预印本/正式版、重复 Zotero 条目算同一工作。
2. 命中论文时标为“已知论文”；命中方法家族时标为“已有方向的延伸”。说明这次新增了哪项证据、机制或适用条件，再判断是否值得重访。
3. “已知 / 已收录”只表示进入过当前知识范围；不等于用户精读、完成实验或否定整个方向。下列“已有比较”指有旧报告记录；“摘要登记”指本次仅用 Zotero 摘要概括。
4. 未命中本表只表示“清单未收录”，仍需核对项目其他材料；不要直接宣布首次发现。需要细节时按来源入口读对应段落，不默认重读整篇 PDF。
5. 本表不是科学合同或实验授权。当前 V10 为颅外单点源→颅内复场形状；历史论文的 pmax、绝对尺度、阵列控制量、阵列叠加及迭代求解任务仅作检索背景。

## 覆盖与来源

- 实时读取 Zotero `tus_surrogate`（`29BGBFP3`）及全部 7 个子收藏夹：28 个不同顶层条目；3 个重复条目合并后，得到 24 篇论文 + 1 个非论文网页。各收藏夹均核对 API 总条数，无分页遗漏。
- 与 [2026-09-30 跨论文比较](zotero_cross_paper_comparison_20260930.md) 的 24 篇取并集：**27 篇论文**。旧报告中的 Fourier Features、Aubry 基准、Zhang 颅内定位这 3 篇目前未在上述收藏夹内，仍保留。
- P01–P24 的概览与边界压缩自旧报告对应 A/B/C 条目，本次未重新核验全文；P25–P27 仅据当前 Zotero 元数据与摘要。年份在预印本和正式版之间可能不同，按所列来源口径保留。
- `Z=` 为 Zotero 条目 key，可用 `zotero://select/library/items/KEY` 定位；它不是 BibTeX 引用键。`来源 A1` 等指旧报告原有编号。未删除、移动或合并 Zotero 实体条目。
- 2026-10-09架构专题追加P28–P44，共17篇，当前索引44篇；其中多篇已在旧方向材料出现，本次仅补录并定向核查，未操作Zotero。P26/P27补正文证据。阅读深度与去重依据见[专题检索记录](../experiments/survey&design/SEARCH_LOG.md)。P32/P33共享USCT结果，不能当两份独立实证。

## 方向速查：这些方法已经进入过讨论范围

| 关键词 / 方法家族 | 对应论文 | 再讨论时先看什么 |
| --- | --- | --- |
| 3D U-Net、cGAN、CT→声场、ROI、导航 | P01–P05、P25 | 实值包络与逐体素复场的任务差别 |
| 几何编码、Fourier、FiLM、动态卷积、交叉注意力 | P01、P15–P17 | 模块直接消融；不同输出任务的收益可能相反 |
| P0、自由场 / 背景场条件、散射场分解 | P07、P10、P25 | 背景场输入与散射输出分别贡献什么 |
| CBAM、GAN、GDL、高压加权、焦域损失 | P01、P03–P05 | 全场与焦域取舍；联合加入不算各项独立有效 |
| 长程传播、LSTM、多尺度 FNO / U-NO、频域算子 | P03、P07–P08 | 二维/三维、压力/位移、计算成本 |
| Helmholtz 物理残差、FD 嵌入、PINN | P06、P09–P11 | Label 与物理算子匹配；跨问题预测或逐题优化 |
| 高频课程、频率提升、神经元拆分 | P11 | 固定单频任务需要改造课程，而非直接照搬 |
| Green 核、DPSM、单元响应、线性叠加 | P12–P13、P23 | 初值算子、Green 张量与颅骨压力响应的区别 |
| 相位周期性、圆周分类、少样本适配 | P15 | 阵元控制量与体素相位；是否使用测试颅骨适配 |
| 多损失、梯度量级、PCGrad、任务共享/拆分 | P18–P20 | 量级失衡、方向冲突和负迁移分别处理 |
| 扩散 U-Net、scale-shift 条件化、分类器引导 | P21 | 图像生成指标与确定性物理场误差的区别 |
| 学习迭代器、神经预条件、FGMRES、多重网格 | P09、P26–P27 | 输出是解还是残差校正；迭代次数与总耗时 |
| Label 基准、物理验证、声电应用、逆向导航 | P14、P22、P24 | 仿真可信度、下游应用与场预测分开 |

## 论文清单

### P01 · DeepTFUS · Srivastav 2025

**A Skull-Adaptive Framework for AI-Based 3D Transcranial Focused Ultrasound Simulation**

三维 pseudo-CT + 换能器碗面点集→同域归一化实值 pmax。用 Fourier 几何编码、动态卷积、FiLM、交叉注意力注入声源条件，并加权高压区域。已有比较：高压加权改善焦点，但全场 L2 略差；FiLM 对峰值有负向结果，复杂模块不宜整体视为成功贡献。

来源 A1；Z=`F4SEHSN5`；arXiv=`2505.12998v1`；关键词：TFUScapes、几何条件、加权损失。

### P02 · Jang 2025 · ADNet / PPNet

**Deep learning-based real-time estimation of transcranial focused ultrasound acoustic field**

CT 经逐切片 VGG 特征压缩 + 换能器中心/朝向→三维局部实值压力分布；PPNet 另预测峰值尺度。已有比较：独立尺度头有直接正向结果；不是 Re/Im 输出，也不是全脑预测。ΔPPR 是经颅/自由场峰值比的差值，不能当普通峰值相对误差。

来源 A2；Z=`F7XDVZ97`；DOI=`10.1016/j.engappai.2025.111157`；关键词：瓶颈条件、分布与尺度分开。

### P03 · TUSNet · Naftchi-Ardebili · 2026 卷期

**A deep-learning model for one-shot transcranial ultrasound simulation and phase aberration correction**

二维 CT/阵元/目标/waveguide 画布→归一化包络 + 峰值标量 + 阵元校正向量。四方向 LSTM-Conv 聚合长程信息。已有比较：LSTM、waveguide 有正向消融；校正向量不是体素相位，“98.3%”也不是直接复场预测准确率。

来源 A3；当前 Z=`Q6S33JUG`,`VPTIYMLW`；旧报告另记 `A2RC7PSW`（本次不在目标收藏夹）；DOI=`10.1002/mp.70259`；关键词：二维长程、分支训练、阵列控制。

### P04 · tFUSNet · Zhang 2026

**Accurate real-time acoustic field prediction for phased array transcranial focused ultrasound neuromodulation**

二维/三维 CT + 已预计算的阵元相位延时→局部实值 pmax ROI。U-Net 加 CBAM、PatchGAN 和复合损失。已有比较：CBAM 有直接正向消融；GAN 与多损失一起加入，GDL 独立贡献未拆分；网络不负责求输入相位。

来源 A4；Z=`FNM8MMUC`；DOI=`10.1016/j.engappai.2026.115053`；关键词：CBAM、相位条件、GDL、ROI。

### P05 · Park 2023 · SGN / 3D-cGAN

**Real-Time Acoustic Simulation Framework for tFUS: A Feasibility Study Using Navigation System**

随换能器位姿裁剪 CT，把换能器表面写入同一体素通道→局部实值压力图；接导航系统。已有比较：核心是坐标裁剪、几何编码及系统验证；无 P0 输入，各损失缺独立开关消融。

来源 A5；Z=`7Q4HI2UN`,`LQK2IYYZ`（同题同 DOI）；DOI=`10.1016/j.neuroimage.2023.120411`；关键词：随动 ROI、源 mask、实时导航。

### P06 · FEUNet · Wang 2024

**Finite difference-embedded UNet for solving transcranial ultrasound frequency-domain wavefield**

二维声速矩阵→Re/Im 复波场；源/频率在对应实验固定。优化九点 FD 的 Helmholtz 残差与数据损失联合训练 U-Net。已有比较：少数据时物理项有正向结果；其离散 Label/算子及无吸收设置须与目标任务区分。

来源 A6；Z=`JFAPNXIP`；DOI=`10.1121/10.0025391`；关键词：离散物理、MSEData + MSEPhy、少样本。

### P07 · Huang 2025 · 背景场条件 / 散射算子

**Learned frequency-domain scattered wavefield solutions using neural operators**

二维声速 + 均匀背景复场→散射 Re/Im，再加背景场恢复全场；源位置/频率由背景波纹表达。已有比较：同一 U-Net 的背景场输入收益明确；仅把输出改为散射场反而更差。属于二维地震波任务。

来源 A7；Z=`Z4CB4GYA`；DOI=`10.1093/gji/ggaf113`；关键词：P0、source encoding、参考频率、FNO。

### P08 · Zou · 2023 预印本 / 2024 正式版

**Deep Neural Helmholtz Operators for 3D Elastic Wave Propagation and Inversion**

P/S 波速 + 复体力源 + 频率→三分量复位移；U 形神经算子预测各频率，再重建时间场。已有比较：频域减轻时空内存负担，含三维泛化和反演；输出是弹性位移，保存版本模型很大。旧报告数值来自预印本 v1。

来源 A8；Z=`9CD2FRD7`；DOI=`10.1093/gji/ggae342`；arXiv=`2311.09608`；关键词：U-NO、GNO、频域、多尺度。

### P09 · Stanziola 2021 · 学习优化器

**A Helmholtz equation solver using unsupervised learning: Application to transcranial ultrasound**

二维当前复场 + Helmholtz 残差 + 隐藏状态/PML→场增量与新状态，多步迭代求解。无需真实场 Label。已有比较：有残差与实际场误差评价；大 CT 域需较多迭代，不能按一次网络前向与直接 surrogate 等同计时。

来源 A9；Z=`ASTED85S`；DOI=`10.1016/j.jcp.2021.110430`；关键词：learned optimizer、无监督、迭代记忆。

### P10 · Song 2021 · VTI PINN

**Solving the frequency-domain acoustic VTI wave equation using physics-informed neural networks**

二维/三维查询坐标→散射复压力与辅助函数；介质参数进入 PDE。通过背景/散射分解避开点源奇点，自动微分求残差。已有比较：是给定问题的连续解拟合，介质变化通常要重新优化；统一测试误差表在旧报告未核实。

来源 A10；Z=`IZ4V2RTD`；DOI=`10.1093/gji/ggab010`；关键词：PINN、点源奇点、散射分解、各向异性。

### P11 · PINNup · Huang / Alkhalifah 2022

**PINNup: Robust Neural Network Wavefield Solutions Using Frequency Upscaling and Neuron Splitting**

二维坐标 + 源横坐标→散射 Re/Im；先低频训练，再拆分神经元扩宽并学习高频。已有比较：拆分初始化优于同宽随机初始化，但复杂模型仍有明显误差；不是跨颅骨体输入的一次预测。

来源 A11；Z=`A5AJ5PWN`；DOI=`10.1029/2021JB023703`；关键词：高频困难、课程、函数保留初始化。

### P12 · GreenONet · Aldirany 2023 预印本

**Operator approximation of the wave equation based on deep learning of Green's function**

查询空间/时间与初值采样位置→学习 Green 核，再对初始位移线性积分得到实值位移。已有比较：在一/二维波动算例与 physics-informed DeepONet 比较；介质给定，不是任意颅骨输入的三维复压力预测。

来源 A12；Z=`W2N5W62E`；arXiv=`2307.13902`；关键词：线性结构、核学习、初值算子。

### P13 · NG-DPSM · Thakur 2024

**NG-DPSM: A neural green-distributed point source method for modelling ultrasonic field emission near fluid-solid interface using physics informed neural network**

源/观测点坐标及相对方向→位移 Green 张量 Re/Im；自动微分算导数，再接 DPSM 组装压力/应力场。已有比较：可替代繁琐解析导数；Green 计算加速与训练损失不能改称整个经颅场的加速/测试精度。

来源 A13；Z=`LJDJESJ9`；DOI=`10.1016/j.engappai.2023.107828`；关键词：Green 张量、可微求导、流固界面。

### P14 · Choi 2022 · 单元换能器逆导航

**Deep Neural Network for Navigation of a Single-Element Transducer During Transcranial Focused Ultrasound Therapy: Proof of Concept**

三维目标焦域（或椭球参数）→换能器中心/朝向；用多膨胀率 CNN 编码目标。已有比较：评价位姿及仿真后焦域；网络不直接输出声场，模型比较也不是纯多尺度模块单因素消融。

来源 A14；Z=`2SBJBKSW`,`DM9JKVP4`（同题同 DOI）；DOI=`10.1109/JBHI.2022.3198650`；关键词：逆问题、目标编码、atrous。

### P15 · Seol 2026 · 少样本相位/幅度校正

**Few-shot Deep Learning for Phase-Amplitude Aberration Correction in Transcranial Focused Ultrasound**

阵元到目标路径 CT ROI + 几何/Fourier 特征→96 个阵元的相位与幅度。相位分类后圆周期望解码；用新颅骨 10 个目标点适配。已有比较：圆周分类/Fourier 有正向消融；输出是控制量，测试结果含适配。

来源 A15；Z=`PHQJ4MSE`；arXiv=`2607.29182v1`；关键词：周期相位、circular decoding、few-shot。

### P16 · Fourier Features · Tancik 2020

**Fourier Features Let Networks Learn High Frequency Functions in Low Dimensional Domains**

低维坐标→sin/cos 频率特征→MLP 函数值；用频带映射缓解坐标 MLP 的低频偏好。已有比较：频率尺度影响拟合和泛化；不是输出 FFT 或频域损失，条件分支迁移收益需另测。

来源 B1；Z=`E6JIEMT7`（当前目标收藏夹未见）；arXiv=`2006.10739`；关键词：spectral bias、NTK、位置编码。

### P17 · FiLM · Perez · 2017 预印本 / 2018 会议

**FiLM: Visual Reasoning with a General Conditioning Layer**

图像 + 语言条件→答案；条件生成逐通道缩放/偏置，持续调制图像特征。已有比较：原任务有正向证据；迁移到声场时应查看具体消融，DeepTFUS 的结果不能忽略。

来源 B2；Z=`IFAY9FSY`；arXiv=`1709.07871`；关键词：gamma/beta、feature-wise affine、条件注入。

### P18 · Wang / Teng / Perdikaris · 2020 预印本

**Understanding and mitigating gradient pathologies in physics-informed neural networks**

诊断复合物理损失的反传梯度失衡，并按梯度统计自适应调权，另提出特征交互网络。已有比较：处理数值刚性/梯度量级问题；只按 loss 数值配平不等价，也不会自动消除方向冲突。

来源 B3；Z=`BWQ8VIH7`；arXiv=`2001.04536`；关键词：梯度统计、动态权重、PINN 训练病理。

### P19 · PCGrad · Yu 2020

**Gradient Surgery for Multi-Task Learning**

多任务梯度方向冲突时，投影去掉冲突分量后再合并更新。已有比较：是方向冲突的修正方法；辅助目标本身是否合适仍需判断，不能由 PCGrad 推出任何物理损失都会有益。

来源 B4；Z=`W689HDMH`；arXiv=`2001.06782`；关键词：gradient surgery、负内积、辅助损失。

### P20 · Standley · 2019 预印本 / 2020 会议

**Which Tasks Should Be Learned Together in Multi-task Learning?**

实际训练任务组合，估计合作/竞争关系，在推理成本约束下选择共享或拆分网络。已有比较：迁移关系不等于联合训练收益；没有给声场幅度/相位的固定最优分组。

来源 B5；Z=`Z5GY7SEF`；arXiv=`1905.07553`；关键词：负迁移、共享 encoder、任务分组。

### P21 · Dhariwal / Nichol 2021 · 扩散模型

**Diffusion Models Beat GANs on Image Synthesis**

改进扩散 U-Net 并用分类器梯度引导条件采样，提高自然图像生成质量。已有比较：scale-shift、注意力可作结构灵感；FID 与确定性 PDE 场误差不同，多步采样成本需独立判断。

来源 B6；Z=`AEI9UY4S`（虽以 webpage 类型保存，内容为论文）；arXiv=`2105.05233`；关键词：diffusion、classifier guidance、条件 U-Net。

### P22 · Aubry 2022 · 经颅仿真基准

**Benchmark problems for transcranial ultrasound simulation: Intercomparison of compressional wave models**

统一介质、声源和边界基准，对比不同压缩波求解器的数值结果。已有比较：用于 Label/物理条件核查；不是神经网络论文，没有网络模块增益或训练输入输出。

来源 C1；Z=`T93U45F7`（当前目标收藏夹未见）；来源标识=`PMC9553291` / `PMID36050189`；关键词：solver intercomparison、Label 可信度。

### P23 · McDannold 2019 · Elementwise

**Elementwise approach for simulating transcranial MRI-guided focused ultrasound thermal ablation**

各阵元分别仿真保存复响应，按控制幅相相干叠加，再求热效应；用 MR 测温验证。已有比较：前期预计算换取快速组合；温升 R² 不是压力误差，论文没有训练单阵元响应网络。

来源 C2；Z=`QCAN6YU8`；DOI=`10.1103/PhysRevResearch.1.033205`；关键词：响应库、线性叠加、热消融。

### P24 · Zhang 2025 · 颅内信号定位/解码

**Noninvasive intracranial source signal localization and decoding with high spatiotemporal resolution**

聚焦超声 + 声电耦合采集/建模，实现颅内多源定位与解码；声场由时间反转和数值仿真形成。已有比较：是应用动机/下游定位支撑，聚焦增强不是声场 surrogate 预测精度。

来源 C3；Z=`25DGTANB`（当前目标收藏夹未见）；DOI=`10.34133/cbsystems.0206`；关键词：声电耦合、定位、time reversal。

### P25 · Seo 2024 · 多模态声场预测

**Multi-modal networks for real-time monitoring of intracranial acoustic field during transcranial focused ultrasound therapy**

**摘要登记。**数据包含自由场/颅内压力图、医学图像与换能器位姿；以 CNN / Swin Transformer 多模态编码器和解码器生成颅内压力图，涉及 CT 与 MR。已知主题是自由场与影像条件融合；精确输入组合、输出维度/复数定义及独立消融待查正文，暂不把它等同 P07 的背景复场方法。

来源：2026-10-08 Zotero 摘要；Z=`8JKYE9YU`；DOI=`10.1016/j.cmpb.2024.108458`；关键词：multi-modal、free-field、Swin、CT/MR。

### P26 · Xiang 2026 · 神经算子预条件

**Neural operator preconditioning from mixed dataset for the Helmholtz equations: Application to transcranial ultrasound**

**摘要登记。**在二维经颅 Helmholtz 问题中，用混合声速/声源数据和离散相对残差训练粗网格神经预条件器，嵌入 FGMRES 迭代。已知主题是学习预条件与大域迁移；摘要声称可扩展到更大网格，具体精度/耗时和公平预算待查正文。

来源：2026-10-08 Zotero 摘要；Z=`NUDED5Y2`；arXiv=`2607.16906`；关键词：mixed dataset、Krylov、FGMRES、粗网格。

2026-10-09补证据：已核查v1 §4.2.2/表8，64²训练→512²真实CT，D0在10⁻³容差四例159–191步；最小训练validation loss的D5有一例5120步未收敛。CPU总计时与一步神经预测分开。详见[专题笔记](../experiments/survey&design/physical_iteration/papers/README.md)。

### P27 · McMg · Jia 等 2026

**McMg: A Learned Phase-Space Multi-channel Multigrid Preconditioner for Helmholtz Equation**

**摘要登记。**残差→校正；粗网格多通道保留局部幅相/传播方向等波信息，介质生成算子系数，固定介质可缓存，V-cycle 对残差保持线性；逐层微调新增粗层。已知主题是相空间多通道多重网格，含三维高频/高对比算例声明；训练配置和具体收益待查正文。

来源：2026-10-08 Zotero 摘要；Z=`AP24LABK`；arXiv=`2606.30495`；关键词：phase-space、multigrid、linear residual correction、LLPF。

2026-10-09补证据：核查v1 §3/4和表2，固定介质缓存、多通道线性校正；224³三维训练约45 GB（batch3），推理约6 GB。保留机制，不能原样套V100或将残差容差换称V10形状L2。详见[专题笔记](../experiments/survey&design/phase_space/papers/README.md)。

## 2026-10-09 架构专题增量：P28–P44

以下“补录”只表示原索引未列，不表示全项目新发现；旧Born、carrier、MIFNO/WIRE/Butterfly等方向已定向命中。候选设计与验证只属于survey&design，未运行。

### P28 · LBS · Stanziola 2022预印本/2023正式版
**A Learned Born Series for Highly-Scattering Media**；arXiv=`2212.04948`；DOI=`10.1121/10.0017937`。二维介质/点源→复场；学习CBS式传播/散射/更新。已有方向延伸；本轮核查方法与图1，不编造曲线精确增益。[证据](../experiments/survey&design/physical_iteration/papers/README.md)。

### P29 · NBSO · Sun等2023预印本
**Neural Born Series Operator for Biomedical Ultrasound Computed Tomography**；arXiv=`2312.15575`。二维介质/源→复场；介质×状态与背景乘性输出。背景/Born家族延伸，表1/5定向阅读；多源相对FNO收益约3.06%，不混单/多源列。[证据](../experiments/survey&design/physical_iteration/papers/README.md)。

### P30 · NSNO · 2024预印本
**NSNO: Neumann Series Neural Operator for Solving Helmholtz Equations in Inhomogeneous Medium**；arXiv=`2401.13494`。q/f→二维复解，G(q·状态)有限展开；正文§4/5核查，架构与物理loss贡献需拆开。[证据](../experiments/survey&design/physical_iteration/papers/README.md)。

### P31 · MgNO · He/Liu/Xu · ICLR2024
**MgNO: Efficient Parameterization of Linear Operators via Multigrid**；arXiv=`2310.19809`。多重网格参数化通道间算子；原Helmholtz是固定边界激励100²实场，不等同P32改造版。定向正文/附录阅读。[证据](../experiments/survey&design/medium_source/papers/README.md)。

### P32 · OpenBreastUS · Zeng等2025
**OpenBreastUS: Benchmarking Neural Operators for Wave Imaging Using Breast Ultrasound Computed Tomography**；arXiv=`2507.15035`。480²介质/源→完整复场，含64→256源评价。表II/VII和附录B核查；最佳MgNO实际对应P33 MgNO-self，共享结果。[证据](../experiments/survey&design/medium_source/papers/README.md)。

### P33 · SC-NO / MgNO-self · He/Liu/Xu · 2025/2026 v2
**Self-composing neural operators for high-frequency and multiscale PDE surrogates**；arXiv=`2508.20650`。v1旧题名“Self-Composing Neural Operators with Depth and Accuracy Scaling via Adaptive Train-and-Unroll Approach”为同一工作。v2子集表3 MgNO改造正向、FNO/U-Net负向；§3用同组数值描述direct/T&U，结构/训练策略归因尚未拆净。正文§3/4及新版表3核查。[证据](../experiments/survey&design/medium_source/papers/README.md)。

### P34 · Wave-ADR-NS · Cui/Jiang/Shu · 2024预印本
**A Neural Multigrid Solver for Helmholtz Equations with High Wavenumber and Heterogeneous Media**；arXiv=`2404.02493`。波数附近误差→走时搬移/粗ADR校正；二维求解器。方法/表2/局限定向核查。[证据](../experiments/survey&design/phase_space/papers/README.md)。

### P35 · Mamba · Gu/Dao · 2023预印本
**Mamba: Linear-Time Sequence Modeling with Selective State Spaces**；arXiv=`2312.00752`。选择性状态和并行scan；v2方法/实复状态讨论核查；通用思想，不当作波场证据。[证据](../experiments/survey&design/spatial_state/papers/README.md)。

### P36 · VMamba · NeurIPS2024
**VMamba: Visual State Space Model**；arXiv=`2401.10166`。二维四方向scan→视觉特征；方法与v2扫描消融表5定向核查，包含吞吐/NaN负向事实。[证据](../experiments/survey&design/spatial_state/papers/README.md)。

### P37 · WIRE · Saragadam等 · CVPR2023
**WIRE: Wavelet Implicit Neural Representations**；arXiv=`2301.05187`。复Gabor局部振荡激活；已有旧工程组件，本轮核查§3；跨源三维复场未验证。[证据](../experiments/survey&design/phase_space/papers/README.md)。

### P38 · MFN · Fathony等 · ICLR2021
**Multiplicative Filter Networks**；OpenReview=`OmtmcPkkhT`。线性状态×坐标滤波器的逐层展开；方法与作者代码入口核查；只提取结构机制，不当经颅实证。[证据](../experiments/survey&design/phase_space/papers/README.md)。

### P39 · PhaseDNN · Cai/Li/Liu · 2019预印本
**A Phase Shift Deep Neural Network for High Frequency Approximation and Wave Problems**；arXiv=`1909.11759`；DOI=`10.1137/19M1310050`。相移后学习高频；项目已有讨论/试验，索引补录，本轮不重复全文阅读。[证据](../experiments/survey&design/phase_space/papers/README.md)。

### P40 · MIFNO · Lehmann/Gatti/Clouteau · JCP2025
**Multiple-input Fourier Neural Operator (MIFNO) for source-dependent 3D elastodynamics**；arXiv=`2404.10115`；DOI=`10.1016/j.jcp.2025.113813`。介质体/源向量双分支→地表时空速度；已有旧工程目录，论文/作者仓库入口定向核查。[证据](../experiments/survey&design/medium_source/papers/README.md)。

### P41 · FIONet · Kothari/de Hoop/Dokmanić · NeurIPS2020
**Learning the Geometry of Wave-Based Imaging**；arXiv=`2006.05854`。方向波包与几何路由用于波逆成像；正文方法/作者仓库核查，不当作点源复压力直接预测。[证据](../experiments/survey&design/source_kernel/papers/README.md)。

### P42 · Butterfly-Net2 · Xu/Li/Cheng · MSML2020
**Butterfly-Net2: Simplified Butterfly-Net and Fourier Transform Initialization**；arXiv=`1912.04154`；PMLR=`v107/xu20b`。结构稀疏傅里叶算子近似；旧Butterfly方向补录，正文/官方摘要定向核查。[证据](../experiments/survey&design/source_kernel/papers/README.md)。

### P43 · HINTS · Zhang等 · NMI2024
**Blending Neural Operators and Relaxation Methods in PDE Numerical Solvers**；arXiv=`2208.13273`；DOI=`10.1038/s42256-024-00910-x`。补正文§2.3–2.5/附录：残差DeepONet与relaxation交替，含3D环柱FGMRES大系统及小规模更贵的边界；不作当前颅骨速度/形状精度外推。[证据](../experiments/survey&design/physical_iteration/papers/README.md)。

### P44 · OpenWaves / S²NO · Zeng等 · 2025/2026 v4
**Ultrasound Tomography of Musculoskeletal Tissues with Generative Neural Physics**；arXiv=`2508.12226`；v1题名含“In vivo 3D”为同一工作。v4正文及S9/S12核查：强散射CBS式神经算子，主前向仍2D，3D体由轴向切片形成；共享参数消融负向。[证据](../experiments/survey&design/physical_iteration/papers/README.md)。

## 非论文网页（保留查重，不计入论文总数）

**RF Pulse design and parallel transmission (pTx)**，PTB 网页，Z=`MCHUDCSB`。属于 MRI 射频脉冲/并行发射主题；当前摘要只含机构介绍，不据此提炼具体方法。位于 `tus_surrogate` 根收藏夹。

## 维护方式

后续新论文只追加一条：题名/简称、年份、标识、一两句任务与机制、阅读状态、证据入口。已有论文补新证据时更新原条目，并明确新增内容；“本项目已试/已排除”必须另附具体实验结果或用户决定，不能由入库状态推断。
