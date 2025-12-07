# Prompt 6: Mini-Project 挑战 (Deep Learning)

> **用途**: 通过综合性小项目来深化理解
> **使用时机**: 完成 2-3 周内容后，想要深化实践时

---

## Prompt Template

```markdown
# Role
You are a project mentor who designs challenging but achievable mini-projects that consolidate multiple learning objectives.

# Context
I've completed Week [X] to Week [Y] of the course. I want to solidify my learning through a hands-on mini-project.

# Skills to Consolidate
- [列出要综合应用的技术，如 "RAG, FastAPI, MCP Server"]

# Constraints
- Time budget: [2-4 hours]
- Must be completable with local resources (Ollama, SQLite, etc.)
- Should produce something I can demo

# Request
Design a mini-project that:
1. **综合应用** 我列出的技术
2. **有明确的验收标准** (test cases or demo checklist)
3. **分步骤指导**，每步预计时间
4. **包含一个"挑战扩展"** 给想加难度的我

# Project Proposal Format
- **Project Name**: 
- **One-liner**: 
- **Tech Stack**: 
- **Steps** (with time estimates):
- **Success Criteria** (checkboxes):
- **Stretch Goal**:
```

---

## 项目难度分级

| 级别 | 时间 | 综合技术数 | 适合阶段 |
|-----|-----|-----------|---------|
| ⭐ Easy | 1-2h | 2 | 刚完成 Week 1-2 |
| ⭐⭐ Medium | 2-4h | 3-4 | 完成 Week 1-4 |
| ⭐⭐⭐ Hard | 4-6h | 4+ | 完成 Week 1-6 |

---

## 项目示例

### Week 1-2 完成后: Smart Note Enhancer

```markdown
## Project: Smart Note Enhancer

**One-liner**: 一个能自动从笔记中提取 action items 并生成摘要的 CLI 工具

**Tech Stack**: 
- CoT prompting (Week 1)
- RAG for context (Week 1)
- FastAPI endpoint (Week 2)

**Steps**:
1. (30min) 设计 prompt 模板
2. (30min) 实现笔记加载和预处理
3. (45min) 构建 FastAPI 端点
4. (30min) 添加简单 CLI
5. (15min) 测试和调试

**Success Criteria**:
- [ ] 能接受 markdown 笔记输入
- [ ] 自动提取 action items (准确率 > 80%)
- [ ] 生成结构化摘要
- [ ] 有基本的错误处理

**Stretch Goal**:
添加 similar notes 推荐功能 (使用 RAG)
```

### Week 1-4 完成后: Personal Coding Assistant

```markdown
## Project: Personal Coding Assistant MCP Server

**One-liner**: 一个可以分析本地代码库并回答问题的 MCP 服务器

**Tech Stack**:
- RAG for code retrieval (Week 1)
- Tool calling (Week 1)
- MCP Server (Week 3)
- Claude Code integration (Week 4)

**Steps**:
1. (45min) 设计代码索引策略
2. (45min) 实现 MCP tools: `search_code`, `explain_function`
3. (30min) 添加 prompt template for explanations
4. (30min) 集成到 Claude Desktop
5. (30min) 测试和优化

**Success Criteria**:
- [ ] 可以在 Claude Desktop 中使用
- [ ] `search_code` 返回相关代码片段
- [ ] `explain_function` 能解释任意函数
- [ ] 处理大文件时不会 timeout

**Stretch Goal**:
添加 `suggest_refactor` tool
```

---

## 项目完成后

1. **更新 learning_notes/projects/** 记录项目过程
2. **提取可复用模式** 到个人代码库
3. **考虑扩展** 为 portfolio project

---

## 保存位置

```
learning_notes/projects/mini_project_[name].md
```
