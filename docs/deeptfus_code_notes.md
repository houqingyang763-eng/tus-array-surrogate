# DeepTFUS 代码阅读笔记

本文件记录 DeepTFUS / TFUScapes 复现过程中的关键代码事实。它不是完整教程，只保留后续迁移到本项目时最容易忘、最需要反复查看的点。

## 2026-07-04：TFUScapes 数据结构与 loader

### 1. 一个 `.npz` 样本包含什么

真实下载样本示例：

```text
external/deeptfus/external/hf_cache/.../data/A00028185/exp_0.npz
```

键名和形状：

```text
tr_coords: (16100, 3), int64
ct:        (256, 256, 256), float32
pmap:      (256, 256, 256), float32
```

含义：

- `ct`：三维 pseudo-CT 体数据，是网络的主要 3D skull / head 输入。
- `pmap`：k-Wave 仿真得到的 3D pressure amplitude / pmax map，是训练标签来源。
- `tr_coords`：换能器 active surface 上的点坐标，不是单个换能器中心点。

大小估算：

```text
ct   = 256^3 * 4 bytes = 64 MiB
pmap = 256^3 * 4 bytes = 64 MiB
tr_coords 示例约 0.37 MiB
```

注意：`.npz` 是压缩文件，磁盘大小不等于训练时展开后的数组大小。

### 2. `data/loader.py` 做了什么

核心文件：

```text
external/deeptfus/data/loader.py
```

读取：

```python
ct = data["ct"]
pmap = data["pmap"]
tr = data["tr_coords"]
```

输出给训练代码的字段：

```text
ct
transducer
pressure
p_max_resized
p_max_raw
sample_id
```

真正送入模型的是：

```text
ct
transducer
```

监督标签是：

```text
pressure
```

### 3. 归一化和形状

`ct` 处理：

```text
ct -> resize 到 resolution^3
ct_r = clip(ct / 2000, 0, 1.5)
```

`pmap` 处理：

```text
pmap -> resize 到 resolution^3
pressure = log(1 + pmap_resized / max(pmap_resized))
```

因此训练标签峰值约为：

```text
log(2) = 0.693147
```

这说明 DeepTFUS 训练时预测的是 normalized / log pressure field，不是原始绝对 Pa 声压场，也不是复声场。

`tr_coords` 处理：

```text
原始坐标范围近似 [0, 255]
tr_norm = (tr / 255) * 2 - 1
```

即换能器点坐标被归一化到 `[-1, 1]`。

### 4. 正式配置与 local_verify 的区别

正式配置来自：

```text
external/deeptfus/configs/base.yaml
```

关键项：

```text
resolution = 256
n_transducer_points = 512
base_width = 16
cond_dim = 128
epochs = 50
batch_size = 4
precision = pure-bf16
```

`scripts/local_verify.py` 会临时改小配置：

```text
resolution = 64
n_transducer_points = 128
base_width = 8
cond_dim = 32
epochs = 1
batch_size = 1
precision = fp32
```

所以 `local_verify.py` 的作用是最小链路验证，不用于判断论文级模型效果。

本轮实际 loader 输出示例：

```text
ct:         (1, 64, 64, 64)
transducer: (128, 3)
pressure:   (1, 64, 64, 64)
```

正式训练单样本大致为：

```text
ct:         (1, 256, 256, 256)
transducer: (512, 3)
pressure:   (1, 256, 256, 256)
```

加入 batch 后为：

```text
ct:         (B, 1, D, D, D)
transducer: (B, N, 3)
pressure:   (B, 1, D, D, D)
```

### 5. 模型输入输出接口

`models/deeptfus.py` 中模型前向接口：

```python
forward(ct, transducer)
```

其中：

- `ct` 进入 3D U-Net 主干；
- `transducer` 先进入 `TransducerEncoder`，变成全局换能器 embedding；
- 输出与 `pressure` 形状一致，是 3D normalized / log pressure map。

训练代码中实际使用：

```python
ct = batch["ct"]
tr = batch["transducer"]
tgt = batch["pressure"]
pred = model(ct, tr)
```

### 6. 对本项目的直接启发

可以借鉴：

1. `3D volume + geometry condition -> 3D field` 的数据接口；
2. 用换能器表面点坐标编码几何信息；
3. 对高压区加权的 loss 思路；
4. `local_verify.py` 这种最小链路验证设计。

不能直接照搬：

1. DeepTFUS 输出 normalized pmax，不输出绝对声压；
2. DeepTFUS 输出不含相位，不适合直接做单阵元复声场相干叠加；
3. `tr_coords` 描述单个 bowl transducer 表面点，不是多阵元阵列；
4. DeepTFUS 的 subject split 适合多 skull 数据，本项目若固定 MIDA skull，数据划分逻辑需要重想。

