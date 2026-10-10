# 架构调研证据入口 — 2026-10-09—10

状态：本轮完成文献筛选、机制核查与候选设计；未运行V10实验。单Agent。入口为AGENTS→MISSION→REVIEW；任务书基线按其快照继承。

## 检索问题

1. 粗层怎样承载振荡场，避免把不同相位、方向混成一个平滑值？寻找多通道多重网格、波包、相位搬移的直接证据。
2. 源条件怎样在传播计算中与介质持续交互？寻找可变源完整复场、多输入算子、介质生成局部权重。
3. 有限空间状态是否能同时传递长程条件和相位？寻找扫描路径与状态类型消融；区分视觉分类和波场。
4. 少量迭代是否真正改正场错误？区分学习状态更新、数值残差校正、预条件器；计入全部步骤。
5. 固定介质能否分解为源系数与空间响应？寻找核的分块压缩、传播几何及低秩失效条件。

## 查重与增量

首先读取[统一索引](../../docs/literature_seen_index.md)。P03/P07/P08/P09/P26/P27均为已知工作；P26/P27从摘要登记补到正文证据。

索引外再定向命中历史材料：

- [旧架构组件目录](../../docs/literature/known_direction_notes.md#catalog)：MIFNO、WIRE、单/多载波、核查询与粗全局/细残差已有讨论。
- [旧检索记录S-ROOT-14](../../docs/literature/known_direction_notes.md#butterfly)：Butterfly压缩已有先例。
- [旧新颖性地图](../../docs/literature/known_direction_notes.md#landscape)：Born、边界核、多载波、POD均有相邻工作。
- [相位因子旧设计](../../docs/literature/known_direction_notes.md#phase)：PhaseDNN与走时分解已知。
- [V10 R002结果](../../docs/evidence/v10_representation.md#r002)：目标旋转小网络改善1.82%，训练拟合仍弱；保留方向，不能用粗重建收益替代源泛化。

本轮将17篇索引外工作登记为P28–P44。**新增索引条目不等于全项目首次发现。**历史V8目标、raw/叠加合同不继承。当前`docs/core_papers/README.md`已在用户文档迁移改动中删除；从docs地图检查后没有恢复或重建旧卡片。

## 原文入口及阅读深度

| 证据组 | 定向阅读 | 单一笔记入口 |
| --- | --- | --- |
| P27、P34、P37–P39 | McMg v1 §3/4与附录；Wave-ADR §3/4；WIRE §3；MFN机制；PhaseDNN已知先例 | [phase_space/papers](phase_space/papers/README.md) |
| P07、P31–P33、P40 | P07已有核查表3；MgNO原文附录D.3；OpenBreastUS表II/VII与附录B；SC-NO **v2** §3/4及表3，追查同组数值归因；MIFNO论文与作者代码入口 | [medium_source/papers](medium_source/papers/README.md) |
| P03、P35–P36 | TUSNet已有正文核查；Mamba §3.6；VMamba扫描路径表5 | [spatial_state/papers](spatial_state/papers/README.md) |
| P09、P26、P28–P30、P43–P44 | 已知Helmnet记录；Xiang v1 §4.2.2；LBS pp.2–4；NBSO表1/5；NSNO §4/5；HINTS补到正文§2.3–2.5及附录S1；OpenWaves **v4** 正文/补充表S9/S12 | [physical_iteration/papers](physical_iteration/papers/README.md) |
| P12、P41–P42 | GreenONet已有索引；FIONet正文§2/3及作者仓库；BNet2正文/官方摘要 | [source_kernel/papers](source_kernel/papers/README.md) |

不把定向正文核查标成全篇逐字精读。HINTS补查真实三维、混合过程与规模边界，不从计时图造精确倍数。论文图线未数字化，不从图上虚构精确增益。所有精度指标按论文对象记录，V10仍只用形状指标。

## 会改变判断的版本/归属核查

- OpenBreastUS表II的MgNO与SC-NO表2的MgNO-self是同组结果。SC-NO v2明确说明此别名关系；合并计算证据，不能记为独立复现。
- SC-NO v1没有USCT骨架内自组合对照；2026-08-02 v2新增25%子集、400 kHz、30 epoch消融：MgNO `0.0194→0.0151`，FNO和U-Net的self版均更差。§3将同一对数值描述为目标深度5的direct/T&U，三种初始化有误差范围；当前按结构/深度/训练策略组合计证，尚未拆净独立共享效应。保留“特定骨架上值得测试有限更新”，不将22.16%当纯架构收益。
- OpenWaves标题与应用含3D，但v4 §III-A/IV-B说明主神经前向为二维，轴向扫描后堆成体；其完整3D对照使用CBS。保留骨组织强散射架构证据，不能作为三维神经复场已解决的先例。
- HINTS正文具有真3D环柱系统至4,462,368自由度，保留大系统互补校正证据；作者报告小系统反而更贵。其GRF源/低波数算例不同于500 kHz多波长点源颅骨场。

## 本轮设计输出

五个机制方向各有README/papers/DESIGN/VALIDATION，M0明确输入、复状态尺度、介质门控、两次V-cycle、rank8轴向全域通路与细解码。解析成本脚本包含全部明确卷积/矩阵步骤，原介质通道数保留C_m变量；内存为单张量存储，不冒充峰值或V100计时。共同验证将oracle表示与真实预测、架构与训练策略、latent差异与物理残差分别取证。

## 本轮实施边界

仓库已有大量迁移改动；本轮仅提交专题新增文件与统一论文索引增量。未改MISSION/REVIEW、科学合同、实验配置、用户Todo；未安装环境、访问服务器、训练或读正式test Label。后续的VALIDATION均为设计。
