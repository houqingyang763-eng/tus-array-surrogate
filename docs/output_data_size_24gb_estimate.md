# 24GB GPU 下输出数据量与显存风险初步估算

日期：2026-07-01

## 0. 结论先行

在当前 `400^3`、`0.5 mm`、单通道输入基准下：

1. **单个全脑 pmax 输出标签本身不会爆**：`400^3 × 1 channel × float32` 约 `244 MiB`；如果用 fp16 / bf16 存储，约 `122 MiB`。
2. **训练显存很可能会爆**：DeepTFUS 风格 3D U-Net 的瓶颈不是最终输出张量，而是高分辨率 encoder/decoder feature maps、skip connection、concat intermediate、反向传播保存的 activations。
3. **24GB GPU 不适合直接训练 `400^3 -> 400^3` full-resolution volume-to-volume DeepTFUS-like 网络**。更现实的第一版应是：
   - low-resolution whole-brain pmax，例如 `128^3`、`160^3`、`200^3`；
   - 加一个 focal ROI high-resolution complex field；
   - 或改成 patch / query-point / implicit output。
4. **完整时域输出 `p(x,y,z,t)` 不应作为第一版输出**。例如 `400^3 × 200 time steps × float32` 已经约 `47.7 GiB / sample`，只存一个标签就接近或超过单卡显存量级。

---

## 1. 依据来源

### 1.1 DeepTFUS / TFUScapes 官方仓库

官方 TFUScapes README 说明：

- dataset 使用 k-Wave simulation；
- 每个 simulation 返回 steady-state pressure field；
- DeepTFUS 从 input 3D CT volume 和 transducer position 估计 normalized pressure fields；
- 官方可视化脚本读取 cropped pseudo-CT volume、pressure map、transducer coordinates。

官方仓库：

- `https://github.com/CAMMA-public/TFUScapes`
- `visualize.py` 中读取：

```python
tr_coords = np.array(data["tr_coords"])
ct = np.array(data["ct"], dtype=np.float32)
pmap = np.array(data["pmap"], dtype=np.float32)
```

我本地临时下载官方 sample 后读到：

```text
file_bytes = 81,961,834

tr_coords: shape = (17107, 3), dtype = int64, nbytes = 410,568
ct:        shape = (256, 256, 256), dtype = float32, nbytes = 67,108,864
pmap:      shape = (256, 256, 256), dtype = float32, nbytes = 67,108,864
```

换算：

```text
ct   = 64 MiB / sample
pmap = 64 MiB / sample
ct + pmap = 128 MiB / sample, uncompressed
sample npz compressed size ≈ 78.2 MiB
```

注意：这是 `256^3 crop`，不能直接证明 `400^3` 全脑输入/输出合理，但它能证明 DeepTFUS 公开数据结构是 `ct -> pmap` 的 3D dense volume-to-volume 形式。

### 1.2 官方模型代码状态

截至本次查看，官方 TFUScapes README 仍写：

```text
Models
coming soon
```

GitHub issue `Release DeepTFUS model on Hugging Face` 仍为 open。

因此官方仓库当前可作为数据结构和样本依据，但不能作为可复现训练显存依据。

### 1.3 GitHub 复现仓库

找到的有效复现参考：

- `https://github.com/masonwang025/deeptfus`

该 README 写明：

```text
Built on Python 3.11, PyTorch 2.x, single H100 80GB.
Should also fit on A100 80GB.
```

其 `configs/base.yaml` 记录：

```yaml
data:
  resolution: 256

train:
  batch_size: 4
  precision: pure-bf16
```

并明确说明：

```text
H100 path needs pure-bf16 to fit batch=4 at 256^3
fp32 OOMs on the first encoder level
```

同一配置还说明 `torch.compile` 会在 decoder `up1` 处 OOM，因为会 materialize：

```text
(B, 48, 256^3) ≈ 6 GiB concat intermediate
```

这个复现仓库不是官方实现，但对 24GB 显存判断很有参考价值：它说明即使是 `256^3`、batch size 4、base_width 16 的小容量 3D U-Net，也已经按 80GB GPU 路线设计。

另一个 GitHub 搜索结果 `rish1614/AI-Based-3D-Transcranial-Focused-Ultrasound-Simulation` 当前 API 返回 empty repo，本次不作为有效依据。

---

## 2. 输出标签大小估算

公式：

```text
bytes = D_x × D_y × D_z × channels × bytes_per_value
```

其中：

```text
float32 = 4 bytes
fp16 / bf16 = 2 bytes
```

| 候选输出 | 元素数 | float32 | fp16 / bf16 |
|---|---:|---:|---:|
| TFUScapes 官方 sample `pmap`, `256^3 × 1` | 16,777,216 | 64.00 MiB | 32.00 MiB |
| 全脑 pmax, `400^3 × 1` | 64,000,000 | 244.14 MiB | 122.07 MiB |
| 全脑复声场, `400^3 × 2` Re+Im | 128,000,000 | 488.28 MiB | 244.14 MiB |
| 全脑时域场, `400^3 × 200t × 1` | 12,800,000,000 | 47.68 GiB | 23.84 GiB |
| 低分辨率全脑 pmax, `200^3 × 1` | 8,000,000 | 30.52 MiB | 15.26 MiB |
| 低分辨率全脑 pmax, `160^3 × 1` | 4,096,000 | 15.62 MiB | 7.81 MiB |
| 低分辨率全脑 pmax, `128^3 × 1` | 2,097,152 | 8.00 MiB | 4.00 MiB |
| 焦点 ROI 复声场, `128^3 × 2` Re+Im | 4,194,304 | 16.00 MiB | 8.00 MiB |
| 焦点 ROI 复声场, `64^3 × 2` Re+Im | 524,288 | 2.00 MiB | 1.00 MiB |

