# DeepTFUS 复现运行日志

本文件记录 DeepTFUS / TFUScapes 复现过程中的每次环境配置、命令运行、结果、报错和结论。目标是防止复现过程“跑过但忘了怎么跑、错过但忘了怎么错”。

记录原则：

1. 每次只记录可追踪事实，不写聊天流水账。
2. 命令、路径、commit、环境、数据规模、结果和失败原因尽量具体。
3. 大文件、checkpoint、数据集不写入本 repo，只记录其路径或来源。
4. 每次运行后都写一个短结论：继续、回退、改配置，还是暂停问人。

## 当前全局状态

状态：阶段 D 低分辨率从零短训练已在 CUDA 环境下跑通。

已知前置判断：

1. 官方 TFUScapes 仓库主要公开数据入口、sample 和可视化脚本；模型部分仍需继续核实。
2. 非官方复现仓库 `masonwang025/deeptfus` 提供训练、评估、local verify、checkpoint 说明和 Hugging Face 权重入口。
3. 完整训练大概率需要较大显存；第一次复现应从 sample / subset / local verify 开始。
4. 2026-07-04 已用 CPU 路径跑通非官方复现仓库的 `scripts/local_verify.py`。

## 运行记录模板

复制以下模板追加新记录。

````markdown
## YYYY-MM-DD：简短标题

目的：

环境：
- OS：
- GPU：
- Python：
- CUDA / PyTorch：
- Conda / venv：

代码来源：
- 仓库：
- commit：
- 本地路径：

数据来源：
- 数据模式：sample / subset / full / checkpoint-only
- 数据路径：
- 样本数量：

命令：

```bash
...
```

结果：
- 是否成功：
- 关键输出：
- 产物路径：

报错 / 异常：

判断：

下一步：

需要人工确认：
````

## 2026-07-03：建立复现计划与运行日志

目的：

为第一次复现 DeepTFUS 建立可持续记录入口，避免后续上下文只留在聊天窗口。

环境：

尚未开始配置。

代码来源：

尚未正式部署到项目目录。此前只做过临时阅读和检查。

数据来源：

尚未下载正式数据。

结果：

已建立：

```text
docs/deeptfus_reproduction_plan.md
docs/deeptfus_run_log.md
```

判断：

下一步优先不是 full training，而是把非官方复现仓库部署到 `external/deeptfus/`，建立环境，并跑 `scripts/local_verify.py` 或等价最小链路。

需要人工确认：

1. 是否采用 `external/deeptfus/` 作为复现仓库本地路径。
2. 数据和运行产物是否统一放在 `data/`、`runs/` 并加入 `.gitignore`。
3. 当前机器 GPU / 显存情况，以决定后续只跑 smoke test、checkpoint eval，还是小规模训练。

## 2026-07-04：阶段 A 最小链路跑通

目的：

部署非官方 DeepTFUS 复现仓库，建立 Python 3.11 环境，并运行 `scripts/local_verify.py`，确认数据读取、模型 forward / backward、tiny training、checkpoint 和 evaluation harness 可以连通。

环境：

- OS：Microsoft Windows 11 家庭版 中文版 10.0.26200
- GPU：NVIDIA GeForce RTX 5060 Laptop GPU，8151 MiB，driver 591.86
- Python：3.11.15
- CUDA / PyTorch：PyTorch 2.12.1+cpu，`torch.cuda.is_available() = False`
- Conda / venv：Conda env `deeptfus-py311`，路径 `D:\anaconda\envs\deeptfus-py311`

代码来源：

- 仓库：`https://github.com/masonwang025/deeptfus`
- commit：`b78bcc65a3634dd89401366169f8a494c7e2bf39`
- 本地路径：`C:\Users\HOU\Desktop\tus-array-surrogate\external\deeptfus`

数据来源：

- 数据模式：subset，由 `scripts/local_verify.py` 触发 `scripts/download_data.py --mode subset`
- 数据路径：`external/deeptfus/external/hf_cache/datasets--vinkle-srivastav--TFUScapes/...`
- 样本数量：8 个 `.npz`，包括 4 train / 2 val / 2 test
- 备注：本次未使用 Hugging Face token；下载成功但出现 unauthenticated request warning。Windows symlink 不可用，HF cache 退化为非 symlink 模式，可能占用更多磁盘。

