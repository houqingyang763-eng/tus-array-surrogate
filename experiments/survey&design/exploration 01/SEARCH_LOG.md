# 首轮检索记录

日期：2026-10-16。状态：首轮检索完成并收束。单Agent，网络检索加定向原文读取；未运行实验、未访问服务器。

每批记录：原样检索式、入口、已知种子、来源/版本、发现或排除、影响判断的证据、下一轮问题。机制重合的结论只写[查重报告](idea查重/REPORT.md)，综合取舍只写[SYNTHESIS](SYNTHESIS.md)。

## 检索前判断

- **判断：**先从三维波动求解的精度—全流程成本约束定位问题，再寻找机制。
- **依据：**用户目标是自主方法贡献；McMg与已有Born/学习预条件工作是强参照。
- **缺口：**具体问题的优先级与可用经典思想尚待本轮核查。
- **下一步：**复用P09/P26/P27/P43/P45/P46等已知入口，再沿问题和通用机制展开。

## 实际检索记录

入口：网页学术搜索发现，arXiv/会议/PMLR/出版社/作者来源核实；第三方摘要只作定位。以下保留原样查询，同一批独立问题同时提交不代表使用多Agent。

### R1：从三维成本与全局传播定位机制

- `Helmholtz neural preconditioner learned Schur complement interface domain decomposition neural operator`
- `Helmholtz neural solver deflation learned coarse space non Hermitian left right subspace`
- `Helmholtz neural operator sweeping polarized traces learned impedance`

发现P62/P63、P66及P49新arXiv入口；P26/P27家族命中。P49归并已有编号。神经粗校正与学习界面不可直接作为新点子。

### R2：波信息、双空间与边界算子

- `neural Helmholtz preconditioner learned deflation left right singular subspace Petrov Galerkin`
- `neural operator Helmholtz impedance to impedance scattering matrix domain decomposition`
- `learned multigrid Helmholtz phase space directional wave packet neural coarse basis`
- `"Large scale scattering using fast solvers based on neural operators"`
- `"Hybrid Neural Operator for Wave Scattering in High-Contrast Media"`
- `"learned" "Petrov" "preconditioner" neural`
- `"neural" "Helmholtz" "impedance" "operator" scattering`

发现P61/P68/P69及GMP线索，McMg、Wave-ADR、Butterfly为已知方向。读取P68/P69正文，区别外层物理残差与散射分解。背景FNO接散射Transformer降级。

### R3：查粗空间构想是否已经被覆盖

- `"Graph Neural Multilevel Preconditioners for Iterative Solvers"`
- `"neural" "deflation" "Helmholtz"`
- `"learning" "Schur complement" "Helmholtz" neural`
- `"neural" "polarized traces"`
- `"NeuraLSP"`
- `"learned" "Petrov-Galerkin" multigrid`
- `"learned" "scattering matrix" Helmholtz preconditioner`

读P61/P63/P64/P65/P70，确认双向限制/插值、近零样本子空间、算子基deflation已有实质先例。普通“学粗基/双空间”不保留。

### R4：物理界面、相容表示与散射组合

- `neural network scattering matrix Redheffer star product Helmholtz preconditioner`
- `"Helmholtz" "neural" "interface" "Schur"`
- `"learned" "coarse space" "singular" preconditioner`
- `"neural" "non-normal" "preconditioner"`
- `"neural" "commuting" "multigrid"`
- `"learned" "compatible" "multigrid" wave`
- `"neural" "de Rham" preconditioner`
- `"Helmholtz" "pressure" "velocity" "neural" multigrid`

P71/P73及FOSLS-deRhaNN线索说明散射组合和相容表示并非空白。后者只读摘要，不以其研究对象替代本项目。上一轮C1已写压力/通量粗传递，因此“加通量”明确标为已有方向，不能重新包装。

### R5：针对双界面构想的第一轮查重

- `"neural" "two" "interfaces" "Helmholtz" preconditioner`
- `"neural" "Schur complement" "scattering"`
- `"neural" "thin layer" "Helmholtz" operator`
- `"neural" "impedance-to-impedance"`
- `"learned" "two-surface" acoustic operator`
- `"Neural" "Schur" "Helmholtz" preconditioner`

部分查询加arxiv.org/openreview.net/epubs.siam.org等域过滤。结果含大量同词异义，未用其支持不存在结论。有效链仍是P62/P66及经典阻抗映射；本轮设计必须比“把网络搬到边界”多出具体结构。

### R6：回查经典来源与最接近的消元工作

- `"Learning to Optimize Multigrid PDE Solvers" Greenfeld 2019`
- `"neural" "Schur complement" preconditioner learning domain decomposition`
- `"Helmholtz" "learned" "surface" "preconditioner"`
- `"neural" "skull" "Schur"`
- `"Learned infinite elements" "Helmholtz" Hohage Lehrenfeld Preuss`
- `"Neural Schur Complement Operator"`
- `"Helmholtz" "surface" "neural" "two" preconditioning`

新增P60/P67/P72与W02，触发设计收紧：Schur、DtN、辅助状态、学习细节映射本身均不申报创新。候选转为“局部骨层法向双面消元＋非可分离切向耦合学习＋完整体残差回注”的具体分工，见DESIGN。

### E1：收束扩展一

- `"Helmholtz" "neural" "Schur complement" interfaces`
- `"learned infinite elements" "neural network"`
- `"acoustic" "neural" "two-port" scattering operator`
- `"learned" "Schur" "skull"`
- `"Helmholtz" "neural" "coupled interfaces"`
- `"MLORAS" "Helmholtz" "indefinite"`

返回既有ELM-DD、learned IE链，以及声管模态分解/声表面器件两端口代理；后两类不是原系统残差预条件。skull/Schur字面查询噪声高，不作为新颖性证据。没有改变候选差异或取舍的机制，记第一次无实质更新。

### E2：收束扩展二（改用功能同义词）

- `learning optimized Schwarz high frequency Helmholtz neural interface`
- `neural boundary operator Schur complement preconditioning wave equation`
- `learned interface operator Helmholtz domain decomposition incoming outgoing`

返回传统耗散声学Schur预条件、sweeping、通量界面耦合及PINN边界方法；其消元/散射思想已被P66/P67覆盖，训练式PDE解不等于固定权重的残差预条件。新增检索线索不改变当前候选或降级判断，记第二次无实质更新，首轮收束。

## 原文核查与访问情况

定向正文：P60–P72（P49只补元数据）、P27结论、P46计时表；P73仅摘要，W02仅作者README。P60与P62读取官方PDF文本，不根据图像估读数值。FNO OpenReview和DeepONet Nature入口出现验证/访问错误，未将其作为本轮核心结论来源；经典工具名称已知，不为此延迟其他机制判断。

覆盖了相关学习预条件、粗空间、Schwarz/Schur、波传播/散射表示及相容表示。未做付费数据库全量被引检索，未声称覆盖所有未发表工作。查询中出现的新标题不自动全部登记；保留与机制判断直接相关的P60–P73及W02，版本与事实见[papers](papers/README.md)。

## 收束条件

本轮按E1/E2满足停止条件。当前只保留一条具体设计继续；查重结果限定于上述覆盖，不写成全领域首次。下一步由[综合判断](SYNTHESIS.md)指定，不继续无目标扩搜。
