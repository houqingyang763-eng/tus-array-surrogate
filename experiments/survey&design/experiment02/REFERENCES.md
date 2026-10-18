# experiment02：关键文献与证据入口

核查日期：2026-10-18。这里只保存来源、读取深度与判断定位；综合取舍见 [REPORT](REPORT.md)。P 编号沿用[统一索引](../../../docs/literature_seen_index.md)。

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

Dolean、Fry、Graham、Langer，*Schwarz preconditioner with Hk-GenEO coarse space for the indefinite Helmholtz problem*，arXiv 2406.06283v1。[正文](https://arxiv.org/html/2406.06283v1)、[FreeFEM 官方示例](https://doc.freefem.org/documentation/ffddm/examples.html)。本轮读问题、粗空间和理论部分，数值未逐表抽取；不为其填写三维经颅性能。用途是确认谱粗空间不是只为 SPD 扩散设计，提醒学习粗基须与传统谱构造竞争。

<a id="r23"></a>
### R23 · P53 · VBS · 已知，全文缺口保留

Sun、Li、Su、Lin，*A viscoacoustic wave equation solver using modified Born series*，JASA 158(4), 2830–2848 (2025)，DOI 10.1121/10.0039529。[PubMed 原始摘要](https://pubmed.ncbi.nlm.nih.gov/41081483/)、[作者机构记录](https://people.ucas.edu.cn/~yubing.li)。

本轮定向查出版社、作者与公开稿入口，仍未取得全文；摘要支持“含变声速、密度、衰减及多尺度策略的二维/三维传统 Born 家族”这一定位。未知完整停止条件、当前尺度成本和可复现实现，暂不据摘要断言优于 R04。补到全文可能改变 Born 内部实现的优先顺序。

## 已知但不重复深入的证据

- P09/P26/P47 的二维经颅学习求解先例：见[统一索引](../../../docs/literature_seen_index.md)和[旧查重报告](../exploration00/idea查重/REPORT.md)。本轮保留其先例身份，不把它们登记为新发现。
- P28/P44 的 Born 式学习更新、P43 HINTS：见[现存卡片](../exploration00/physical_iteration/papers/README.md)。P29 已撤回并指向 P44，按演进链处理。
- P51/P54/P55 的超分辨率/局部峰压输出：按已有原文核查筛出本任务核心比较；输出差异比网络名称更重要。

本轮未读取与比较无关的历史项目协议、未把论文版本的新公开时间当新算法，也未为了凑文献数给每条搜索命中分配编号。

## 用户质疑后的漏项补查：入口已确认，深入比较未完成

<a id="r24"></a>
### R24 · P87–P91 · 会改变判断的强竞争方法

以下为首轮真实漏项或未深入的关键后续工作。已先查统一索引，不宣称新方法发现；本次用于确认遗漏和纠正推理，尚未完成各自全部数值、实现和成本比较。不能把这5个入口计成5篇深入读完。

| 编号与来源 | 本次核到哪里 | 为什么影响首轮取舍 | 尚需补什么 |
| --- | --- | --- | --- |
| **P87** Stolk、Ahmed、Bhowmik，*A multigrid method for the Helmholtz equation with optimized coarse grid corrections*，SISC36(6), A2819–A2841 (2014)，arXiv1304.4103。[正文](https://arxiv.org/html/1304.4103) | 引言、三维/边界处理与结论：对齐粗细相速，三维优化粗算子；粗层约3.5点的条件与细层分辨率不同；PML有针对性粗化 | 先进MG并非只有P76/P77；粗相位失配处理有成熟前序，原先10–12点比较不完整 | 细算子适配、平滑/粗解的总成本、三维强界面和边界条件、作者实现 |
| **P88** Stolk，*A dispersion minimizing scheme for the 3-D Helmholtz equation based on ray theory*，arXiv1504.01609。[正文](https://arxiv.org/html/1504.01609) | 引言和§7附近：常系数/平滑介质5–6点传播例；两网格结合double-sweep粗逆，含三维盐丘测试 | 低点/波长及MG/扫描混合有具体研究，不能将6点条件仅作为MG迁移负面因素 | 精确版本和正式发表信息、异质跳变条件、准备/在线及原方程精度；不把光滑介质结论套给颅骨 |
| **P89** Dwarka、Vuik，*Scalable multi-level deflation preconditioning for highly indefinite time-harmonic waves*，JCP469,111327 (2022)，DOI10.1016/j.jcp.2022.111327。[大学记录](https://repository.tudelft.nl/record/uuid%3Ac4014afa-f934-41e1-99e4-76f696fe8dd5)、[出版社](https://doi.org/10.1016/j.jcp.2022.111327) | 摘要、出版社§3.1–3.2方法片段：高阶粗基、递归deflation与CSLP/内层迭代组合 | 强基底不仅是给普通MG换平滑器；近零模式对齐和粗层成本还有一套完整传统解法 | 2D/3D范围、嵌套容差/运算、硬件与精度计时，及后续实现关系 |
| **P90** Chen、Dwarka、Vuik，*Matrix-Free Parallel Scalable Multilevel Deflation Preconditioning for Heterogeneous Time-Harmonic Wave Problems*，JSC102,47 (2025)，arXiv2412.04980，DOI10.1007/s10915-024-02786-w。[正文](https://arxiv.org/html/2412.04980v1)、[大学记录](https://repository.tudelft.nl/record/uuid%3A687f0019-1b3c-41b9-bdbe-89bb8cb1e010) | 核元数据/摘要并定位正文，确认是P78之后独立的多层deflation工作 | 首轮读了P78基础CSLP却没追到后续更强组合，传统基底比较不完整 | 正文、数值表和实现尚需深入；当前不引用其速度作排序 |
| **P91** Liu、Ghysels、Claus、Li，*Sparse Approximate Multifrontal Factorization with Butterfly Compression for High-Frequency Wave Equations*，SISC43(5),S367–S391 (2021)，DOI10.1137/20M1349667，arXiv2007.00202。[正文](https://arxiv.org/html/2007.00202)、[出版社](https://epubs.siam.org/doi/10.1137/20M1349667) | 摘要、引言及格式机制：针对高频振荡前沿矩阵，使用butterfly/complementary low-rank，区别于一般低秩压缩 | 用未压缩LU或一般低秩的扩展性来降级所有压缩因子不充分；它也可作迭代预条件 | 三维实际常数、因子准备/在线/内存、压缩误差和迭代成本，及当前变密度算子适配 |

此处确认的是补查必要性，不提前认定这组方法优于Born或McMg。[报告第11节](REPORT.md#11-用户质疑后的反思哪些工作实际没有做完)列出补齐判断的要求。
