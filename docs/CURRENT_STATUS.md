# 当前状态：experiment02深入比较与报告重写已完成

资料更新：2026-10-19。文献/源码比较已完成，待人工阅读验收。本次未访问实验服务器、未运行求解或训练、未修改既有V10接口。

## 当前任务和交付

在可更换介质下，对临时给定的同频多源配置求一份总Re/Im复场形状。先相加构造总源项，再求一次总场；配置中源的个数K与同一介质复用的配置次数Q分别计算。

- [综合报告](../experiments/survey&design/experiment02/REPORT.md)：七项缺口已逐项补齐；完整C1–C4基底、准备及在线成本、学习接入与换介质证据均已重写。
- [证据入口](../experiments/survey&design/experiment02/REFERENCES.md)：30组来源、8组固定提交源码核查，明确测试版本、计时范围和可获得实现边界。
- [检索记录](../experiments/survey&design/experiment02/SEARCH_LOG.md)保留首轮不足、补读过程、数字纠正和收束依据。统一索引连续至P98；同一方法演进不重复计作独立成功。
- 主比较为变密度Born、优化两网格/粗扫描和递归deflation/CSLP，压缩分解条件性保留。学习粗层/全局校正优先，学习构造次之；GPU时域和快速传播分别保留强参照与条件速度支线。
- [既有本地工程证据摘要](evidence/experiment02_existing_engineering.md)用于约束迁移推断，不作为本轮新增实测。

当前MIDA任务同输入、同精度、同硬件的胜出路线，以及充分训练后的速度/泛化，仍需要独立实验合同。文献比较的完成不表示这些实验已经执行，也不恢复前轮自主运行安排。

本地来源提交：`cbd5c00`（原文与实现证据）和 `c141a45`（综合比较重写）。仅作为来源标识，不上传完整本地提交历史。

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
