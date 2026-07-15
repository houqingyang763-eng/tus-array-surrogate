# 项目构想 v3：全脑 / 大区域 pmax 预测 + 单阵元大区域响应候选路线

## 0. 文件用途

这是本项目当前源构想文件。它继承 `project_concept_v2.md`，但修正一个关键路线表述：

> 当前不再研究“长条形传播通道输入 + 焦点附近小 ROI 输出”作为主线。项目优先围绕 whole-brain / `400^3` 级别大区域输入输出设计。单阵元复声场叠加路线仍保留，但其输入和输出也应面向全脑或大区域声场。

---

## 1. 项目定位

本项目面向 3D 经颅超声阵列初设计，目标是构建神经网络 surrogate model，用于快速评估候选阵列在个体头颅声学模型中的脑内声场。

当前用途不是替代临床级 full-wave simulation，而是服务早期阵列设计和技术路线判断：

```text
输入候选阵列设计 + 3D 头颅声学体数据 + 目标焦点
-> 快速预测 whole-brain / 大区域 pmax field
-> 输出焦点、峰值、旁瓣和安全性相关指标
```

---

## 2. 当前输入

候选输入基准：

```text
1. 3D skull acoustic volume
   候选尺寸：400 × 400 × 400
   候选间距：0.5 mm
   候选通道：CT / pseudo-CT 单通道
   待验证扩展：c(x,y,z), rho(x,y,z), alpha(x,y,z)

2. 阵列 / 阵元几何
   element_positions = [(x_i, y_i, z_i)]
   element_normals = [(n_ix, n_iy, n_iz)]
   element_mask / active element set
   可选：element_size, element_shape, fill_factor
   可选：类似 DeepTFUS 的换能器表面点坐标

3. 目标焦点
   target_position = (x_t, y_t, z_t)

4. 可选物理先验特征
   distance_to_scalp
   incidence_angle
   skull_thickness
   path_speed_statistics
   frequency
   amplitude
```

注意：入射角、颅骨厚度等特征仍可保留为物理先验，但不再绑定到“长条形传播通道输入”。

---

## 3. 当前输出

### 3.1 主输出：全脑 / 大区域 pmax field

```text
whole-brain intracranial pmax field
= 3D time-maximum pressure field inside brain
```

候选输出分辨率：

```text
128^3 / 160^3 / 200^3 low-resolution whole-brain pmax
或更高分辨率的大区域输出
```

用途：

1. 评价整个脑内高压风险；
2. 观察旁瓣和非目标区域高压；
3. 满足组内“整个脑内声场”的需求；
4. 支撑阵列设计方案比较。

### 3.2 指标输出

```text
P_target
P_peak
focus_error
side_lobe_ratio
brain pmax distribution statistics
```

这些指标不应完全依赖 normalized pmax，需要继续判断是否必须保留绝对声压标定或额外幅值缩放因子。

### 3.3 候选扩展：单阵元大区域复声场响应

```text
single-element large-region complex response field
Re[G(x,y,z)], Im[G(x,y,z)]
```

用途：

1. 保留相位信息；
2. 支持多阵元相干叠加；
3. 支持阵列位置、形状、阵元数量变化；
4. 通过单阵元响应构造整阵列大区域声场。

边界：

```text
不再采用窄长条传播通道输入；
不再把焦点附近小 ROI 输出作为单阵元路线的主要设定；
是否可行取决于 3D label 成本、显存和线性叠加误差。
```

---

## 4. 当前路线设计

### 路线 A：全阵列 -> 全脑 / 大区域 pmax field

```text
skull volume + array geometry + target
-> whole-brain / large-region pmax field
-> scalar metrics
```

优点：

1. 最直接满足全脑声场需求；
2. 与 DeepTFUS 这类 3D pmax surrogate 工作可对照；
3. 适合组会展示和阵列方案初筛。

风险：

1. 3D 输出和中间特征显存压力大；
2. 阵列位置、形状、阵元数量变化下的泛化仍不确定；
3. normalized pmax 可能不足以比较真实声压强度；
4. 只输出 pmax 不含相位，不能直接用于相干叠加和相位优化。

### 路线 B：单阵元大区域复声场 -> 相干叠加 -> 阵列声场

```text
skull volume + single element geometry + target
-> single-element whole-brain / large-region complex field
-> delay / amplitude weighted coherent summation
-> array large-region pmax field and metrics
```

优点：

1. 更自然支持阵元数量变化；
2. 更自然支持阵列形状变化；
3. 保留相位信息；
4. 有潜力降低任意阵列组合的重复 full-wave label 需求。

风险：

1. 单阵元大区域复场 label 仍然很大；
2. 必须验证线性叠加在经颅复杂介质中的误差；
3. 有限尺寸阵元、硬件耦合、非线性传播或热效应可能破坏独立源假设。

---

## 5. 当前近期关注

1. whole-brain / 大区域 pmax field 的最低可用分辨率；
2. `400^3` 单通道输入基准的边界条件；
3. DeepTFUS 的可借鉴边界：geometry encoding、weighted loss、label 成本、normalized pmax 限制；
4. 高质量 3D label 成本是否会成为主瓶颈；
5. normalized pmax、绝对声压、scalar metrics 是否需要共同输出。

---

## 6. 已舍弃路线

### 长条形传播通道输入

已不再作为当前问题或推荐实验方向。

原因：

1. 用户明确确认当前“就做全脑的，而非长条形”。
2. 全脑声场、旁瓣和非目标高压区域需要大区域输出，窄长条输入不匹配当前主需求。
3. 单阵元路线仍保留，但应改为全脑 / 大区域响应预测。

---

## 7. 一句话总结

v3 的核心路线是：

> 本项目当前以 whole-brain / `400^3` 级别大区域 pmax field 预测为中心，优先判断 3D 全脑输出、label 成本、几何编码和 normalized pmax 边界；单阵元复声场叠加路线仍保留，但不再采用长条形传播通道输入或焦点附近小 ROI 输出，而应面向全脑 / 大区域复声场响应。
