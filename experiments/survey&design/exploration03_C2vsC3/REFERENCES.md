# exploration03：关键来源及读取定位

核查日期：2026-10-19。本文只保存来源、版本与证据定位；综合推理只在[REPORT](REPORT.md)。P编号沿用[统一索引](../../../docs/literature_seen_index.md)。P99为本轮新增登记的作者博士论文，属于已有C3家族延伸；其余均为已知论文重访。DD29与P99的相同数据不计两份独立成果。

网页文本、PDF和作者材料实际已读；关键表格用PDF页图视觉核对。PDF页码以下同时区分印刷页与文件页。公开材料缓存放在 `D:\tus-array-surrogate-experiments\survey03-20261019\`，旧PDF复用 `survey02-deep-20261018\papers\`；原文、图片、源码均未纳入Git。本轮未安装环境、未运行作者代码或任何求解/训练。

## C2证据

<a id="r01"></a>
### R01 · P92 · Stolk：两网格双向扫描

Christiaan C. Stolk, *An improved sweeping domain decomposition preconditioner for the Helmholtz equation*, Advances in Computational Mathematics 43, 45–76 (2017)。本轮固定读取 [arXiv:1412.0464v4，2016-07-11 HTML](https://arxiv.org/html/1412.0464v4)与[同版PDF](https://arxiv.org/pdf/1412.0464v4)。早期题名含two-grid accelerated sweeping，不另算一篇。

- §4/附录A：相位匹配粗离散、PML法向保留分辨率；细层原二阶格式与P88细IOFD版本分开。
- §5，PDF印刷p12附近：MPI、Cartesian分布、MUMPS4.10.0、nRHS与组进程、X-sweep的两组并行；多RHS流水线及GMRES/因子内存。作者未报逐例精度与峰值内存。
- §6.2，PDF p17–18：盐丘原域、最少10 ppw、随机RHS、3格PML、Lisa节点参数；表8在p18（文件页18）。**本轮视觉核了整表，包含空格对齐与全部MUMPS组配置。**
- 表8单RHS的49 s setup＋22 s solve（13M、X16、总32核）和82＋43 s（25M、X32、总64核）是不同真实案例。没有将50M四RHS的31 s/rhs改称单配置。
- 表7的partial-sweep恶化是二维反例，只用于说明传播依赖与并行取舍。跨节点通信的慢因在作者正文仍属推断，没有时间占比。
- [作者官方主页](https://staff.fnwi.uva.nl/c.c.stolk/)只有论文/预印本入口，未定位本三维实现下载；不能写“已核作者三维源码”。

<a id="r02"></a>
### R02 · P88 · Stolk：IOFD与6 ppw三维结果

*A dispersion minimizing scheme for the 3-D Helmholtz equation based on ray theory*, JCP314 (2016), DOI [10.1016/j.jcp.2016.03.023](https://doi.org/10.1016/j.jcp.2016.03.023)。固定[arXiv1504.01609v2 HTML](https://arxiv.org/html/1504.01609v2)、[PDF](https://arxiv.org/pdf/1504.01609v2)。

- §6–8：有限差分传播相位、低色散与强梯度/反射条件；不将粗层3 ppw直接当最终细场精度。
- §7表5为二维精确粗解ppw敏感性，表6才是真三维盐丘；细IOFD6 ppw、粗约3 ppw，ν=3、ω=0.65。
- **PDF p30/表6已视觉核对**：13/25/50/100M、32/64/128/256核、1/2/4/8个RHS、12/12/13/15步、26/35/45/73 s每RHS。正文明确50M整批179 s，不由45×4覆盖原文精确批时间。
- 本文没给新的setup表和逐例峰值内存，不用R01的setup给本版补“实测总时间”；所称残差降10⁻⁶未在计时表明确真/预条件范数。§8原文承认梯度、介质和源离散需要更细或不同格式。
- 与R01同演进链；不是两份独立颅骨验证。

## C3证据

<a id="r03"></a>
### R03 · P89 · Dwarka/Vuik：原多层deflation

*Scalable multi-level deflation preconditioning for highly indefinite time-harmonic waves*, JCP469 (2022) 111327，DOI [10.1016/j.jcp.2022.111327](https://doi.org/10.1016/j.jcp.2022.111327)。[Delft正式全文](https://repository.tudelft.nl/file/File_ac31135c-762a-47a3-ab8c-5d774fbeb62d)。复用本地PDF/文本并重新读相应段落。

- §3：递归结构、CSLP小移位、BiCGSTAB内迭代、n_l^(1/4)上限；内层不要求每次达到统一容差。
- §5，印刷p17前后：顺序MATLAB2019Rb、i7-8665U、8GB；计时**含粗矩阵构造**，不冒充现代并行实现速度。
- §5.3/表7（印刷p20，文件页21）已重新查看页图；Sine三行V/W的步数和1259.18/1359.92等时间按同一行配对。原文Sine式、表注MP3编号与频率记号有不一致，未据此生成声速对比度或可靠波长尺度。
- 表8（印刷p21、文件页22）：三维弹性向量系统、20 gpw，三行CPU时间；未给三轴网格/完整物理域/精度/峰值内存。三维表外停止阈值未明确，保持未报，不从R04/R05反填。
- 所读全文没有与P99相同的完整3D可固定源码链接。

<a id="r04"></a>
### R04 · P90 · Chen/Dwarka/Vuik：matrix-free递归方法

*Matrix-Free Parallel Scalable Multilevel Deflation Preconditioning for Heterogeneous Time-Harmonic Wave Problems*, JSC102,47 (2025)，DOI [10.1007/s10915-024-02786-w](https://doi.org/10.1007/s10915-024-02786-w)。[arXiv2412.04980v1](https://arxiv.org/html/2412.04980v1)；[作者正式稿](https://diamhomes.ewi.tudelft.nl/~kvuik/papers/Che25DV.pdf)。数值提取固定于v1，不把后续3D数据写进它的表格。

- §3及§4.1–4.4：ReD-Glk近似Galerkin、不同移位和粗层解法、L2容差优化；MADP-v3用0.1，最终MADP用0.3；最细两层MG-CSLP、shift=0.5，其他层CSLP-GMRES。
- 表6/7的内CSLP迭代说明慢因；表14显示外10→17、L2 2→47、时间趋近N^1.4；**这组为二维**，只解释成本组织。
- §5：Fortran90、GNU8.5.0/OpenMPI4.1.1、每节点48核/192GB、原文写E5-6248R；不据此替R05的64核机器填型号。
- 附录matrix-free/CSR比较约3倍来自二维五点matvec，不给三维总求解乘该倍数。
- 正文全部二维测试；旧轮以此排除C3大三维资格的依据已被R05替代。

<a id="r05"></a>
### R05 · P99 · Chen博士论文：补齐大三维后续

Jinqiang Chen, *High-Performance Iterative Methods for the Helmholtz Equation*，TU Delft博士论文，2025，DOI [10.4233/uuid:8e7c44b5-091a-4a14-98d7-762be3ee59dd](https://doi.org/10.4233/uuid:8e7c44b5-091a-4a14-98d7-762be3ee59dd)。[学校记录](https://repository.tudelft.nl/record/uuid:8e7c44b5-091a-4a14-98d7-762be3ee59dd)、[学校PDF](https://repository.tudelft.nl/file/File_b7fcca3c-0678-411d-bbb8-2508ef0f32c9)、[作者主页镜像](https://diamhomes.ewi.tudelft.nl/~kvuik/numanal/JinqiangChen_PhD_Thesis.pdf)。实际下载学校PDF，211个文件页；正文印刷页比文件页少16。

- 定向读§1.2.2，印刷p10–13：常系数点源、盐丘/GO的域、声速、源及边界；第6章采用的裁选物理域按§6.1单独记，未与原模型尺寸混用。
- 第6章印刷p147–165（文件163–181），§6.1–6.3.3：完整三维方法及成果；restarted FGMRES(5)、L2 0.1、真残差10⁻⁶，硬件64核/约250GB；原CPU前缀疑点照录。
- **表6.1，p153/文件169已视觉核**：点源外的解析复场L2误差；同时读作者对色散与边界/源的解释，不把全部误差纯归因于离散色散。
- 表6.2，p154/文件170：62716/28441/24681等为**sequential computing**，不是千核时间。
- 表6.3/6.4，p155–156：盐丘层数、频率与外步；14660同样为顺序。
- **表6.5及图6.5，p158/文件174已视觉核**：同盐丘例1→64 MPI ranks为14660.09→367.56 s；32MPI×2线程362.51 s；与顺序表对上。图6.6按MPI rank横轴比较时hybrid额外使用线程，不写成等核两倍加速。
- **p160–162/文件176–178**：GO的L2常达100上限、未限制可能>300；**表6.6/6.7，p162已视觉核**。γ=1→1.5的外29→25、L2 97→73、5114.29→3124.98 s；最大3.80B例1152核22006 s、2304核12607 s，两V-cycle、γ=3。
- 附录B的3D粗模板、5³传递及7³粗算子已读；局部常k近似与项目密度薄壳迁移推理分开。
- 公开字段仍缺：setup/计时函数/峰值内存/数值精度类型及全3D作者源码。表列CPU time按作者solution time/强扩展语境理解，不能核实为含I/O的端到端墙钟。

相关[DD29作者演示，2025-06-24](https://diamhomes.ewi.tudelft.nl/~kvuik/talks/DD29_MS07-JinqiangChen_An_Efficient_Parallel_Multilevel_Deflation_Method_for_Large_Scale_Helmholtz_Problems.pdf)：复用已存PDF，文件第16–19页（投影片编号15–18）与论文第6章同源。它提供了本轮追索入口，不能再用演示缺硬件来代替读取博士论文。

作者[Helmholtz出版入口](https://diamhomes.ewi.tudelft.nl/~kvuik/pub_it_helmholtz.html) → [软件页](https://diamhomes.ewi.tudelft.nl/~kvuik/software/helmholtz/helmholtz.html)已读；下载入口是旧二维ADEF1/CSLP。未将它说成第6章三维源代码。没有向作者发信或操作账户。

## 学习后标杆及强传统竞争

<a id="r06"></a>
### R06 · P27 · McMg v2：学习后标杆

Jia等，*McMg: A Learned Phase-Space Multi-channel Multigrid Preconditioner for Helmholtz Equations*。[arXiv2606.30495v2，2026-07-02 HTML](https://arxiv.org/html/2606.30495v2)、[PDF](https://arxiv.org/pdf/2606.30495v2)。先复用统一索引/旧卡片，再定向核§3.3–3.5、§4.1–4.3、附录A.1–A.3。

- §4.1，PDF p11–13；**表2/p13已视觉核**：224³ Kimberlina 6 ppw、速度2637–4201、16格sponge；A6000、6.3步/0.608 s与CBS284/4.128 s，50样本均值、10⁻⁶；FP32/FP64规则、训练/测试划分及45GB/6GB记载。
- 表1的21.04 s/epoch是二维训练；没有拿来补三维训练时间。setup与solver分离的结构能力不等于表2明确披露了每介质setup计时。三维段未完整列物理长度/Hz、各样本源坐标分布及冷热计时；图8点源型展示不等于任意总源验证。
- 附录A.1的PML/FSM较差是作者同文证据；主文FD+sponge成绩不改叫项目全物理。
- 附录A.3的SL参数为shift1、Jacobi(2,2)、粗Jacobi2次、GMRES(25)；不当优化C2/C3对照。原文CBS最快经典对照的6.79倍仍如实承认。
- 正文未定位完整作者实现链接；本项目的McMg重建不是作者源码，本轮不执行或审计重建实验。

<a id="r07"></a>
### R07 · P78 · 强matrix-free CSLP＋IDR(s)

Chen/Dwarka/Vuik, *A matrix-free parallel solution method for the three-dimensional heterogeneous Helmholtz equation*，ETNA59,270–294，DOI [10.1553/etna_vol59s270](https://doi.org/10.1553/etna_vol59s270)。[arXiv2308.06085v1](https://arxiv.org/html/2308.06085v1)。

实际读§2.3/2.4、§3.3–3.5、§4/5和性能分析附录：7点FD、盐丘域与源、Sommerfeld、每节点48核/192GB、Fortran90；GMRES用预条件残差，IDR/BiCGSTAB用真残差，不混称统一停止。§5.3.3表6：641×641×193、5Hz、IDR(4)在1/2/4/6节点的matvec为413/423/423/404，897.25/510.56/298.86/203.31 s。setup、输出和峰值内存未独立报告。附录的通信序列化针对该版本，不能代填R05。

<a id="r08"></a>
### R08 · P76 · Jacobi＋Vanka及固定作者实现

Yovel/He/Treister，[arXiv2511.16808v2](https://arxiv.org/html/2511.16808v2)。重读§5开头、§5.5/表6、时间备注：双核32GB笔记本、Julia、10 ppw、残差10⁻⁶、20格ABC；Overthrust细Jacobi/粗Vanka与全Jacobi的3/4/5层同文比较；solve计时不含setup。

实际只读固定版本 `0e28ebbab7128450d84e189ad74463acf3a7e168`：

- [SolverFunctions.jl L118–169](https://github.com/RacheliYovel/VankaHelmholtz/blob/0e28ebbab7128450d84e189ad74463acf3a7e168/Numerical%20-%20Julia/src/SolverFunctions.jl#L118)：点源、R/P/Ac/LUcoarsest、Vanka小块或Jacobi准备。
- [L200–224](https://github.com/RacheliYovel/VankaHelmholtz/blob/0e28ebbab7128450d84e189ad74463acf3a7e168/Numerical%20-%20Julia/src/SolverFunctions.jl#L200)：默认inner=5/tol=10⁻⁶，`@elapsed`只包FGMRES。已核原始固定URL，不仅复述仓库README。
- 它是显式矩阵Julia研究实现，不是matrix-free GPU全域即用程序；未执行。

<a id="r09"></a>
### R09 · P77 · RS-CGC

Yovel/Treister，[arXiv2604.19501v1](https://arxiv.org/html/2604.19501v1)。定向核§3临界规模/ppw条件、§5通用硬件/停止、§5.2表5：双核32GB、Julia、20格ABC、10⁻⁶；Overthrust物理域20×20×4.65km、底部延展12–16格、顶部中央点源且顶部无ABC。192×192×72 cells约2.72M DOF、10步67.25 s，6次均值。没有用二维速度反差或10–12 ppw成绩代填项目6 ppw。未定位独立可固定源码，不以Vanka仓库替代。

<a id="r10"></a>
### R10 · P91 · HOD-BF与STRUMPACK

Liu/Ghysels/Claus/Li，*Sparse Approximate Multifrontal Factorization with Butterfly Compression for High Frequency Wave Equations*, SISC43(5),S367–S391 (2021)，DOI [10.1137/20M1349667](https://doi.org/10.1137/20M1349667)。[arXiv2007.00202v2](https://arxiv.org/html/2007.00202v2)。重读§6/§6.1、表3及停止说明；Marmousi2沿一轴复制是三维算子、非全三维变化介质。记录7.5 ppw、27点交错FD/8格PML、ρ=1、Q=10⁴、32节点×32核/每节点128GB、FP64；GMRES(30)以预条件残差绝对10⁻¹⁰或相对10⁻⁶停止。分解/solve/因子内存分列，800GB是因子存储，不是峰值；压缩ε不是停止阈值。

只读固定提交 `819ff1beaef0379e575fd77baaed8393948ca6d9` 的 [testHelmholtz.cpp L128–171](https://github.com/pghysels/STRUMPACK/blob/819ff1beaef0379e575fd77baaed8393948ca6d9/examples/sparse/testHelmholtz.cpp#L128)：set_matrix/reorder/factor/solve可分离，默认制造解而非论文同例；同版本[HOD预条件文档](https://github.com/pghysels/STRUMPACK/blob/819ff1beaef0379e575fd77baaed8393948ca6d9/doc/doxygen/pages/HOD_Preconditioning.txt)。复用已存源码并实际读取相应入口，未执行。GPU-BLR与该CPU-HOD-BF的结果不拼接。

## 未重复预载的既有材料

P87（优化粗相位）、P63（学习粗解表达能力）、P96（紧凑隐式encoder–solver）先按统一索引和experiment02来源定位，作为机制/查重背景；本轮没有从未重核的表格抽取新速度数字。当前 `docs/core_papers/README.md` 在工作树中缺失，沿统一索引及旧REFERENCES进入来源，未恢复被删除文件。

项目任务/物理边界来源：[MISSION](MISSION.md)及用户2026-10-19正式启动指令、[V10 handoff](../../../docs/project_design_handoff_v10.md)。该handoff读取仅为核完整域/输出、密度吸收边界与权限；旧训练/Label状态不作为当前服务器状态。未来实验仍需独立合同。
