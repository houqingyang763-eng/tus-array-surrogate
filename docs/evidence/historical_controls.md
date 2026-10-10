# 旧路线比较：只保留对本轮有用的线索

以下均是V9等历史材料，不能替代V10匹配对照或恢复旧科学合同。原结果多为PENDING_REVIEW；本次没有重算。完整本地路径在[SOURCE_MAP](../SOURCE_MAP.md)。

<a id="p0"></a>
## P0背景场

P4修复无P0在600 epoch的12个TRAIN-SEEN mean unit-shape L2 .508163；历史P0同epoch .368362。观察支持参考场有价值，但precision、硬件、初始化/runner不同；不是严格单因素P0因果幅度。V10基线已经含P0，本轮应研究如何利用，而非将再次加入P0称为新贡献。

<a id="gdl"></a>
## GDL

历史64 train参数比较保留工作建议lambda=.2、clip=1；共同窗口中提高lambda=.4未获益，clip变化没有稳定主L2优势。这不是跨seed最优参数；当前T512-V9BASE为纯Lshape且无clip，不能将旧配置自动接回V10。

<a id="ffl"></a>
## FFL

共同≤560 epoch：FFL最佳val L2 .671122（e560）、GDL .672185（e540），约.16%改善。FFL训练更长的全范围最佳值不作等预算收益。复杂纹理未按预期恢复，主频带内幅相组合仍是诊断线索。

<a id="helmholtz"></a>
## Helmholtz

V9 P5和历史T160按各自val-selected checkpoint：test64 mean unit-shape L2 .700375/.716016，相对改善2.18%；batch和训练设置存在差异，物理监督区域也不同。不能把这一结果当V10颅内算子已匹配；新真实校正先过边界/尺度/离散门。
