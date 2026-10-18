# Idea 查重检索记录

执行日期：2026-10-11，Asia/Shanghai。无起始年份限制，纳入截至当日已公开版本。检索目标和分类按 [AGENTS.md](AGENTS.md)；结论及原文定位见 [REPORT.md](REPORT.md)。本轮单 Agent、仅文献研究。

## 入口、已有证据与工作边界

先检查 Git 状态，再依次读取上级 AGENTS → MISSION → REVIEW、本目录原始要求，以及论文摘要/分类工作流。只迁移去重、原文核查、指标区分等规则；架构设计任务和训练预算不迁移。

检索前查[统一索引](../../../../docs/literature_seen_index.md)。P09/P26、McMg P27、Learned Born P28、NBSO P29、HINTS P43、OpenWaves P44、变密度Born P45均标为已知工作或方法家族延伸。复用 [physical_iteration证据](../physical_iteration/papers/README.md)、[McMg线证据](../McMg线/papers/README.md)和[既有跨论文比较](../../../../docs/zotero_cross_paper_comparison_20260930.md)。旧 core_papers入口因仓库已有文档迁移缺失，本轮沿现存证据链查找，未恢复旧文件。

初始 Git 有大量与本任务无关的既有修改/删除；统一索引初始无改动；本目录原先仅有未跟踪的查重要求.md。仅新建本任务三份文档并增量修改统一索引，原始要求不改写。PDF、抽取文本和图表核对页保存于 D:/tus-array-surrogate-experiments/idea_dedup_20261011，未放入仓库。未访问服务器、训练或运行求解器，未操作 Zotero。

## 通用与学术条目检索式

以下51条均在2026-10-11执行。来源是通用搜索及其学术条目结果；域过滤行另行注明。不是 Google Scholar/Scopus/WoS 全量被引检索。二手结果只用于找到原文。

