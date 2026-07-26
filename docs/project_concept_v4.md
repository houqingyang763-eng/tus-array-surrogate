# 项目构想 v4：低分辨率大区域绝对 pmax 基线 + 单阵元复声场候选路线

## 0. 当前版本解决什么问题

本文件是当前项目源构想，继承 `project_concept_v3.md`，并纳入 2026-07-04 之后已经确认的范围收缩：

1. 第一版不是严格 whole-brain 全域输出，而是约覆盖上半 / 一半颅骨或脑区的大区域输出；
2. 第一版固定 MIDA skull、频率、阵元尺寸和幅值；
3. 第一版优先研究阵元位置和法向变化；
4. pmax 必须保留绝对声压标定，normalized pmax 只能作为辅助表示或 DeepTFUS 对照；
5. 单阵元大区域复声场 + 多阵元相干叠加仍是支持阵列形状和阵元数量变化的长期候选路线。

v1-v3 继续作为历史来源，不覆盖、不删除。

---

## 1. 项目定位

项目面向 3D 经颅超声阵列早期设计，目标是建立神经网络 surrogate model，快速评估候选阵元位置 / 法向或阵列方案在头颅声学模型中的脑内声场。

当前目标不是替代临床级 full-wave simulation，而是回答：

```text
给定头颅声学体数据 + 阵元/阵列几何 + 聚焦条件
-> 能否快速预测大区域绝对 pmax field 和关键指标
-> 能否为不同阵列方案提供可靠的初筛依据
```

---

## 2. 第一版范围

### 2.1 固定条件

```text
skull / head model: MIDA（第一阶段固定）
frequency: 固定
element size: 固定
amplitude: 固定
```

固定这些变量的目的，是先隔离并研究阵元几何变化，而不是声称它们长期不重要。

### 2.2 主要变化变量

```text
element_position = (x, y, z)
element_normal = (nx, ny, nz)
```

目标点是否固定、离散变化或连续条件化，尚未最终确认，应作为开放问题保留。

### 2.3 候选输入

1. 3D skull acoustic volume：第一版可从 CT / pseudo-CT 单通道开始；
2. 阵元位置和法向；
3. 目标焦点或目标区域条件；
4. 候选物理先验：贴附距离、入射角、颅骨厚度、路径声速统计量。

`400×400×400`、`0.5 mm` 仍只作为原始物理网格和数据量估算参考，不等于第一版网络必须密集输入或输出 `400^3`。

### 2.4 第一版输出

主输出：

```text
low-resolution large-region absolute pmax field
```

候选分辨率：

```text
128^3 / 160^3 / 200^3
或与物理裁剪范围更匹配的非立方网格
```

指标：

```text
P_target
P_peak
focus_error
side_lobe_ratio
大区域脑内最大压力统计
```

normalized pmax 可作为辅助训练目标、显示方式或 DeepTFUS 对照，但不能替代绝对声压输出。

---

## 3. 路线 A：第一版大区域 pmax baseline

```text
skull volume + element/array geometry + target condition
-> low-resolution large-region absolute pmax field
-> scalar metrics
```

用途：

1. 尽快验证本项目自己的输入、label、loss、指标和日志链路；
2. 检查低分辨率大区域场能否保留焦点、旁瓣和非目标高压信息；
3. 与 DeepTFUS 的 3D normalized pmax 路线建立可解释对照。

主要风险：

1. 大区域裁剪边界和坐标系尚未确定；
2. 绝对声压 label 的生成、缩放和 loss 设计尚未确定；
3. 固定 MIDA 下的位置 / 法向采样是否足以泛化尚未验证；
4. 整阵列黑箱模型对阵元数量和阵列形状变化的泛化仍可能较弱。

---

## 4. 路线 B：单阵元大区域复声场响应候选路线

```text
skull volume + single-element geometry + target condition
-> single-element large-region complex response
-> delay / amplitude weighted coherent summation
-> array pmax field and metrics
```

候选复场表示：

```text
Re[G], Im[G]
或经过验证的幅值 / 相位表示
```

保留价值：

1. 更自然地支持阵元数量变化；
2. 更自然地支持阵列形状变化；
3. 保留相位信息，可进行相干叠加；
4. 可能减少为每个阵列组合单独生成 full-wave label 的需求。

必须先验证：

1. 单源复场叠加能否准确重建多源场；
2. 线性声学假设在当前经颅设置下的适用边界；
3. 单阵元大区域复场 label 的生成和存储成本；
4. 阵元有限尺寸、硬件耦合、非线性传播和热效应是否破坏独立源假设。

---

## 5. 当前优先问题

1. 大区域具体裁剪范围、坐标系和物理覆盖；
2. 第一版低分辨率网格的最低可用分辨率；
3. 绝对声压 label、归一化策略、loss 和指标定义；
4. 固定 MIDA 下位置 / 法向的采样与数据划分；
5. 单阵元复场相干叠加的最小验证实验；
6. DeepTFUS 可迁移的工程结构与不可迁移的任务假设。

---

## 6. 当前边界

1. 不把整阵列黑箱网络当作唯一方案；
2. 不把 pmax 当成可直接相干叠加的复场；
3. 不把 `0.5 mm` 仿真网格点当作独立 delay 通道；
4. 不默认某个网络一定适合 3D 经颅超声；
5. 不在当前 8GB 笔记本上继续追求 DeepTFUS full training；
6. 不把相位延迟矫正单独带偏成主线。

---

## 7. 一句话总结

> 第一版先在固定 MIDA、频率、阵元尺寸和幅值下，验证“阵元位置 / 法向条件 -> 低分辨率大区域绝对 pmax field”的完整链路；长期保留“单阵元大区域复声场预测 + 多阵元相干叠加”作为支持阵列数量和形状变化的核心候选路线。
