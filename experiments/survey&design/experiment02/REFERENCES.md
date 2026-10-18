# experiment02：关键文献与证据入口

核查日期：2026-10-18—19。这里只保存来源、读取深度与判断定位；综合取舍见 [REPORT](REPORT.md)。P 编号沿用[统一索引](../../../docs/literature_seen_index.md)。

“已知”指索引已有；“本轮补录”只指索引此前未登记，属于已有方法家族延伸。预印本和正式版不重复计证据。本文没有把作者结果改写为项目实测，也没有操作 Zotero。

## 直接决定路线取舍的来源

<a id="r01"></a>
### R01 · P22 · 经颅求解器共同基准 · 已知

Aubry 等，*Benchmark problems for transcranial ultrasound simulation: Intercomparison of compressional wave models*，JASA 152, 1003–1019 (2022)，DOI 10.1121/10.0013426。[原文](https://arxiv.org/html/2202.04552)。

- 定向核查 §II、§III.1–III.11、§IV：时域、频域、角谱、边界元等均可进入单频经颅比较；共同比较网格和各求解器的实际计算网格分开。
- 本轮用途：建立分类与比较任务。它主要给声压幅值及焦域比较，不提供当前整个颅内复场形状合同下的速度排名。
- 特别定位：§III.6 JWAVE；§III.7 KWAVE；§III.8 MSOUND。不能把 0.5 mm 比较分辨率说成每个工具都在 0.5 mm 直接求解。

<a id="r02"></a>
### R02 · k-Wave 官方文档 · 工具证据

[kspaceFirstOrder3D](https://www.k-wave.org/documentation/kspaceFirstOrder3D.php)，Description、Source terms、Input options；与 R01 §III.7 互证。

核查：三维时域一阶系统、异质声速/密度、吸收、FFT 空间导数、PML 与多位置源输入。用途是说明完整时域传播流程；不从文档推测本项目耗时。时域求解无需保存所有时间步的完整体场，不能仅以“4D”推导其必然有四维存储负担。

<a id="r03"></a>
### R03 · P74 · 收敛 Born 的经典原始机制 · 本轮补录

Osnabrugge、Leedumrongwatthanakun、Vellekoop，*A convergent Born series for solving the inhomogeneous Helmholtz equation in arbitrarily large media*，JCP 322, 113–124 (2016)，DOI 10.1016/j.jcp.2016.06.034。[原文](https://arxiv.org/html/1601.05997)。

定向读 §2–4：带背景逆作用的收敛迭代、伪传播及介质反差相关的传播距离。用于区分只算一次散射的 Born 近似和持续迭代的 CBS；原文收敛条件不能自动传给替换过更新器的神经网络。

<a id="r04"></a>
### R04 · P45 · 三维变密度 Born · 已知，复用卡片

Stanziola、Arridge、Treeby、Cox，*Iterative Born solver for the Acoustic Helmholtz Equation with Heterogeneous Sound Speed and Density*，arXiv 2507.16087v1；正式版 JASA (2026)，DOI 10.1121/10.0042259。[原文](https://arxiv.org/html/2507.16087v1)、[作者代码](https://github.com/ucl-bug/born-density-matlab)、[旧事实卡片](../exploration00/McMg线/papers/born_density_2025.md)。

- 复用旧卡片的三维输入、四复场状态、源项、代码停止条件与每次调用重新准备的事实；本轮只回查 §2.2–2.3、§4，确认代价和反差瓶颈。
- 原文 §2、算法 1、附录 B：压力与三分量速度组成系统，使用可 FFT 应用的背景逆；§4：每次三维迭代 8 次三维 FFT，声速/密度反差增大会拖慢收敛。
- 原经颅证据与参数问题均保留在旧卡片，不在此复制。现有代码能接收新介质和新源，固定介质缓存复用仍需后续工程整理；论文没有当前 MIDA 配置的全流程秒数。

<a id="r05"></a>
### R05 · P75 · Born 的域分解扩展 · 本轮补录

Mache、Vellekoop，*Domain decomposition of the modified Born series approach for large-scale wave propagation simulations*，arXiv 2410.02395v3 (2025-10-16)；后续 JCP 期刊入口与此为同一工作。[v3 正文](https://arxiv.org/html/2410.02395v3)、[作者软件文档](https://wavesim.readthedocs.io/en/latest/readme.html)。

- §3.1 式 9、§4.2：拆域使缩放更保守，第一次拆分可能增加迭代；并非免费把全局 FFT 拆小。
- §3.3、§4.3 表 2：约 21.6 亿体素，2×A40 48 GB，2730 s、4697 次迭代；停止量是经预条件的相对残差 10⁻⁶。物理算例为光学标量介质，平面源、两横向周期边界。
- 2024 v1 摘要的 379 s 不是 v3 此大算例的 2730 s；不混版本。其约 20 倍对照是 CPU 单域与 GPU 拆域，不能当同 GPU 算法加速比。
- 文档明确 `HelmholtzDomain/MultiDomain` 的介质构造和 `run_algorithm(domain, source, ...)` 分离；这支持介质对象复用的工程方向。软件不是神经网络，也不是现成变密度经颅适配器。

<a id="r06"></a>
### R06 · P57 · mSOUND 异质颅骨验证 · 已知，本轮由摘要升级为全文

Bell、Xu、Chen、Jing，*Numerical Validation of mSOUND Using Fully Heterogeneous Skull Models*，IEEE OJUFFC 6, 80–89 (2026)，DOI 10.1109/OJUFFC.2026.3677158。[作者稿全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC13064427/)、[同稿全文 XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13064427/fullTextXML)。

本轮经 Europe PMC 读取全文正文、表 1，弥补原记录的摘要限制。关键定位：

- §II、图 1：ESSF 单向传播、两个参考声速插值、近法向透射近似及有限阶反射。
- §III：2 名受试者的 4 个颅骨片段；500 kHz；曲面源由 FOCUS 转成入射平面；mSOUND/FOCUS 总域与 k-Wave 域不同。硬件为 EPYC 7702P、约 1 TB RAM，使用 C++ CPU k-Wave。
- §III 计时段、§IV、表 1：不含通用前后处理，FOCUS 另列。0.5 mm 时分别为 FOCUS 287.77 s、mSOUND 36.45 s、k-Wave 3646.48 s；相加后约 11.25 倍。0.25 mm 时联合计时为 651.38 s。
- §IV–V：主要误差图和 L2/焦域指标基于压力幅值；尚缺本任务完整 Re/Im 形状指标。平面输入约束和反射模型影响围绕整个头颅的任意点源配置。

<a id="r07"></a>
### R07 · P76 · Vanka 改进多重网格 · 本轮补录

Yovel、He、Treister，*Vanka-smoothed shifted Laplacian multigrid preconditioners for the Helmholtz equations*，arXiv 2511.16808v2。[正文](https://arxiv.org/html/2511.16808v2)、[作者实现](https://github.com/RacheliYovel/VankaHelmholtz)。

§3–4：用小块联立平滑降低所需复移位；§5：Julia，双核笔记本、32 GB RAM，相对残差 <10⁻⁶，10 点/波长。§5.5 表 6：Overthrust 三维例同时给三/四/五层循环的次数与时间。较深循环的改善很明显，但最快三层循环中改善小；不能只挑最差 Jacobi 版本宣称新方法普遍大幅领先。作为更新传统强对照的依据，非项目实测。

<a id="r08"></a>
### R08 · P77 · RS-CGC 粗网格色散修正 · 本轮补录

Yovel、Treister，*Scalable Multigrid Solver for the Helmholtz Equation: Real-Shifted Coarse Grid Correction*，arXiv 2604.19501v1 (2026-04-21)。[正文](https://arxiv.org/html/2604.19501v1)。

- §3、§4 表 1–2：高阶离散/网格转移与最粗 Galerkin 算子的实移位配合，减小粗细网格传播相位失配；存在临界规模限制。
- §5：Julia，双核笔记本、32 GB RAM，20 层吸收边界，残差 <10⁻⁶。§5.2 表 5：最大约 272 万自由度的三维 Overthrust，10 次迭代、67.25 s。该时间属于论文求解计时，不填作包含介质装配和输入输出的总时间。
- §3 第二项说明：三层最粗问题需要可负担地求解。§6：一般结论偏向 11–12 点/波长，10 点有组合策略；未给当前 6 点/波长的保证。不能靠扩大网格改变本任务配置来继承论文性能。
- 此次正文未定位到独立作者代码地址，不把另一篇 Vanka 仓库当本篇实现。

<a id="r09"></a>
### R09 · P78 · matrix-free 三维经典实现 · 本轮补录

Chen、Dwarka、Vuik，*A matrix-free parallel solution method for the three-dimensional heterogeneous Helmholtz equation*，ETNA 59, 270–294 (2023)，DOI 10.1553/etna_vol59s270。[正文](https://arxiv.org/html/2308.06085v1)。

§3–4：CSLP、三维几何多重网格、并行粗 GMRES 与 matrix-free 运算；§5 给 GMRES、BiCGSTAB 和 IDR(4) 的不同停止量。§5.3.3 表 6：641×641×193，约 7930 万未知量，CSLP-IDR(4)，1/6 个 DelftBlue CPU 节点为 897.25/203.31 s，原残差 10⁻⁶；每节点 48 核、192 GB RAM。用途是确认“大三维可运行”的传统基底；不是 GPU 秒级证据。

<a id="r10"></a>
### R10 · P79 · OSM 与 ORAS 完整成本对照 · 本轮补录

Martin、Jolivet、Geuzaine，*Comparison of substructured non-overlapping domain decomposition and overlapping additive Schwarz methods for large-scale Helmholtz problems with multiple sources*，arXiv 2506.16875v1 (2025)。[元数据](https://arxiv.org/abs/2506.16875)、[正文](https://arxiv.org/html/2506.16875v1)。

- §3.1–3.4：ORAS 对全体场用预条件 GMRES；OSM 在界面变量上用 GMRES，每次算子作用本身包含局部解。后者省向量与正交化内存，但粗糙的局部近似会改变它实际求解的算子。
- §4–5、表 1–5：高阶 FEM、常密度地质三维例；CPU LUMI，每节点 128 核/256 GB；大规模测试 complex64、restart 50、各自残差 10⁻⁴，64 个独立 RHS。约 6.3 亿自由度可计算，但这种批量吞吐条件不同于本轮单总场。
- §5.2 “Comparison with a direct solver”：1100 万自由度的 MUMPS-BLR 分解 74 s、64 RHS 解 6 s；作者提出的摊销依赖独立 RHS 次数。
- HTML 顶端混入模板作者，作者据 arXiv 元数据核对为以上三人；图 10 标题的两种时间次序与表 4/5 不一致，本轮数字采用表格，不据标题引用。

<a id="r11"></a>
### R11 · P80/P81 · 扫描与 polarized traces · 本轮补录

- **P80** Taus、Zepeda-Núñez、Hewett、Demanet，*L-Sweeps: A scalable, parallel preconditioner for the high-frequency Helmholtz equation*，JCP (2020)，arXiv 1909.01467。[正文](https://arxiv.org/html/1909.01467)、[作者公开的 2D 实现](https://github.com/L-Sweeps/L-Sweeps-2D)。读 §3–5：棋盘式扫描、原系统 GMRES、局部分解缓存；§4 给反射的影响；§5.5 表 10 给三维计时。不能把公开 2D 仓库说成现成 3D 包。
- **P81** Zepeda-Núñez、Scheuer、Hewett、Demanet，*The method of polarized traces for the 3D Helmholtz equation*，arXiv 1801.08655。[正文](https://arxiv.org/html/1801.08655)。读 §1.1 表 1、§2–4：分离介质离线准备和在线解，批 RHS 流水线的收益依赖源数与计算节点条件。
- 与已知 **P66** [共同机制综述](https://epubs.siam.org/doi/10.1137/16M109781X)合读：扫描、source transfer、polarized traces 是相关的块消元/优化 Schwarz 思想，不能算三个相互独立的创新家族。

<a id="r12"></a>
### R12 · P82/P83 · WaveHoltz 桥接路线 · 本轮补录

- **P82** Appelö、Garcia、Runborg，*WaveHoltz: Iterative Solution of the Helmholtz Equation via the Wave Equation*，SISC (2020)，arXiv 1910.10148。[正文](https://arxiv.org/html/1910.10148)。定向读 §2、§2.5、§4.3：对短时受迫传播做周期滤波，求稳态固定点；原文已有阻抗边界和三维算例。其对称/正定性质须对应文中边界及离散条件，不能转给所有有耗散 PML 系统。
- **P83** Appelö 等，*A Multi-Frequency Helmholtz Solver Based on the WaveHoltz Algorithm*，arXiv 2507.23613v1 (2025)。[正文](https://arxiv.org/html/2507.23613v1)。§1、§3–4：同时提取不同频率，可用 GMRES；本篇数值范围为简单闭域、能量守恒的 Dirichlet/Neumann 问题。这个限制属于此扩展，不倒推整个 WaveHoltz 家族不能做开域。

## 网络接入位置与反证

<a id="r13"></a>
### R13 · P27 · McMg · 已知，复用与定向补证

Jia 等，arXiv 2606.30495v2。[正文](https://arxiv.org/html/2606.30495v2)、[旧卡片](../exploration00/McMg线/papers/README.md)。

复用旧卡片的方程对象、三维表 2 和迁移条件。本轮补核 §3.1–3.3 的 setup/solve 分离、随机残差训练，§3.5/§4.3 的 LLPF 与固定权重迁移区别，附录 A.5 表 8 的逐步开销。它给出真实三维学习预条件速度证据，但三维是地质声速场；当前经颅密度/吸收/边界与换患者准备时间须另测。附录 A.3 也说明其 SL 基线的具体平滑/粗解配置，不能由表 2 排除整个先进多重网格家族。

<a id="r14"></a>
### R14 · P61 · encoder–solver 与 mini-retrain · 已知，本轮补摊销条件

Azulay、Treister，*Multigrid-augmented deep learning preconditioners for the Helmholtz equation*，SISC (2022)，arXiv 2203.11025。[正文](https://arxiv.org/html/2203.11025v1)、[旧笔记](<../exploration 01/papers/README.md>)。

§3：CNN 与 SL 校正、FGMRES、介质编码和残差求解分离；§4.3.3、§4.4：特定介质的 30 epoch mini-retraining 有额外成本，地质例按作者估算约需 270 个独立 RHS 才摊回。这是二维特定计数模型，不是患者所需配置次数的预测；同一次含几千点源的总场只算 1 个 RHS。

<a id="r15"></a>
### R15 · P46 · NPBS · 已知，保留负向时间证据

Wang、Jia、Liu，arXiv 2603.18527v4。[正文](https://arxiv.org/html/2603.18527v4)。读 §3、§5.1.3 表 3、附录 G–J。Born 坐标中的残差训练；256²、H100、FP64 推理、10⁻⁶。表 3 的 NPBS 123 步/0.107 s，比 CBS 1124 步/0.086 s 更慢；FGMRES+NPBS 为 37 步/0.078 s。该结果只用于说明收益须按全流程判断，不外推三维颅骨速度。

<a id="r16"></a>
### R16 · P63 · 学习粗解的结构与容量 · 已知

*When can a neural operator replace a coarse solve? Architectural principles for two-level preconditioning*，arXiv 2605.19867v1。[正文](https://arxiv.org/html/2605.19867v1)、[旧笔记](<../exploration 01/papers/README.md>)。§2–3：粗基与残差投影、源线性；§4.3、§5：高波数时有限维固定基和学习粗逆分别形成障碍。用来要求学习粗空间方案明确表示能力与训练输入覆盖，不把二维观察升级成三维波动求解定理。

<a id="r17"></a>
### R17 · P34 · Wave-ADR-NS · 已知，本轮补多源限制

Cui、Jiang、Shu，arXiv 2404.02493v2。[正文](https://arxiv.org/html/2404.02493v2)。§3.2：FNO 从慢度和点源预测分离走时，随后 ADR 校正；§4.3 表 2–4：二维、高波数、FGMRES(20)、原残差 10⁻⁶及域外迁移。相位函数与点源相关，因此不能把某一源的走时准备当任意多源配置共享的介质缓存；本文不是单一源无关粗逆的现成替代品。

<a id="r18"></a>
### R18 · P62/P68 · 学习界面与边界校正 · 已知

- **P62 MLORAS**，*Learning Interface Conditions in Domain Decomposition Solvers*，NeurIPS (2022)。[正文](https://papers.nips.cc/paper_files/paper/2022/file/2f8928efe957139e9c0efc98f173f4be-Paper-Conference.pdf)、[现存事实卡片](<../exploration 01/papers/README.md>)。复用卡片：学习 Robin 附加矩阵；§2 式 1 为正定的 η−Δ、η>0，不能当作高频不定经颅加速实验。
- **P68**，*Large scale scattering using fast solvers based on neural operators*，arXiv 2405.12380v1。[正文](https://arxiv.org/html/2405.12380v1)。复用卡片并补读 §3–4、附录 C：体强迫/入射边界网络与迭代结合、含三维障碍散射；改变障碍可不重训，但偏离训练分布较远会退化甚至失效。不能把障碍泛化改写成跨患者异质颅骨泛化。

<a id="r19"></a>
### R19 · P08 · 真三维直接算子，作为认真筛选的对照 · 已知

Zou 等，*Deep Neural Helmholtz Operators for 3D Elastic Wave Propagation and Inversion*，GJI (2024)，arXiv 2311.09608。[所读版本](https://arxiv.org/html/2311.09608)。§3–4.2：64³ 三维复位移、随机介质与源，全部目标频率约 0.3 s/单 GPU，推理显存 20 GB；训练有大量 SEM 标签。该版频域测试 loss 约 0.176/0.238，采用 L1/L2 混合度量。它是快直接算子的真实先例；波长尺度、物理对象、规模及误差合同不符合当前直接入选条件。0.4 s/350 倍是 §4.3 反演步计时，不用作纯前向时间。

## 补充筛选与未补齐来源

<a id="r20"></a>
### R20 · P84 · FFT 插值伪微分预条件 · 本轮补录，降级

Acosta、Khajah、Palacios，*A new interpolated pseudodifferential preconditioner for the Helmholtz equation in heterogeneous media*，SISC 47(2), A1017–A1039 (2025)，DOI 10.1137/24M1642184。[v2 正文](https://arxiv.org/html/2409.16172v2)。§4 以声速插值逆符号、用少数 FFT 实现；§5.2 是二维合成头模；§6 明述尖锐声速变化使效果变差、PML 仍待扩展。保留为低 setup 代价的非学习比较线索，未进入本轮三大强基底。

<a id="r21"></a>
### R21 · P85 · GPU 压缩直接解 · 本轮补录，读取摘要/实现定位

Claus、Ghysels、Boukaram、Li，*A graphics processing unit accelerated sparse direct solver and preconditioner with block low rank compression*，IJHPCA 39(1), 18–31 (2025)，DOI 10.1177/10943420241288567。[出版社](https://journals.sagepub.com/doi/10.1177/10943420241288567)、[作者稿](https://escholarship.org/content/qt7tn9n67r/qt7tn9n67r.pdf)。

本轮只核摘要及 STRUMPACK 角色，不据未读的数值表给速度或内存承诺。作用是避免将“直接法太大”绝对化；定量摊销采用已读 R10 的 MUMPS-BLR 小算例。压缩后的分解有近似误差，必要时配迭代校正，不等于零误差的精确逆。

<a id="r22"></a>
### R22 · P86 · Hk-GenEO 粗空间 · 本轮补录，机制定位

Dolean、Fry、Graham、Langer，*Schwarz preconditioner with Hk-GenEO coarse space for the indefinite Helmholtz problem*，arXiv 2406.06283v1。[正文](https://arxiv.org/html/2406.06283v1)、[FreeFEM 官方示例](https://doc.freefem.org/documentation/ffddm/examples.html)。本轮读问题、粗空间和理论部分；所读v1正文没有独立数值实验章节或表格，不填写三维经颅性能。实际粗空间数值竞争补读R30，二者不混称。用途是确认谱粗空间不是只为SPD扩散设计，提醒学习粗基须与传统谱构造竞争。

<a id="r23"></a>
### R23 · P53 · VBS · 已知，全文缺口保留

Sun、Li、Su、Lin，*A viscoacoustic wave equation solver using modified Born series*，JASA 158(4), 2830–2848 (2025)，DOI 10.1121/10.0039529。[PubMed 原始摘要](https://pubmed.ncbi.nlm.nih.gov/41081483/)、[作者机构记录](https://people.ucas.edu.cn/~yubing.li)。

本轮定向查出版社、作者与公开稿入口，仍未取得全文；摘要支持“含变声速、密度、衰减及多尺度策略的二维/三维传统 Born 家族”这一定位。未知完整停止条件、当前尺度成本和可复现实现，暂不据摘要断言优于 R04。补到全文可能改变 Born 内部实现的优先顺序。

## 已知但不重复深入的证据

- P09/P26/P47 的二维经颅学习求解先例：见[统一索引](../../../docs/literature_seen_index.md)和[旧查重报告](../exploration00/idea查重/REPORT.md)。本轮保留其先例身份，不把它们登记为新发现。
- P28/P44 的 Born 式学习更新、P43 HINTS：见[现存卡片](../exploration00/physical_iteration/papers/README.md)。P29 已撤回并指向 P44，按演进链处理。
- P51/P54/P55 的超分辨率/局部峰压输出：按已有原文核查筛出本任务核心比较；输出差异比网络名称更重要。

本轮未读取与比较无关的历史项目协议、未把论文版本的新公开时间当新算法，也未为了凑文献数给每条搜索命中分配编号。

## 深入补查：强基底、反例与实现

<a id="r24"></a>
### R24 · P87–P91 · 优化粗网格、多层 deflation 与 butterfly 分解

这组是首轮遗漏后补读的既有强方法。本次已读对应算法、数值和成本段；它们改变了报告的比较对象。以下表中的时间均为作者条件，不能外推为 MIDA 时间。

| 编号与来源 | 原文定位及关键事实 | 本轮用途与边界 |
| --- | --- | --- |
| **P87** Stolk、Ahmed、Bhowmik，SISC36(6), A2819–A2841 (2014)，arXiv1304.4103。[正文](https://arxiv.org/html/1304.4103) | §2、§5.2/表11–12：粗细相速匹配；三维常系数在粗层≥3.5点时表现良好；直接粗化 PML 失败后保留法向分辨率 | 低点/波长的主要障碍是具体粗算子和边界处理，不能按家族一概降级。该表不是复杂三维颅骨测试 |
| **P88** Stolk，*A dispersion minimizing scheme for the 3-D Helmholtz equation based on ray theory*，JCP314,618–646 (2016)，DOI10.1016/j.jcp.2016.03.023，arXiv1504.01609v2。[正文](https://arxiv.org/html/1504.01609) | §6–8/表5–6：IOFD 细层6点、粗层3点；三维盐丘两网格+双向扫描，约5千万未知量、128核、4右端总179 s（45 s/右端），13步；平滑例的离散精度与跳变反射分开 | 原文明确强梯度需要更细的介质/源离散。可保留优化粗层机制；不能直接替换本项目细算子，或把批处理吞吐写成单配置延迟 |
| **P89** Dwarka、Vuik，JCP469,111327 (2022)，DOI10.1016/j.jcp.2022.111327。[公开全文](https://repository.tudelft.nl/file/File_ac31135c-762a-47a3-ab8c-5d774fbeb62d) | §3/算法、§5/表6–8；PDF印刷p17–21：递归高阶基、CSLP内用BiCGSTAB，定层内迭代上限。顺序MATLAB/i7-8665U/8GB；三维sine约177万未知量，V/W为49/28步、1259.18/1359.92 s。计时含粗矩阵构造 | 有真实三维证据，但外迭代下降未必省时；不把35点/波长的波数独立性套到6点。本次已视觉核表7 |
| **P90** Chen、Dwarka、Vuik，JSC102,47 (2025)，DOI10.1007/s10915-024-02786-w。[正文](https://arxiv.org/html/2412.04980v1)；[作者DD29报告，2025-06-24](https://diamhomes.ewi.tudelft.nl/~kvuik/talks/DD29_MS07-JinqiangChen_An_Efficient_Parallel_Multilevel_Deflation_Method_for_Large_Scale_Helmholtz_Problems.pdf) | 论文§3–5/表9–13：matrix-free递归FGMRES、细两层用MG-CSLP、粗层Krylov；最终L2容差0.3，其他粗层一次。论文算例为二维。**作者后续报告**第15–18张另有三维：约6.3亿未知量及更大地质模型，并改变粗校正权重γ；不能将其称作论文表 | 补查到三维实现后，不再用“新版只有二维”排除其大三维竞争资格。后续报告未公开完整计时合同/可核源码，不借其秒数做跨论文排名 |
| **P91** Liu等，SISC43(5),S367–S391 (2021)，DOI10.1137/20M1349667。[正文](https://arxiv.org/html/2007.00202) | §5–6/表2–3：HOD-BF压缩多前沿因子+GMRES(30)，FP64，预条件残差停止。32×32核Cori。250³例：分解433 s、在线3.5 s、因子730 GB；21.18M异质例：ε=1e-4为1049/11.0 s、800 GB，ε=1e-6为1657/4.1 s、870 GB | O(N)因子存储仍有很大常数，且表给因子存储而非峰值。强压缩基底必须保留，但与单GPU快速换介质有实际资源差距；容差摊销在报告定量计算 |

P90后续报告三维常系数513³例，CSLP与三层deflation分别343/12个外迭代，但时间62716/24681 s；129³小例则76/225 s。它支持“越大越值得额外粗层工作”的条件判断。第17张SEG/EAGE表已视觉核验。未知硬件/停止范围不由前一篇论文代填。

<a id="r25"></a>
### R25 · P92 · 两网格扫描的完整准备—在线分离

Stolk，*An improved sweeping domain decomposition preconditioner for the Helmholtz equation*，arXiv1412.0464（早期题名为two-grid accelerated sweeping）。[正文](https://arxiv.org/html/1412.0464)。§4–6/表8/附录A：优化粗算子、Jacobi、粗层PML子域MUMPS分解及UD/X扫描。约13M三维盐丘，32核、单右端X-sweep：setup49 s，solve22 s，11步；约50M的31 s/右端来自4右端。准备未计入在线表列。薄PML和并行partial sweep均有迭代恶化反例。与P88是一条方法演进链，不计为独立成功验证。

<a id="r26"></a>
### R26 · P93 · GPU局部WaveHoltz

Rotem，*Efficient Domain Decomposition for the Helmholtz Equation on GPUs*，arXiv2606.21695v1。[正文](https://arxiv.org/html/2606.21695)。§III、V–VII/表I：谱元、零阶传输、子域驻留单thread block、局部WaveHoltz；A100，局部单精度/双精度相对残差1e-6/1e-12。三维对MINRES加速范围0.71–8.48倍；“25倍”来自二维。作者将优化传输及粗空间列作后续工作。本次核正文和benchmark，不把局部核速度当整个复杂介质求解速度；未定位带论文身份的公开完整实现。

<a id="r27"></a>
### R27 · P94–P95 · 快速传播的强例与公开版本边界

- **P94** Almquist、Parker、Christensen，*Rapid full-wave phase aberration correction method for transcranial high-intensity focused ultrasound therapies*，J Therapeutic Ultrasound4:30 (2016)，DOI10.1186/s40349-016-0074-7。[原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC5143441/)、[同一原文JATS](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5143441/fullTextXML)。Methods及Computation time：GPU HAS支持阻抗反射，本文未启用散射；421×648×170颅骨、256阵元逐阵元压力模式和校正约15min。该数字是场库/校正批任务，不是本轮一次总场，也不除256造单次延迟。没有把HAS等同于射线。
- **P95** Gu、Jing，*mSOUND: An Open Source Toolbox for Modeling Acoustic Wave Propagation in Heterogeneous Media*，TUFFC68(5),1476–1486 (2021)，DOI10.1109/TUFFC.2021.3051729。[原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC8101065/)、[作者发布入口](https://github.com/m-SOUND/mSOUND)。实际读取公开zip中的`Forward3D_fund`和三维多源例。公开v01为混合域Simpson积分；**不等同**P57/2026的ESSF新版。P57正文§II和Methods注明新算法不同于原版、反射阶数设4；未找到该测试版本独立公开源码链接。

P57全文通过[EuropePMC JATS](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13064427/fullTextXML)读取，§IV的0.5mm时间应为FOCUS287.77+mSOUND36.45=324.22 s；k-Wave C++ CPU3646.48 s。不能省掉输入平面构造，也不能把CPU倍数当GPU倍数。

<a id="r28"></a>
### R28 · P96 · compact implicit encoder–solver

Lerer、Ben-Yair、Treister，*Multigrid-Augmented Deep Learning Preconditioners for the Helmholtz Equation Using Compact Implicit Layers*，SISC46(5),S123–S144 (2024)，DOI10.1137/23M1583302，arXiv2306.17486。[正文](https://arxiv.org/html/2306.17486)、[作者代码](https://github.com/BGUCompSci/CompactImplicitHelmholtz)。这是P61的方向延伸，本次新增粗层隐式逆、实际缓存和OOD证据。§4.1–4.2、§5.1–5.3/表1、4、5：网络校正后再V-cycle、FGMRES(10)，二维；4096²编码0.052 s、每FGMRES步0.114 s，不能把每步时间当求解时间。固定权重OOD和300对/30epoch适配两组分开；只在128²训练的网络放大到4096²可能失败。代码实现核查见C06。

<a id="r29"></a>
### R29 · P97 · GPU高阶时域有限元

Mohd Adeeb Bin Mohd Arif Kor，*Fast finite element methods for focused ultrasound applications*，Cambridge博士论文 (2024)，DOI10.17863/CAM.116100。[学校记录与全文](https://www.repository.cam.ac.uk/items/22a5121c-ea96-4920-9639-26238644adc7)、[作者GPU实现](https://github.com/adeebkor/fenicsx-fus-gpu)。第7章§7.2–7.6：高阶质量集块、sum-factorisation、显式RK4、多GPU直接通信；§7.6.1平面源benchmark单RTX A4000双精度约6min，含最后一周期二维切片输出。此项是强时域实现能力证据，未把它写成完整异质头颅体复场耗时。源码确认GPU时间推进和介质算子预计算；只读未运行。

<a id="r30"></a>
### R30 · P98 · 两层ORAS的实际粗空间竞争

Bootland、Dolean、Jolivet、Tournier，*A comparison of coarse spaces for Helmholtz problems in the high frequency regime*，Computers & Mathematics with Applications98,239–253 (2021)，arXiv2012.02678v3。[正文](https://arxiv.org/html/2012.02678)。§4–6/表17–19：网格、DtN、H-GenEO各有条件；3D Overthrust11.33M，网格粗层23–24外步中仍含7–13内步；DtN减至6外步时每子域160基向量，最大粗空间因资源代价缺项。文末明确未充分比较优化计时；不是速度排行榜。P86的Hk-GenEO理论并不自动提供此表的成本结论，v1也无可抽取数值表。

<a id="code-audit"></a>
## 作者实现只读核查（2026-10-18—19）

固定提交用于定位事实，不表示重现了论文数值；下载的公开代码和PDF留在D盘研究缓存，未安装、执行求解或上传原文。C01–C08均已读取列出的关键函数；未定位源码的工作如实列明，未拿自写重建代替作者实现。

| 编号 | 固定版本与可核位置 | 实际核到的比较事实 |
| --- | --- | --- |
| C01 Born-density | [`2b59c72`主函数L145–152、376–485、488–529](https://github.com/ucl-bug/born-density-matlab/blob/2b59c72acf8637a8f314157a28d00380e19b0084/src/acousticHelmholtzSolver.m#L376)；同目录`singleIteration`/`residualMagnitude` | 介质准备在单调用内；循环计时之后仍分配输出/重标度/gather；每次检查真实残差额外调用算子；相对残差以第一次更新后的值归一化。3D更新与一次残差计算各8次FFT |
| C02 WaveSim | [`5949196` iteration.py L7–90、93–132](https://github.com/IvoVellekoop/wavesim_py/blob/594919609784c99c0a003cada6173e282dd378f9/src/wavesim/iteration.py#L61)；`helmholtzdomain.py`L46–88、103–176 | 当前分离domain和source；复用介质/传播核。停止比较的是预条件残差范数平方；不能直接把threshold1e-6称为真实残差1e-6。当前NumPy/CuPy代码与P75论文时代实现有演进，2730s论文数字不由最新代码再次验证 |
| C03 STRUMPACK | [`819ff1b` testHelmholtz.cpp L128–171](https://github.com/pghysels/STRUMPACK/blob/819ff1beaef0379e575fd77baaed8393948ca6d9/examples/sparse/testHelmholtz.cpp#L128)；[`HOD_Preconditioning.txt`L11–65](https://github.com/pghysels/STRUMPACK/blob/819ff1beaef0379e575fd77baaed8393948ca6d9/doc/doxygen/pages/HOD_Preconditioning.txt#L11) | `set_matrix→reorder→factor→solve`可复用因子；HODBF要HODLR格式加butterfly层参数，不是普通BLR开关。P85 GPU-BLR性能不可拼接到P91 CPU-HODBF，示例默认制造解也非颅骨应用 |
| C04 Vanka | [`0e28ebb` SolverFunctions.jl L118–169](https://github.com/RacheliYovel/VankaHelmholtz/blob/0e28ebbab7128450d84e189ad74463acf3a7e168/Numerical%20-%20Julia/src/SolverFunctions.jl#L118) | 细真矩阵与移位预条件矩阵分开；显式`R/P/Ac/LUcoarsest`及Vanka块准备。此Julia研究代码不是matrix-free GPU大域实现，最细3层Jacobi也是必须比较的强同文对照 |
| C05 mSOUND | [`9bfb65d`发布zip](https://github.com/m-SOUND/mSOUND/blob/9bfb65d3546807e7419b4a3794fcdc75c4fc26c0/download/mSOUND%20v01.zip)，内`Forward3D_fund.m`和`Example_FSMDM_3D_multi_sources.m` | 输入是一个复激励平面，多孔径先在该平面相加；函数内构造介质项，再逐层FFT。`tic/toc`主要包循环，前处理/反射另段不可漏计。该zip不是P57的新版ESSF |
| C06 implicit encoder–solver | [`27efa77` implicit_unet.py L114–123、220–263](https://github.com/BGUCompSci/CompactImplicitHelmholtz/blob/27efa77ab0ffb5fd95d9e309a5c75dbfc4b6d267/unet/implicit_unet.py#L114)；[`helmholtz.py`末尾`nn_precond`](https://github.com/BGUCompSci/CompactImplicitHelmholtz/blob/27efa77ab0ffb5fd95d9e309a5c75dbfc4b6d267/helmholtz.py)；`evaluate.py`L27–41、86–100 | 公布包装器每次forward调用encoder；可直接调用独立encoder/solver以实现论文缓存，但默认评估包装没有显式跨迭代缓存。隐式Green缓存依赖权重/尺寸，和介质编码缓存不同。计时脚本有CUDA同步且含3步V-cycle初值 |
| C07 Wave-ADR | [`07b3aff` diff_rhs.py L34–92](https://github.com/cuichen1996/Wave-ADR-NS/blob/07b3affc1149abcd2ebe3d7b32d76569eaacaf51/diff_rhs.py#L34)；`model/model.py`中`setup`/`test` | `setup`使用参考源坐标；但作者也以同一参考相位图解随机体右端。故不能断言多源必需逐源建图；准确判断是缓存含参考源选择，任意右端的收敛/成本要另分情况。`test`在线计时不包setup |
| C08 FreeFEM / 时域代码 | [`418220d`三维ORAS示例L79–101](https://github.com/FreeFem/FreeFem-sources/blob/418220d29d26f6f83a3ad856e69c255058c94c44/examples/ffddm/Helmholtz-3d-simple.edp#L79)；[`c7f67f1`FUS GPU](https://github.com/adeebkor/fenicsx-fus-gpu/tree/c7f67f19fc27808fe6c5a027cddefe87980f96d0)；[`44ca4ed`k-Wave衍生CUDA](https://github.com/klepo/k-Wave-Fluid-CUDA/blob/44ca4ed1fce2319c1558ec5ba3a165d3d44a5da1/KSpaceSolver/KSpaceFirstOrderSolver.cpp#L275) | ORAS局部准备后再建粗网格；FUS GPU为作者原型、RK4和预计算真实存在；k-Wave衍生CUDA区分load/preprocess/simulation/postprocess，并支持压缩输出。它不是ucl官方最新CUDA源码，不将二者混称 |

定向核论文链接、作者题名/主页后，仍未定位P27 McMg、P46 NPBS、P89/P90、Stolk完整三维实验的可核作者源码；这限制“现成复现容易”的工程评级，**不降低已核原文的数值能力评级**。L-Sweeps公开库`4166377`也已读取GMRES与局部分解入口，但库明确只有二维，未据此声称已检查三维作者实现。
