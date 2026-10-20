# 经颅复声场求解：当前调研资料

更新：2026-10-20。当前轮次为exploration04：简单传统底座上的集中学习改进。S1文献与源码比较已完成，推荐现有变密度Born/Universal Split；尚未设计学习方案或启动实验。

1. [当前报告](experiments/survey&design/exploration04_simple_baseline/REPORT.md)：明确推荐、与标量CBS/普通CSLP比较、论文结果和关键代码解释。
2. [来源定位](experiments/survey&design/exploration04_simple_baseline/REFERENCES.md)：固定作者版本、原文章节/图表及本地证据摘要。
3. [任务书](experiments/survey&design/exploration04_simple_baseline/MISSION.md)与[本轮入口](experiments/survey&design/exploration04_simple_baseline/README.md)。
4. [历史归档](experiments/survey&design/README.md)、[统一论文索引](docs/literature_seen_index.md)、[来源地图](docs/SOURCE_MAP.md)。

目标是六周内可理解、可复现的传统底座与小而有效的学习改进。1%与1–10秒是讨论示例，不是冻结阈值；不强制残差10⁻⁶，不要求超过McMg。多源总场与换介质是研究需求，不自动修改V10接口或授权实验。

本仓库main仍是精选阅读快照；完整本地代码、数据、服务器控制、日志、checkpoint、个人Todo和PDF原文不随此次同步上传。