| 编号 | 实际检索式 | 发现、处理或本轮增量 |
| --- | --- | --- |
| S01 | transcranial ultrasound neural preconditioner learned iterative Helmholtz solver | P09/P26已知；转原文 |
| S02 | transcranial ultrasound "learned" "Born" | P28及Born链；经颅动机不等于颅骨实验 |
| S03 | transcranial ultrasound neural multigrid Green solver | McMg/HINTS等已知方法；检查应用对象 |
| S04 | "transcranial" "learned" solver -site:researchgate.net -site:papers.cool -site:arxiv.gg | 学习求解候选扩展 |
| S05 | "skull" "neural" "preconditioner" | 神经预条件链，未凭标签判断 |
| S06 | "transcranial" "Green" "neural" | 大量神经生物学噪声，未作为证据 |
| S07 | "transcranial" "Born" "deep learning" | Born/NBSO链 |
| S08 | "Neural Preconditioned Born Series" | 新增P46；v1→v4归并 |
| S09 | "transcranial ultrasound" "neural" "solver" 3D | Nguyen学位论文/展示线索；不因查询含3D就认定真3D |
| S10 | "transcranial ultrasound" "learned Born" | P28原文及正式版 |
| S11 | transcranial ultrasound (Helmholtz OR solver) (learning OR preconditioning) | 域限制 pubmed.ncbi.nlm.nih.gov、pmc.ncbi.nlm.nih.gov；生物“preconditioning”噪声，改用结构化PubMed查询 |
| S12 | transcranial ultrasound learned solver preconditioner | 域限制 arxiv.org；P09/P26 |
| S13 | "transcranial ultrasound" "neural" "Green" -optogenetic -magnetic | 排除光遗传/磁刺激噪声 |
| S14 | "Approximation of Sound Propagation by Neural Networks" Nguyen | P48大学元数据及全文 |
| S15 | "Neural network preconditioning" "Helmholtz" Giraud Mycek Xiang 2025 | P49，取得机构报告全文 |
| S16 | "transcranial ultrasound" "learned optimizer" citations | P09后续比较及P26 |
| S17 | "Solution of large linear systems with a massive number of right-hand sides and machine learning" Xiang | P47作者博士论文；早期经颅FGMRES先例 |
| S18 | "Son Hai Nguyen" "Helmholtz" | P48同作者/同题归并 |
| S19 | "Approximation of Sound Propagation" neural network | 会议展示与学位论文归并 |
| S20 | "transcranial" "preconditioning" -site:papers.cool -site:researchgate.net -site:academ.us | 数值预条件与生物预处理区别 |
| S21 | "10.1121/10.0017937" | P28正式版2023，非另计新论文 |
| S22 | "transcranial ultrasound" "hybrid solver" neural | PACT混合重建等近邻 |
| S23 | "skull" "learned" "Green" ultrasound | 传播/Green宽口径覆盖；控制与逆问题单列 |
| S24 | "transcranial" "neural" "Born series" | P28/P29/P45；检查有无颅骨 |
| S25 | "Fast aberration correction in 3D transcranial photoacoustic" learning | P56作者全文，输出重建图像，排除正向复场 |
| S26 | "transcranial" "neural multigrid" | 未新增经颅神经多重网格实证 |
| S27 | "skull" "learned" "propagation operator" | 同上及代理候选 |
| S28 | "transcranial ultrasound" "neural preconditioner" 2026 | P26；查新公开版本 |
| S29 | "Multivariable-incorporating super-resolution residual network" phase | P51出版社摘要，复场仍待核 |
| S30 | "Shpakovych" "preconditioning" "2023" Helmholtz report | P59 RT-0518，Inria元数据核实，全文访问缺口 |
| S31 | "tFUSFormer" "phase" | P54及作者后续线 |
| S32 | "tFUSFormer" full text | 找到大学PDF线索；原链接404，后由IEEE取得作者接受稿 |
| S33 | "tFUSFormer" "complex" | 未凭“complex”修饰词认定复数场；正文/代码确认pmax |
| S34 | "Optimization of acoustic lens design for transcranial holographic ultrasound" "active learning" | P58出版社摘要，逆设计代理 |
| S35 | "tFUSOperator" paper 2026 | P55 arXiv/会议稿/作者代码；明确pmax |
| S36 | transcranial ultrasound ("learned solver" OR "learned preconditioner" OR "neural preconditioner") -site:researchgate.net -site:papers.cool | 收束准备轮：P26/P09、已有P02；未新增核心候选 |
| S37 | (tFUS OR TUS OR HIFU) skull "neural" ("Green function" OR "propagation operator") | 生物刺激及传统传播噪声 |
| S38 | "transcranial" ("unrolled" OR "hybrid") ("Helmholtz" OR "finite difference") neural | 学习正向/逆向过程交叉核查 |
| S39 | "tFUSFormer" site:yscholarhub.yonsei.ac.kr "maximum pressure" | 定向补输出证据；后用全文/代码确认 |
| S40 | "transcranial ultrasound" "learned iterative" -site:researchgate.net -site:papers.cool | 仅已有P26/P09及Born动机 |
| S41 | "skull" "neural" "Helmholtz" "preconditioner" -site:researchgate.net -site:papers.cool | 沿作者/引文链复核 |
| S42 | "transcranial" "Green function" "deep learning" simulation -magnetic -optogenetic | 逆问题、非声学及传统源编码排除 |
| S43 | "transcranial" "Born series" learning -site:researchgate.net -site:papers.cool | P28及P45重复，未新增核心候选 |
| S44 | "transcranial" ("learning-based" OR learned) ("solver" OR preconditioner) Helmholtz -site:researchgate.net -site:papers.cool | 收束轮1：P09/P26/P49/P45复现 |
| S45 | "skull" ("learned multigrid" OR "learned Green" OR "neural solver") acoustic -site:researchgate.net | 通用FNS/McMg等非经颅方法；不扩张精选参考数量 |
| S46 | "MRgFUS" ("preconditioner" OR "learned solver" OR "Green") neural | 检出机器人相位控制（liver/pancreas）；非颅骨正向复场 |
| S47 | "tFUS" ("Born" OR "residual correction" OR "iterative solver") learning | 未新增符合对象/机制的经颅候选 |
| S48 | "transcranial ultrasound" "operator acceleration" learning | 收束轮2：无新增经颅复场学习求解候选 |
| S49 | "transcranial" "learned propagation" acoustic | 同上；已有主动学习透镜/代理 |
| S50 | "skull" "learning" "FGMRES" -site:researchgate.net -site:papers.cool | 已核P26及神经预条件作者链 |
| S51 | "transcranial" "neural" "multigrid" -site:researchgate.net -site:papers.cool | 电场/tDCS/TMS噪声，不与超声混淆 |

