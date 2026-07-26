# 第一版网络设计记录

## 目的

本目录只记录第一版 3D 单阵元“相对复场 + 绝对尺度”网络的设计问题、研究顺序和证据。它不把估算结果写成正式实验结论。

当前目标：固定 MIDA、500 kHz 与激励幅值，网络输入单通道三维声速场，以理想方向性点源的位置和法向为主要变量；target focus 只在网络外用于相位 / 延迟、阵列组合和评价。主网络预测相对复声场，A4 预测绝对尺度，共同重建单阵元绝对 `Re/Im`，再在网络外相干叠加。

## 已冻结、不再重复讨论的决定

1. 第一版不用 GAN。
2. 第一版上采样使用 `ConvTranspose3d(kernel_size=2, stride=2)`。
3. 激励相位不作为网络输入；网络预测统一参考相位下的相对 `q_Re/q_Im`，外部对重建后的绝对复场施加阵元相位并相干叠加。
4. 采用逐样本 `Pmax_brain` 归一化主复场，并由 A4 独立预测该尺度。

## 工作流

对每一个待定问题，依次执行：

1. 明确 2--4 个候选；
2. 分开记录论文证据、代码/仓库证据、本项目推导和未知项；
3. 给出一个第一版选择及其适用边界；
4. 设计能区分候选的最小实验；
5. 与用户讨论、答疑后，再冻结决定。

当前探索顺序：

`T2 -> A1 -> A2 -> A3 -> A4 -> L1 -> L2 -> L4 -> L3 -> T1 -> T3`

选择 T2 作为起点，是因为三维物理范围、网格和显存会先约束网络深度、宽度和 batch；这不是用显存反向决定物理分辨率，物理分辨率仍须通过波长和网格收敛确认。

## 文件

- `question_checklist.md`：三大块的全部待确定问题和顺序。
- `T2_grid_memory_batch.md`：T2 的第一轮研究、估算和当前判断。
- `t2_memory_probe.py`：当前五次下采样 A1 候选的整步 CUDA 显存探针。
- `t2_current_memory_analysis.py`：拟合当前探针并生成 `288³` 显存规划值和图。
- `A1_depth_width.md`：A1 的深度、宽度、感受野、显存比较和 V0 决定。
- `A2_geometry_conditioning_papers.md`：A2 前置调研；两篇直接相关论文中的阵元坐标表示、注入层和消融证据。
- `A2_geometry_conditioning_decision.md`：A2a 已确认的方向性点源六维条件与瓶颈接入方法；位置和法向均为变量，不含有限孔径。
- `A2b_layer_design.md`：只保存 A2b 的短状态；具体参数、依据、解释和讨论在对话中完成。
- `A3_reim_output_head_decision.md`：A3 已确认的共享 U-Net 双通道相对复场输出头。
- `A4_pmax_auxiliary_head_decision.md`：A4 已确认的绝对尺度头、两阶段训练和绝对复场重建协议。

## 状态

- T2 已形成 V0 决定：单通道声速输入、`144³ mm³`、`0.5 mm`、`288³`、BF16 网络前向、FP32 损失、native batch 1。
- A2a 已确认输入为理想方向性点源的六维位置/法向；二者均会变化，具体范围未定；不含孔径、直径、表面点集或有限孔径 source mask。
- 当前五层 A1 已完成 8 个小尺寸整步显存探针；`288³` 加 15% 余量后的外推为 `18.474 GiB`，仍需 24 GB GPU 直接实测。
- A1 已更新为 5 次下采样，通道为 `8 -> 16 -> 32 -> 64 -> 128 -> 128`；最底层为 `9³`，理论感受野约 `190–206 mm`。真实最大路径已撤回为未知，后续须结合几何协议和有效感受野验证五层充分性。
- A2a 点源条件接入及共享融合输出已确认，详见 `A2_geometry_conditioning_decision.md`；`Z` 为 `1×1×1 Conv + GroupNorm + ReLU` 的输出。
- A2 已完成：双卷积块采用 `Conv3d -> GroupNorm -> LeakyReLU(0.01)`，GroupNorm 固定每组 8 通道；使用 `MaxPool3d(2,2)`、`ConvTranspose3d(2,2) -> concat -> 双卷积块`；相关卷积 `bias=false`，采用 Kaiming normal 初始化；不使用 CBAM、Dropout、残差块或深监督。
- A3 已完成：共享 U-Net 以线性 `Conv3d(8,2,3,1,1)` 输出 `q_Re/q_Im`；末层无归一化和 activation，`bias=true`，Xavier normal 初始化。
- A4 绝对尺度头已确认：预测 `A_hat=Pmax_brain`，并按 `A_hat/max|q_hat|` 统一缩放两个复数通道，得到绝对 `Re/Im`。brain mask 用于归一化、label、重建和指标；PML 位于物理网格外。
- `t2_analyze_results.py`、`t2_domain_ppt_figure.py`、`t2_placement_recheck.py` 和 `t2_literature_geometry.py` 仍保存旧 `82 mm` 几何探针假设。它们是历史工程材料，不代表当前最大路径；在几何范围重新确认前不得作为现行设计依据运行或引用。
