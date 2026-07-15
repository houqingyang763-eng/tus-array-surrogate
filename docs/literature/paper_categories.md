# 本项目论文阅读三分类 v1

## 项目当前核心目标

当前阶段读论文不是为了泛泛综述，而是为了服务：

1. 6 月 8 日组会 PPT；
2. 3D 经颅超声神经网络加速技术路线判断；
3. 阵列初设计；
4. 阵列位置、阵列形状、阵元数量变化下的声场快速预测；
5. peak pressure + brain pmax field 预测；
6. 单阵元响应预测 + 线性叠加路线判断。

相位延迟矫正不是当前主线，只作为可选扩展。

---

# 第一类：直接对标类

## 核心问题

有没有人已经用神经网络加速经颅超声声场预测？

## 代表方向

- TUSNet
- transcranial ultrasound simulation
- acoustic field prediction
- phase-corrected pressure field prediction
- neural network surrogate for focused ultrasound

## 这类论文的作用

这类论文是项目锚点，用来证明：

1. 经颅超声声场预测可以被神经网络近似；
2. k-Wave / full-wave simulation 可以作为监督标签；
3. 输入 skull CT / 声学参数 + target + transducer geometry，输出 pressure field 这件事已经有人做；
4. 我们不是凭空提出问题，而是在已有工作的基础上扩展。

## 重点看什么

1. 输入是什么；
2. 输出是什么；
3. 网络预测的是 normalized field、absolute field，还是指标；
4. 是否支持 2D / 3D；
5. 阵列 geometry 是否可变；
6. target 是否可变；
7. 数据怎么由仿真生成；
8. loss 怎么设；
9. 和 k-Wave / HAS / ray tracing 比什么；
10. 局限在哪里。

## 和我们项目的关系

直接对标类论文用于回答：

> 已有工作做到哪一步？我们为什么还要做 3D？

尤其要抓住已有工作的不足：

1. 多数是 2D；
2. 多数阵列固定；
3. 多数不支持阵列位置变化；
4. 多数不支持阵列形状变化；
5. 多数不服务阵列初设计；
6. 很少关注单阵元响应预测 + 多阵元叠加。

## PPT 位置

适合放在：

- 已有工作；
- TUSNet 启发；
- 当前方法缺口；
- 为什么需要 3D 化。

## 搜索关键词

- TUSNet
- transcranial ultrasound deep learning
- transcranial ultrasound acoustic field prediction
- focused ultrasound neural network surrogate
- pressure field prediction ultrasound
- phase aberration correction deep learning ultrasound

## 阅读优先级

高。

这类论文数量不需要很多，但必须读透。TUSNet 是主锚点。

---

# 第二类：3D 物理场神经网络类

## 核心问题

如果我们要做 3D 声场预测，应该选什么网络？  
3D volume / 3D geometry / 3D field 怎么被神经网络处理？

## 代表方向

- 3D U-Net
- V-Net
- 3D CNN
- Fourier Neural Operator, FNO
- DeepONet
- neural operator
- implicit neural representation
- coordinate-based field prediction
- wave propagation surrogate
- acoustic wave surrogate
- PDE surrogate model
- electromagnetic / seismic / acoustic field prediction

## 这类论文的作用

这是当前最重要的一类论文。

它用来回答：

1. 3D 场预测到底能不能做；
2. 是一次性输出 3D volume，还是按坐标点查询；
3. 如何避免 3D 输出张量太大；
4. 如何处理长程空间传播关系；
5. 如何处理介质分布到物理场的映射；
6. 哪些网络结构适合我们。

## 重点看什么

1. 输入是不是 3D 介质参数场；
2. 输出是不是 3D 物理场；
3. 是否支持 source / target / boundary condition 变化；
4. 是否支持 query point 输出；
5. 是否支持多源叠加；
6. 是否有物理场指标预测；
7. 是否有仿真数据训练；
8. 是否说明速度提升；
9. 是否验证了没见过的 geometry；
10. 是否适合迁移到 skull + array + target → pmax field。

## 重点比较的 IO 形式

### 方案 A：3D volume → 3D volume

对应我们项目：

> skull sound-speed volume + array mask + target mask → 3D brain pmax field

优点：直观。  
缺点：显存和数据压力大。

可能网络：

- 3D U-Net
- V-Net
- 3D CNN encoder-decoder

---

### 方案 B：3D volume + coordinate → query point value

对应我们项目：

> 输入 skull volume 和 array geometry，再输入某个 brain 坐标点，输出该点 pmax

优点：避免一次性输出完整 3D volume。  
缺点：需要大量 query point 训练，推全场时要多次查询。

可能网络：

- DeepONet
- implicit neural representation
- coordinate MLP
- neural operator variants

---

### 方案 C：3D volume + array geometry → low-dimensional metrics

对应我们项目：

> 输入 skull + array + target，输出 peak pressure / focal pressure / focal gain / peak location

优点：适合最小可行实验。  
缺点：不能直接获得全脑 pmax field。

可能网络：

- 3D CNN encoder + MLP head
- transformer head
- graph/point encoder + MLP head

---

### 方案 D：single-element response prediction

对应我们项目核心设想：

> 预测单个阵元的 3D response field，再对多个阵元做相位/幅值加权叠加

优点：

1. 天然支持阵元数量变化；
2. 天然支持阵列形状变化；
3. 适合阵列初设计；
4. 能把复杂阵列问题拆成单阵元响应库。