其他搜索结果包括通用NCS-BEMNet、随机神经基预条件、瞬态SPD求解在线预条件，以及非学习的头部伪微分预条件。未见其经颅学习复场实证；仅作范围排除，未逐篇扩张全文审查。2026 arXiv 2606.05628的题名线索为非线性FUS治疗/监测，摘要属透镜拓扑优化等主题，本轮未据此登记学习预条件先例。

## PubMed结构化交叉检索

网站部分页面返回访问检查，改用 NCBI ESearch → ESummary → 重点 EFetch（官方公开API）。retmax=200，两组命中均小于上限，无分页遗漏。**47个不同条目完成题名/可见主题筛查，重点10条取得API摘要；并非47篇全文阅读。**

**Q1：19条**

    (transcranial[Title/Abstract] OR skull[Title/Abstract]) AND (ultrasound[Title/Abstract] OR acoustic[Title/Abstract]) AND (Helmholtz[Title/Abstract] OR solver[Title/Abstract] OR precondition*[Title/Abstract] OR "Born series"[Title/Abstract])

**Q2：29条**

    (transcranial[Title/Abstract] OR skull[Title/Abstract]) AND ultrasound[Title/Abstract] AND ("deep learning"[Title/Abstract] OR "neural network"[Title/Abstract]) AND (simulation[Title/Abstract] OR prediction[Title/Abstract] OR propagation[Title/Abstract])

两组交集只有 PMID 37844771（已知P05），故19+29−1=47。Q2没有检出以“Transformer”而非“neural network/deep learning”措辞的tFUSFormer；作者后续追踪补到P54/P55。这是词项漏检的实际例子，不以PubMed查询代替全领域覆盖。

| 去重后的处理 | PMID（完整47条，按处理归组） | 去留依据 |
| --- | --- | --- |
| 学习求解/混合近邻重点复核，3条 | 38329866、37182263、37137219 | P50/P51/P52；保留全文缺口 |
| 已知场代理，4条 | 41474058、39437458、38536062、37844771 | P03/P25/P06/P05；已有方法，非新发现 |
| 传统传播/求解/导航，7条 | 42619907、41971001、41685921、41081483、40030863、39094682、23927357 | 学习环节不匹配；补P45正式版、P53/P57背景 |
| 逆向图像、物性、伪CT/影像任务，11条 | 42697166、41129992、39844940、39072036、37837171、37292518、36669697、35984788、32883668、39536407、40603533 | 输出声速/物性/图像/临床量，不把重建时间当复场求解时间 |
| 控制/规划/透镜/逆设计，6条 | 41337402、41192313、40782467、40117699、37849682、35700694 | 输出位姿、相位或设计/控制，不是全复场传统算子加速 |
| 标量或温度，2条 | 41637984、40939202 | 插入损失／温度，不是复场 |
| 神经生物学、血流、电磁等噪声，14条 | 40768797、37616337、35841853、32488831、28901969、28279642、21848678、20033235、9172630、7699100、2370449、40581220、38905990、27148032 | “neural”或“preconditioning”等词指生物作用；有的不是超声 |

重点EFetch：38329866、41129992、37182263、37844771、37137219、42697166、41971001、41685921、41081483、38536062。PMID42697166虽期刊卷期标2027年1月，API元数据显示2026-08-30已在线，纳入截至当日的公开范围；不拿未来卷期冒充未来才发表的研究。

## 引文追踪、版本归并与原文取得

