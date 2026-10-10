# T512-V9BASE：最少必要基线证据

来源：本地V10 `v92v10/protocols/T512_V9BASE.md`与对应`results/T512-V9BASE/RESULTS.md`。只提炼既有记录，截至2026-10-08；未做新推理/实时查询。原结果科学解释状态为PENDING_REVIEW。

<a id="protocol"></a>
## 协议与接口

六级3D U-Net通道[8,16,32,64,128,128]，五次max-pool，跳接与反卷积；介质1通道、P0 Re/Im两通道、源XYZ。瓶颈坐标融合、粗FiLM、细Fourier/FiLM。纯Lshape=1−Re/Im联合cosine，Lgrad=0、Helmholtz关闭，FP16/GradScaler、AdamW wd0、无clip、checkpointing=false。固定512/32/64；val最佳选模型。

完整共同mask单位场误差L2=sqrt(2−2C)，C为Re/Im联合余弦。mean(L2²)/2=mean Lshape，不能用mean(L2)²替换。无raw或全局相位对齐。

<a id="results"></a>
## 已记录结果

| 对象 | 事实 |
|---|---|
| best checkpoint | e280/update28672；val32 mean L2=.46193813 |
| 同阶段train512 mean L2 | .34860901 |
| 局部图像 | 主要能量区和波前重现，幅值纹理/干涉/Re细节明显平滑 |
| ROI hook | 介质[1,1,352,352,192]，P0[1,2,352,352,192]，首层拼接3通道，head输出2通道；各层与ROI同步 |
| 有效mask | 5,101,889体素；不是整个ROI都作颅内评价 |
| test | 本资料包未收录该模型正式test数值 |

新版Fourier/FiLM重写在e180 val .521369，V9BASE .470479；两轮同时涉及条件结构/初始化、硬件和batch差异。它提示新版未按预期改善，不作为单独FiLM或Fourier组件的因果消融。

本文件是读者证据摘要，未发布checkpoint/图像全套/完整日志。数值的本地来源映射见[SOURCE_MAP](../SOURCE_MAP.md)。
