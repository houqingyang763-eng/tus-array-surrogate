# 有限传播更新与真实残差校正

- **判断：继续有限学习状态更新；真实Helmholtz校正先定向补算子、边界与尺度证据。**
- **依据：**LBS/NSNO/OpenWaves在网络内组织传播和局部散射，适合作少量更新。McMg/Helmnet/Xiang是数值求解路径，总迭代与残差容差不能当直接shape预测成本/精度。
- **缺口：**ROI不含外部源、Label算子与可用差分算子的一致性、单位形状场的源尺度。
- **下一步：**M0只使用latent差异；真实残差路线先过边界及Label残差门，再决定是否值得两三步纠正。

入口：[论文](papers/README.md)｜[设计](DESIGN.md)｜[验证](VALIDATION.md)。不修改现有Label、Helmholtz或runner；以下是备选设计。
