# 理论关：位移 GreenONet 能否过渡到固定频率复声压

结论：在本项目当前的线性、标量、流体声学设置下可以过渡。过渡的是 Green 算子表示，不是原论文的网络结构或精度结论。

## 从实数时间信号到复声压

线性声压满足抽象方程：

```text
L p(x,t) = s(x,t)
```

`p` 是随时间变化的实声压，单位 Pa；`s` 是声源。固定角频率 `ω=2πf` 时，可以把稳态声压写成：

```text
p(x,t) = Re{P(x,ω) exp(-iωt)}
```

`P` 是复声压。它的模表示幅值，辐角表示相位；它不是另一种声压，而是同一个实数正弦信号的紧凑表示。代回时间方程得到频域算子：

```text
Lω P(x,ω) = S(x,ω)
```

定义满足 `Lω Gω(x,ξ) = δ(x-ξ)` 的频域 Green 核后：

```text
P(x,ω) = ∫ Gω(x,ξ) S(ξ,ω) dξ
```

因此原 GreenONet 使用的波动变量是位移，不会从数学上阻止我们把同样的算子分解用于声压。

## 有限阵元不是点源

对表面为 `Ae` 的有限尺寸阵元，其表面各点的 Green 响应需要积分：

```text
Pe(x,ω) = ∫Ae Gω(x,ξ) qe(ξ,ω) dA
```

固定阵元直径、频率和驱动后，可以把整个积分定义为一个有效阵元响应：

```text
H(re,ne,x) = Pe(x,ω)
```

这就是本实验学习的对象。网络不声称自己输出严格点源 Green 函数。

线性条件下，多阵元仍可在复数域叠加：

```text
Parray(x) = Σe ae exp(iφe) H(re,ne,x)
```

## 成立和失效边界

- 当前 `kspaceFirstOrder3DG` 流体模型只包含压缩波，并且没有启用 `BonA` 非线性参数，因此线性 Green 表示成立。
- 线性吸收不会破坏表示，只会让固定频率算子和 Green 核变成带衰减、色散的复数形式。
- 固定 MIDA、频率、PML和边界时，介质可以隐含在网络权重里；改变这些条件相当于改变 Green 算子。
- 如果启用非线性传播，普通线性叠加失效。
- 如果改用流固耦合弹性颅骨，标量压力 Green 核必须扩展为压力、速度和应力耦合的矩阵算子。

关键来源：

- [原始 GreenONet](https://arxiv.org/abs/2307.13902)：给出初始位移函数到波场的时域 Green 算子表示。
- [k-Wave 一阶与二阶声学模型比较](https://www.k-wave.org/documentation/example_ivp_comparison_modelling_functions.php)：说明线性均匀声学的一阶压力/速度方程可合并为二阶波动方程并用 Green 方法求解。
- [k-Wave 非线性示例](https://www.k-wave.org/documentation/example_na_modelling_nonlinearity.php)：说明未设置 `medium.BonA` 时使用线性控制方程，输出随输入线性缩放。
