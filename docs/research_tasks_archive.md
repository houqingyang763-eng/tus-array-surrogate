# Research Tasks Archive

本文件记录旧任务系统的迁移摘要。完整原文保存在 Git 基线 commit `9db93af` 的 `docs/research_tasks.md` 中。

## 2026-07-15：旧 task 系统被自主研究任务合同替代

原因：

1. 旧 task 容易和 `ideas.md`、`questions.md` 重复；
2. 容易生成“做 PPT / 写汇报”等用户没有授权的细任务；
3. 无法表达 Codex 自主执行所需的权限、预算、停止条件和人工验收；
4. 用户明确批准改为少量 Research Mission 合同。

历史任务：

### 2026-07-01：基于 `400^3` 单通道输入估算数据量和显存

状态：阶段产出已形成。

保留产物：`docs/output_data_size_24gb_estimate.md`。

### 2026-07-02：整理 DeepTFUS 对 3D 阵列 surrogate 的借鉴边界

状态：已由后续复现、代码笔记和迁移判断覆盖。

保留产物：

- `docs/deeptfus_run_log.md`
- `docs/deeptfus_code_notes.md`
- `docs/decisions.md`

旧任务不自动迁移为新 mission；只有用户再次批准时，才进入新的执行队列。
