# 来源声明：历史自定义 Green 工程探索

```text
method_source: GreenONet / Green函数思想仅作为概念启发，不是网络复现
implementation_source: 本地临时自设计 PyTorch 实现
source_commit_or_release: N/A
reproduction_level: custom
changes_from_source: 网络、Fourier特征、复修正输出、解析教师、损失和训练流程均为项目自定义
claim_boundary: 只能评价该自定义实现和本机工程资源，不能评价 GreenONet、SIREN 或 Green 路线是否可学习
```

## 仍然有效的证据

- V1 显存和吞吐属于纯工程探针，可以说明当前笔记本运行该自定义坐标网络时的资源占用。
- `THEORY_GATE.md` 的线性声学与频域 Green 表示是有文献来源的数学 / 物理推导，但不证明任何神经网络实现有效。

## 必须降级的结论

- V2 不是 GreenONet、SIREN、Fourier Features 论文实现或任何公开波场方法的复现。
- V2 只能说明该自定义 `Fourier-SiLU` 基线及其600步训练方案未通过预设门槛。
- V2 不得用于 GreenONet 或 Green 项目路线的生死判断。
- V3 代码同样属于自定义方案，而且本轮没有运行。

后续正式验证必须先读取并补全同目录的 `SOURCE_EVIDENCE.md`，只从其中“可复现目标”选择有明确论文和代码来源的方法。
