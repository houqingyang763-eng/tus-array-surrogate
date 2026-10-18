# 已知论文与方向检索清单

初始核对：2026-10-08；专题增量核查：2026-10-09—18。用途：讨论或检索新方向前先查重；允许重访和借鉴，但应明确说出“已有方向 + 本次新增内容”。

## 给 GPT / Codex 的使用规则

1. 提出“新论文 / 新道路”前，先查本文件的题名、简称、DOI 和方法关键词；同题、预印本/正式版、重复 Zotero 条目算同一工作。
2. 命中论文时标为“已知论文”；命中方法家族时标为“已有方向的延伸”。说明这次新增了哪项证据、机制或适用条件，再判断是否值得重访。
3. “已知 / 已收录”只表示进入过当前知识范围；不等于用户精读、完成实验或否定整个方向。下列“已有比较”指有旧报告记录；“摘要登记”指本次仅用 Zotero 摘要概括。
4. 未命中本表只表示“清单未收录”，仍需核对项目其他材料；不要直接宣布首次发现。需要细节时按来源入口读对应段落，不默认重读整篇 PDF。
5. 本表不是科学合同或实验授权。当前 V10 为颅外单点源→颅内复场形状；历史论文的 pmax、绝对尺度、阵列控制量、阵列叠加及迭代求解任务仅作检索背景。

## 覆盖与来源

- 实时读取 Zotero `tus_surrogate`（`29BGBFP3`）及全部 7 个子收藏夹：28 个不同顶层条目；3 个重复条目合并后，得到 24 篇论文 + 1 个非论文网页。各收藏夹均核对 API 总条数，无分页遗漏。
- 与 [2026-09-30 跨论文比较](zotero_cross_paper_comparison_20260930.md) 的 24 篇取并集：**27 篇论文**。旧报告中的 Fourier Features、Aubry 基准、Zhang 颅内定位这 3 篇目前未在上述收藏夹内，仍保留。
- P01–P24 的初始概览与边界压缩自旧报告对应 A/B/C 条目；P25–P27 初始仅据 Zotero 元数据与摘要。后续正文核查以各条目的增量为准。年份在预印本和正式版之间可能不同，按所列来源口径保留。
- `Z=` 为 Zotero 条目 key，可用 `zotero://select/library/items/KEY` 定位；它不是 BibTeX 引用键。`来源 A1` 等指旧报告原有编号。未删除、移动或合并 Zotero 实体条目。
- 2026-10-09架构专题追加P28–P44，共17篇，当日索引44篇；其中多篇已在旧方向材料出现，本次仅补录并定向核查，未操作Zotero。P26/P27补正文证据。阅读深度与去重依据见[专题检索记录](../experiments/survey&design/exploration00/SEARCH_LOG.md)。P32/P33共享USCT结果，不能当两份独立实证。
- 2026-10-10 McMg线补录P45，当日索引45篇；P27新增用户指定v2的频域求解迁移审查，证据见[方向入口](../experiments/survey&design/exploration00/McMg线/README.md)。未操作Zotero、未运行求解或训练。
- 2026-10-11 Idea查重新增P46–P59，共14项（含2份学位论文、2份技术报告），当前为**59个登记条目**，含历史/撤回入口，并非59份独立实证；P09/P26/P27/P29/P44/P45补证据、撤回或正式版。P29已撤回并指向P44更新工作，保留编号、合并演进链证据计数。新增不等于全项目首次发现；全文未取得的条目明确标注。见[检索记录](../experiments/survey&design/exploration00/idea查重/SEARCH_LOG.md)与[查重报告](../experiments/survey&design/exploration00/idea查重/REPORT.md)。未操作Zotero、未运行实验。

## 方向速查：这些方法已经进入过讨论范围

2026-10-16 exploration 01增量：P60–P73共14个登记条目，合计73个编号；另记作者仓库W02，不计论文。均为已有机制家族延伸，不宣称全项目首次发现；P49新arXiv与旧报告归并。正文深度和证据见[本轮论文笔记](<../experiments/survey&design/exploration 01/papers/README.md>)与[机制查重](<../experiments/survey&design/exploration 01/idea查重/REPORT.md>)。未操作Zotero、未运行实验。

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
| 学习迭代器、神经预条件、FGMRES、多重网格 | P09、P26–P27、P46–P49、P59、P76–P78 | 经颅先例已到2022学位论文；传统强MG已有新改进；迭代次数、完整时间与复场误差分开 |
| 学习延拓、近零子空间、deflation、Petrov–Galerkin | P60–P61、P63–P65、P70 | SPD/不定适用条件；近零样本矩阵与物理A的奇异空间分开 |
| 界面条件、Schwarz、Schur、DtN、辅助状态 | P62、P66–P67、P72、W02 | 学习什么未知量；预训练残差校正与逐题求网络权重分开 |
| 散射分解、HINTS散射、双端口、相容空间 | P68–P69、P71、P73 | 原方程残差与场差值分开；端口组合和结构相容本身已有先例 |
| 粗仿真+超分辨率、坐标算子、局部峰压 | P51、P54–P55 | 真3D/未见颅骨仍不等于复场；网络前向与粗仿真总时间分开 |
| Label 基准、物理验证、声电应用、逆向导航 | P14、P22、P24 | 仿真可信度、下游应用与场预测分开 |
| 传统Born、快速传播、时频桥接、压缩直接解 | P45、P53、P57、P74–P85 | 单配置总场与独立多RHS分开；计入源处理、介质准备及离散/边界条件 |
| 三维域分解、OSM/ORAS、扫描、谱粗空间 | P66、P75、P79–P81、P86 | 局部因子可复用；批量吞吐不直接迁移；真算子中的近似与预条件近似分开 |