命令：

```powershell
conda create -y -n deeptfus-py311 python=3.11
& 'D:\anaconda\envs\deeptfus-py311\python.exe' -m pip install -r requirements.txt
@'
import torch, numpy, scipy, yaml, huggingface_hub
print('python ok')
print('torch', torch.__version__)
print('cuda_available', torch.cuda.is_available())
print('cuda_version', getattr(torch.version, 'cuda', None))
print('numpy', numpy.__version__)
print('scipy', scipy.__version__)
print('yaml', yaml.__version__)
print('huggingface_hub', huggingface_hub.__version__)
'@ | & 'D:\anaconda\envs\deeptfus-py311\python.exe' -
$env:PYTHONUTF8='1'
& 'D:\anaconda\envs\deeptfus-py311\python.exe' scripts\local_verify.py
```

结果：

- 是否成功：成功。`local_verify.py` 最终 PASS。
- 关键输出：
  - device：CPU
  - local verify model output shape：`(1, 1, 64, 64, 64)`
  - tiny model params：`613,137`
  - forward/backward loss：`total=0.0047`
  - one-epoch tiny train：完成，`best_val_rel_l2=0.9055`
  - eval：2 个 test samples，生成 2 个 prediction `.npz`
- 产物路径：
  - `external/deeptfus/runs/_local_verify/ckpt_best.pt`
  - `external/deeptfus/runs/_local_verify/ckpt_last.pt`
  - `external/deeptfus/runs/_local_verify/eval_test/metrics.json`
  - `external/deeptfus/runs/_local_verify/eval_test/per_voxel_mse.npy`
  - `external/deeptfus/runs/_local_verify/eval_test/predictions/A00033747_exp_0.npz`
  - `external/deeptfus/runs/_local_verify/eval_test/predictions/A00033747_exp_1.npz`

报错 / 异常：

1. 当前 conda 版本较老：`conda 4.5.11`，没有 `conda run`。后续命令改用环境 Python 的绝对路径。
2. 第一次运行 `local_verify.py` 失败在 Windows 默认编码：

```text
UnicodeDecodeError: 'gbk' codec can't decode byte 0x88 in position 4611
```

原因是脚本读取 `configs/base.yaml` 时使用了系统默认 GBK。未改代码，设置 `$env:PYTHONUTF8='1'` 后重跑成功。

3. 依赖安装得到的是 CPU 版 PyTorch：

```text
torch 2.12.1+cpu
cuda_available False
cuda_version None
```

这不影响本次 `local_verify.py`，但不适合后续 GPU 训练或真实性能评估。

判断：

阶段 A 的最小链路已经完成。当前能证明：非官方复现仓库可以在本机 Python 3.11 环境下完成小样本下载、数据读取、模型前向/反向、tiny train、checkpoint 和 eval。由于当前是 CPU 版 PyTorch，结果只说明 pipeline 连通，不说明 GPU 训练可行性。

下一步：

1. 若继续阶段 B，建议读取并解释 `data/loader.py`、sample `.npz`、`configs/base.yaml`，建立 `docs/deeptfus_code_notes.md` 或在当前对话中先总结数据结构。
2. 若准备阶段 C checkpoint eval，需要先解决 Hugging Face checkpoint 下载和可能的权限 / 存储路径问题。
3. 若准备小规模 GPU 训练，需要单独安装 CUDA 版 PyTorch，并重新验证 `torch.cuda.is_available()`。

需要人工确认：

1. 是否要为后续 GPU 尝试安装 CUDA 版 PyTorch，还是暂时保持 CPU 环境只做代码阅读和数据结构理解。
2. 是否接受 Hugging Face cache 位于 `external/deeptfus/external/hf_cache/`，还是希望后续统一迁移到项目级 `data/tfuscapes/` 或其他大盘目录。
3. 是否进入阶段 B：理解 TFUScapes 数据结构和 loader。

## 2026-07-04：阶段 C base checkpoint 评估尝试

目的：

下载非官方复现仓库提供的 base checkpoint，并在本地已有 TFUScapes subset 上运行 `eval.py`，确认预训练模型是否能加载、推理并输出指标。

环境：