### 7. 当前边界判断

DeepTFUS 的 loader 和模型接口适合作为 3D pmax baseline 的参考。  
如果本项目要走“单阵元大区域复声场 + 多阵元相干叠加”，至少需要重做：

```text
label: 从 normalized pmax 改为 Re/Im 或幅相复场
output channels: 从 1 通道改为 2 通道或其他复场表示
loss: 从 pmax MSE/gradient loss 改为复场误差 + 叠加后指标
metrics: 增加相位、P_target、P_peak、side_lobe_ratio 等项目指标
geometry: 从单换能器点云扩展到阵元坐标 / 法向 / array mask
```

依据：

- GitHub/代码：`external/deeptfus/data/loader.py` 读取 `ct`、`pmap`、`tr_coords` 并生成 `ct`、`transducer`、`pressure`。
- GitHub/代码：`external/deeptfus/configs/base.yaml` 给出正式 `resolution=256`、`n_transducer_points=512`。
- GitHub/代码：`external/deeptfus/scripts/local_verify.py` 将配置改为 `resolution=64`、`n_transducer_points=128`、`epochs=1`。
- 代码实证：本地 subset 样本 `A00028185/exp_0.npz` 中 `ct` 和 `pmap` 均为 `256^3 float32`，`tr_coords` 为 `(16100, 3)`。
- 项目文档：`docs/project_concept_v3.md` 保留 whole-brain pmax 与单阵元大区域复声场两条候选路线。

## 2026-07-04：迁移到本项目的可借鉴点和必须重做点

### 可迁移点

1. **3D volume + geometry condition -> 3D field 接口**
   DeepTFUS 的 `forward(ct, transducer)` 说明 3D 头颅体数据和几何条件可以共同作为网络输入，输出 3D 场。这对本项目的大区域 pmax baseline 有直接参考价值。

2. **点云式几何编码**
   DeepTFUS 使用 `tr_coords` 表示换能器表面点坐标。本项目不能直接照搬单 bowl transducer，但可以借鉴“几何不做 dense volume，而以坐标 / 点云 / token 条件输入”的思路。

3. **高压区域加权 loss**
   DeepTFUS 的 weighted MSE + gradient loss 体现了一个重要思想：普通全场 MSE 可能被低压背景主导，pmax surrogate 需要让焦点和高压区域在 loss 中更有权重。

4. **local verify / eval / log 工程结构**
   `scripts/local_verify.py`、`train.py`、`eval.py`、checkpoint、`metrics.json`、`per_sample.csv`、`train_log.csv` 这一套链路适合作为本项目最小复现和实验记录模板。

### 必须重做点

1. **输出不能只做 normalized / log pmax**
   本项目需要保留绝对声压标定。DeepTFUS 的 `pressure = log(1 + pmap / max(pmap))` 会丢失绝对幅值，不能直接满足 `P_target`、`P_peak` 和安全阈值比较。

2. **若走单阵元叠加，必须输出复声场**
   pmax 不含相位，不能直接用于多阵元相干叠加。本项目若要支持阵元数量、阵列形状和相位 / 延迟策略变化，至少需要考虑 Re/Im 或幅相形式的单阵元大区域复声场 label。

3. **几何表示需要从单 bowl transducer 改为阵元级表示**
   DeepTFUS 的 `tr_coords` 描述单个 bowl transducer 表面点。本项目需要表达阵元位置、法向、active element set、阵元尺寸 / 形状等信息。

4. **数据划分逻辑需要重想**
   DeepTFUS 的 subject split 面向多颅骨数据。本项目第一阶段只训练 MIDA 标准颅骨模型，因此更关键的是位置 / 法向 / 目标点等几何条件的 train-val-test 划分。

5. **输出范围从严格 whole-brain 修正为大区域**
   用户已确认第一版不是严格 whole-brain，而是大区域，差不多切一半。后续 loader、label 和 metrics 都应围绕大区域裁剪边界重新定义。

依据：

- 代码实证：阶段 A/C/D 已证明非官方 DeepTFUS 的数据读取、eval、训练和日志链路可跑通。
- 代码笔记：本文件前文记录 DeepTFUS 输出为 normalized / log pmax，不是绝对 Pa，也不是复声场。
- 用户确认：第一版先做低分辨率大区域；固定频率、阵元尺寸和幅值；优先研究位置 / 法向变化；pmax 必须保留绝对声压标定。
- 项目文档：`docs/project_concept_v3.md` 保留大区域 pmax 与单阵元大区域复声场两条候选路线。
