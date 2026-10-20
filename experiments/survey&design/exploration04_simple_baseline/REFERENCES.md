# S1来源定位

2026-10-19。分析与取舍只见[REPORT](REPORT.md)。以下标明实际阅读范围和固定版本；公开源码只读，未安装依赖或执行作者程序。P编号沿用[统一索引](../../../docs/literature_seen_index.md)，既有论文重访不计新发现。

## R01

**P45，Stanziola等，Iterative Born Solver for the Acoustic Helmholtz Equation with Heterogeneous Sound Speed and Density。**[arXiv v1正文](https://arxiv.org/html/2507.16087v1)，[JASA DOI](https://doi.org/10.1121/10.0042259)。复用旧事实卡，仅为本轮代码/成果比较补原文。

- 已读：§2.1–2.3方程/拆分/迭代，§3.1球散射、§3.2 BM7、§4讨论及逆算子附录相关部分；核对图3/4。PDF第9页图4已渲染查看，确认对比度与衰减曲线及边界讨论。
- 本地只读PDF：[P45_born_density_v1.pdf](https://arxiv.org/pdf/2507.16087v1)。摘要不作为速度来源；原文无可直接用于项目的硬件/实际停止步数/墙钟表。
- [作者固定版本](https://github.com/ucl-bug/born-density-matlab/tree/2b59c72acf8637a8f314157a28d00380e19b0084)，本地[vendor来源](../../../docs/evidence/exploration04_born.md#code)。`src/`、README、许可证已随此前复现保留，原示例大数据不在vendor。
- [acousticHelmholtzSolver.m](https://github.com/ucl-bug/born-density-matlab/blob/2b59c72acf8637a8f314157a28d00380e19b0084/src/acousticHelmholtzSolver.m)：188–268源/介质pad；278–321交错rho与gamma；323–362吸收、shift/scaling和源；382–468迭代、首次更新后残差归一及判停；478–528计时、还原与输出。
- [singleIteration.m](https://github.com/ucl-bug/born-density-matlab/blob/2b59c72acf8637a8f314157a28d00380e19b0084/src/singleIteration.m)、`B.m`、`L_I_inv.m`、`L0.m`、`V0.m`、`residualMagnitude.m`、`findShifts.m`、`findScalingConstant.m`均读相关核心；逆的四分量代数与本地逐项对应。`findShifts`用包围矩形中心，scaling取最大偏差除0.95。
- [bm7.m](https://github.com/ucl-bug/born-density-matlab/blob/2b59c72acf8637a8f314157a28d00380e19b0084/examples/bm7.m)、`sphere_scattering.m`、`convergence.m`、`tests/TestHomogeneous.m`已读：BM7依赖 `data/bm7_inputs_12ppw.mat`，固定仓库树未含该数据；对照/测试中的幅值误差与解析源尺度处理不搬入项目评价。
- 本轮Git树及补充小源码缓存：`D:/tus-array-surrogate-experiments/survey04-20261019/ucl-bug__born-density-matlab/`及同级 `tree_ucl-bug__born-density-matlab.json`；未向C盘仓库复制PDF或大数据。

## R02

**P100，Vettenburg/Vellekoop，A universal matrix-free split preconditioner for the fixed-point iterative solution of non-symmetric linear systems。**[arXiv 2207.14222v2](https://arxiv.org/html/2207.14222v2)。已有Born家族的基础理论补录，不是新方向发现。

- 已读：§2、算法1、§2.2缩放，§3.1声/波方程，§4.1和表1不同迭代方法比较、§4.2相关比较；核定定理条件与附录相关收敛解释。未把任意学习替换纳入原理论保证。
- 公式定位：算法1的 `B[(L+I)⁻¹(Bx+y)−x]`、式4预条件等价关系；原文的步长和缩放含义。
- 实验定位：1D玻璃、2D高反差铁腔；MATLAB2021b、单精度、RTX3050Ti。该文不提供三维经颅性能。
- 作者实现[Anysim固定树](https://github.com/ivovellekoop/anysim/tree/7031178635af9402c8f48e95692b30acbc3eaa11)与论文代码标识70311786相符；本轮仅核来源版本，不以它为新的项目复现候选。核心更新核查落在R01实际采用的作者代码与本地代码。

**本地Born：**[born_solver.py](../../../docs/evidence/exploration04_born.md#code)全文件230行已读；该文件最后提交为 `7fd816b833eecc8f0388c88890f2aa0007ce6de7`，本轮未改动。

- 43–118 `Context.__init__`；127–131单点源；134–150逆；153–161更新；164–182真残差；184–189输出；192–230主循环、计时和判停。
- [PHYSICS_MAPPING](../../../docs/evidence/exploration04_born.md#physics)：物理输入、α²分支、质量源/相位映射与诊断尺度。
- [B1 RESULTS](../../../docs/evidence/exploration04_born.md#results)：既有CPU/GPU作者对照、五源结果、300/500/1000/10000步形状和计时、评价范围与完整成本。
- [reference_cpu.json](../../../docs/evidence/exploration04_born.md#scaling)：第一case缩放常数；是小域参考，不代指MIDA的分量残差。
- [summary.json](../../../docs/evidence/exploration04_born.md#results)：历史五源曲线及Context准备记录；来自同一头模，不是换头模或多点总场实验。

## R03

**P74，Osnabrugge等，A convergent Born series for solving the inhomogeneous Helmholtz equation in arbitrarily large media。**[arXiv 1601.05997](https://arxiv.org/html/1601.05997)，[JCP DOI](https://doi.org/10.1016/j.jcp.2016.06.034)。已知经典来源重访。

- 已读：§2构造/收敛/波包解释，§3–4数值与讨论。PDF第8页图2已渲染核对；`E`是平方相对误差，原文1D/2D计时不当三维结果。
- 本地只读PDF：[P74_CBS_v1.pdf](https://arxiv.org/pdf/1601.05997)。
- [WaveSim MATLAB固定版本](https://github.com/IvoVellekoop/wavesim/tree/cc49f494a164269a06523913f13ae907afd98add)：读 `WaveSim.m`（单分量FFT传播）、`WaveSimBase.m`，重点84–196循环、源注入/增量累计与能量判停，201–217参数；当前版本含后续Universal Split发展，不能全部称为2016原样代码。
- [WaveSim Python固定版本](https://github.com/IvoVellekoop/wavesim_py/tree/594919609784c99c0a003cada6173e282dd378f9)：已读README、`pyproject.toml`、`src/wavesim/iteration.py`、`helmholtzdomain.py`的准备/算子/边界相关部分、`domain.py`、`simulate.py`的调用流程，以及三维示例、`tests/test_operators.py`、`tests/test_analytical.py`。
- `iteration.py` 7–90主循环；61–83预条件源归一、平方范数与停止；93–132一次更新；136以后forward、preconditioned_operator、preconditioner。`helmholtzdomain.py`确认permittivity输入与wrap校正；不是变密度声学接口。
- 固定版 `0.2.0a1` 的技术栈为NumPy/CuPy/Numba，Python≥3.11；网上旧PyTorch说明不用于判断当前训练兼容性。三维示例有MATLAB标量场对照，未将其当作经颅密度验证。
- 源码小文件缓存分布于 `D:/tus-array-surrogate-experiments/survey02-deep-20261018/IvoVellekoop__wavesim_py/` 和本轮 `survey04-20261019/IvoVellekoop__wavesim_py/`；固定树见本轮 `tree_IvoVellekoop__wavesim_py.json`。未安装执行。

## R04

**P101，Erlangga/Oosterlee/Vuik，A Novel Multigrid Based Preconditioner for Heterogeneous Helmholtz Problems，SISC27(4),1471–1492，2006。**[DOI](https://doi.org/10.1137/040615195)，[作者公开正式版PDF](https://diamhomes.ewi.tudelft.nl/~kvuik/papers/Erl06OV.pdf)。已有CSLP家族的经典来源补录，不是新路线。

- 已读§3–5方法及数值设置，重点复移位、F(1,1)、BiCGSTAB两次预条件应用与表6/7；原计算二维，Pentium4/2.4GHz/2GB。
- PDF第17页、印刷页1487已渲染查看表6/7：移位、吸收和波数会改变迭代数/时间；不是频率无关的固定步数承诺。
- 本地只读PDF：[Erl06OV.pdf](https://diamhomes.ewi.tudelft.nl/~kvuik/papers/Erl06OV.pdf)。未把早期技术报告Erl04OV混作这份正式版。

## R05

**P76，Yovel/He/Treister，Vanka-smoothed Shifted Laplacian multigrid preconditioners for the Helmholtz equations。**[2511.16808v2](https://arxiv.org/html/2511.16808v2)。已知方向，本轮只用其中传统全Jacobi分支判断简单CSLP的真实建设成本，不采用Vanka新机制。

- 已读三维§5、图10–12、表6及相关设置/讨论。计时排除setup、六次平均；CPU与10点/波长，不能横比MIDA/GPU。表6的传统三层Jacobi列是本轮选取的代表结果。
- [作者代码固定版本](https://github.com/RacheliYovel/VankaHelmholtz/tree/0e28ebbab7128450d84e189ad74463acf3a7e168)；代码树含Project/Manifest，但未见LICENSE文件。公开可读不等于本轮已核实开放许可证。
- `Numerical - Julia/src/SolverFunctions.jl`：14起setup；89–114边界/吸收/`HelmholtzParam`与稀疏算子；125以后MGsetup；200–224 solve与仅包裹fgmres的计时。声学路径无项目rho输入。
- `MGsetup.jl`全32行：粗层RAP及最粗LU；`MGcycle.jl`全64行：前后平滑、真残差、限制、递归粗解和延拓。
- `getModels.jl` 的 `getOverthrustAcoustic`，233以后读取外部 `BenchmarkModels/3DOverthrust801801187.dat`、reshape/resample；245以后底部补层并更新网格。本轮固定树未含该模型文件。
- `experiments/table6.jl`：15为初始网格尺寸；约86–165按网格/层数/平滑器各setup和solve；167以后输出。没有显式六次平均循环；网格标签直接使用输入尺寸。`output/Table6.csv`的秒数不同于论文，运行差异未获元数据解释。
- 本轮补充代码缓存 `D:/tus-array-surrogate-experiments/survey04-20261019/RacheliYovel__VankaHelmholtz/`；SolverFunctions等沿用 `survey02-deep-20261018`同固定版本；固定源码树记录在 `tree_RacheliYovel__VankaHelmholtz.json`，未执行重现。

## R06

**P28，LBS，Stanziola等，2022预印本/2023正式版。**[2212.04948](https://arxiv.org/html/2212.04948)。已读完整短文：2D MNIST声速图、展开层数、作者学习的算子/Green参数、对CBS的相近误差步数比较及未来密度扩展。本轮用途是核实CBS实际baseline使用及标明已知学习先例，不将步数比作为墙钟比。

**P46，NPBS，Wang/Jia/Liu，Neural Preconditioned Born Series: A Metric-Matched Framework for Learning-based Preconditioners。**[2603.18527v4](https://arxiv.org/html/2603.18527v4)。已读§5.1.3/表3及相应实验设置、方法相关公式；二维OpenFWI、FGMRES重启50。用途是核实经典对照和“少迭代不一定更快”的实际反例，不把它列为本轮要迁移的学习方案或三维成绩。

## R07

**引用元数据。**2026-10-19读取Crossref原始记录（`is-referenced-by-count`）：[CBS2016](https://api.crossref.org/works/10.1016/j.jcp.2016.06.034)117；[CSLP2006](https://api.crossref.org/works/10.1137/040615195)261；[变密度Born2026](https://api.crossref.org/works/10.1121/10.0042259)0。只是单数据库计数，非总引用或影响力排名。

原始响应保存在 `D:/tus-array-surrogate-experiments/survey04-20261019/crossref_*.json`。GitHub固定树缓存及所有PDF/提取文本/三个图表页PNG也在该D盘目录；本轮没有运行任何候选算法。
