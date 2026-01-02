# Prompt 1: 概念深度理解 (Pre-Learning)

> **用途**: 学习每周新概念前，先通过 AI 获取高质量的背景知识
> **使用时机**: 开始每周学习的第一步

---

## Prompt Template

```markdown
# Role
You are a senior AI Engineer with 10+ years of experience in both traditional software development and modern AI-powered systems.

# Context
I am about to learn [TOPIC] for [WEEK X] of a Modern Software Development course. My goal is to become an AI Engineer.

# Task
Before I dive into the hands-on implementation, help me build a strong mental model:

1. **核心概念图谱** (5 min read)
   - 用 Mermaid 图展示这个概念与其他 AI 工程概念的关系
   - 列出 3-5 个关键术语及其精确定义

2. **为什么重要** (AI Engineer 视角)
   - 这个技术解决了什么痛点？
   - 在真实 AI 系统中的典型应用场景

3. **常见误区与陷阱**
   - 初学者常犯的错误
   - 专家级的最佳实践

4. **动手前的思考题** (苏格拉底式)
   - 3 个帮助我思考的问题，答案留空让我自己填写

# Output Format
使用中文回答，技术术语保持英文。使用 Markdown 格式，便于我保存为笔记。

# Variables
- TOPIC: [填写本周主题，如 "Chain-of-Thought Prompting"]
- WEEK: [填写周数]
```

---

## 使用示例

### Week 1: Chain-of-Thought Prompting

```markdown
# Role
You are a senior AI Engineer with 10+ years of experience...

# Context
I am about to learn **Chain-of-Thought Prompting** for **Week 1** of a Modern Software Development course. My goal is to become an AI Engineer.

# Task
...
```

### Week 3: MCP Server

```markdown
# Context
I am about to learn **Model Context Protocol (MCP) Server** for **Week 3** of a Modern Software Development course...
```

---

## 输出保存位置

将生成的内容保存到:
```
learning_notes/weekX/01_pre_learning_concepts.md
```
