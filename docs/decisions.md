# Decisions

本文件只记录已经相对稳定的项目共识，不记录聊天流水账。

新写入的稳定结论应尽量包含简短依据和边界 / 适用范围。依据可以来自用户明确确认、组内反馈、论文 / 网页、代码 / 数据、实验结果或项目文档。未经验证的想法不要写入本文件。

## 当前有效共识索引（2026-07-15）

1. 当前源构想为 `docs/project_concept_v4.md`。
2. 第一版固定 MIDA、频率、阵元尺寸和幅值，优先研究阵元位置 / 法向变化。
3. 第一版输出为低分辨率大区域绝对 pmax field；normalized pmax 只作辅助或对照。
4. 单阵元大区域复声场 + 多阵元相干叠加是长期核心候选，但必须先验证线性叠加误差和 label 成本。
5. 项目工作流采用“稳定知识—任务合同—执行证据—人工验收”四层结构。
6. `docs/research_tasks.md` 改为只容纳 1-3 个用户批准的自主研究 mission，不恢复细粒度 todo 系统。
7. 论文多 Agent 工作流采用主 Agent 汇总、子 Agent 独立取证与质疑；子 Agent 不直接写核心记忆。
8. 先用 3 篇有代表性的论文获取用户详细批注，再用第 4 篇盲测初版 research taste；三篇必须按单篇顺序推进，多个 Agent 同时精读同一篇，不并行扫读多篇。

依据：

- 用户 2026-07-15 明确批准四层工作流、多 Agent 论文互相质疑、三篇论文 taste 样本和自主研究任务合同试点。
- 用户 2026-07-15 明确确认两个旧项目 Skill 长期未用，可以移除。
- 用户 2026-07-15 明确提出多 Agent 应增加单篇论文的精读深度和互相质疑强度，而不是增加一次扫读的论文数量。
- 项目决策：2026-07-04 已确认第一版的大区域输出、固定条件、位置 / 法向变量与绝对声压要求。

边界 / 适用范围：

1. 自主 mission 必须有授权范围、证据标准、资源预算、停止条件和人工验收项。
2. 未经用户批准，不得把 Agent 的候选结论直接写入 `decisions.md` 或覆盖项目源构想。
3. 三篇论文只能形成初版 taste，必须通过未参与校准的论文检验。

---

## 历史决策记录

## 2026-06-30：建立 Codex 本地科研项目模板

结论：

1. 采用本地 repo / 项目文件夹作为 Codex app 的主要工作区。
2. 重要上下文不只放在聊天记录或 memory 中，而是沉淀到 Markdown 文件。
3. `AGENTS.md` 作为 Codex 的总规则。
4. `docs/project_concept_v2.md` 作为当前项目源构想。
5. `docs/decisions.md` 记录稳定共识。
6. `docs/questions.md` 记录待问、待查、待验证事项。

状态：

`docs/project_concept_v2.md` 已被 2026-07-02 的 `docs/project_concept_v3.md` 替代为当前源构想；v2 作为历史版本保留。

## 2026-06-30：whole-brain pmax field 成为主输出之一

结论：

1. v1 中“不优先做全脑输出”的判断已被组内新需求修正。
2. v2 将 whole-brain intracranial pmax field / 3D time-maximum pressure field 设为主输出之一。
3. 单阵元复声场预测 + 多阵元相干叠加路线仍保留，用于支持阵列 geometry variation。
4. 第一阶段建议采用“低分辨率全脑 pmax + 焦点 ROI 高分辨率复声场”的双层输出思路。

状态：

该结论中“whole-brain pmax field 成为主输出之一”仍然有效；“焦点 ROI 高分辨率复声场”已被 2026-07-02 的路线调整降级，不再作为当前主线输出设定。当前单阵元候选路线改为全脑 / 大区域复声场响应。

## 2026-06-30：采用简化科研记忆管理工作流

结论：

