# P45 变密度 Born：三维、移动点源与更换颅骨

2026-10-10。已知论文的进一步核查：本轮新增作者源码、精度口径和复现障碍；只读，未运行。论文为 Stanziola、Arridge、Treeby、Cox 的 *Iterative Born Solver for the Acoustic Helmholtz Equation with Heterogeneous Sound Speed and Density*，arXiv:2507.16087 v1（2025-07-21）。[原文][paper]、[作者仓库][repo]；源码固定在 `2b59c72acf8637a8f314157a28d00380e19b0084`，查询时 main 指向该提交（2026-01-29）。

## 判断：保留为核心频域基线，值得精读

| 用户要求 | 核查结论 | 证据边界 |
|---|---|---|
| 三维 | 已有实现及三维算例 | 主函数有3D扩域/输出分支；球散射与经颅计算均为3D |
| 可移动点源 | 输入机制支持 | 改变 `source_p` 的非零体素即可移动网格点源；球例还用 `offGridPoints` 表示离网格点源；未做经颅多位置统计 |
| 可改颅骨 | 输入机制支持 | 可替换体素级 c/ρ/α及骨几何，重新准备并求解，无训练；经颅验证只展示一个截断颅骨 |

定位：[主函数233–258、278–297、514–516行][solver]；[球例74–81行][sphere]。这三项在算法输入层面成立。它是经典数值求解器，换颅骨的意义是解一个新方程；收敛速度会随介质改变。

**迁移判断：**它直接求我们的单频复场物理对象，可作为参考求解器及学习加速底座。它没有神经网络；采用它本身是工程路线选择，论文贡献仍需在其已有能力上增加明确机制与收益。“三维+变密度+经颅”已不是空白。

## 机制与阅读地图

它同时更新复压力和三个复速度场，把局部介质作用与空间微分分开，通过FFT应用均匀背景逆作用，再迭代修正强散射；不是只保留一次散射的弱散射Born近似。

1. **§2.1，式3–7：**变密度Helmholtz与等价压力/速度系统；吸收进入复声速。
2. **§2.2，式9–13：**universal split预条件及收敛条件；正密度/声速、被动损耗和适当缩放是关键。
3. **§2.3、算法1、附录B：**交错网格、背景逆作用；每次3D迭代8次FFT。
4. **§3.1、图2：**三维点源球散射解析对照，展示中心切片幅值。
5. **§3.2、图3及§4图4：**经颅对照、介质反差导致的慢收敛、吸收层厚度与成本取舍。

## 五个决定可用性的核查点

**1. 精度指标还缺完整复场。**经颅基准7为500 kHz聚焦碗源，骨参数均匀、几何取自MNI152；原文报告焦点误差<1%，展示中心平面幅值。球例及k-Wave对照脚本也主要使用 `abs(pressure)`；不是全颅内Re/Im联合unit-shape L2。[球例98、116、129–135行][sphere]、[对照283–285行][compare]。目前缺当前MIDA点源下的完整复场形状误差和相位一致性。

**2. 吸收文档与代码约定不一致。**README写α为Np/m；默认分支却采用 `c²=c₀²(1+2iωc₀α)`，二维例传入 `db2neper(alpha_coeff,2)`。[主函数323–335行][solver]、[示例50–55行][hetero]。官方[db2neper][db]输出单位为Np/((rad/s)²·m)，不是固定频率的Np/m。原文式4另写 `c²=c₀²/(1−2iαc₀/ω)`。两种形式也不能直接视为完全相同。该差异提示先明确损耗模型和参数映射，不能照README填值；不据此判定整个算法错误。当前项目恰好继承 `alpha_power=2`，有适配基础，详见[DESIGN](../DESIGN.md#1-理论对象与必须一致的信息)。

**3. 点源幅相要对齐。**源码含源项缩放和输出 `2c₀/dx` 因子，球例另有经验离散幅值缩放。[主函数338–340、491–493行][solver]、[球例83–84行][sphere]。当前1 Pa是additive注入前幅值，不是强制源点压力；统一实数幅值缩放可在最终形状归一化时消去，相位约定、注入形式和空间源表示仍需对应。不能逐样本拟合全局相位。

**4. 可复现入口存在，原图不能一键重建。**仓库有求解器、GPU选项和示例，许可证LGPL-3.0；`data/`仅占位，缺 `bm7_inputs_12ppw.mat` 与k-Wave参考MAT。球例默认12点/波长、20层边界，与原文24点/波长、4波长边界不同。[bm7][bm7]设置48层边界、1000次上限、rtol=2e−5及极小atol，区别于主函数默认200次/1e−3。停止判据允许绝对残差达标直接退出，因此不能照默认值验收弱点源。经颅[绘图脚本][figure]明确人工对齐，传入2dx/dx两种采样间距并插值；缺原MAT，尚待辨认是求解网格、记录采样还是后处理差异。该过程不能直接替代我们的共同网格评价。

**5. 速度收益要重新计量。**正文给FFT成本和收敛曲线，未给可用于当前配置的k-Wave墙钟加速倍数。原文经颅空间分辨率12点/水波长，当前0.5 mm为6点；同物理域升到12点约需8倍体素，不能借用其精度而忽略成本。公开主函数每次调用重新准备介质，固定颅骨多源缓存需要后续改造；这也应纳入经典对照成本。

## 下一步与论文叙事

先读式4/7/13、图2/3，再对照吸收分支和bm7脚本。后续调研优先弄清二次幂损耗与相位转换，找到或按公开基准规范重建原始输入；授权实验后才测已有MIDA少量源的共同mask复场形状与完整耗时。[VALIDATION](../VALIDATION.md)是未来设计。

若该基线仍慢，才比较学习校正、初值或多尺度改造；介质反差使传播修正变慢，是原文给出的明确瓶颈。McMg原来针对标量系统，不能原封接入这套压力/速度系统；压力标量等价算子与四场系统是两个待选实现。界面通量候选继续保留，尚未选定。需要补学：复相位约定、方程残差、预条件与Born迭代；不必先学全部数值分析。

[paper]: https://arxiv.org/html/2507.16087v1
[repo]: https://github.com/ucl-bug/born-density-matlab
[solver]: https://github.com/ucl-bug/born-density-matlab/blob/2b59c72acf8637a8f314157a28d00380e19b0084/src/acousticHelmholtzSolver.m
[sphere]: https://github.com/ucl-bug/born-density-matlab/blob/2b59c72acf8637a8f314157a28d00380e19b0084/examples/sphere_scattering.m
[compare]: https://github.com/ucl-bug/born-density-matlab/blob/2b59c72acf8637a8f314157a28d00380e19b0084/examples/checkAgainstKWave.m
[hetero]: https://github.com/ucl-bug/born-density-matlab/blob/2b59c72acf8637a8f314157a28d00380e19b0084/examples/heterogeneous_all_2D.m
[db]: https://www.k-wave.org/documentation/db2neper.php
[bm7]: https://github.com/ucl-bug/born-density-matlab/blob/2b59c72acf8637a8f314157a28d00380e19b0084/examples/bm7.m
[figure]: https://github.com/ucl-bug/born-density-matlab/blob/2b59c72acf8637a8f314157a28d00380e19b0084/examples/figures/make_bm7_figures.m
