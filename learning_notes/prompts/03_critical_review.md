# Prompt 3: 批判性审查 (Post-Implementation)

> **用途**: 完成实现后，进行高质量的 AI 工程级代码审查
> **使用时机**: 每个 assignment 完成后，提交前

---

## Prompt Template

```markdown
# Role
You are a strict but fair code reviewer at a top AI company. You have high standards for code quality, especially for AI-related systems.

# Context
I just completed [ASSIGNMENT/FEATURE] for Week [X]. I need a rigorous review before I can consider this "learned".

# Code/Implementation to Review
```[language]
[粘贴你的代码]
```

# Review Request
Perform a multi-dimensional code review:

## 1. 正确性审查 (Correctness)
- 逻辑是否正确？边界情况处理？
- 对于 AI 相关代码：prompt 设计是否健壮？

## 2. AI 工程质量 (AI Engineering Quality)
- Prompt 是否可维护、可测试？
- 是否处理了 LLM 的不确定性？（如重试、验证输出）
- Token 效率如何？

## 3. 生产级考量 (Production Readiness)
- 错误处理是否完善？
- 是否有安全漏洞？（参考 Week 6 Semgrep 检查点）
- 可观测性：日志、监控点

## 4. 与最佳实践对比
- 和业界标准方案相比如何？
- 给出 1-2 个改进建议（可选实施）

# Output Format
分数 (1-10) + 详细反馈 + 学习要点总结
```

---

## AI 工程特有的审查维度

### Prompt 设计质量检查清单

| 检查项 | 问题 | 为什么重要 |
|-------|-----|-----------|
| **结构清晰** | Prompt 有明确的 Role/Context/Task 分离吗？ | 可维护性 |
| **examples 质量** | Few-shot examples 是否多样且有代表性？ | 泛化能力 |
| **输出格式** | 是否明确指定了期望的输出格式？ | 解析可靠性 |
| **边界处理** | 对空输入、异常输入有处理吗？ | 健壮性 |
| **Token 效率** | 是否有冗余的 prompt 内容？ | 成本控制 |

### LLM 调用质量检查清单

| 检查项 | 问题 | 改进方向 |
|-------|-----|---------|
| **重试机制** | API 失败时有重试吗？ | 添加 exponential backoff |
| **输出验证** | 验证 LLM 输出符合预期格式吗？ | 添加 schema 验证 |
| **超时处理** | 设置了请求超时吗？ | 防止 hanging requests |
| **降级策略** | LLM 不可用时的 fallback？ | 优雅降级 |

---

## 使用示例

```markdown
# Context
I just completed **Chain-of-Thought prompting** for Week 1. I need a rigorous review.

# Code/Implementation to Review
```python
def solve_with_cot(problem: str) -> str:
    prompt = f"""
    Let's solve this step by step.
    
    Problem: {problem}
    
    Think through each step carefully:
    """
    
    response = ollama.chat(
        model="mistral-nemo:12b",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["message"]["content"]
```

# Review Request
...
```

---

## 审查后的行动

1. **记录所有 feedback** 到 `learning_notes/weekX/03_code_review_feedback.md`
2. **分类问题**：必须修复 vs 可选改进
3. **修复后再次审查**：确认问题已解决
4. **提炼模式**：将好的实践添加到个人代码库
