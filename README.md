# 三维总复声场求解：当前调查与历史资料

更新：2026-10-19。main 是供 GPT 阅读的精选资料。当前轮次为 **experiment02：传统求解路线、强迭代基底与神经网络接入位置比较**。七项深入补查及报告重写已完成，待人工阅读验收；本轮没有新增求解或训练实测。

## 阅读顺序

1. [综合报告](experiments/survey&design/experiment02/REPORT.md)：先读判断，再看完整强基底、成本与网络接入位置。
2. [关键证据](experiments/survey&design/experiment02/REFERENCES.md)：30组来源入口、原文定位及8组固定提交的作者实现核查。
3. [七项补齐对应表](experiments/survey&design/experiment02/REPORT.md#10-七项缺口的补齐结果与最终取舍)：补查如何改变首轮结论。
4. [任务书](experiments/survey&design/experiment02/MISSION.md)、[评审要求](experiments/survey&design/experiment02/REVIEW.md)、[检索记录](experiments/survey&design/experiment02/SEARCH_LOG.md)与[统一文献索引](docs/literature_seen_index.md)。

本轮为可更换介质、临时多个同频源共同作用、交付一份总复场形状；源数不是独立求解次数。该目标仍是比较研究，不修改既有V10单源接口、Label或已运行实验。

## 当前判断与状态

主比较保留变密度Born、优化两网格配粗扫描、递归deflation配CSLP；压缩多前沿分解是大内存和多配置复用条件下的候选。Born的工程接近性不等于速度第一。学习优先研究强基底中昂贵的粗层/全局校正，学习构造次之。报告区分准备、在线、内层求解、缓存、残差检查和输出，并给出压缩精度随配置次数摊销的原文数值例子。

优化GPU时域保留强全波参照；mSOUND/HAS保留有明确源几何及误差条件的快速支线。文献与作者实现的比较已完成；当前任务同输入/硬件的实际速度、充分训练精度及未见介质表现仍需另行实验，见[报告剩余问题](experiments/survey&design/experiment02/REPORT.md#11-收束后具体还剩什么)。

- [当前experiment02](experiments/survey&design/experiment02/README.md)与[当前状态](docs/CURRENT_STATUS.md)。
- [前轮exploration 01](<experiments/survey&design/exploration 01/README.md>)：创新机制探索与未验证界面候选，保留为历史研究。
- [更早exploration00](experiments/survey&design/exploration00/README.md)：架构、M0、McMg深化与早期查重。
- [资料地图](docs/README.md)、[来源地图](docs/SOURCE_MAP.md)和[V10科学合同](docs/project_design_handoff_v10.md)。

文献事实、迁移分析、既有工程检查和科学结果分别解释。完整代码、数据、checkpoint、服务器配置和个人Todo不随阅读快照发布。