- OS：Microsoft Windows 11 家庭版 中文版 10.0.26200
- GPU：NVIDIA GeForce RTX 5060 Laptop GPU，8151 MiB，driver 591.86
- Python：3.11.15
- CUDA / PyTorch：PyTorch 2.12.1+cpu，`torch.cuda.is_available() = False`，`torch.version.cuda = None`
- Conda / venv：Conda env `deeptfus-py311`，路径 `D:\anaconda\envs\deeptfus-py311`

代码来源：

- 仓库：`https://github.com/masonwang025/deeptfus`
- commit：`b78bcc65a3634dd89401366169f8a494c7e2bf39`
- 本地路径：`C:\Users\HOU\Desktop\tus-array-surrogate\external\deeptfus`

数据来源：

- 数据模式：已有 subset，不下载 full dataset
- 数据路径：`external/deeptfus/external/hf_cache/datasets--vinkle-srivastav--TFUScapes/...`
- 样本数量：`train: 4 files`，`val: 2 files`，`test: 2 files`

checkpoint 来源：

- Hugging Face repo：`masonwang025/deeptfus-base`
- 下载路径：`external/deeptfus/runs/deeptfus_base_hf/`
- 文件：
  - `ckpt_best.pt`：20,743,755 bytes
  - `config.snapshot.yaml`：6,695 bytes
  - `README.md`：2,919 bytes
- 下载时未使用 Hugging Face token；下载成功，但出现 unauthenticated request warning。

checkpoint 内容检查：

```text
top_keys: ['config', 'epoch', 'global_step', 'model', 'optim', 'val']
model_state_keys: 139
data.resolution: 256
data.n_transducer_points: 512
train.precision: pure-bf16
train.epochs: 50
train.batch_size: 4
output.run_dir: runs/deeptfus
model.base_width: 16
model.cond_dim: 128
model.cross_attention_levels: ['level1', 'level2', 'level3', 'bottleneck']
epoch: 43
global_step: 18568
```

命令：

```powershell
git -C external/deeptfus remote -v
git -C external/deeptfus rev-parse HEAD
git -C external/deeptfus status --short

& 'D:\anaconda\envs\deeptfus-py311\python.exe' -m data.splits
& 'D:\anaconda\envs\deeptfus-py311\python.exe' -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.version.cuda)"

@'
from pathlib import Path
from huggingface_hub import snapshot_download
repo_id = 'masonwang025/deeptfus-base'
target = Path('runs/deeptfus_base_hf')
target.mkdir(parents=True, exist_ok=True)
snapshot_download(
    repo_id=repo_id,
    repo_type='model',
    local_dir=str(target),
    allow_patterns=['ckpt_best.pt', 'config.snapshot.yaml', 'README.md'],
)
'@ | & 'D:\anaconda\envs\deeptfus-py311\python.exe' -

$env:PYTHONUTF8='1'
& 'D:\anaconda\envs\deeptfus-py311\python.exe' eval.py `
  --checkpoint runs/deeptfus_base_hf/ckpt_best.pt `
  --split test `
  --device cpu `
  --output-dir runs/deeptfus_base_hf/eval_test_subset_cpu_nopred `
  --no-save-predictions
