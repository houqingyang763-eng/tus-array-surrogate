# 论文总结 Skill：经颅超声 3D 阵列设计项目专用 v2

## 使用场景

当用户让我阅读、筛选、总结论文时，必须默认服务于这个科研项目：

“经颅超声波束成形 / 声场预测 / 相位延迟矫正神经网络加速”，当前更准确的重点是：

面向 3D 阵列初设计的神经网络 surrogate model。

核心目的不是泛泛读论文，而是帮助用户判断：

1. 这篇论文是否能支撑组会 PPT；
2. 是否能启发 3D 神经网络 IO 设计；
3. 是否能服务阵列初设计；
4. 是否能帮助判断阵列位置、阵列形状、阵元数量变化时的声场预测方案；
5. 是否能启发“单阵元响应预测 + 线性叠加”的技术路线。

论文总结必须围绕项目判断，不要写成普通文献综述。

---

# 总体原则

先判断，再总结。

不要一上来堆细节。  
不要把背景写很长。  
不要只翻译论文摘要。  
不要只报术语。

必须回答：

这篇论文对我们的项目到底有没有用？  
能偷什么？  
不能偷什么？  
放在 PPT 哪个位置？  
值得精读、略读，还是放弃？

用户当前最关心的不是相位延迟，而是：

1. 阵列位置能不能变；
2. 阵列形状能不能变；
3. 是否支持 3D；
4. 是否能预测单阵元响应并叠加；
5. 输出是否匹配 peak pressure + brain pmax field；
6. 数据是否覆盖 array geometry variation；
7. 网络结构是否能讲懂、能迁移。

---

# 输出模板

每篇论文必须按以下模块总结。

---

## A. 一句话判断

先用 1 到 3 句话判断这篇论文的价值。

必须明确说：

这篇是：
- 主线论文；
- 辅助论文；
- 只适合借鉴某个点；
- 还是可以放弃。

同时说明它最适合放在 PPT 的哪个位置，例如：

- 直接对标 TUSNet；
- 3D 网络可行性；
- 阵列几何编码；
- 单阵元响应预测；
- 跨领域 IO 借鉴；
- 训练数据生成；
- 不适合作为主线。

---

## B. 论文做了什么

只讲任务，不堆背景。

必须说清楚：

1. 论文要解决什么问题；
2. 它加速/预测/优化的对象是什么；
3. 它和传统仿真、传统算法、传统实验相比解决了什么痛点；
4. 它是不是和我们的经颅超声项目同构。

不要写很长的领域背景。

---

## C. 具体 IO

这是最重要模块之一。

必须具体说明：

1. 输入是什么；
2. 输出是什么；
3. 输入输出维度是什么；
4. 哪些变量是固定的；
5. 哪些变量是可以变化的；
6. 输入里几何信息是怎么编码的；
7. target / source / sensor / array / boundary condition 是怎么给网络的。

尤其要关注：

- 输入是不是 2D image、3D volume、point cloud、mesh、坐标点、token、graph；
- 输出是不是 2D field、3D field、标量指标、局部 ROI、query point value、trajectory、控制量；
- 是否支持 variable geometry；
- 是否支持 variable number of sources/elements；
- 是否支持不同位置、不同形状、不同尺度。

对于我们的项目，要始终类比到：

输入：
3D skull sound-speed / density / attenuation volume  
+ bowl array geometry / element coordinates / array mask  
+ target point / target region  
+ distance-to-scalp / projection / propagation prior

输出：
peak pressure / focal pressure  
+ brain pmax field / 3D time-maximum pressure field  
+ 可选：single-element response field  
+ 可选：phase/delay correction

---

## D. 用了什么网络

必须讲网络结构，但要讲成人能听懂的话。

不能只写：
“用了 U-Net / FNO / Transformer / DeepONet”。

必须解释：

1. 这个网络为什么适合这个任务；
2. 它怎么处理空间信息；
3. 它怎么处理几何信息；
4. 它怎么处理长程依赖；
5. 它怎么降低 3D 计算量；
6. 它和普通 CNN / U-Net 的区别是什么；
7. 它迁移到我们的项目会遇到什么问题。

讲术语时必须翻译成项目语言。

例如：

- U-Net：适合 volume-to-volume，把 3D 介质图映射成 3D 物理场，但显存压力大；
- FNO：学函数到函数的映射，适合 PDE surrogate，但要看能否处理复杂 skull 和 array geometry；
- DeepONet：适合“输入一个函数/结构 + 查询坐标 → 输出该点物理量”；
- implicit representation：适合避免一次性输出巨大 3D volume；
- PointNet / GNN / Transformer：可能适合可变数量阵元和阵列几何编码；
- CNN encoder + MLP head：适合先预测 peak pressure 等低维指标。

---

## E. 训练过程

必须说清楚：

1. 数据怎么来；
2. label 怎么来；
3. 是否来自仿真；
4. 用什么仿真工具；
5. 训练集覆盖了哪些变量；
6. loss 怎么设；
7. 为什么这样设 loss；
8. 有没有物理约束；
9. 有没有数据增强；
10. 怎么验证泛化。

对于我们的项目，特别要看：

- 是否需要大量 3D 仿真；
- 是否可以先固定 skull；
- 是否可以改变 array position / shape / element number；
- 是否能训练单阵元响应；
- 是否能用线性叠加生成多阵元场；
- 是否需要 focal-region weighted loss；
- 是否需要 peak pressure loss；
- 是否需要 pmax field loss；
- 是否需要高压区 / 非目标风险区加权，而不是大区域均匀 MSE。

---

## F. 最终效果

必须具体说：

1. 速度；
2. 误差；
3. 指标；
4. 和谁比；
5. 测试集是什么；
6. 是否泛化到没见过的 geometry / target / subject；
7. 结果是否可信；
8. 是否只是 numerical ground truth；
9. 是否有真实实验验证。

