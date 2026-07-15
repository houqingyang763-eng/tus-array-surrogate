# Project Memory

本文件是项目跟进主入口。当前状态和近期关注放在最前；时间线按最新到最旧排列。实验细节、论文细节和旧版本通过链接追踪，避免重复消耗上下文。

## 当前状态摘要（2026-07-15）

1. 当前源构想是 `docs/project_concept_v4.md`。
2. 第一版固定 MIDA、频率、阵元尺寸和幅值，优先研究阵元位置 / 法向变化。
3. 第一版输出为低分辨率大区域绝对 pmax field，约覆盖上半 / 一半颅骨或脑区；具体裁剪边界仍待确定。
4. normalized pmax 只作为辅助表示、训练技巧或 DeepTFUS 对照，不能替代绝对声压。
5. 长期候选路线仍是单阵元大区域复声场预测 + 多阵元相干叠加，用于支持阵元数量和阵列形状变化。
6. DeepTFUS 复现阶段 A-D 已收束；当前只把它作为 3D pmax baseline 和工程参考。
7. 项目采用“稳定知识—任务合同—执行证据—人工验收”四层工作流。
8. R001 多 Agent 论文试点已停止；论文工作流改为“AI 预读并给短导览，用户自己精读”。

依据：

- 用户 2026-07-04 对第一版范围、固定变量、位置 / 法向和绝对声压的确认；
- 用户 2026-07-15 对四层工作流的批准，以及对多 Agent 论文试点的复盘和终止决定；
- `docs/decisions.md`、`docs/deeptfus_run_log.md`、`docs/deeptfus_code_notes.md`。

---

## 当前自主 Mission

- 当前没有活跃 mission。
- `R001` 状态：`stopped / workflow_replaced`。
- 入口：`docs/research_tasks.md`。
- 第一篇的新默认入口：`docs/agent_runs/R001/paper1_guide.md`。

---

## 近期关注

1. **大区域裁剪范围与第一版分辨率**
   需要确定坐标系、物理覆盖和 `128^3 / 160^3 / 200^3 / 非立方网格` 的最低可用方案。

2. **绝对声压 label 与评价链路**
   需要定义 label 缩放、loss、`P_target`、`P_peak`、`focus_error` 和 `side_lobe_ratio`。

3. **MIDA 固定 skull 下的位置 / 法向采样**
   需要判断多少位置 / 法向 label 才能支撑初步 surrogate，并设计避免几何泄漏的数据划分。

4. **单阵元复声场相干叠加最小实验**
   在扩大数据生成前，验证单源复场能否可靠叠加成多源场；不再在论文导读中重复解释已经确认的 pmax 结论。

---

## 时间线（最新在上）

### 2026-07-15：停止多 Agent 论文精读，改为短导览

- 第一篇试点完成后，用户确认多 Agent 耗时和 token 过高，结论增益不显著；
- 长报告存在重复、细碎和公式渲染问题；
- 后续默认只给一份论文导览：结构、最多 5 个关键审计问题、理论分块和阅读路线；
- 用户自己完成精读，Codex 在读后负责反问、讨论和记录；
- R001 停止，不启动第二、第三篇，也不生成 `taste_v0`。

### 2026-07-15：R001 改为单篇优先的多 Agent 精读

- 用户指定 FDE-UNet、3-D elastic Helmholtz operator、scattered wavefield neural operator 三篇论文；
- 明确反对多篇泛泛扫读，要求多个 Agent 对同一篇逐节精读并提取最有价值部分；
- 第一阶段只启动 `Finite difference-embedded UNet for solving transcranial ultrasound frequency-domain wavefield`；
- Zotero 本地 PDF 已定位，共 13 页。
- 状态：同日被后续用户复盘替代，作为历史试点保留。

### 2026-07-15：建立 Git 基线和个人自主科研工作流

- 创建首个 Git baseline commit `9db93af`；
- 修正临时文件忽略规则并移除完全重复的 Word 副本；
- 用户批准四层工作流；
- `research_tasks.md` 从废弃 task 文件改为自主研究任务合同；
- 移除长期未使用的两个项目 Skill；
- 曾建立三篇论文批注 + 第四篇盲测方案；该论文试点后于同日终止，四层项目工作流继续保留。

### 2026-07-04：DeepTFUS 复现收束，转入本项目迁移判断

- 非官方复现阶段 A-D 已跑通工程链路：本地验证、checkpoint subset eval、`64^3` 短训练、日志和后验 eval；
- 不继续 `96^3 / 128^3` 探针，也不在当前 8GB 笔记本上做 full training；
- 第一版从严格 whole-brain 收缩为低分辨率大区域输出；
- 固定 MIDA、频率、阵元尺寸和幅值，优先研究位置 / 法向；
- 确认 pmax 必须保留绝对声压标定。

详细证据：

- `docs/deeptfus_run_log.md`
- `docs/deeptfus_code_notes.md`
- `docs/decisions.md`

### 2026-07-02：路线与记忆入口调整

- DeepTFUS / TFUScapes 成为核心参考，但不能覆盖绝对声压、复声场和任意阵列几何；
- 舍弃窄长条传播通道 + 焦点小 ROI 作为主线；
- `memory.md` 成为项目状态主入口；
- 当时废弃了细粒度 `research_tasks.md`，该判断于 2026-07-15 被“少量自主 mission 合同”修正。

### 2026-07-01：形成 `400^3` 数据量估算基准

- 采用 `400×400×400`、`0.5 mm`、单通道作为物理覆盖和数据量候选基准；
- 该基准不等于第一版网络必须密集输入 / 输出 `400^3`；
- 估算结果见 `docs/output_data_size_24gb_estimate.md`。

### 2026-06-30：建立本地科研记忆 repo

- 建立 project concept、decisions、questions、ideas 和 task 文件；
- whole-brain / 大区域脑内声场需求取代 v1 中“不优先全脑”的判断；
- Zotero `波场深度学习` collection 被确定为项目论文主目录。

---

## 已舍弃 / 已降级路线

### 窄长条传播通道输入

状态：不再作为主线。

原因：不能充分覆盖大区域旁瓣和非目标高压风险。入射角、颅骨厚度和路径统计仍可作为大区域模型的候选物理先验。

### 焦点附近小 ROI 作为单阵元主要输出

状态：降级。

原因：当前单阵元候选路线需要面向大区域复声场，才能服务阵列组合和全局风险判断。

### 细粒度 task 系统

状态：已舍弃；2026-07-15 由少量用户批准的 Research Mission 合同替代。

### DeepTFUS full training 复现

状态：当前笔记本上停止。

原因：工程验证目的已经达到，正式 3D 训练超出当前 8GB GPU 的合理范围；后续精力转向本项目自己的数据、输出和路线验证。
