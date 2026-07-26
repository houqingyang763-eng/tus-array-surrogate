# Jang 2025 论文组后续进展与公开资源

核查日期：2026-07-22

目标论文：Minyeong Jang et al., *Deep learning-based real-time estimation of transcranial focused ultrasound acoustic field* (2025)

## 1. 目标论文本身

- 论文 DOI：https://doi.org/10.1016/j.engappai.2025.111157
- 高丽大学论文页：https://pure.korea.ac.kr/en/publications/deep-learning-based-real-time-estimation-of-transcranial-focused-/
- 公开代码：截至核查日未找到与该论文直接对应的 ADNet、PPNet 或 FDTD 官方仓库。
- 数据：论文仅声明 `Data will be made available on request`，未给公开下载地址。
- 通讯作者：Kyungho Yoon（yoonkh@yonsei.ac.kr）；Gunwoo Noh（gunwoonoh@korea.ac.kr）。

检索范围包括论文完整标题、DOI、`ADNet`/`PPNet` 名称、作者公开 GitHub 账号和 CMME Lab GitHub 组织。下面的仓库均为同一合作网络的相邻或后续成果，不是目标论文原代码。

## 2. 后续公开成果：优先查看

### Acoustic Simulation with Deep Learning for Low-Intensity Transcranial Focused Ultrasound Digital Twins

- 论文 DOI：https://doi.org/10.1007/978-3-032-07694-6_6
- 官方论文信息：https://yonsei.elsevierpure.com/en/publications/acoustic-simulation-withdeep-learning-forlow-intensity-transcrani/
- 官方代码（MIT）：https://github.com/CMME-Lab/LIFUSimul-DL
- 预训练权重：https://drive.google.com/drive/folders/1IT0JOh9819Eo5B5ovuIkgjQV6c1pTUvJ?usp=drive_link

与本项目的关系：输入自由场、颅骨 CT/MR 和换能器位置，输出三维颅内声场；代码包含 3D AE/U-Net/Swin、训练、测试和 HDF5 数据加载，默认体数据为 `112×112×112`。适合学习三维多模态输入与位置条件化。

边界：原始数据因隐私不公开，仓库未包含声场仿真生成器；默认输出是单通道、Sigmoid 归一化场，不是绝对 `Re/Im` 复声场，不能直接支持本项目的阵元复场相干叠加。

## 3. 同实验室新方向：仅作观察

### Deep Learning Based Real-Time Phase-Amplitude Correction for Phased Array Transducers

- 代码：https://github.com/CMME-Lab/tFUS-PhaseAmplitudeCorrection
- 权重与单个示例数据：https://drive.google.com/drive/folders/1Hw5GOtM4PqualxSg2lXmMF2VakDnGVZf?usp=sharing

状态：仓库写明 `Manuscript in preparation`，尚不是可核验的正式论文；仓库未声明许可证。提供训练、微调、推理代码，以及固定 1024 阵元的相位和幅值模型。

与本项目的关系：直接涉及阵元相位/幅值，但目标是固定大阵列的校正量，不是“单阵元绝对三维复声场 + 网络外相干叠加”，也不能据此证明可变阵元数量或可变阵列形状的泛化。

## 4. 前序可学习资源：不是后续成果

### tFUSFormer (2024)

- 论文 DOI：https://doi.org/10.1109/JBHI.2024.3389708
- 原始代码：https://github.com/iangilan/tFUSFormer
- CMME Lab 镜像：https://github.com/CMME-Lab/tFUSFormer
- Zenodo 数据：https://doi.org/10.5281/zenodo.10791265
- 预训练权重：https://drive.google.com/drive/folders/1jtnmlbGqD_9zAyIBLx4SNvGik_OzvVsk

用途：学习 3D 超分辨率网络、数据加载、损失和评估。公开数据不含 CT，方法仍需要低分辨率仿真作为输入；不是从颅骨和阵元几何直接预测绝对复声场。仓库未声明许可证。

## 5. 研究组入口

- CMME Lab GitHub：https://github.com/CMME-Lab
- Kyungho Yoon 实验室：https://sites.google.com/view/yoonlabyonsei/
- Gunwoo Noh 高丽大学主页：https://pure.korea.ac.kr/en/persons/gunwoo-noh/

## 当前建议

1. 学习/静态审计优先级：`LIFUSimul-DL` > `tFUSFormer` > `tFUS-PhaseAmplitudeCorrection`。
2. 不把 `LIFUSimul-DL` 当作 Jang 2025 的原始复现代码。
3. 若要复现 Jang 2025，应先向通讯作者索取：训练数据、FDTD 数据生成代码、ADNet/PPNet 实现、预训练权重及数据划分清单。
