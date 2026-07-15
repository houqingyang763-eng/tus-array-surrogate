# 项目构想 v2：全脑 pmax 输出 + 单阵元复声场叠加路线

## 0. 文件用途

这是本项目当前源构想文件。它继承 `project_concept_v1.md`，但修正一个关键需求：

> 组内要求必须考虑整个脑内声场，因此 whole-brain intracranial pmax field / 3D time-maximum pressure field 不再是“暂不优先”，而是主输出之一。

---

## 1. 项目定位

搭建一个面向 3D 经颅超声阵列初设计的神经网络 surrogate model。

当前用途不是完全替代临床级 full-wave simulation，而是服务阵列初设计迭代：

```text
输入一个候选阵列设计 + 头颅声学模型 + 目标焦点，快速评估整个脑内声场和焦点聚焦效果。
```

核心评价对象包括：

1. 整个脑内 pmax field；
2. 焦点处压力；
3. 脑内峰值压力；
4. 焦点偏移；
5. 旁瓣风险；
6. 阵列几何变化下的鲁棒性。

---

## 2. 当前输入

推荐输入：

```text
1. 3D skull acoustic volume
   c(x, y, z), 可选 rho(x, y, z), alpha(x, y, z)

2. 阵列几何
   element_positions = [(x_i, y_i, z_i)]
   element_normals = [(n_ix, n_iy, n_iz)]
   element_mask / active element set
   可选：element_size, element_shape, fill_factor

3. 目标焦点
   target_position = (x_t, y_t, z_t)

4. 可选物理先验特征
   distance_to_scalp
   incidence_angle
   skull_thickness
   path_speed_statistics
```

---

## 3. 当前输出

### 3.1 主输出：全脑 pmax field

```text
whole-brain intracranial pmax field
= 3D time-maximum pressure field inside brain
```

用途：

1. 评价脑内整体安全性；
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

### 3.3 辅助输出：焦点附近复声场

```text
focal ROI complex pressure field
Re[G(x,y,z)], Im[G(x,y,z)]
```

用途：

1. 支持相干叠加；
2. 支持相位 / 延迟分析；
3. 在焦点附近做高分辨率预测。

### 3.4 候选扩展：单阵元响应

```text
single-element complex response field
```

用途：

1. 支持阵列位置变化；
2. 支持阵列形状变化；
3. 支持阵元数量变化；
4. 通过多阵元相干叠加构造完整阵列声场。

---

## 4. 两层路线设计

### 路线 A：全阵列 → 全脑 pmax field

```text
skull volume + array geometry + target
→ whole-brain pmax field + scalar metrics
```

优点：

1. 直接满足组内需求；
2. 适合输出安全性和旁瓣评价；
3. 组会表述直观。

风险：

1. 3D 输出张量大；
2. 对阵列 geometry variation 泛化难；
3. 如果只输出 pmax，不能直接用于相干叠加和相位优化。

### 路线 B：单阵元复声场 → 相干叠加 → 阵列声场

```text
single element position + normal + skull context
→ single-element complex field
→ delay / amplitude weighted coherent summation
→ array field
→ pmax field and metrics
```

优点：

1. 天然支持阵元数量变化；
2. 天然支持阵列形状变化；
3. 更适合阵列初设计；
4. 保留相位信息。

风险：

1. 必须验证线性叠加误差；
2. 单阵元复场输出仍然很大；
3. 有限尺寸阵元和硬件耦合可能破坏理想独立源假设。

### 当前推荐态度

不要二选一。第一阶段可以采用：

```text
低分辨率 whole-brain pmax field 作为主输出；
焦点附近 high-resolution complex field / single-element response 作为辅助输出或后续路线。
```

---

## 5. 第一阶段最小可行任务

优先验证：

1. 全脑 pmax 输出的数据量和显存压力；
2. 低分辨率 whole-brain pmax 是否足够用于阵列方案比较；
3. 单阵元复声场叠加能否近似整阵列 full-wave 仿真；
4. 只输出 pmax 与输出复声场在相位优化上的差别；
5. 阵列位置 / 形状变化如何编码进网络。

---

## 6. 需要重点查证的问题

1. whole-brain pmax field 的合理分辨率是多少？
2. 对阵列初设计，低分辨率全脑场是否足够？
3. 论文中是否已有 3D 经颅超声 full-field surrogate？
4. 单阵元响应叠加在经颅复杂介质中误差多大？
5. array geometry 用 mask、点云、graph、token 还是 Fourier positional encoding 更合适？
6. loss 是否需要对焦点和非目标高压区域加权？

---

## 7. 一句话总结

v2 的核心路线是：

> 本项目以 whole-brain intracranial pmax field / 3D time-maximum pressure field 作为主输出，满足组内对整个脑内声场的要求；同时保留“单阵元复声场预测 + 多阵元相干叠加”作为支持阵列位置、形状、阵元数量变化的核心候选路线。第一阶段不应直接追求临床级完整仿真替代，而应先验证低分辨率全脑 pmax 输出、焦点 ROI 复声场输出和单阵元叠加路线的可行性与误差边界。
