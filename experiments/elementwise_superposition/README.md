# 四阵元大区域复场叠加验证

## 最小验证问题

在线性、单频、完全相同的全局网格和源离散条件下，四份单阵元绝对复声压场
`P_n = Re[P_n] + i Im[P_n]` 经幅相加权后，能否重建同一四阵元配置的一次整体
k-Wave 仿真；若能，复用多少种驱动方案后响应库才可能节省时间。

本实验不实现局部窄传播域、局部旋转/插值、热仿真、surrogate 训练或随机生成
100 组驱动。McDannold 2019 只提供逐阵元响应库的方法依据；颅骨 STL、坐标变换、
介质参数和评价思路来自公开的 Aubry benchmark。

- McDannold: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8218657/>
- Aubry paper: <https://pmc.ncbi.nlm.nih.gov/articles/PMC9553291/>
- Aubry code/STL: <https://github.com/ucl-bug/transcranial-ultrasound-benchmarks>
- iso2mesh: <https://github.com/fangq/iso2mesh>

## 实现边界

- 正式求解只调用 `kspaceFirstOrder3DG`，不会静默切到 CPU。
- 物理域为 `200 × 160 × 160 mm³`，首轮 `dx = 1 mm`，PML 在域外 10 点。
- 大区域以 2 mm 采样；目标周围 `±20 mm` 另以 1 mm 采样。
- 四个直径 10 mm 的平面圆阵元按 2×2、12 mm pitch 放置，指向共同目标。
- 连续波 500 kHz、每阵元驱动峰值 100 kPa、4 周期渐入；直达传播后额外等待
  400 周期以衰减颅内长寿命相移启动瞬态，只记录最后 4 个整数周期。400 周期来自
  同一颅骨大域的 0°/90° 收敛测试（复场旋转 L2 为 `7.19e-6`）；不是随意加长。
- 结果保存为单精度 `Re[P]`、`Im[P]`，单位 Pa。k-Wave CUDA 包装器的时序 HDF5
  位于临时目录，并在每次调用结束时由包装器删除。
- benchmark 使用 V1 仿射变换后的内/外颅骨 STL；首轮把颅骨作为均匀皮质骨，
  脑内为 brain，颅外为 water。衰减参数取 Aubry Table I 并转换到 k-Wave 的
  `dB/(MHz^2 cm)`。

## 一次性依赖

```powershell
cd C:\Users\HOU\Desktop\tus-array-surrogate
powershell -ExecutionPolicy Bypass -File experiments\elementwise_superposition\setup_dependencies.ps1
```

默认还要求：

- MATLAB R2024a；
- `D:\k-wave\k-Wave`；
- `D:\k-wave\k-Wave\binaries\kspaceFirstOrder-CUDA.exe`；
- NVIDIA GPU/驱动可被该独立 CUDA 程序识别。

## 运行顺序

在仓库根目录启动 MATLAB：

```matlab
addpath('experiments/elementwise_superposition');

% 先做四次小水域 GPU 检查
smoke = run_elementwise_experiment('water_smoke');

% 再做 4 次单阵元 + 3 次整体的大区域颅骨实验
benchmark = run_elementwise_experiment('benchmark_skull');
```

可先只生成介质、网格和几何检查文件：

```matlab
run_elementwise_experiment('benchmark_skull', 'DryRun', true);
```

长任务中断后，用原目录恢复；已有场文件不会重算：

```matlab
run_elementwise_experiment('benchmark_skull', ...
    'RunDir', 'C:/Users/HOU/Desktop/tus-array-surrogate/runs/elementwise_superposition/benchmark_skull/20260715_XXXXXX');
```

若要强制重算，增加 `'Overwrite', true`。

诊断稳态启动瞬态时可显式增加等待周期，例如
`'ExtraSettlePeriods', 24`；正式默认值以通过水域相移测试的最小稳妥值为准。

## MIDA

MIDA 需要单独接受许可证并取得 voxel 标签体。复制
`config/mida_config.example.json` 为 `config/mida_config.json`，然后明确填写：

- 本地 `.mat`/`.nii`/`.nii.gz` 标签路径；
- 0.5 mm 原始体中的裁剪起点；
- 目标和四个阵元在裁剪后世界坐标中的位置；
- background/water、brain、soft tissue、cortical bone、trabecular bone 的标签 ID。

代码会拒绝未映射的标签，避免把未知组织静默当成脑或水。配置完成后运行：

```matlab
run_elementwise_experiment('mida');
```

## 产物

每个运行目录包含：

- `config.json`、`environment.json`、`geometry.json`；
- 四份 `element_N_field.mat` 单阵元 Re/Im 场；
- 三组整体场、叠加场、逐 case 指标 JSON；
- `comparison_metrics.csv`、`timing_summary.json`、`summary.json`；
- 中心/峰值切片差值图和三轴剖面图；
- 每次 GPU 调用的 console、准备/求解/后处理/保存时间、峰值显存（可解析时）和文件大小。

响应库盈亏平衡按实际 wrapper 时间计算：

```text
K_break_even = ceil(T_library / (T_monolithic - T_sum))
```

这里没有额外生成随机幅相数据；三组既定驱动已复用同一四场响应库。

## 验收标准

- 复场相对 L2 ≤ `1e-4`；
- 幅值相对 L2 ≤ `1e-4`；
- 参考峰值 −20 dB 以上区域相位 MAE ≤ `0.1°`；
- `P_target`、`P_peak` 相对误差 ≤ `0.1%`；
- 峰值位置为同一 2 mm 输出体素。

同一线性全局域理论上应近乎完全一致。若未通过，应先检查源离散、相位符号、
稳态周期、传感器线性索引恢复，再讨论物理假设。
