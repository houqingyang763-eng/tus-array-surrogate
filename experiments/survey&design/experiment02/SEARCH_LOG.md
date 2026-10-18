# experiment02：检索与取舍记录

日期：2026-10-18。范围为公开文献、作者代码和官方文档。按 `AGENTS → MISSION → REVIEW` 启动，单 Agent；未访问服务器、未执行声学/训练实验、未安装环境、未操作 Zotero。

## 1. 起点与查重

- 先检索 `docs/literature_seen_index.md` 的题名、标识、Born、多重网格、FGMRES、Schur、mSOUND 等家族词。
- 命中 P22、P27、P45、P46、P57、P61–P68 等；复用现有卡片。`docs/core_papers/README.md` 当前工作树不存在，按本轮规则沿索引到 exploration00 / exploration 01，未恢复历史删除文件。
- 旧轮候选与连续设计授权不继承。多源总场、可更换介质，以 experiment02 最新任务书为准。
- 论文导读规则和分类文件已读；分类文件中的旧峰压/阵列目标不覆盖当前任务。本轮为用户明确要求的综合调查，采用任务书规定的综合报告格式。

## 2. 检索链与改变判断的结果

| 链 | 代表检索词/入口 | 结果与取舍 | 证据 |
| --- | --- | --- | --- |
| 大路线 | `transcranial ultrasound benchmark frequency domain time domain`, P22 | 时域、频域全波、单向传播要先分层；不把 McMg 与时域并列 | R01–R02 |
| 近期快速传播 | `mSOUND fully heterogeneous skull validation 2026` | P57 从摘要升级全文；必须合入 FOCUS 源平面成本，任意环绕点源输入成为关键限制 | R06 |
| Born 强基底 | `convergent Born`, `heterogeneous density`, `domain decomposition modified Born` | P45 保留物理贴合度；新补 P74/P75；拆域主要解决容量，增加迭代及通信，不当免费提速 | R03–R05 |
| 近期强 MG | `Helmholtz shifted Laplacian 3D 2025 2026` | 新补 Vanka、RS-CGC；基础 SL 的慢不能排除先进 MG；同时记录 10–12 点/波长和粗解条件 | R07–R09 |
| 大三维 DD | `ORAS OSM 3D Helmholtz multiple sources`, `sweeping`, `polarized traces` | 确认可复用局部因子/界面方法；独立 RHS 批量结果与本轮单总场分开；局部近似放预条件器和放真算子后果不同 | R10–R11 |
| 时域—频域桥接 | `WaveHoltz 3D`, `multi frequency WaveHoltz 2025` | 原版已有阻抗边界/三维，不能把新多频闭域限制误说成整个家族限制；单频任务暂不优先该扩展 | R12 |
| 学习加速 | McMg / NPBS / encoder–solver 旧卡片后定向原文 | setup 与残差路径分离最契合换介质复用；mini-retrain 单列；少迭代并不总更快 | R13–R16 |
| 相位/界面 | Wave-ADR、MLORAS、HINTS scattering | 走时依赖源；MLORAS 的正定问题不能冒充声学不定问题；3D 障碍迁移不等于跨患者异质体 | R17–R18 |
| 直接预测反查 | `Deep Neural Helmholtz Operators 3D` 与既有 P51/P54/P55 | P08 确有 0.3 s 的真三维直接算子证据，但规模/误差/物理任务不满足当前主候选条件；局部峰压网络不进入复场核心对照 | R19 |
| 可能遗漏的传统竞争者 | `interpolated pseudodifferential preconditioner`, `STRUMPACK Helmholtz GPU`, Hk-GenEO | 补 P84–P86；低 setup FFT 近似、压缩直接解、谱粗空间均保留条件性位置，未据摘要给当前性能排名 | R20–R22 |
| Born 内部替代 | P53 题名/DOI、出版社及作者机构 | 未取得全文；留作可能改变 Born 内部选择的具体缺口，不扩大为无限查找 | R23 |

R 编号对应 [REFERENCES](REFERENCES.md)。检索同时覆盖近年实现和必要经典机制；没有把搜索结果页、聚合站或 AI 摘要作为性能判断来源。

## 3. 定向复核和纠正

1. **mSOUND**：PMC 网页连续遇到验证页，经 Europe PMC 同一作者稿的公开全文 XML 读取正文和表格。核对 0.5 mm：287.77 + 36.45 = 324.22 s；3646.48 / 324.22 = 11.2469。原文仅传播部分约百倍，不能作为包括源处理的总流程倍数。没有把幅值 L2 当 Re/Im unit-shape L2。
2. **DD-Born 版本**：检索摘要出现 379 s；追到 v3 后大算例为 2730 s。记录版本及边界、硬件，不混用不同规模数字。
3. **OSM 文本抽取**：HTML 作者行混入模板姓名，arXiv 元数据确认为 Martin/Jolivet/Geuzaine。图 10 时间顺序有歧义，本文以表 4/5 为准。表中 64 个源是 64 个独立 RHS，非一份合成总场。
4. **先进 MG**：Vanka 三层本身很快，只与四/五层差基线比较会夸大收益；RS-CGC 三维测试约 272 万自由度，当前完整域约 4129 万格点。二者都是 CPU 文献计时，不能与 A6000 McMg 数字直接排列冠军。
5. **NPBS**：查到附录 H 为 H100，统一补进计时语境；表 3 的少迭代反而慢于 CBS 的分支保留。附录的 padding 尺寸叙述有歧义，本文只写正文 256² 和作者边界设置，不自行补算实际 padded 网格。
6. **直接 U-NO**：0.3 s 是所读版三维全部目标频率的前向，0.4 s/350 倍属于反演步；分别处理。其频域 loss 是 L1/L2 混合，不能替换项目 unit-shape L2。
7. **容量核算**：只执行网格数量、字节和论文计时四则运算；没有做求解、精度试验或 GPU 探测。全域一个 complex64 向量为 0.307617 GiB，四复场为 1.230469 GiB；FGMRES 的 V/Z 计数在报告明确列出假设。

## 4. 收束依据

主要路线、强迭代基底、网络接入位置、介质更换和总场计时已形成闭合比较。定向补检新增先进 MG 和 mSOUND 全文后，保留的取舍稳定为：Born 主基底、先进 MG 强竞争路线、传播感知 DD 条件性路线，外加有输入几何限制的快速传播支线。

继续增加同家族论文当前不会改变这个层级。仍会改变排序的事项集中到报告末尾的少数问题：当前规模的真实总场计时与形状曲线、换患者 setup/泛化、6 点/波长上的强 MG、P53 完整实现及 mSOUND 任意源接入。前几项需要另行批准计算验证，本轮不伪装成文献已给出的答案。

## 5. 保存与复查范围

本轮只保存 `experiment02/REPORT.md`、`REFERENCES.md`、本文件、入口状态更新及统一文献索引增量。已有不相关改动保持原样。最小验证为文档链接、编号、关键数字/单位和任务覆盖；只暂存这些明确路径，阶段本地提交，最终上传现有 `origin/main`。
