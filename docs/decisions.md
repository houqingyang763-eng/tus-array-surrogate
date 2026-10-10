# 当前适用决定：V10阅读版

提炼自本地decisions及后续V10 handoff，2026-10-10。这里只列持续适用项；旧迁移阶段的“尚未选网络/尚未选档位”不作为当前状态。

1. 唯一当前主线V10，颅外单点源→颅内Re/Im形状；V8/V9只提供历史工程或比较线索。
2. 头皮外移10 mm、水耦合、各向同性单点，500 kHz；保持完整求解域与普通档临时网络ROI。
3. 所有新评价禁用raw；主指标unit-shape L2，保留共同相位，不恢复A4/阵列拼接/Park目标。
4. A档55 mm与512/32/64划分固定，val选模型、test最终确认；不继承V9颅内源划分。
5. 实际V10实验归属本地唯一route；实验设计、当前机器状态与结果分由protocol、CONTROL、RESULTS记录。
6. 持续关闭activation checkpointing：正式配置显式false。若OOM，报告并落实新的授权；不得自动改batch/precision/网络/loss/GPU或重新开启。架构成本页讨论重算是设计可能性，不替代此执行决定。
7. 用户Todo由用户独占；本包不发布该区。文献/诊断/设计/运行事实与科学确认分开，新的VALIDATION不自动授权运行。

完整稳定合同见[handoff](project_design_handoff_v10.md)，运行事实快照见[状态](CURRENT_STATUS.md)。
