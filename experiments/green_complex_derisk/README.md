# Green 复声场路线排雷实验

> **当前状态（2026-07-20）：实验冻结。** 先读 `ROUTE_DECISION.md`。本目录是历史自定义 `Fourier-SiLU` 工程探索，不是 GreenONet、SIREN 或其他论文方法的复现。除 V1 显存 / 吞吐外，结果不得用于 Green 路线生死判断。历史来源边界见 `PROVENANCE.md`；后续实验准入依据统一记录在 `SOURCE_EVIDENCE.md`。

下列执行命令只用于复核历史记录，不代表当前获准继续训练、重做 V2 或生成颅骨标签。重新运行科研实验必须先满足 `ROUTE_DECISION.md` 的解冻条件并获得用户批准。

本实验只判断冻结的坐标查询架构是否存在资源或表示层面的致命问题，不训练最终 surrogate，也不与 U-Net 比较。

## 冻结任务

```text
阵元中心 re + 阵元法向 ne + 查询点 x
-> 有限尺寸单阵元绝对复声压 [Re P, Im P]
```

固定 500 kHz、10 mm 阵元、100 kPa 驱动和同一介质。目标焦点不进入网络，多阵元在网络外以复数形式相干叠加。

网络先显式计算 `(100 mm/r) exp(ikr)`，再学习有限孔径和介质造成的无量纲复修正。模型结构、损失和两个解析实验随机种子在测试期间不调整。

## 执行

使用已安装 CUDA PyTorch 的环境：

```powershell
D:\anaconda\envs\deeptfus-gpu-py311\python.exe experiments\green_complex_derisk\run_derisk.py --stage all --time-budget-min 120
```

逐关运行：

```powershell
D:\anaconda\envs\deeptfus-gpu-py311\python.exe experiments\green_complex_derisk\run_derisk.py --stage probe
D:\anaconda\envs\deeptfus-gpu-py311\python.exe experiments\green_complex_derisk\run_derisk.py --stage analytic
```

`all` 会执行严格门控：V1 失败不运行 V2，V2 失败不生成颅骨标签。运行产物保存在 `runs/green_complex_derisk/<timestamp>/`。

## 边界

- V1 是坐标网络计算探针，不包含磁盘读取和 k-Wave 标签时间。
- V2 教师是32点有限圆盘 Green 核积分，验证复相位、距离衰减、孔径方向性及未见几何；不是颅骨仿真。
- V3 使用 Aubry V1 流体声学 benchmark skull，8个内部位置训练、4个外圈位置测试。它不是 MIDA，也不能给出正式泛化结论。
- 8阵元叠加只能采用4个训练位置与4个未见位置的混合集合，因为固定12标签中只有4个测试位置，结果会明确标注这一边界。
