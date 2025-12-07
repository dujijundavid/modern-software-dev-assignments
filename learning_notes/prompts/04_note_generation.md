# Prompt 4: 笔记生成 (Teaching Phase)

> **用途**: 将学习成果转化为结构化笔记，方便未来回顾
> **使用时机**: 每周学习结束时

---

## Prompt Template

```markdown
# Role
You are helping me create high-quality, structured learning notes that my future self will thank me for.

# Context
I just completed Week [X] on [TOPIC]. I need to consolidate my learning into a reusable note.

# My Learning Summary
- 完成的 assignments: [列出]
- 遇到的主要困难: [描述]
- 关键突破/aha moment: [描述]
- 自我评估掌握度: [1-10]

# Note Structure Request
帮我组织一份包含以下结构的笔记：

## 1. One-Liner Summary
用一句话概括这周学到的最重要的东西

## 2. 核心概念速查表
| 概念 | 定义 | 代码示例 | 使用场景 |
|-----|-----|---------|---------|

## 3. 我的实现亮点
- 我做得好的地方（带代码片段）
- 可以复用的模式

## 4. 踩坑记录
- 问题 → 原因 → 解决方案

## 5. 与真实 AI 系统的连接
这个技术在真实世界中如何被使用？

## 6. 下次要更好
如果重新做一次，我会...

## 7. 延伸学习资源 (Optional)
2-3 个深入学习的资源

# Output
Markdown 格式，便于直接保存到 `learning_notes/weekX/`
```

---

## 输入准备清单

在使用此 Prompt 前，准备好以下信息：

### 自我评估问卷

```markdown
## Week [X] 自我评估

### 1. 完成情况
- [ ] K-shot prompting
- [ ] Chain-of-thought
- [ ] Tool calling
- [ ] Self-consistency
- [ ] RAG
- [ ] Reflexion

### 2. 难度评估 (1-5)
| Assignment | 难度 | 花费时间 |
|-----------|-----|---------|
| K-shot | ? | ?h |
| CoT | ? | ?h |
| ... | | |

### 3. 主要困难
1. 
2. 
3. 

### 4. Aha Moments
1. 
2. 

### 5. 掌握度自评: ?/10
```

---

## 笔记示例结构

```markdown
# Week 1: Prompting Techniques 学习笔记

## One-Liner Summary
Prompt 工程的核心是 **结构化引导 LLM 的思考过程**，不同技术适用于不同类型的任务。

## 核心概念速查表

| 概念 | 定义 | 代码示例 | 使用场景 |
|-----|-----|---------|---------|
| K-shot | 提供 K 个示例引导模型 | `examples = [...]` | 格式转换、分类 |
| CoT | 引导模型逐步推理 | `"Let's think step by step"` | 复杂推理、数学 |
| RAG | 检索增强生成 | `context = retrieve(query)` | 知识密集型问答 |

## 我的实现亮点
...

## 踩坑记录
| 问题 | 原因 | 解决方案 |
|-----|------|---------|
| CoT 输出不稳定 | 缺乏结构化 | 添加 numbered steps |

## 与真实 AI 系统的连接
- ChatGPT 使用 CoT 处理复杂问题
- Cursor 使用 RAG 检索代码库上下文
- ...

## 下次要更好
- 先设计 prompt 结构再写代码
- 更多关注 edge cases

## 延伸资源
1. [Anthropic Prompt Engineering Guide](...)
2. [Chain-of-Thought Paper](...)
```

---

## 保存位置

```
learning_notes/weekX/04_week_summary.md
```