1. 日常科研输入先归档到 `docs/ideas.md`、`docs/questions.md`、`docs/research_tasks.md` 三类文件。
2. `docs/decisions.md` 只记录用户确认后的稳定共识，不作为日常笔记入口。
3. 用户输入自然语言科研笔记后，Codex 必须先提出分类和写入建议，反问确认后再修改文件。
4. 当前阶段暂不主动建立论文 summaries、实验记录和组会目录，除非用户明确要求。
5. 详细流程沉淀到 `docs/memory_workflow.md`，`AGENTS.md` 只保留项目级触发规则。

状态：

该工作流已被 2026-07-02 的 memory-first 工作流替代。`docs/research_tasks.md` 不再作为 Codex 主动维护的任务入口。

## 2026-06-30：Zotero 项目论文主目录

结论：

1. 本项目主要论文存储在 Zotero 的 `波场深度学习` collection 中。
2. 检索项目相关论文时，优先查看 `波场深度学习` 及其子 collection，例如 `第一类_贴近`。

## 2026-07-02：DeepTFUS / TFUScapes 作为本项目核心参考论文

结论：

1. `A Skull-Adaptive Framework for AI-Based 3D Transcranial Focused Ultrasound Simulation` / DeepTFUS / TFUScapes 应作为本项目核心参考论文之一。
2. 该论文直接证明了 `3D skull / pseudo-CT volume + transducer geometry -> 3D pmax / pressure amplitude field` 的经颅超声 surrogate 路线已有公开工作。
3. 该论文适合用于组会 PPT 中的“3D TUS surrogate 已有工作”“3D IO 设计”“训练数据生成成本”“当前方法缺口”部分。
4. 该论文不能直接作为本项目完整方案，因为它输出 normalized pmax field，不输出绝对声压或复声场；它也不支持多阵元数量变化、任意阵列形状变化或单阵元复声场相干叠加。
5. 该工作有公开 GitHub 仓库和数据入口；用户本轮确认已有复现案例，可作为后续查代码、查复现和做对比实验的重要入口。

依据：

- 论文：Srivastav et al., `A Skull-Adaptive Framework for AI-Based 3D Transcranial Focused Ultrasound Simulation`, arXiv:2505.12998, 2025。
- GitHub/代码：官方仓库 https://github.com/CAMMA-public/TFUScapes 公开 TFUScapes 数据下载入口、样例数据和 `visualize.py`；README 描述 DeepTFUS 从 3D CT volumes 和 transducer position 估计 normalized pressure fields。
- 用户明确确认：需要把 DeepTFUS 作为核心参考写入 decision，并强调其在 GitHub 上有开源代码且已有复现。
- 项目文档：`docs/project_concept_v2.md` 当前主线包括 whole-brain pmax field 和单阵元复声场叠加路线；DeepTFUS 直接对照前者，但不能覆盖后者。

边界/适用范围：

1. 截至本次检查，官方 GitHub README 的 `Models` 部分写为 `coming soon`；因此“开源代码”当前应谨慎理解为公开仓库、数据入口、样例和可视化脚本，完整模型训练代码是否已公开仍需继续核实。
2. “已有复现”来自用户本轮确认，后续应补充具体复现仓库、复现实验或复现报告链接。
3. 该论文可作为 3D pmax surrogate 的主线参考，但不能证明本项目的多阵元阵列、阵元数量变化、阵列形状变化和复声场相干叠加路线已经可行。

## 2026-07-02：科研记忆改为 memory-first，research_tasks 历史保留

结论：

1. `docs/memory.md` 成为项目科研跟进主入口，用于记录完整时间线、当前状态概要、近期 3-5 个关注方向和已舍弃 / 已降级路线。
2. `docs/research_tasks.md` 保留为历史文件，不再由 Codex 主动维护。
3. Codex 的职责是总结、判断、记录，帮助用户自己定任务；不应主动生成细粒度科研 task。
4. `docs/ideas.md`、`docs/questions.md`、`docs/decisions.md` 保留为精细分类文件，但不替代 `memory.md` 的长期时间线功能。

依据：

- 用户明确确认：`research_tasks.md` 功能重复且不符合需求，不需要 Codex 维护“做 PPT / 汇报”等细任务。
- 用户明确确认：需要类似 memory 的文件，作为概要、完整时间线、长流程记录。
- 项目文件：`docs/memory.md` 和 `docs/memory_workflow.md` 已按该结构更新。