## 研究条目清单

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

2026-10-11查重补证据：v2 §3.1的理想化测试平均相对L∞0.36%与§3.3真实CT演示分开；大CT最小全场误差约3000步，20步焦域进展不当全场成绩。原文速度为初步测试声明，缺完整计时表；经颅学习迭代基础先例明确，仍为2D。与P47博士论文共享CT设置；P26后续四CT复测不记为P09自身结果。[原文](https://arxiv.org/html/2010.15761v2)、[查重证据](../experiments/survey&design/exploration00/idea查重/REPORT.md)。

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

**定向正文核查。**二维经颅Helmholtz，混合声速/源数据训练神经预条件器，真实算子与FGMRES保留。2026-10-11补v1 §4.2.2表8：64²训练到512²真实CT切片；D0在4个算例达到相对残差1e−3合计737.70 s、1e−6合计2773.70 s，均为CPU节点，非4×V100小网格计时。GMRES三例失败，不将总时间比写成四例同精度加速；缺独立复场误差及真3D联合泛化。基础Idea直接先例，最高威胁未达到。[原文](https://arxiv.org/html/2607.16906v1)、[查重证据](../experiments/survey&design/exploration00/idea查重/REPORT.md)。

来源：2026-10-08 Zotero 摘要；Z=`NUDED5Y2`；arXiv=`2607.16906`；关键词：mixed dataset、Krylov、FGMRES、粗网格。

2026-10-09补证据：已核查v1 §4.2.2/表8，64²训练→512²真实CT，D0在10⁻³容差四例159–191步；最小训练validation loss的D5有一例5120步未收敛。CPU总计时与一步神经预测分开。详见[专题笔记](../experiments/survey&design/exploration00/physical_iteration/papers/README.md)。

### P27 · McMg · Jia 等 2026

**McMg: A Learned Phase-Space Multi-channel Multigrid Preconditioner for Helmholtz Equation**

**定向正文核查。**残差→复校正；介质生成系数可缓存，固定介质V-cycle对残差线性。2026-10-11查重补v2表2：224³ Kimberlina地质介质真3D，容差1e−6，CBS4.128 s／McMg0.608 s；不是颅骨实证。小块到大域直接迁移与新增粗层LLPF微调分开；迭代降幅与总时间降幅分开。[原文](https://arxiv.org/html/2606.30495v2)、[查重证据](../experiments/survey&design/exploration00/idea查重/REPORT.md)。

来源：2026-10-08 Zotero 摘要；Z=`AP24LABK`；arXiv=`2606.30495`；关键词：phase-space、multigrid、linear residual correction、LLPF。

2026-10-09补证据：核查v1 §3/4和表2，固定介质缓存、多通道线性校正；224³三维训练约45 GB（batch3），推理约6 GB。保留机制，不能原样套V100或将残差容差换称V10形状L2。详见[专题笔记](../experiments/survey&design/exploration00/phase_space/papers/README.md)。

2026-10-10补证据：核查v2（2026-07-02）§2–4及附录A.1–A.7，转向完整求解路线分析；原声速标量算子与V10的密度/吸收/边界差异、随机残差训练、三维总求解成本及负向边界证据见[McMg线](../experiments/survey&design/exploration00/McMg线/README.md)。这是已知论文深化，不是新发现或迁移成功。

## 2026-10-09 架构专题增量：P28–P44

以下“补录”只表示原索引未列，不表示全项目新发现；旧Born、carrier、MIFNO/WIRE/Butterfly等方向已定向命中。候选设计与验证只属于survey&design，未运行。

### P28 · LBS · Stanziola 2022预印本/2023正式版
**A Learned Born Series for Highly-Scattering Media**；arXiv=`2212.04948`；DOI=`10.1121/10.0017937`。二维介质/点源→复场；学习CBS式传播/散射/更新。已有方向延伸；本轮核查方法与图1，不编造曲线精确增益。[证据](../experiments/survey&design/exploration00/physical_iteration/papers/README.md)。

### P29 · NBSO · Sun等2023预印本（2026撤回）

**历史入口。**2026-10-11核实：2026-08-03的v2为撤回公告，作者说明v1未完成、现已扩展更新为P44（2508.12226）。保留以下历史登记，旧版数值不作现行性能，P29/P44不计两份独立实证。[作者撤回记录](https://arxiv.org/abs/2312.15575)。
**Neural Born Series Operator for Biomedical Ultrasound Computed Tomography**；arXiv=`2312.15575`。二维介质/源→复场；介质×状态与背景乘性输出。背景/Born家族延伸，表1/5定向阅读；多源相对FNO收益约3.06%，不混单/多源列。[证据](../experiments/survey&design/exploration00/physical_iteration/papers/README.md)。

2026-10-11查重补证据：v1 §4.1.2明确脑模体排除颅骨（MRI骨信号不足），不是经颅先例；3D模体切片用于2D前向，不升级为3D传播。表3网络前向与CBS计时不是同复场误差容差的完整FWI比较。[原文](https://arxiv.org/html/2312.15575v1)、[查重证据](../experiments/survey&design/exploration00/idea查重/REPORT.md)。

### P30 · NSNO · 2024预印本
**NSNO: Neumann Series Neural Operator for Solving Helmholtz Equations in Inhomogeneous Medium**；arXiv=`2401.13494`。q/f→二维复解，G(q·状态)有限展开；正文§4/5核查，架构与物理loss贡献需拆开。[证据](../experiments/survey&design/exploration00/physical_iteration/papers/README.md)。

### P31 · MgNO · He/Liu/Xu · ICLR2024
**MgNO: Efficient Parameterization of Linear Operators via Multigrid**；arXiv=`2310.19809`。多重网格参数化通道间算子；原Helmholtz是固定边界激励100²实场，不等同P32改造版。定向正文/附录阅读。[证据](../experiments/survey&design/exploration00/medium_source/papers/README.md)。

### P32 · OpenBreastUS · Zeng等2025
**OpenBreastUS: Benchmarking Neural Operators for Wave Imaging Using Breast Ultrasound Computed Tomography**；arXiv=`2507.15035`。480²介质/源→完整复场，含64→256源评价。表II/VII和附录B核查；最佳MgNO实际对应P33 MgNO-self，共享结果。[证据](../experiments/survey&design/exploration00/medium_source/papers/README.md)。

### P33 · SC-NO / MgNO-self · He/Liu/Xu · 2025/2026 v2
**Self-composing neural operators for high-frequency and multiscale PDE surrogates**；arXiv=`2508.20650`。v1旧题名“Self-Composing Neural Operators with Depth and Accuracy Scaling via Adaptive Train-and-Unroll Approach”为同一工作。v2子集表3 MgNO改造正向、FNO/U-Net负向；§3用同组数值描述direct/T&U，结构/训练策略归因尚未拆净。正文§3/4及新版表3核查。[证据](../experiments/survey&design/exploration00/medium_source/papers/README.md)。

### P34 · Wave-ADR-NS · Cui/Jiang/Shu · 2024预印本
**A Neural Multigrid Solver for Helmholtz Equations with High Wavenumber and Heterogeneous Media**；arXiv=`2404.02493`。波数附近误差→走时搬移/粗ADR校正；二维求解器。方法/表2/局限定向核查。[证据](../experiments/survey&design/exploration00/phase_space/papers/README.md)。

### P35 · Mamba · Gu/Dao · 2023预印本
**Mamba: Linear-Time Sequence Modeling with Selective State Spaces**；arXiv=`2312.00752`。选择性状态和并行scan；v2方法/实复状态讨论核查；通用思想，不当作波场证据。[证据](../experiments/survey&design/exploration00/spatial_state/papers/README.md)。

### P36 · VMamba · NeurIPS2024
**VMamba: Visual State Space Model**；arXiv=`2401.10166`。二维四方向scan→视觉特征；方法与v2扫描消融表5定向核查，包含吞吐/NaN负向事实。[证据](../experiments/survey&design/exploration00/spatial_state/papers/README.md)。

### P37 · WIRE · Saragadam等 · CVPR2023
**WIRE: Wavelet Implicit Neural Representations**；arXiv=`2301.05187`。复Gabor局部振荡激活；已有旧工程组件，本轮核查§3；跨源三维复场未验证。[证据](../experiments/survey&design/exploration00/phase_space/papers/README.md)。

### P38 · MFN · Fathony等 · ICLR2021
**Multiplicative Filter Networks**；OpenReview=`OmtmcPkkhT`。线性状态×坐标滤波器的逐层展开；方法与作者代码入口核查；只提取结构机制，不当经颅实证。[证据](../experiments/survey&design/exploration00/phase_space/papers/README.md)。

### P39 · PhaseDNN · Cai/Li/Liu · 2019预印本
**A Phase Shift Deep Neural Network for High Frequency Approximation and Wave Problems**；arXiv=`1909.11759`；DOI=`10.1137/19M1310050`。相移后学习高频；项目已有讨论/试验，索引补录，本轮不重复全文阅读。[证据](../experiments/survey&design/exploration00/phase_space/papers/README.md)。

### P40 · MIFNO · Lehmann/Gatti/Clouteau · JCP2025
**Multiple-input Fourier Neural Operator (MIFNO) for source-dependent 3D elastodynamics**；arXiv=`2404.10115`；DOI=`10.1016/j.jcp.2025.113813`。介质体/源向量双分支→地表时空速度；已有旧工程目录，论文/作者仓库入口定向核查。[证据](../experiments/survey&design/exploration00/medium_source/papers/README.md)。

### P41 · FIONet · Kothari/de Hoop/Dokmanić · NeurIPS2020
**Learning the Geometry of Wave-Based Imaging**；arXiv=`2006.05854`。方向波包与几何路由用于波逆成像；正文方法/作者仓库核查，不当作点源复压力直接预测。[证据](../experiments/survey&design/exploration00/source_kernel/papers/README.md)。

### P42 · Butterfly-Net2 · Xu/Li/Cheng · MSML2020
**Butterfly-Net2: Simplified Butterfly-Net and Fourier Transform Initialization**；arXiv=`1912.04154`；PMLR=`v107/xu20b`。结构稀疏傅里叶算子近似；旧Butterfly方向补录，正文/官方摘要定向核查。[证据](../experiments/survey&design/exploration00/source_kernel/papers/README.md)。

### P43 · HINTS · Zhang等 · NMI2024
**Blending Neural Operators and Relaxation Methods in PDE Numerical Solvers**；arXiv=`2208.13273`；DOI=`10.1038/s42256-024-00910-x`。补正文§2.3–2.5/附录：残差DeepONet与relaxation交替，含3D环柱FGMRES大系统及小规模更贵的边界；不作当前颅骨速度/形状精度外推。[证据](../experiments/survey&design/exploration00/physical_iteration/papers/README.md)。

### P44 · OpenWaves / S²NO · Zeng等 · 2025/2026 v4

2026-10-11补版本关系：当前v4为2026-08-06；P29作者撤回公告明确指向本工作，按同一演进链处理，保留历史编号但不重复计证据。[当前版本](https://arxiv.org/abs/2508.12226)。
**Ultrasound Tomography of Musculoskeletal Tissues with Generative Neural Physics**；arXiv=`2508.12226`；v1题名含“In vivo 3D”为同一工作。v4正文及S9/S12核查：强散射CBS式神经算子，主前向仍2D，3D体由轴向切片形成；共享参数消融负向。[证据](../experiments/survey&design/exploration00/physical_iteration/papers/README.md)。

## 2026-10-10 McMg线增量

### P45 · 变密度Born · Stanziola等 · 2025预印本／2026 JASA

**Iterative Born Solver for the Acoustic Helmholtz Equation with Heterogeneous Sound Speed and Density**；arXiv=`2507.16087`。属于已有Born方向延伸。v1正文及作者MATLAB源码核查：一阶压力/速度系统与universal split预条件，支持3D、移动点源及可变c/ρ/α；经颅基准7的焦点幅值结果不等于全颅内复场形状L2。2026-10-10新增吸收文档/代码约定、缺失参考MAT与人工绘图对齐问题；固定作者提交，未运行。[单篇导读与证据](../experiments/survey&design/exploration00/McMg线/papers/born_density_2025.md)。

2026-10-11补正式版：JASA 2026，DOI 10.1121/10.0042259，与2507.16087合并；没有学习模块，属于传统基线而非神经加速先例。[出版社原文](https://doi.org/10.1121/10.0042259)。

## 2026-10-11 Idea查重增量

以下新增只表示统一索引此前未登记；全文深度与缺口见[查重报告](../experiments/survey&design/exploration00/idea查重/REPORT.md)。

### P46 · NPBS · Wang/Jia/Liu · 2026预印本

**Neural Preconditioned Born Series: A Metric-Matched Framework for Learning-based Preconditioners**；arXiv 2603.18527v4。v1题名Born-Series-Inspired Residual Metric for Learning-based Preconditioners，同一工作。定向正文§3/5及附录G/H/J：学习Born预条件残差坐标中的校正；2D OpenFWI，无颅骨。表3减迭代不必更快，须比较最快CBS完整时间。已有Born/神经预条件家族延伸。[原文](https://arxiv.org/html/2603.18527v4)。

### P47 · Xiang · 2022博士论文

**Solution of large linear systems with a massive number of right-hand sides and machine learning**。作者全文第5章定向核查，§5.4.2.3印刷页112–119含真实512²颅骨CT、神经预条件FGMRES与场图；继承P09设置，非独立CT数据。经颅神经预条件先例已于2022出现；2D、检查点泛化有失效、完整颅骨性能表有缺项。学位论文不计独立期刊论文。[作者全文](https://irma.math.unistra.fr/~xiang/research/XIANG_YANFEI_2022.pdf)。

### P48 · Nguyen Son Hai · 2022硕士论文

**Approximation of Sound Propagation by Neural Networks**。同题会议展示合并。大学全文§6–8：GNN利用当前场和显式Helmholtz残差迭代，2D理想化颅骨，96²→512²大域；图7.6/结论明确速度与精度弱于Helmnet/k-Wave，大域训练调整须单列。方法部分先例，非高性能经颅实现。[大学元数据](https://www.fit.vut.cz/study/thesis/24521/.en)、[全文](https://www.fit.vut.cz/study/thesis-file/24521/24521.pdf)。

### P49 · Giraud/Kruse/Mycek/Shpakovych/Xiang · 2025技术报告

**Neural network preconditioning: a case study for the solution of the parametric Helmholtz equation**；HAL 05157038，Inria RR-9593。定向全文核查：学习预条件与参数/域迁移，实际实验为通用2D；仅参考文献引用P09，不当自身经颅测试。与P26同作者/机制前序。[机构全文](https://cerfacs.fr/wp-content/uploads/2026/01/RR-9593-1-1.pdf)。

2026-10-16版本补查：[arXiv2610.16542](https://arxiv.org/abs/2610.16542)于2026-10-12公开，同题作者链与上述技术报告归并，不新增编号；本次只核元数据/摘要。

### P50 · PEN-FWI · 2024 TMI

**Deep Learning With Physics-Embedded Neural Network for Full Waveform Ultrasonic Brain Imaging**；DOI 10.1109/TMI.2024.3363144，PMID38329866。**摘要登记，未取得全文。**学习FCNN替代FD前向，再用于学习逆网络，最终是2D脑声速图像；1.13 s为重建时间，不作复场数值求解速度。前向输出/物理残差细节待全文。[NCBI](https://pubmed.ncbi.nlm.nih.gov/38329866/)。

### P51 · Shin/Peng/Kim/Yoo/Yoon · 2023 SR-ResNet

**Multivariable-incorporating super-resolution residual network for transcranial focused ultrasound simulation**；DOI 10.1016/j.cmpb.2023.107591，PMID37182263。**出版社/NCBI摘要登记，未取得全文。**3D粗仿真压力/速度/CT→超分辨率压力，3个离体颅骨，1.0→0.5 mm；焦体积准确率和成本改善不等于全复场误差。宽口径混合流程近邻；复数输出、域与严格拆分待核。不与P05混淆。[出版社](https://www.sciencedirect.com/science/article/pii/S0169260723002560)。

### P52 · 经颅PINN · 2023 Ultrasonics

**Physics-informed neural networks for transcranial ultrasound wave propagation**；DOI 10.1016/j.ultras.2023.107026，PMID37137219。**摘要登记，未取得全文。**2D时域传播与PDE/边界损失；物理训练损失不等于学习残差预条件，权重共享和完整性能待核。区别于P10/P11地震PINN。[NCBI](https://pubmed.ncbi.nlm.nih.gov/37137219/)。

### P53 · Viscoacoustic modified Born · 2025 JASA

**A viscoacoustic wave equation solver using modified Born series**；DOI 10.1121/10.0039529，PMID41081483。**摘要登记。**2D/3D变声速、密度、衰减及颅骨算例，纯传统Born类求解；非学习先例。全文公平性能本轮未核，不混P45。[NCBI](https://pubmed.ncbi.nlm.nih.gov/41081483/)。

### P54 · tFUSFormer · Shin/Seo/Yoo/Yoon · 2024 JBHI

**tFUSFormer: Physics-Guided Super-Resolution Transformer for Simulation of Transcranial Focused Ultrasound Propagation in Brain Stimulation**；DOI 10.1109/JBHI.2024.3389708，PMID38625763。作者接受稿及代码核查：25³→100³局部3D最大压力超分辨率，12训练颅骨/2未见颅骨；表IX完整LR+SR为2.3054 s而非仅0.0947 s网络前向。输出pmax及焦域IoU，不是Re/Im或复场残差求解。与P51有作者/前序关系。[作者接受稿](https://ieeexplore.ieee.org/ielx7/6221020/6363502/10500878.pdf)、[代码](https://github.com/iangilan/tFUSFormer)。

### P55 · tFUSOperator · Seo等 · 2026预印本／MICCAI DT4H

**tFUSOperator: Operator Learning for Transcranial Focused Ultrasound Digital Twins**；arXiv 2608.01839v1，会议camera-ready合并。正文§2/3及作者README核查：自由场峰压/CT或MR/位姿频率→3D56³局部pmax；13颅骨8/2/3划分、已见颅骨留出30/300位置。坐标注意力端到端代理，没有真实A残差预条件回路；名称“operator”不等于传统数值算子加速。[原文](https://arxiv.org/html/2608.01839v1)、[会议](https://papers.miccai.org/miccai-2026-sat/DT4H_010.html)。

### P56 · Huang等 · 2025三维经颅PACT

**Fast aberration correction in 3D transcranial photoacoustic computed tomography via a learning-based image reconstruction method**；DOI 10.1016/j.pacs.2025.100698。作者全文§1/3定向核查：近似伴随重建后接图像恢复网络，输出初始压力图像；是真3D颅骨逆成像，不是颅外源到稳态复场的正向求解先例。[作者全文](https://coilab.caltech.edu/documents/30905/Huang-2025-Photoacoustics.pdf)。

### P57 · mSOUND颅骨验证 · 2026 OJUFFC

**Numerical Validation of mSOUND Using Fully Heterogeneous Skull Models**；DOI 10.1109/OJUFFC.2026.3677158，PMID41971001。**摘要登记。**真实异质颅骨快速传统传播验证，非学习先例；焦域精度和速度声明不等于全复场形状误差。本轮不凭摘要做公平基线定量。[NCBI](https://pubmed.ncbi.nlm.nih.gov/41971001/)。

2026-10-18 experiment02补全文：经公开作者稿XML核查§II–V、表1，属于已知论文深化。ESSF单向传播/有限反射，平面输入需FOCUS；4片段来自2名受试者。0.5 mm时源平面287.77 s+传播36.45 s，k-Wave CPU3646.48 s；全文指标主要是幅值/焦域，非当前Re/Im形状。[证据与条件](../experiments/survey&design/experiment02/REFERENCES.md#r06)。

### P58 · Seo等 · 2026主动学习声透镜优化

**Optimization of Acoustic Lens Design for Transcranial Holographic Ultrasound using an Active Learning-Based Genetic Algorithm**；DOI 10.1093/jcde/qwag077，2026-09-18在线。**出版社摘要登记。**透镜几何→聚焦性能代理，主动学习接遗传算法，目标是逆设计；不计正向复场学习求解先例。[出版社](https://academic.oup.com/jcde/advance-article/doi/10.1093/jcde/qwag077/8817259?searchresult=1)。

### P59 · Shpakovych · 2023技术报告

**Neural network preconditioning of large linear systems**；Inria RT-0518，HAL 04254315。**仅元数据/引文登记，未取得全文。**P26引文与Inria年度报告互证；是否有经颅实验与其维度/性能待核，不因后续引用就记为经颅直接先例。[机构记录](https://radar.inria.fr/report/2023/concace/index.html)、[HAL入口](https://hal.science/hal-04254315/document)。

## 2026-10-16 exploration 01：机制查重与经典思想

以下均为原索引新增、已有方向延伸。唯一公共事实笔记：[papers](<../experiments/survey&design/exploration 01/papers/README.md>)。

### P60 · Greenfeld等 · ICML2019

**Learning to Optimize Multigrid PDE Solvers**；arXiv1902.10248，PMLR97:2415–2423。定向读§2–4：从二维扩散离散算子学延拓规则，非直接学解。[官方PDF](https://proceedings.mlr.press/v97/greenfeld19a/greenfeld19a.pdf)。

### P61 · Azulay/Treister · SISC2022

**Multigrid-augmented deep learning preconditioners for the Helmholtz equation**；arXiv2203.11025，DOI10.1137/21M1433514。定向读§3–4：U-Net/移位Laplacian/FGMRES与encoder–solver分工。[v1正文](https://arxiv.org/html/2203.11025v1)。

### P62 · MLORAS · NeurIPS2022

**Learning Interface Conditions in Domain Decomposition Solvers**。定向读§2–4：学习Robin附加矩阵；式1为η−Δ、η>0的正定问题，不误读成高频不定声学实证。[官方正文](https://papers.nips.cc/paper_files/paper/2022/file/2f8928efe957139e9c0efc98f173f4be-Paper-Conference.pdf)。

### P63 · NGO粗空间结构比较 · 2026

**When can a neural operator replace a coarse solve? Architectural principles for two-level preconditioning**；arXiv2605.19867。定向读§2–4：基积分/采样与源线性两轴；Helmholtz粗逆退化及固定基容量问题分开。[v1](https://arxiv.org/html/2605.19867v1)。

### P64 · NeuraLSP · 2026

**NeuraLSP: An Efficient and Rigorous Neural Left Singular Subspace Preconditioner for Conjugate Gradient Methods**；arXiv2601.20174。定向读§3–5：学近零样本矩阵S的主左奇异子空间，不是直接学A最小奇异向量；PCG范围。[v1](https://arxiv.org/html/2601.20174v1)。

### P65 · GMP · 2026

**Graph Neural Multilevel Preconditioners for Iterative Solvers**；arXiv2607.28456。定向读§3及结论：AMG图层次、分别参数化的限制/插值，非SPD测试及开销边界。[v1](https://arxiv.org/html/2607.28456v1)。

### P66 · Gander/Zhang · SIAM Review2019

**A Class of Iterative Solvers for the Helmholtz Equation: Factorizations, Sweeping Preconditioners, Source Transfer, Single Layer Potentials, Polarized Traces, and Optimized Schwarz Methods**；DOI10.1137/16M109781X。定向读共同块LU/Schwarz框架，防止将异名同机制当新颖。[原文](https://epubs.siam.org/doi/10.1137/16M109781X)。

### P67 · Learned infinite elements · 2020/2021

**Learned infinite elements**；arXiv2010.15479。定向读v2§2–4：可分离外域DtN拟合、稀疏辅助系统Schur；非预训练NN。[v2正文](https://arxiv.org/html/2010.15479v2)。

### P68 · HINTS散射扩展 · 2024

**Large scale scattering using fast solvers based on neural operators**；arXiv2405.12380。定向读§3–4：体强迫/边界入射双网络结合传统迭代，含3D障碍散射。P43家族延伸，非同篇版本。[v1](https://arxiv.org/html/2405.12380v1)。

### P69 · Hybrid scattering · 2026

**Hybrid operator learning of wave scattering maps in high-contrast media**；arXiv2602.11197。定向读§3–5：FNO背景＋ViT散射校正，固定源；场差值不等于真实迭代残差。[v1](https://arxiv.org/html/2602.11197v1)。

### P70 · 学习算子增强PCG · 2025

**Leveraging Operator Learning to Accelerate Convergence of the Preconditioned Conjugate Gradient Method**；arXiv2508.00101。定向读§2–3：SPD对象，学得基用于deflation并稀疏化。[v1](https://arxiv.org/html/2508.00101v1)。

### P71 · 光子散射矩阵设计 · 2026

**Surrogate Scattering Matrix-Guided Inverse Design of Nanophotonic Neural Networks**；DOI10.1002/nap2.70302，2026-09-23。定向读§2.1：双向散射块/互易性/组合，光学分类器逆设计，非残差求解器。[正文](https://onlinelibrary.wiley.com/doi/full/10.1002/nap2.70302)。

### P72 · ELM-DD · 2024/2025

**A Nonoverlapping Domain Decomposition Method for Extreme Learning Machines: Elliptic Problems**；arXiv2406.15959。定向读§2–3：消局部网络输出层系数得到界面Schur，不是固定预训练残差映射。[v1](https://arxiv.org/html/2406.15959v1)。

### P73 · de Rham兼容DNN-FEM · 2023

**De Rham compatible Deep Neural Network FEM**；DOI10.1016/j.neunet.2023.06.008。**只核出版社摘要**：最低阶de Rham有限元空间的精确神经表示；不作声学迭代性能判断。[出版社](https://www.sciencedirect.com/science/article/pii/S0893608023003088)。

## 2026-10-18 experiment02：传统强基底与网络接入比较

P74–P86为13个新登记编号，合计86个编号；不等于86份独立实证。均为已有Born/MG/DD/时频求解家族的延伸或补录，不宣称全项目首次发现。P57升级全文；其他已知论文的本轮补查见[证据入口](../experiments/survey&design/experiment02/REFERENCES.md)及[检索记录](../experiments/survey&design/experiment02/SEARCH_LOG.md)。仅文献研究，无服务器/实验/Zotero操作。

### P74 · 收敛Born原始机制 · Osnabrugge等 · JCP2016

**A convergent Born series for solving the inhomogeneous Helmholtz equation in arbitrarily large media**；arXiv1601.05997，DOI10.1016/j.jcp.2016.06.034。定向读§2–4：收敛迭代、FFT背景逆和反差相关伪传播。与只保留单次散射的Born近似分开。[原文](https://arxiv.org/html/1601.05997)、[本轮定位](../experiments/survey&design/experiment02/REFERENCES.md#r03)。

### P75 · 域分解MBS · Mache/Vellekoop · 2024预印本/后续JCP

**Domain decomposition of the modified Born series approach for large-scale wave propagation simulations**；arXiv2410.02395v3（2025-10-16），期刊同题归并。§3–4：多GPU局部FFT加边界耦合，拆分增加缩放保守性/迭代；标量光学算例。v1摘要379 s不与v3大算例2730 s混用。[v3](https://arxiv.org/html/2410.02395v3)、[证据](../experiments/survey&design/experiment02/REFERENCES.md#r05)。

### P76 · Vanka-SL-MG · Yovel/He/Treister · 2025预印本

**Vanka-smoothed shifted Laplacian multigrid preconditioners for the Helmholtz equations**；arXiv2511.16808v2。§3–5、表6：小块平滑降低所需移位，含三维Overthrust和作者Julia实现；10点/波长、CPU，三层与深层循环的收益不同。[正文](https://arxiv.org/html/2511.16808v2)、[证据](../experiments/survey&design/experiment02/REFERENCES.md#r07)。

### P77 · RS-CGC · Yovel/Treister · 2026预印本

**Scalable Multigrid Solver for the Helmholtz Equation: Real-Shifted Coarse Grid Correction**；arXiv2604.19501v1。§3–5：高阶网格转移与最粗Galerkin实移位对齐色散，三维约272万自由度10次迭代；10–12点/波长、粗解与临界规模条件不直接覆盖当前6点/波长。[正文](https://arxiv.org/html/2604.19501v1)、[证据](../experiments/survey&design/experiment02/REFERENCES.md#r08)。

### P78 · 三维matrix-free CSLP · Chen/Dwarka/Vuik · ETNA2023

**A matrix-free parallel solution method for the three-dimensional heterogeneous Helmholtz equation**；arXiv2308.06085，DOI10.1553/etna_vol59s270。§3–5：CSLP+三维MG，含IDR(4)/GMRES等和CPU并行大域；真三维基底能力，非GPU速度承诺。[正文](https://arxiv.org/html/2308.06085v1)、[证据](../experiments/survey&design/experiment02/REFERENCES.md#r09)。

### P79 · OSM/ORAS成本比较 · Martin/Jolivet/Geuzaine · 2025预印本

**Comparison of substructured non-overlapping domain decomposition and overlapping additive Schwarz methods for large-scale Helmholtz problems with multiple sources**；arXiv2506.16875v1。§3–5：全域预条件与界面真算子不同，三维CPU内存/分解/正交化/批RHS计时；不把64个独立RHS当本任务一份总场。[正文](https://arxiv.org/html/2506.16875v1)、[证据](../experiments/survey&design/experiment02/REFERENCES.md#r10)。

### P80 · L-Sweeps · Taus等 · JCP2020

**L-Sweeps: A scalable, parallel preconditioner for the high-frequency Helmholtz equation**；arXiv1909.01467。§3–5：棋盘扫描、局部因子和全局GMRES；含2D/3D，反射影响次数；公开所查仓库为2D。已有P66家族延伸。[正文](https://arxiv.org/html/1909.01467)、[证据](../experiments/survey&design/experiment02/REFERENCES.md#r11)。

### P81 · 三维polarized traces · Zepeda-Núñez等 · 2018预印本

**The method of polarized traces for the 3D Helmholtz equation**；arXiv1801.08655。§1.1、§2–4：介质离线准备与在线求解分离，批源流水线有并行/源数条件。已有扫描方向延伸，不计独立新机制。[正文](https://arxiv.org/html/1801.08655)、[证据](../experiments/survey&design/experiment02/REFERENCES.md#r11)。

### P82 · WaveHoltz · Appelö/Garcia/Runborg · SISC2020

**WaveHoltz: Iterative Solution of the Helmholtz Equation via the Wave Equation**；arXiv1910.10148。§2、§2.5、§4.3：短时受迫传播、滤波、Krylov，原版有阻抗边界及三维；正定/对称条件按原问题，不任意搬给PML。[正文](https://arxiv.org/html/1910.10148)、[证据](../experiments/survey&design/experiment02/REFERENCES.md#r12)。

### P83 · Multi-Frequency WaveHoltz · Appelö等 · 2025预印本

**A Multi-Frequency Helmholtz Solver Based on the WaveHoltz Algorithm**；arXiv2507.23613v1。§1/3–4：一次波传播配多滤波器，实验限简单能量守恒闭域；不是本轮单频总场优势的直接证据，也不据此否定P82开域能力。[正文](https://arxiv.org/html/2507.23613v1)、[证据](../experiments/survey&design/experiment02/REFERENCES.md#r12)。

### P84 · 插值伪微分预条件 · Acosta/Khajah/Palacios · SISC2025

**A new interpolated pseudodifferential preconditioner for the Helmholtz equation in heterogeneous media**；arXiv2409.16172v2，DOI10.1137/24M1642184。§4–6：声速一维插值FFT逆符号，二维合成头模；尖锐界面/独立衰减/PML扩展边界明确。降级为低setup比较线索。[正文](https://arxiv.org/html/2409.16172v2)、[证据](../experiments/survey&design/experiment02/REFERENCES.md#r20)。

### P85 · GPU压缩直接解 · Claus等 · IJHPCA2025

**A graphics processing unit accelerated sparse direct solver and preconditioner with block low rank compression**；DOI10.1177/10943420241288567。仅核出版社摘要/作者实现定位：STRUMPACK多前沿近似因子与GPU支持，不据未读数值表作当前速度或内存判断。[出版社](https://journals.sagepub.com/doi/10.1177/10943420241288567)、[证据](../experiments/survey&design/experiment02/REFERENCES.md#r21)。

### P86 · Hk-GenEO · Dolean/Fry/Graham/Langer · 2024预印本

**Schwarz preconditioner with Hk-GenEO coarse space for the indefinite Helmholtz problem**；arXiv2406.06283v1。定向读问题、谱粗空间和理论部分；数值未逐表抽取。说明不定Helmholtz有传统谱粗空间竞争，未作为三维经颅性能证据。[正文](https://arxiv.org/html/2406.06283v1)、[证据](../experiments/survey&design/experiment02/REFERENCES.md#r22)。

## 非论文网页（保留查重，不计入研究条目总数）

**RF Pulse design and parallel transmission (pTx)**，PTB 网页，Z=`MCHUDCSB`。属于 MRI 射频脉冲/并行发射主题；当前摘要只含机构介绍，不据此提炼具体方法。位于 `tus_surrogate` 根收藏夹。

**W02 · NSO作者仓库**：[Neural Schur Complement Operators](https://github.com/ansschh/NSO)。2026-10-16仅核README：SPD粗到细迁移中学`ker R`细节并保持粗预测。独立论文/正式发表未核，不算论文实证；作为神经Schur机制查重线索。

## 维护方式

后续新论文只追加一条：题名/简称、年份、标识、一两句任务与机制、阅读状态、证据入口。已有论文补新证据时更新原条目，并明确新增内容；“本项目已试/已排除”必须另附具体实验结果或用户决定，不能由入库状态推断。