不要只说“效果很好”。

要明确判断：

这个效果对我们的项目有多大参考价值。

---

## G. 陌生概念解释

把术语翻译成项目语言。

用户不是要背名词，而是要知道：

这个概念在我们的项目里对应什么。

例如：

- time reversal；
- k-Wave；
- FWHM；
- IoU；
- modified Hausdorff distance；
- neural operator；
- Fourier Neural Operator；
- DeepONet；
- implicit neural representation；
- SDF；
- occupancy grid；
- point cloud；
- graph neural network；
- dose prediction；
- differentiable simulation；
- surrogate model；
- Green’s function / impulse response；
- superposition。

解释时要简短、清楚、和本项目挂钩。

---

## H. 我们真正关心的问题

这一节必须单独写，不能混在其他模块里。

必须逐项回答：

### 1. 能不能服务阵列设计？

它是否能用于快速评估不同阵列方案？

包括：

- 阵列放哪里；
- 离头皮多远；
- 阵列多大；
- 阵元多少；
- 阵列形状如何；
- 法向投影到头皮后的覆盖区域如何。

判断：能 / 不能 / 部分能。  
说明原因。

---

### 2. 阵列位置能不能变？

重点看模型是否支持：

- 阵列平移；
- 阵列旋转；
- 贴附距离变化；
- 距头皮 0 mm、0.5 mm、1 mm 等变化；
- 阵列沿头皮法向移动；
- 阵列投影到不同头皮区域。

必须判断：

这篇论文是真的把位置作为输入变量，还是只是固定位置下做鲁棒性测试。

---

### 3. 阵列形状能不能变？

重点看模型是否支持：

- 阵列变大 / 变小；
- 阵元数量变化；
- 阵元间距变化；
- 碗状曲率变化；
- 不规则阵列；
- 阵列 mask 变化；
- 法向投影到头皮后的不同形状。

如果不能，要说明它为什么不能。

---

### 4. 是否支持 3D？

必须判断：

- 输入是不是 3D；
- 输出是不是 3D；
- 是否能处理 3D volume；
- 是否能输出全场；
- 是否只是在 2D proof-of-concept；
- 3D 化需要付出什么代价。

---

### 5. 是否适合“单阵元响应预测 + 叠加”？

这是项目核心假设之一。

必须判断论文是：

- 直接预测整个阵列总场；
- 预测单 source / 单 element response；
- 预测 Green’s function / impulse response；
- 预测局部场；
- 预测可叠加的 basis response；
- 还是完全不支持叠加思路。

对于我们的项目，优先关注：

如果单个阵元场能预测准，多阵元场能否通过相位/幅值加权线性叠加得到。

要提醒：

这个思路依赖线性声学近似。  
如果涉及非线性传播或强热效应，需要重新判断。

---

### 6. 输出是否匹配 peak pressure + brain pmax field？

必须判断输出和我们目标是否一致。

我们的重点输出是：

- peak pressure / focal pressure；
- 第一版低分辨率大区域绝对 pmax field，并评估 whole-brain 扩展边界。

相位延迟不是当前主线，只作为可选扩展。

如果论文只输出分类、分割、位置、低维指标，也要说明它只能借鉴 IO 或网络，不是直接对标。

---

### 7. 数据是否覆盖 array geometry variation？

必须列清楚训练数据覆盖了哪些变化：

- skull 是否变化；
- target 是否变化；
- array position 是否变化；
- array shape 是否变化；
- element number 是否变化；
- element spacing 是否变化；
- distance-to-scalp 是否变化；
- frequency / amplitude 是否变化。

用户当前可以暂时妥协 skull 泛化，但最关心：

- 阵列位置；
- 阵列形状；
- 3D。

---

### 8. 对我们项目到底能偷什么、不能偷什么？

必须给出明确结论。

能偷的可能包括：

- IO 编码方式；
- 几何条件输入方式；
- 网络结构；
- loss 设计；
- 数据生成方式；
- 评价指标；
- 训练变量采样方式；
- 可视化方式；
- PPT 表述方式。

不能偷的可能包括：

- 固定阵列假设；
- 2D 假设；
- 固定 target grid；
- 固定 skull；
- 只输出 normalized field；
- 不支持 variable geometry；
- 不支持阵元数量变化；
- 只做图像任务、不做物理场。

---

## I. 对我们项目的启发

最后只给短判断，不写空话。

必须回答：

1. 这篇论文是否值得进入核心文献表；
2. 是否值得精读；
3. 是否值得放进组会 PPT；
4. 放在 PPT 哪个板块；
5. 它对我们的 3D 阵列设计路线提供了什么具体启发；
6. 下一步应该找什么类型的论文来补它的不足。

---

# 风格要求

1. 默认中文。
2. 先大局，后细节。
3. 不要一口气列几十个任务。
4. 不要为了完整而完整。
5. 每篇论文都要围绕项目做判断。
6. 用户更需要“这东西该不该读、怎么用”，不是普通摘要。
7. 网络结构必须讲懂，不能只堆术语。
8. IO 必须具体，不能模糊。
9. H 模块必须单独写。
10. 最后必须给出明确结论。

---

# 当前项目优先级

最高优先级：

1. 阵列位置可变；
2. 阵列形状可变；
3. 支持 3D；
4. 服务阵列初设计；
5. 单阵元响应预测 + 叠加；
6. 输出 peak pressure + brain pmax field。

次级优先级：

1. target 连续变化；
2. skull 泛化；
3. 相位延迟直接预测。

当前相位延迟不是主线，不要把论文总结带偏到 phase correction 上。除非论文对 label 生成或阵列聚焦有直接帮助，否则只简短提及。
