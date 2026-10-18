# V10科学合同：GitHub阅读版

阅读版更新2026-10-18。来源为本地同名handoff/构想/decisions，及2026-10-16采纳的exploration 01任务书。旧文件中“Label生成中”“网络未选”的2026-10-03机器/阶段快照未沿用为今日状态；已有基线与本轮研究见[CURRENT_STATUS](CURRENT_STATUS.md)。本页不执行实验。

| 对象 | 当前适用合同 |
|---|---|
| 目标 | 固定MIDA、颅外单点源→颅内Re/Im复声场形状；相对幅值与共同相位 |
| 源 | 头皮外移10 mm、水耦合、各向同性单网格additive压力源；500 kHz、1 Pa、零初相、四周期渐入 |
| 求解域 | 完整384×480×224 @0.5 mm，原介质/PML/求解配置不因网络ROI缩小 |
| 临时网络ROI | 352×352×192，176×176×96 mm³；XYZ [16:368,64:416,32:224] |
| 源区域与划分 | A档：颅骨交线沿曲面内缩55 mm，保留颅顶；512 train/32 val/64 test，同域互斥，holdout固定 |
| 基线输入输出 | 介质[1通道]、P0[Re/Im]、源XYZ；输出全ROI Re/Im，评价在共同有效mask |
| 评价 | Re/Im在mask联合归一化，unit-shape L2；不旋转全局相位、不逐slice归一化，禁用raw |
| 模型选择 | val平均unit-shape L2选checkpoint；test在方案选定后确认，不参与调参 |
| 当前成本口径 | 全部物理迭代和输出成本计入，setup/编译/训练另报；旧四秒训练指标仅为历史约束，不自动用于当前求解器 |
| 现有基线 | T512-V9BASE六级3D U-Net；纯Lshape，Lgrad/Helmholtz关闭。e280 train .348609 /val .461938，正式test本包未收录 |
| 当前候选 | 骨层双面耦合界面校正，尚未实现/训练/实测；M0已归上一轮历史 |

网络ROI共23,789,568体素；当前共同有效颅内mask为5,101,889体素，含脑实质/CSF/血液。这是记录中的评价mask，不将临时ROI写成最终全脑论文域。

实际新实验仍由本地V10 route中的protocol/CONTROL落实；本包未发布实时CONTROL、服务器地址、完整runner或训练数据。已有正式执行规则（例如关闭activation checkpointing）见[decisions](decisions.md)。

证据：[基线](evidence/v10_baseline.md)、[表示诊断](evidence/v10_representation.md)、[本轮任务书](<../experiments/survey&design/exploration 01/MISSION.md>)。
