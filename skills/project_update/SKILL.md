# Project Update Skill

## 触发场景

当用户输入科研笔记、论文阅读心得、项目想法、师兄反馈、待查问题或调研任务，并希望沉淀为长期 Markdown 记忆时使用。

## 目标

把无序自然语言输入整理成可长期使用的项目文件，而不是只在聊天中回答。

## 执行规则

1. 先读取 `docs/project_concept_v2.md`、`docs/decisions.md`、`docs/questions.md`、`docs/ideas.md`、`docs/research_tasks.md`、`docs/memory_workflow.md`。
2. 先把用户输入拆成 `idea`、`question`、`research task`、`decision candidate` 四类。
3. 写入前必须先给出归档提案，并反问用户确认。
4. 未经确认，不要写入 `docs/decisions.md`。
5. 如果改变项目源构想，创建新版本文件，例如 `project_concept_v3.md`，不要覆盖旧版本。
6. 最后输出修改文件列表、修改原因和需要人工确认的风险点。

## 禁止事项

1. 不要把聊天流水账写入核心文档。
2. 不要无理由删除历史版本。
3. 不要把未验证想法写成确定结论。
4. 不要把普通科研笔记直接扩展成论文 summaries、实验记录或组会材料，除非用户明确要求。