边界/适用范围：

1. 如果用户明确要求整理任务，可以在当前对话中临时总结。
2. 只有用户明确要求写入任务文件时，才修改 `docs/research_tasks.md`。

## 2026-07-02：舍弃窄长条输入，保留单阵元大区域叠加候选路线

结论：

1. “长条形传播通道输入 + 焦点附近小 ROI 输出”不再作为当前主线问题。
2. 当前重点转向 whole-brain / `400^3` 级别大区域输入输出。
3. 单阵元复声场预测 + 多阵元相干叠加路线没有被放弃，但其候选形式应改为全脑 / 大区域响应预测。

依据：

- 用户明确确认：现在就做全脑的，而非长条形。
- 用户明确确认：仍然走单阵元叠加，但输入和输出都是全脑或 `400^3` 大区域。
- 项目文件：`docs/project_concept_v3.md` 已新建，记录该路线调整。

边界/适用范围：

1. 入射角、颅骨厚度、路径声速统计量等低维物理特征仍可作为大区域模型的候选先验。
2. 单阵元叠加仍需验证 label 成本、显存压力和线性叠加误差。

## 2026-07-04：DeepTFUS 复现暂告一段落，转入迁移判断

结论：

1. DeepTFUS 非官方复现阶段 A-D 已完成当前目的：验证代码、环境、checkpoint eval、低分辨率训练和日志链路可跑通。
2. 后续不继续做 `96^3` / `128^3` 显存探针，也不在当前笔记本上尝试 full training。
3. DeepTFUS 继续作为 3D pmax baseline、工程结构和方法参考，但不作为本项目最终模型方案。

依据：

- 用户明确确认：无需再做探针，停止复现，先做迁移判断。
- 运行记录：`docs/deeptfus_run_log.md` 记录阶段 A `local_verify.py` 跑通、阶段 C base checkpoint 在 CUDA 上完成 subset eval、阶段 D `64^3` 从零短训练跑通。
- 代码/README：非官方仓库 README 说明正式训练使用 single H100 80GB，base run 约 9 小时；本机 RTX 5060 Laptop 8GB 只适合 smoke test 和小实验。
- 计算推导：阶段 D `64^3` tiny model 实测峰值显存约 `0.222 GiB`；按体素数粗略外推，`300×200×300` 和 `400^3` 大区域训练已超出当前笔记本正式训练能力。

边界/适用范围：

1. 本结论不否认未来可在服务器或云 GPU 上做更完整复现；只是当前项目推进不再以复现 DeepTFUS 为主线。
2. 已下载的外部仓库、checkpoint、run log 和代码笔记保留，作为后续迁移判断和 baseline 对照材料。

## 2026-07-04：第一版固定物理参数，优先研究阵元位置和法向变化

结论：

1. 本项目第一版固定频率、阵元尺寸和幅值。
2. 第一版主要研究阵元位置和法向变化。
3. 当前输出范围从严格 whole-brain 修正为大区域，约取上半 / 一半颅骨或脑区覆盖；具体裁剪边界后续再定。
4. pmax 输出必须保留绝对声压标定；normalized pmax 只能作为辅助表示、训练技巧或与 DeepTFUS 对照。

依据：

- 用户明确确认：不是严格 whole-brain，而是大区域，差不多切一半。
- 用户明确确认：第一阶段固定频率、阵元尺寸、幅值，只研究位置 / 法向变化。
- 用户明确确认：pmax 必须保留绝对声压标定。
- 项目文档：`docs/project_concept_v3.md` 已把 pmax field、`P_target`、`P_peak`、`focus_error`、`side_lobe_ratio` 作为重要输出；DeepTFUS 代码笔记显示其 normalized / log pmax 不足以直接给出绝对声压。

边界/适用范围：

1. “大区域，差不多切一半”是稳定方向；具体裁剪尺寸、坐标系、是否非立方网格仍需后续确认。
2. 后续是否扩展频率、幅值、阵元尺寸为输入条件，留到第一版链路验证后再评估。