| 种子和方向 | 实际到达的来源 | 新增事实／去重结果 |
| --- | --- | --- |
| P09 → 后续学习优化器比较 | P26全文；Xiang博士论文；Nguyen学位论文 | P26的4个CT复测不是P09原报告；P47/P09共享CT设置，非独立颅骨实证；P48性能弱 |
| P26参考文献及作者前序 | P47第5章、P49 RR-9593、P59 RT-0518；Inria年度报告 | 更早经颅神经预条件已出现；P49正文为通用二维；P59仅元数据核实 |
| McMg → Born/NPBS；LBS → 同作者后续 | P27 v2、P46 v4、P28正式版、P45正式版 | 通用三维多重网格先例不等于颅骨；NPBS减迭代不必然减少时间；变密度Born仍无学习 |
| NBSO/OpenWaves应用对象及现行状态 | P29历史v1及当前abs、P44当前v4/S9/S12 | P29已撤回并指向P44，按同一演进链处理；不将旧版成绩或两个编号计为独立实证 |
| Shin/Yoon SR论文 → 作者年度成果/代码 | P51 → P54作者接受稿/代码 → P55 arXiv与MICCAI → P58透镜优化 | 补到PubMed关键词漏掉的tFUSFormer及2026工作；查清pmax输出和粗仿真+SR计时 |
| 三维“transcranial+learning”交叉线 | P56 Caltech作者PDF | 近似伴随+图像恢复是PACT逆成像，非正向稳态复场 |

版本合并：

- P09：2020 arXiv 2010.15761、2021 JCP DOI 10.1016/j.jcp.2021.110430；本次读v2，不新增编号。
- P27：2606.30495 v1/v2以及题名Equation/Equations差异，同一工作；用v2。
- P28：2212.04948（2022）／JASA Express Letters（2023）DOI 10.1121/10.0017937，合并。
- P29/P44：2312.15575当前v2是2026-08-03的撤回公告，作者说明v1是未完成早稿、更新工作为2508.12226。P44当前为2026-08-06的v4。保留原P编号作为历史入口，合并演进链及证据计数；旧NBSO数值不作为现行结果。
- P46：2603.18527 v1题名 Born-Series-Inspired Residual Metric for Learning-based Preconditioners，v4题名 Neural Preconditioned Born Series: A Metric-Matched Framework for Learning-based Preconditioners；同一工作，用v4。
- P45：2507.16087（2025）／JASA正式2026 DOI 10.1121/10.0042259，原编号补正式版。
- P48：同题2022会议展示与大学硕士论文，统一为一项；详细事实来自学位论文。
- P54：大学归档元数据、IEEE作者接受稿、最终2024卷期和作者代码对应同一DOI，不重复计数；页码引用按本次取得的接受稿。
- P55：2608.01839v1／MICCAI2026 DT4H camera-ready同题，合并；未逐行审计两个版本全部差异，方法/拆分判断以v1为准。