判断：

1. 如果只看**最终标签文件大小**，`400^3` pmax 是可以接受的。
2. 如果输出全脑复声场，标签大小翻倍，但仍不是最致命瓶颈。
3. 如果输出完整时域波形，单样本标签已经到几十 GiB，第一阶段不现实。

---

## 3. 磁盘数据量粗估

以当前输入基准 `400^3 × 1 channel` 为例：

```text
输入 CT / pseudo-CT, float32: 244.14 MiB
输出 pmax, float32:          244.14 MiB
合计 raw input + label:      488.28 MiB / sample
```

如果存 `1000` 个样本：

```text
float32 uncompressed ≈ 477 GiB
fp16 / bf16 uncompressed ≈ 238 GiB
```

如果存 `5000` 个样本：

```text
float32 uncompressed ≈ 2.33 TiB
fp16 / bf16 uncompressed ≈ 1.16 TiB
```

实际 npz / zarr / hdf5 压缩后大小取决于 CT、pmax 稀疏性和数值分布。TFUScapes 官方 sample 的 `ct+pmap+tr_coords` 从约 `128.4 MiB` 未压缩压到约 `78.2 MiB`，但这个压缩比不能直接套用到 `400^3` 全脑数据。

---

## 4. 24GB 显存风险不是由最终输出单独决定

DeepTFUS-like 3D U-Net 训练时，显存主要来自：

1. input / target / prediction；
2. encoder/decoder activations；
3. skip features；
4. concat intermediate；
5. loss 中的梯度项 / 加权项；
6. 参数、梯度、optimizer state；
7. CUDA allocator 碎片和临时 workspace。

以复现仓库的 base setting 为参考：

```text
resolution = 256
batch_size = 4
base_width = 16
precision = pure-bf16
```

一个关键 decoder concat intermediate 是：

```text
(B, 48, 256^3) bf16 ≈ 6.00 GiB
```

如果改成我们的候选：

```text
resolution = 400
batch_size = 1
base_width = 16
precision = bf16
```

同类 intermediate 变为：

```text
(1, 48, 400^3) bf16 ≈ 5.72 GiB
```

也就是说：

```text
400^3, batch=1 的一个高分辨率 concat intermediate
≈
256^3, batch=4 的同类 concat intermediate
```

再看最浅层 skip feature：

| 设置 | `x1 = B × 16 × N^3` bf16 | `up1 concat = B × 48 × N^3` bf16 |
|---|---:|---:|
| `B=4, N=256` | 2.00 GiB | 6.00 GiB |
| `B=1, N=400` | 1.91 GiB | 5.72 GiB |
| `B=2, N=400` | 3.81 GiB | 11.44 GiB |

这些还只是少数显式 feature / intermediate，不包含完整反向传播所需的多层 activations、梯度、optimizer state 和 loss 计算缓冲。

因此：

```text
24GB GPU 上直接训练 400^3 full-resolution volume-to-volume DeepTFUS-like 网络：高风险 / 基本不建议作为第一版。
```

---

## 5. 当前推荐输出设置

### 推荐第一版

```text
输入：
400^3 × 1 channel CT / pseudo-CT
+ 低维 transducer geometry
+ target / frequency / amplitude 等必要低维条件

主输出：
low-resolution whole-brain pmax
建议先试 128^3 或 160^3，最多再评估 200^3

辅助输出：
focal ROI complex field
例如 64^3 或 128^3，2 channels = Re + Im
```

理由：

1. `128^3` pmax 标签只有 `8 MiB` float32，适合快速试错。
2. `160^3` pmax 标签约 `15.6 MiB` float32，仍比较温和。
3. `200^3` pmax 标签约 `30.5 MiB` float32，对标签存储仍可接受，但 3D 网络 activation 会明显上升。
4. ROI complex field 用于保留相位信息，服务后续单阵元复声场叠加。

### 暂不推荐第一版

```text
400^3 full-resolution pmax 作为直接训练输出
400^3 full-resolution complex field
400^3 × time steps 的时域压力波形
```

这些可以作为后续验证路线，但不适合一开始就在 24GB GPU 上硬训。

---

## 6. 需要人工确认 / 下一步验证

1. `whole-brain pmax` 的最低可接受分辨率：`128^3`、`160^3`、`200^3` 哪个能满足组内“整个脑内声场”的可视化和旁瓣判断？
2. 输出 pmax 是只在 brain mask 内计算 loss，还是整个 `400^3` / downsample volume 都计算 loss？
3. pmax 标签是否可以用 fp16 / bf16 存盘？如果后续要做安全阈值和峰值误差，需确认量化误差是否可接受。
4. DeepTFUS 输出的是 normalized pressure field；本项目是否需要保留绝对压力 Pa，或同时输出 normalized map + scalar `P_max`？
5. 如果坚持 `400^3 -> 400^3`，应优先验证：
   - batch size 1；
   - bf16 / fp16；
   - gradient checkpointing；
   - base_width 降到 8 或更小；
   - patch / tiled training；
   - output downsampling head。

当前状态：初步估算完成，尚未做本项目模型的真实 GPU profiling。