缺点：

1. 要确认线性声学假设适用；
2. 单阵元响应也可能需要大量 3D 仿真；
3. 叠加前需要处理相位/时间信息，而不仅是 pmax。

这是本项目特别需要寻找的方向。

## 和我们项目的关系

第二类论文决定我们的技术路线：

> 不是简单把 TUSNet 放大到 3D，而是选择适合 3D 阵列设计的神经网络 IO 形式。

## PPT 位置

适合放在：

- 3D 网络方案选择；
- 为什么 3D 化可行；
- 候选模型比较；
- volume-to-volume vs coordinate-query vs single-element response；
- 技术路线图。

## 搜索关键词

- 3D U-Net physical field prediction
- 3D pressure field prediction neural network
- acoustic wave propagation surrogate neural network
- Fourier neural operator wave propagation
- DeepONet wave equation
- neural operator acoustic simulation
- implicit neural representation physical fields
- coordinate-based neural field prediction
- PDE surrogate 3D wave equation
- seismic wavefield neural operator
- electromagnetic field neural network surrogate

## 阅读优先级

最高。

这类论文决定我们到底怎么做 3D 网络。

---

# 第三类：跨领域 3D 输入输出设计类

## 核心问题

CT、放疗、机器人、3D 空间智能等领域，是怎么把复杂 3D 空间信息编码进神经网络的？

## 代表方向

### 医学 3D / CT 类

- CT reconstruction
- 3D medical image-to-image
- radiotherapy dose prediction
- anatomy-to-dose prediction
- 3D segmentation
- 3D registration
- multi-resolution medical volume learning

### 机器人 / 3D 空间智能类

- point cloud network
- occupancy network
- SDF
- goal-conditioned network
- sensor placement / robot geometry encoding
- graph neural network for spatial systems
- transformer for 3D spatial tokens
- neural radiance / neural field representations

## 这类论文的作用

这类论文不是直接做经颅超声，但能启发：

1. 3D volume 怎么输入网络；
2. 几何结构怎么编码；
3. target point 怎么作为条件；
4. 可变数量的点/阵元怎么处理；
5. 大尺寸 3D 数据怎么降低显存；
6. 如何从完整 3D 场转成 patch / ROI / coordinate query；
7. 如何处理不同形状、位置、尺度的空间对象。

## 重点看什么

1. 输入是 volume、patch、point cloud、mesh、SDF、occupancy grid，还是 token；
2. 输出是 volume、指标、query point value，还是控制量；
3. target / goal / sensor / actuator 位置怎么编码；
4. 是否支持 variable geometry；
5. 是否支持 variable number of points；
6. 是否支持坐标条件输入；
7. 是否能迁移到 array element coordinates；
8. 是否能启发 bowl array geometry encoding；
9. 是否能处理大规模 3D 数据。

## CT / 医学类给我们的启发

CT 和医学 3D 论文主要启发：

> skull sound-speed volume 本质上可以看作 3D 医学体数据。

重点借鉴：

1. 3D volume-to-volume 网络；
2. patch-based training；
3. coarse-to-fine；
4. multi-resolution；
5. anatomy-to-field / anatomy-to-dose 的任务定义；
6. 3D 输出太大时如何处理。

尤其值得关注：

> radiotherapy dose prediction

因为它和我们项目抽象上很像：

> 输入人体解剖结构 + 治疗计划参数，输出 3D 剂量场。

类比我们项目：

> 输入头颅声学结构 + 阵列几何参数，输出 3D 声场 / pmax field。

## 机器人 / 3D 空间智能类给我们的启发

机器人和 3D 空间智能论文主要启发：

> array geometry 更像一组 3D 空间点，而不是普通图像通道。

重点借鉴：

1. 点云编码；
2. 可变数量点编码；
3. 目标点条件输入；
4. 传感器/执行器几何编码；
5. point token / graph / attention；
6. 物体位置、姿态、尺度变化下的泛化。

类比我们项目：

- 阵元 = 一组 3D source points；
- 碗状阵列 = 空间几何结构；
- target = goal point；
- skull = environment map；
- pressure field = environment-conditioned response。

## 和我们项目的关系

第三类论文用于让我们跳出 TUSNet 的固定阵列思路。

它帮助我们设计：

1. array geometry 怎么作为输入；
2. 阵列位置变化怎么编码；
3. 阵列形状变化怎么编码；
4. 阵元数量变化怎么编码；
5. 3D target 怎么编码；
6. 是否使用 mask、坐标、距离场、SDF、point cloud、graph、token。

## PPT 位置

适合放在：

- 跨领域启发；
- 3D IO 设计；
- array geometry encoding；
- 为什么阵列不应只作为固定 mask；
- 候选输入表示方式。

## 搜索关键词

### CT / 医学 3D

- 3D medical image-to-image translation
- CT to dose prediction deep learning
- radiotherapy dose prediction 3D U-Net
- anatomy to dose neural network
- 3D U-Net dose distribution prediction
- medical volume neural network surrogate

### 机器人 / 3D 空间

- point cloud neural network variable geometry
- PointNet sensor placement
- graph neural network physical simulation
- goal conditioned 3D neural network
- occupancy network 3D representation
- signed distance function neural network
- transformer point cloud geometry encoding
- neural fields 3D coordinate representation

## 阅读优先级

中高。

它不是直接对标，但可能提供最亮眼的 IO 设计灵感。