```

结果：

- 是否成功：未完成 eval，属于可解释阻塞。
- 已完成：
  - base checkpoint 下载成功；
  - checkpoint 可被 `torch.load(..., map_location='cpu')` 读取；
  - checkpoint 内 config 与预期一致，为 `256^3`、512 个 transducer points、`pure-bf16`。
- 未完成：
  - `eval.py` 未进入完整 test subset 评估；
  - 未生成 `metrics.json`；
  - 未生成 `per_sample.csv`；
  - 未保存 prediction `.npz`。
- 产物路径：
  - `external/deeptfus/runs/deeptfus_base_hf/ckpt_best.pt`
  - `external/deeptfus/runs/deeptfus_base_hf/config.snapshot.yaml`
  - `external/deeptfus/runs/deeptfus_base_hf/README.md`
  - `external/deeptfus/runs/deeptfus_base_hf/eval_test_subset_cpu_nopred/`，目录已创建但无评估产物。

报错 / 异常：

`eval.py` 在 warm-up forward 中失败：

```text
NotImplementedError: "avg_pool3d_out_frame" not implemented for 'BFloat16'
```

报错位置：

```text
eval.py -> evaluate() -> _time_inference()
models/deeptfus.py forward()
self.pool(x1)
torch.nn.functional.avg_pool3d
```

判断：

阶段 C 的 checkpoint 下载和只读检查已经完成，但当前 CPU 版 PyTorch 无法运行该 checkpoint 的 `pure-bf16` 推理。该阻塞不说明 checkpoint 损坏，也不说明 DeepTFUS eval 代码错误；它说明当前 `deeptfus-py311` 环境不适合直接评估 `pure-bf16` 的正式 base checkpoint。

本轮按计划停止，没有安装 CUDA 版 PyTorch，没有改 `eval.py` 或模型代码，也没有尝试 full dataset / training / fine-tune。

下一步：

1. 若继续阶段 C，建议优先建立或修正 CUDA 版 PyTorch 环境，然后重新验证 `torch.cuda.is_available()`，再用同一 checkpoint 跑 `eval.py`。
2. 若暂时不动 GPU 环境，可以单独设计一个“只用于 CPU 验证的 fp32 checkpoint/eval 路径”，但这会偏离原始 checkpoint 的 `pure-bf16` 运行设置，应作为新一轮明确任务处理。
3. 若后续 GPU eval 成功，再考虑是否保存 subset predictions，并阅读 `metrics.json`、`per_sample.csv`。

需要人工确认：

1. 下一轮是否优先安装 CUDA 版 PyTorch 到 `deeptfus-py311`，还是新建一个单独 GPU 环境，避免破坏当前 CPU smoke-test 环境。
2. 是否允许下一轮为了 CPU-only 验证临时转换模型到 fp32，还是严格坚持 checkpoint 原始 `pure-bf16` 配置。

## 2026-07-04：建立 GPU 环境并跑通阶段 C subset eval

目的：

解决上一轮 CPU 版 PyTorch 无法运行 `pure-bf16` checkpoint 的问题；建立独立 GPU 环境，并用 base checkpoint 在已有 test subset 上完成 `eval.py`。

环境：

- OS：Microsoft Windows 11 家庭版 中文版 10.0.26200
- GPU：NVIDIA GeForce RTX 5060 Laptop GPU，8151 MiB，driver 591.86
- Python：3.11.15
- CUDA / PyTorch：PyTorch `2.11.0+cu128`，`torch.cuda.is_available() = True`，`torch.version.cuda = 12.8`
- Conda / venv：Conda env `deeptfus-gpu-py311`，路径 `D:\anaconda\envs\deeptfus-gpu-py311`
- 备注：保留原 CPU 环境 `deeptfus-py311`，本轮没有覆盖它。

代码来源：

- 仓库：`https://github.com/masonwang025/deeptfus`
- commit：`b78bcc65a3634dd89401366169f8a494c7e2bf39`
- 本地路径：`C:\Users\HOU\Desktop\tus-array-surrogate\external\deeptfus`

数据来源：

- 数据模式：已有 subset，不下载 full dataset
- 数据路径：`external/deeptfus/external/hf_cache/datasets--vinkle-srivastav--TFUScapes/...`
- 样本数量：`train: 4 files`，`val: 2 files`，`test: 2 files`

checkpoint 来源：

- Hugging Face repo：`masonwang025/deeptfus-base`
- 本地路径：`external/deeptfus/runs/deeptfus_base_hf/ckpt_best.pt`
- checkpoint 配置：`resolution=256`，`n_transducer_points=512`，`precision=pure-bf16`

命令：

