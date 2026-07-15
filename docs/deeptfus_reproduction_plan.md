# DeepTFUS 复现计划

本文件用于记录 DeepTFUS / TFUScapes 复现工作的路线、阶段目标和当前判断。它不是本项目的总任务系统；只服务于“先把已有 3D TUS surrogate 复现链路跑通，再判断如何迁移到本项目”的过程。

## 0. 当前定位

DeepTFUS 对本项目的作用是：

1. 学会 3D skull volume + transducer geometry -> 3D normalized pmax field 的完整代码链路；
2. 了解 TFUScapes 数据结构、训练显存压力、loss 设计和 evaluation 指标；
3. 为本项目后续的 MIDA skull、阵元几何、单阵元复声场响应和多阵元相干叠加提供对照基线。

当前不要把 DeepTFUS 直接当成本项目最终方案。它输出 normalized pmax，不输出绝对声压或复声场，也不直接支持多阵元数量变化、任意阵列形状变化和相干叠加。

## 1. 仓库和文件夹建议

建议在当前大项目文件夹下管理复现代码，但把外部代码、数据和运行产物隔离：

```text
tus-array-surrogate/
  docs/
    deeptfus_reproduction_plan.md
    deeptfus_run_log.md
    deeptfus_code_notes.md          # 可后续建立
    deeptfus_vs_ours.md             # 可后续建立
  external/
    deeptfus/                       # 非官方 DeepTFUS 复现仓库
    TFUScapes/                      # 官方数据/可视化仓库
  data/
    tfuscapes/                      # 数据或数据软链接，不进 git
  runs/
    deeptfus_smoke/
    deeptfus_eval/
```

`external/`、`data/`、`runs/`、checkpoint、large `.npz` 数据应加入 `.gitignore`。本 repo 只沉淀项目判断、代码阅读笔记、运行日志和必要的小脚本。

## 2. 信息源优先级

1. 官方论文：`A Skull-Adaptive Framework for AI-Based 3D Transcranial Focused Ultrasound Simulation`。
2. 官方仓库：`https://github.com/CAMMA-public/TFUScapes`。
3. 官方数据：`https://huggingface.co/datasets/vinkle-srivastav/TFUScapes`。
4. 非官方复现仓库：`https://github.com/masonwang025/deeptfus`。
5. 本项目文档：`docs/project_concept_v3.md`、`docs/decisions.md`、`docs/questions.md`、`docs/memory.md`。

注意：截至当前检查，官方 TFUScapes 仓库主要提供数据入口、sample 和可视化脚本，`Models` 仍为 `coming soon`。因此训练代码和 checkpoint 主要依赖非官方复现仓库。

## 3. 阶段路线

### 阶段 A：最小链路跑通

目标：确认环境、数据读取、模型前向/反向、checkpoint 和 evaluation harness 可以跑通。

建议动作：

1. 克隆非官方复现仓库到 `external/deeptfus/`。
2. 建立独立 Python 环境。
3. 安装 `requirements.txt`。
4. 先跑 `scripts/local_verify.py`，不要直接下载完整 200GB 数据。

通过标准：

1. 脚本完成数据小样本下载或找到缓存；
2. 模型能 forward / backward；
3. 能保存和读取 checkpoint；
4. 能输出 `metrics.json`、预测 `.npz` 或等价评估产物。

### 阶段 B：理解 TFUScapes 数据结构

目标：知道每个 `.npz` 文件到底包含什么，以及这些数组在训练中如何归一化。

重点确认：

```text
ct:        256^3 pseudo-CT volume
pmap:      256^3 pressure / pmax amplitude map
tr_coords: N x 3 transducer active surface coordinates
```

需要记录：

1. 数组 shape、dtype、数值范围；
2. `pmap` 是否为绝对 Pa、normalized field、还是 loader 中再归一化；
3. `tr_coords` 是 voxel index、物理坐标，还是归一化坐标；
4. 训练 loader 如何 resize、normalize、subsample transducer points。

### 阶段 C：评估预训练 checkpoint

目标：优先验证别人训练好的模型是否可用，而不是从零训练。

建议动作：

1. 下载非官方复现仓库提供的 checkpoint 和 config；
2. 使用 `eval.py` 跑 test 或小 subset；
3. 保存并阅读 `metrics.json`、`per_sample.csv`、预测 `.npz`。

通过标准：

1. 能加载 checkpoint；
2. 能输出 paper metrics：`relative_l2`、`focal_position_error_mm`、`max_pressure_error`；
3. 能看到预测场和 ground truth 的基本差异；
4. 能解释 normalized/log space 指标代表什么。

### 阶段 D：小规模训练

目标：确认训练代码可用，并理解显存、batch size、precision 和 resolution 的关系。

建议动作：

1. 用 subset 或低分辨率配置跑短训练；
2. 先记录每步显存、时间、loss；
3. 再考虑 `256^3`、batch size、bf16、gradient checkpointing。

注意：

非官方复现仓库 README 指向 H100/A100 80GB 路线。若本机是 24GB GPU，不建议一开始直接 full training。

### 阶段 E：面向本项目的迁移判断

目标：不是直接改成最终模型，而是判断哪些部分能偷，哪些必须重做。

重点问题：

1. DeepTFUS 的 transducer point encoding 能否改成阵元坐标、法向和 array mask？
2. 固定 MIDA skull 时，是否还需要跨 subject 的数据划分逻辑？
3. 输出从 normalized pmax 改成复声场 `Re/Im` 后，loss 和 evaluation 如何改？
4. 单阵元复声场 label 如何生成，能否线性叠加验证多阵元声场？
5. 如果只做 whole-brain low-resolution pmax baseline，最低可用分辨率是多少？

## 4. 当前不做

1. 不直接把 DeepTFUS 当成本项目最终方案；
2. 不一开始下载完整数据并跑 full training；
3. 不把官方 TFUScapes 仓库误认为已经公开完整模型训练代码；
4. 不在没有复场 label 的情况下声称可以做多阵元相干叠加；
5. 不把 `research_tasks.md` 重新变成细粒度任务系统。

## 5. 每次推进前的 Codex 提示模板

```text
请先读取：
1. docs/deeptfus_reproduction_plan.md
2. docs/deeptfus_run_log.md
3. docs/project_concept_v3.md
4. docs/decisions.md
5. docs/questions.md

本轮目标：
...

请只做：
...

不要做：
...

完成后请更新 docs/deeptfus_run_log.md，并总结风险点。
```