| 全文/原文入口 | 本轮核查位置与取得方式 |
| --- | --- |
| [P09 arXiv v2](https://arxiv.org/html/2010.15761v2)、[UCL PDF](https://discovery.ucl.ac.uk/id/eprint/10129267/1/helmholtz.pdf) | 正文方法、泛化、误差；PDF24页保存并抽取 |
| [P26 arXiv v1](https://arxiv.org/html/2607.16906v1) | §2/3、§4.2.2表8、引文及硬件；HTML原文 |
| [P47作者论文](https://irma.math.unistra.fr/~xiang/research/XIANG_YANFEI_2022.pdf) | PDF144页，定向第5章；印刷页与PDF页差1 |
| [P48大学全文](https://www.fit.vut.cz/study/thesis-file/24521/24521.pdf) | PDF56页，§6/7/8；印刷页与PDF页差6 |
| [P49机构镜像](https://cerfacs.fr/wp-content/uploads/2026/01/RR-9593-1-1.pdf) | PDF23页，实际实验为二维；未见颅骨正文算例 |
| [P54 IEEE作者稿](https://ieeexplore.ieee.org/ielx7/6221020/6363502/10500878.pdf) | PDF12页；§IV-A、§V-C/D；表VIII/IX页9经Poppler渲染肉眼核对 |
| [P54作者数据代码](https://github.com/iangilan/tFUSFormer/blob/main/tFUS_dataset_creator.py)、[模型](https://github.com/iangilan/tFUSFormer/blob/main/models.py) | pmax_LR/HR路径及实值标签辅助确认输出；未运行代码 |
| [P55原文](https://arxiv.org/html/2608.01839v1)、[会议来源](https://papers.miccai.org/miccai-2026-sat/DT4H_010.html)、[作者仓库](https://github.com/CMME-Lab/tFUSOperator) | pmax定义、56³ ROI、8/2/3颅骨拆分及位置留出；归并版本 |
| [P56作者PDF](https://coilab.caltech.edu/documents/30905/Huang-2025-Photoacoustics.pdf) | §1/3直接确认输出为初始压力重建图像 |
| [P46原文](https://arxiv.org/html/2603.18527v4) | 表3、附录G/H/J；比较最强CBS而非只比较慢Krylov |
| [P28原文](https://arxiv.org/html/2212.04948v1)、[P29历史原文](https://arxiv.org/html/2312.15575v1)、[P27原文](https://arxiv.org/html/2606.30495v2) | 定向补查实验对象、维度、指标/耗时和迁移/微调区别；P29已另核撤回状态，旧版仅作历史信息 |

部分web PDF读取失败（长度/超时）、HAL访问检查、PubMed网站检查和大学旧PDF路径404均已记录为来源限制。公开作者/机构PDF通过原生下载取得后使用已有Python/pypdf抽取；未安装环境、未关闭TLS验证。P54的fitz不可用，改用已有Poppler渲染表页；不估读曲线精确数值。

## 未解决缺口及停止依据

| 缺口 | 目前证据 | 定向补齐事项 |
| --- | --- | --- |
| P51 Shin 2023全文 | 出版社/NCBI摘要；P54引言引用其先前工作，但不替代P51自身正文 | 查Re/Im或幅相、ROI/源/颅骨拆分、低分辨率求解是否计入时间 |
| P50 PEN-FWI全文 | NCBI摘要确认二维逆图像及学习前向模块 | 查FCNN输出对象及是否保留真实物理残差；分离重建与前向时间 |
| P52 PINN全文 | NCBI摘要 | 查逐题优化/权重共享、复场或时域输出及完整速度 |
| P59 RT-0518全文 | P26引文及Inria原始元数据，HAL入口访问检查 | 查是否有实际颅骨测试及维度/性能；当前不登记经颅直接先例 |
| 多篇求解的准备成本／复场误差缺项 | P26残差、P09初步速度、McMg/NPBS计时、NBSO表口径 | 不把缺项补成结论；若后续比较速度，单查准备/缓存、容差和独立复场误差 |

收束轮1（S44–S47）和收束轮2（S48–S51）连续未新增需进入直接威胁／待核实审查的经颅复场学习求解候选。新增搜索噪声是非声学、传统求解或控制任务，均按对象/输出排除。主要入口、危险候选和关键作者/引文链已经完成，故结束本轮；上述全文缺口保留，不假定已排除所有未知候选。

本轮统一索引新增P46–P59共14个研究条目（含2份学位论文、2份技术报告），登记总59项；P09/P26/P27/P29/P44/P45补新证据/版本。59是保留历史编号后的登记数，不是59份独立实证。精选方法参考只有3篇；撤回的NBSO移出精选，不把方法参考或新增数量写成经颅先例数量。

## 文档验收

最小验收检查：本目录三份文档与统一索引之间的新增链接；P编号唯一和版本归并；关键结论与上表原文对应；P26四例总时间、P54完整LR+SR计时及不同指标的边界；Git差异与明确路径暂存。旧材料既有失效链接不在本任务中修复。验证通过后本地提交本任务文件和索引增量，不push；原始要求保持未改写。