```powershell
conda create -y -n deeptfus-gpu-py311 python=3.11

& 'D:\anaconda\envs\deeptfus-gpu-py311\python.exe' -m pip install torch --index-url https://download.pytorch.org/whl/cu128
& 'D:\anaconda\envs\deeptfus-gpu-py311\python.exe' -m pip install -r requirements.txt

@'
import torch
print('torch', torch.__version__)
print('cuda_available', torch.cuda.is_available())
print('torch_cuda_version', torch.version.cuda)
print('device_count', torch.cuda.device_count())
if torch.cuda.is_available():
    print('device_name', torch.cuda.get_device_name(0))
    print('capability', torch.cuda.get_device_capability(0))
    props = torch.cuda.get_device_properties(0)
    print('total_memory_mib', props.total_memory // 1024 // 1024)
    x = torch.randn(1, 1, 8, 8, 8, device='cuda', dtype=torch.bfloat16)
    y = torch.nn.functional.avg_pool3d(x, kernel_size=2)
    print('bf16_avg_pool3d_ok', y.shape, y.dtype, y.device)
'@ | & 'D:\anaconda\envs\deeptfus-gpu-py311\python.exe' -

$env:PYTHONUTF8='1'
& 'D:\anaconda\envs\deeptfus-gpu-py311\python.exe' eval.py `
  --checkpoint runs/deeptfus_base_hf/ckpt_best.pt `
  --split test `
  --device cuda `
  --output-dir runs/deeptfus_base_hf/eval_test_subset_cuda_nopred `
  --no-save-predictions

$env:PYTHONUTF8='1'
& 'D:\anaconda\envs\deeptfus-gpu-py311\python.exe' eval.py `
  --checkpoint runs/deeptfus_base_hf/ckpt_best.pt `
  --split test `
  --device cuda `
  --output-dir runs/deeptfus_base_hf/eval_test_subset_cuda_withpred
