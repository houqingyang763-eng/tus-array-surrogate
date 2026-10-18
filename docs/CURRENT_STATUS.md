# 当前状态：experiment02比较调查已完成

资料更新：2026-10-18。本次只做公开文献研究和Markdown交付，未访问实验服务器、未运行求解或训练、未修改既有V10接口。

## 当前任务和交付

在可更换介质下，对临时给定的同频多源配置求一份总Re/Im复场形状。重点比较传统大路线、少数强迭代基底、网络具体接入位置，并分清离线训练、介质准备和每配置成本。

- [综合报告](../experiments/survey&design/experiment02/REPORT.md)：文献比较完成，有条件推荐Born、先进MG与传播感知DD；快速传播保留几何条件支线。
- [证据入口](../experiments/survey&design/experiment02/REFERENCES.md)与[检索记录](../experiments/survey&design/experiment02/SEARCH_LOG.md)。
- 文献索引新增P74–P86共13编号；P57升级全文。补录不等于全项目首次发现。
- 本地阶段提交为 `5af0d86` 和 `160f522`，仅作来源标识，不上传完整本地提交历史。

推荐尚不是MIDA实测排序。下一步会改变选择的具体工作集中在报告§9；实际计算需要独立实验合同。本轮不要求立即原创网络，也不恢复前轮连续设计授权。

## 前轮exploration 01记录（历史快照）

以下保留前轮原有日期、候选及证据，不作为本轮已选方案：

资料同步：2026-10-18；本轮研究材料日期2026-10-16。仅同步文献与设计，没有查询或改变远端实验进程。

### 当前任务

固定MIDA、500 kHz、可变颅外单点源，交付颅内Re/Im复场形状。完整物理域384×480×224 @0.5 mm，临时输出ROI352×352×192。研究目标是以真实物理残差迭代为基础，提出有实质方法贡献的学习加速机制。[任务书](<../experiments/survey&design/exploration 01/MISSION.md>)。

### 已完成

- 重建任务书、审查与工作规则，明确纯迁移和标准骨干替换只作基线。
- 完成首轮检索和跨领域机制查重，论文编号补至P73，另存W02作者仓库线索及P49版本更新。
- 只保留一个继续设计的候选：**骨层双面耦合的界面残差校正**。法向参考块、学习切向/跨面作用与体残差回注的分工详见[DESIGN](<../experiments/survey&design/exploration 01/coupled_interface/DESIGN.md>)。
- 给出解析存储/运算口径、外层FGMRES基向量成本与贡献消融方案；文档链接、编号和块消元代数已检查。

本地研究提交：`9485a88`（框架）与`3e3386b`（首轮研究），是来源标识，不表示这些完整本地提交历史随资料包上传。

### 当前判断与下一步

候选尚未实现、训练或实测。最有区分力的问题是界面校正的表示价值，以及额外体域算子成本能否被收益抵消。[综合判断](<../experiments/survey&design/exploration 01/SYNTHESIS.md>)与[验证设计](<../experiments/survey&design/exploration 01/coupled_interface/VALIDATION.md>)。

McMg是强方法对照和创新深度参照。上一轮M0等材料单独保存在[exploration00](../experiments/survey&design/exploration00/README.md)。旧四秒完整训练更新目标不作为本轮求解推理门槛。

历史T512-V9BASE e280 train/val unit-shape L2为0.348609/0.461938，来自截至2026-10-08的既有记录；不是本次查询的新结果。[基线来源](evidence/v10_baseline.md)。
