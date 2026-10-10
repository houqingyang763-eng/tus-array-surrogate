# 经颅复声场预测：V10研究资料

这是供GPT网页版读取的精简资料快照，整理日期2026-10-10。当前研究：固定MIDA、500 kHz、可变颅外单点源，预测大三维ROI内颅内Re/Im复声场形状。

## 给GPT的最短阅读顺序

1. [当前状态与Codex已完成工作](docs/CURRENT_STATUS.md)：项目现在研究什么、已有结果、新设计处于什么阶段。
2. [V10科学合同](docs/project_design_handoff_v10.md)：输入输出、数据、评价与保留的边界。
3. [本轮架构综合判断](experiments/survey&design/SYNTHESIS.md)：论文怎样改变取舍，主候选为什么这样设计。
4. 按问题读取[论文索引](docs/literature_seen_index.md)、[M0设计](experiments/survey&design/medium_source/DESIGN.md)或[验证方案](experiments/survey&design/VALIDATION.md)。

## 目录

- [docs](docs/README.md)：V10、已读论文、最少必要证据及来源地图。
- [experiments/survey&design](experiments/survey&design/README.md)：调研任务书、审查规则、五个方向的论文/设计/验证与解析成本。

解释时分别说清：已有运行事实、论文结果、诊断线索、候选假设。新M0尚未训练，82.15 GMAC是解析前向核心运算量，4 s完整五卡更新尚待实测；基线引用截至2026-10-08记录，不代表实时服务器状态。

本分支展示部分研究资料，完整代码、历史实验、Label/checkpoint、日志和用户Todo保留在本地或原存储位置。旧版本与旧实验从当前目录清理，Git历史仍保留。导出取舍与来源见[来源地图](docs/SOURCE_MAP.md)。