```

验证输出：

```text
torch 2.11.0+cu128
cuda_available True
torch_cuda_version 12.8
device_count 1
device_name NVIDIA GeForce RTX 5060 Laptop GPU
capability (12, 0)
total_memory_mib 8150
bf16_avg_pool3d_ok torch.Size([1, 1, 4, 4, 4]) torch.bfloat16 cuda:0
```

结果：

- 是否成功：成功。base checkpoint 在 CUDA 环境下完成 2 个 test subset 样本评估。
- no-pred eval：
  - 输出目录：`external/deeptfus/runs/deeptfus_base_hf/eval_test_subset_cuda_nopred/`
  - 生成 `metrics.json`、`per_sample.csv`、`per_voxel_mse.npy`
- with-pred eval：
  - 输出目录：`external/deeptfus/runs/deeptfus_base_hf/eval_test_subset_cuda_withpred/`
  - 生成 `metrics.json`、`per_sample.csv`、`per_voxel_mse.npy`、`predictions/*.npz`

指标摘要（with-pred eval，n=2）：

```text
relative_l2 mean = 0.382666
focal_position_error_mm mean = 4.637771
max_pressure_error mean = 0.301195
focal_iou_fwhm mean = 0.096924
focal_dice mean = 0.168889
off_target_volume_mm3 mean = 9.875000
inference_latency_s mean = 8.694013
```

单样本摘要：

```text
A00033747_exp_0:
  relative_l2 = 0.372515
  focal_position_error_mm = 3.937004
  max_pressure_error = 0.304012
  focal_iou_fwhm = 0.088929
  prediction npz = 94,030,136 bytes

A00033747_exp_1:
  relative_l2 = 0.392818
  focal_position_error_mm = 5.338539
  max_pressure_error = 0.298377
  focal_iou_fwhm = 0.104919
  prediction npz = 102,682,812 bytes
```

产物路径：

```text
external/deeptfus/runs/deeptfus_base_hf/eval_test_subset_cuda_nopred/metrics.json
external/deeptfus/runs/deeptfus_base_hf/eval_test_subset_cuda_nopred/per_sample.csv
external/deeptfus/runs/deeptfus_base_hf/eval_test_subset_cuda_nopred/per_voxel_mse.npy
external/deeptfus/runs/deeptfus_base_hf/eval_test_subset_cuda_withpred/metrics.json
external/deeptfus/runs/deeptfus_base_hf/eval_test_subset_cuda_withpred/per_sample.csv
external/deeptfus/runs/deeptfus_base_hf/eval_test_subset_cuda_withpred/per_voxel_mse.npy
external/deeptfus/runs/deeptfus_base_hf/eval_test_subset_cuda_withpred/predictions/A00033747_exp_0.npz
external/deeptfus/runs/deeptfus_base_hf/eval_test_subset_cuda_withpred/predictions/A00033747_exp_1.npz
```

报错 / 异常：

1. `conda 4.5.11` 仍较旧；本轮继续使用环境 Python 绝对路径，未使用 `conda run`。
2. CUDA 版 PyTorch wheel 较大，下载的 `torch-2.11.0+cu128` wheel 约 2.8 GB。
3. 本机 8GB 显存可以跑 `batch=1` 的 subset eval，但本轮不证明 full training、full test set 保存 predictions 或 batch size 更大时可行。

判断：

阶段 C 的核心目标已经完成：非官方 base checkpoint 可以在本机 CUDA 环境下加载、推理并输出指标文件。上一轮 CPU 阻塞来自 CPU 对 `BFloat16 avg_pool3d` 的算子支持不足；使用 CUDA 版 PyTorch 后该问题消失。

这些指标只来自 2 个 subset test 样本，不能当作论文级 test-set 结论。它们可以证明评估链路可用，但不应过度解释模型泛化效果。

下一步：

1. 阅读 `metrics.json`、`per_sample.csv` 和 prediction `.npz` 的字段，解释各指标含义和 normalized/log space 边界。
2. 可视化 2 个 prediction 与 target 的切片或最大投影，直观看差异。
3. 若要评估论文级 test-set，需要下载更多 test 数据；这会涉及 full/subset 数据规模和磁盘策略。
4. 若进入阶段 D，只做低分辨率 / subset 小训练，不做 full training。

需要人工确认：

1. 是否进入“阶段 C 结果阅读与可视化”，先看这 2 个样本的预测场和 ground truth 差异。
2. 是否保持两个环境并行：`deeptfus-py311` 用于 CPU smoke test，`deeptfus-gpu-py311` 用于 checkpoint eval / 后续 GPU 小实验。

## 2026-07-04：阶段 D 低分辨率从零短训练跑通

目的：

验证非官方 DeepTFUS 复现仓库的训练入口 `train.py` 能否在本机 GPU 上完成低分辨率从零训练，并记录显存、耗时、loss、checkpoint 和后验 eval 链路。该实验不追求论文级效果，不做 full training，不下载 full dataset，不改模型代码。

环境：

- OS：Microsoft Windows 11 家庭版 中文版 10.0.26200
- GPU：NVIDIA GeForce RTX 5060 Laptop GPU，8151 MiB，driver 591.86
- Python：3.11.15
- CUDA / PyTorch：PyTorch `2.11.0+cu128`，`torch.cuda.is_available() = True`，`torch.version.cuda = 12.8`
- Conda / venv：Conda env `deeptfus-gpu-py311`，路径 `D:\anaconda\envs\deeptfus-gpu-py311`

代码来源：

- 仓库：`https://github.com/masonwang025/deeptfus`
- commit：`b78bcc65a3634dd89401366169f8a494c7e2bf39`
- 本地路径：`C:\Users\HOU\Desktop\tus-array-surrogate\external\deeptfus`

数据来源：

- 数据模式：已有 subset，不下载 full dataset
- 数据路径：`external/deeptfus/external/hf_cache/datasets--vinkle-srivastav--TFUScapes/...`
- 样本数量：`train: 4 files`，`val: 2 files`，`test: 2 files`

训练配置：

```text
data.resolution = 64
data.n_transducer_points = 128
model.base_width = 8
model.cond_dim = 32
model.n_transducer_freqs = 4
model.cross_attention_heads = 2
model.cross_attention_levels = [bottleneck]
train.epochs = 2
train.batch_size = 1
train.num_workers = 0
train.precision = fp32
train.grad_checkpoint_encoder = false
train.channels_last = false
train.compile = false
train.wandb_project = null
output.run_dir = runs/deeptfus_stage_d_lowres_scratch
```

命令：

```powershell
& 'D:\anaconda\envs\deeptfus-gpu-py311\python.exe' -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.version.cuda)"
& 'D:\anaconda\envs\deeptfus-gpu-py311\python.exe' -m data.splits
nvidia-smi

$env:PYTHONUTF8='1'
$env:WANDB_MODE='disabled'
& 'D:\anaconda\envs\deeptfus-gpu-py311\python.exe' train.py `
  --config configs/base.yaml `
  --overrides `
  data.resolution=64 `
  data.n_transducer_points=128 `
  model.base_width=8 `
  model.cond_dim=32 `
  model.n_transducer_freqs=4 `
  model.cross_attention_heads=2 `
  "model.cross_attention_levels=[bottleneck]" `
  train.epochs=2 `
  train.batch_size=1 `
  train.num_workers=0 `
  train.precision=fp32 `
  train.grad_checkpoint_encoder=false `
  train.channels_last=false `
  train.compile=false `
  train.wandb_project=null `
  output.run_dir=runs/deeptfus_stage_d_lowres_scratch

$env:PYTHONUTF8='1'
& 'D:\anaconda\envs\deeptfus-gpu-py311\python.exe' eval.py `
  --checkpoint runs/deeptfus_stage_d_lowres_scratch/ckpt_best.pt `
  --split test `
  --device cuda `
  --output-dir runs/deeptfus_stage_d_lowres_scratch/eval_test_subset_nopred `
  --no-save-predictions
```

训练结果：

- 是否成功：成功。`train.py` 跑完 2 epoch。
- 模型参数量：`613,137`
- 总训练 step：8
- 训练耗时：约 5.0 s
- checkpoint：
  - `ckpt_last.pt`：7,489,355 bytes
  - `ckpt_best.pt`：7,489,355 bytes
- summary：

```json
{
  "best_val_rel_l2": 0.8336784036688516,
  "epochs_trained": 2,
  "n_train": 4,
  "n_val": 2,
  "n_params": 613137,
  "precision": "fp32",
  "grad_checkpoint_encoder": false,
  "wall_s": 4.9987969398498535,
  "resumed_from": null
}
```

训练 epoch 日志：

```text
epoch 0:
  train_total = 0.004911
  weighted_mse = 0.003455
  gradient_l1 = 0.014555
  grad_norm = 0.060083
  val_rel_l2_mean = 0.883704
  val_focal_mm_mean = 23.5350
  val_max_p_mean = 0.9421
  val_total = 0.005299
  wall_s = 2.6

epoch 1:
  train_total = 0.004097
  weighted_mse = 0.002645
  gradient_l1 = 0.014520
  grad_norm = 0.066487
  val_rel_l2_mean = 0.833678
  val_focal_mm_mean = 36.7527
  val_max_p_mean = 0.8639
  val_total = 0.004770
  wall_s = 4.9
```

step 日志摘要：

```text
gpu_mem_GiB:
  first step = 0.206
  later steps = 0.222
step_wall_s:
  first step = 0.4567
  later steps about 0.023 s
grad_norm range:
  0.052550 - 0.077866
```

后验 eval 结果：

- 是否成功：成功。训练出的 `ckpt_best.pt` 可被 `eval.py` 读取并完成 test subset eval。
- 输出目录：`external/deeptfus/runs/deeptfus_stage_d_lowres_scratch/eval_test_subset_nopred/`
- 样本数：2
- 未保存 prediction `.npz`

指标摘要：

```text
relative_l2 mean = 0.726697
focal_position_error_mm mean = 34.005764
max_pressure_error mean = 0.857508
focal_iou_fwhm mean = 0.001334
focal_dice mean = 0.000000
inference_latency_s mean = 0.007030
```

产物路径：

```text
external/deeptfus/runs/deeptfus_stage_d_lowres_scratch/ckpt_best.pt
external/deeptfus/runs/deeptfus_stage_d_lowres_scratch/ckpt_last.pt
external/deeptfus/runs/deeptfus_stage_d_lowres_scratch/config.snapshot.yaml
external/deeptfus/runs/deeptfus_stage_d_lowres_scratch/summary.json
external/deeptfus/runs/deeptfus_stage_d_lowres_scratch/train_log.csv
external/deeptfus/runs/deeptfus_stage_d_lowres_scratch/train_step_log.csv
external/deeptfus/runs/deeptfus_stage_d_lowres_scratch/eval_test_subset_nopred/metrics.json
external/deeptfus/runs/deeptfus_stage_d_lowres_scratch/eval_test_subset_nopred/per_sample.csv
external/deeptfus/runs/deeptfus_stage_d_lowres_scratch/eval_test_subset_nopred/per_voxel_mse.npy
```

报错 / 异常：

1. PyTorch 输出 warning：

```text
UserWarning: expandable_segments not supported on this platform
```

该 warning 来自 `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` 在当前 Windows / CUDA 平台不支持。训练仍成功完成，本轮未修改代码。

2. 本轮训练配置极小，峰值显存约 `0.222 GiB`，不能外推到正式 `256^3`、`batch_size=4` 或 full training。

判断：

阶段 D 的低分辨率从零短训练目标已经完成。当前已证明：在本机 8GB GPU 和 `deeptfus-gpu-py311` 环境下，DeepTFUS 的 `train.py` 可以完成低分辨率 3D 数据读取、forward、loss、backward、optimizer step、validation、checkpoint 保存、CSV 日志和后验 eval。

本轮训练结果只说明训练链路可用，不说明模型学得好，也不能作为论文级性能复现。`64^3`、4 个 train 样本、2 epoch 的结果主要用于工程验证。

下一步：

1. 可进入“阶段 D 结果解释”：逐行解释 `train_log.csv`、`train_step_log.csv`、`summary.json` 的含义。
2. 可做一个稍高分辨率显存探针，例如 `96^3` 或 `128^3`、1 epoch、batch size 1，专门测显存与时间；但不要直接尝试 `256^3 batch=4`。
3. 可进入阶段 E：总结 DeepTFUS 训练链路中哪些可迁移到本项目，哪些必须重做。

需要人工确认：

1. 是否继续做分辨率/显存探针（`96^3` 或 `128^3`），还是停止 DeepTFUS 训练复现，转向阶段 E 迁移判断。
2. 是否需要把阶段 D 的关键训练日志整理进 `docs/deeptfus_code_notes.md`，作为长期代码笔记。

## 2026-07-04：复现阶段 A-D 收束与人工确认

目的：

对 DeepTFUS 论文和非官方复现仓库的本轮复现进行阶段性收束，明确后续不再继续做本机显存探针或 full training，而是转入本项目迁移判断。

已完成：

1. 阶段 A：非官方仓库 `masonwang025/deeptfus` 部署成功，`scripts/local_verify.py` 跑通。
2. 阶段 C：`masonwang025/deeptfus-base` checkpoint 下载成功，并在 CUDA 环境下完成 2 个 test subset 样本 eval。
3. 阶段 D：`64^3`、tiny model、batch size 1、fp32 从零短训练跑通，生成 checkpoint、CSV log、summary 和后验 eval。

本机验证边界：

1. 本机只验证了工程链路和 subset 推理，不验证论文级准确率。
2. 阶段 C 的 subset eval 只有 2 个 test 样本，不能代表完整 test set。
3. 阶段 D 的低分辨率短训练只有 4 个 train 样本、2 epoch，不能说明模型学得好。
4. 本机 RTX 5060 Laptop 8GB 适合 smoke test、小规模验证和迁移判断，不适合 DeepTFUS 正式 `256^3 batch=4` full training。

非官方模型自证信息：

非官方 checkpoint README 报告 base reproduction 在 `n=597` held-out CT × placement combinations 上的结果：

```text
relative_l2:
  paper = 0.414 ± 0.086
  base reproduction = 0.384 ± 0.078

focal_position_error_mm:
  paper = 2.89 ± 2.14
  base reproduction = 6.49 ± 4.58

max_pressure_error:
  paper = 0.199 ± 0.158
  base reproduction = 0.225 ± 0.116
```

判断：该非官方复现属于部分复现；`relative_l2` 接近论文，焦点位置误差明显差于论文。该信息来自 `external/deeptfus/runs/deeptfus_base_hf/README.md` 和非官方仓库 README / 项目页。

人工确认：

1. 停止 DeepTFUS 复现探针，不继续做 `96^3` / `128^3` 显存探针。
2. 不在当前笔记本上尝试 DeepTFUS full training。
3. 后续转入阶段 E：DeepTFUS 到本项目的迁移判断。
4. 本项目第一版先做低分辨率大区域输出，不是严格 whole-brain，而是约取上半 / 一半区域。
5. 第一阶段固定频率、阵元尺寸和幅值，优先研究阵元位置 / 法向变化。
6. pmax 输出必须保留绝对声压标定；normalized pmax 只能作为辅助或对照。

下一步：

围绕本项目路线整理 DeepTFUS 的可迁移点和不可迁移点，并优先设计低分辨率大区域 pmax baseline 与单阵元大区域复声场候选路线。
