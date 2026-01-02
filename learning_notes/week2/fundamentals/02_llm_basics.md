# LLM 集成基础

> 结构化输出、Prompt 工程和错误处理

---

## 🎯 核心问题：LLM 输出不可靠

### LLM 的工作原理

```
输入提示词 → Token 生成 → 概率采样 → 文本输出
```

每个 Token 都是概率分布的采样结果：

| 特性 | 说明 | 影响 |
|------|------|------|
| **非确定性** | 同一提示词可能产生不同输出 | 输出不稳定 |
| **格式不保证** | 要求 JSON 也可能返回纯文本 | `json.loads()` 可能失败 |
| **容易幻觉** | 生成看似合理但实际错误的内容 | 需要验证 |
| **难以验证** | 输出正确性需要人工检查 | 增加测试负担 |

### 真实例子

**你要求**：返回 JSON 格式，包含 name 和 age

**LLM 可能返回**：
```json
{
  "name": "John",
  "age": "thirty years old",  // ❌ 不是数字！
  "city": "New York"           // ❌ 你没要求的字段
}
```

或者甚至：
```
嗯，这是一个关于 John 的信息：
姓名是 John，年龄是 30 岁...
```

**结论**：自然语言是灵活的，但系统需要结构化的、可验证的数据。

---

## ✅ 解决方案：Structured Output

### 什么是 Structured Output

通过 **JSON Schema 约束** 强制 LLM 遵守格式：

```python
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0, "maximum": 150},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["name", "age"]
}
```

**保证**：
- ✅ 返回值一定是 JSON 对象
- ✅ `age` 一定是整数
- ✅ `name` 一定存在
- ✅ 无法返回你没定义的字段

### JSON Schema 三层防护

| 层级 | 作用 | 例子 |
|------|------|------|
| **类型约束** | 确保数据类型正确 | `age: integer` |
| **值约束** | 限制可能的取值 | `enum: ["active", "inactive"]` |
| **结构约束** | 定义必需字段 | `required: ["id", "name"]` |

### 成本-收益分析

**成本**：
- 定义 JSON Schema（一次性投入）
- 某些 API 需要额外费用

**收益**（远大于成本）：
- 消除 95%+ 的格式错误
- 减少数据验证代码
- 减少调试时间
- 提高系统可靠性
- 降低运维成本

---

## 🔧 Ollama 实现 Structured Output

### JSON Mode

```bash
# 基本模式（松散）
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.1:8b",
    "prompt": "Extract user info: name, age",
    "format": "json"
  }'

# 严格 Schema 模式（推荐）
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.1:8b",
    "prompt": "Extract user info",
    "format": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"}
      },
      "required": ["name", "age"]
    }
  }'
```

### Python 实现

```python
from ollama import chat

# 定义 JSON Schema
json_schema = {
    'type': 'object',
    'properties': {
        'action_items': {
            'type': 'array',
            'items': {'type': 'string'},
            'description': 'List of actionable items'
        }
    },
    'required': ['action_items']
}

# 调用 LLM
response = chat(
    model='llama3.1:8b',
    messages=[{
        "role": "system",
        "content": "You are an action item extraction assistant."
    }, {
        "role": "user",
        "content": "Extract action items from this text..."
    }],
    format='json',  # 启用 JSON 模式
    options={'temperature': 0.1}  # 低温度 = 更稳定
)

# 解析响应（保证是有效 JSON）
import json
data = json.loads(response['message']['content'])
items = data['action_items']
```

### 最佳实践

```python
# ✅ 推荐配置
response = chat(
    model='llama3.1:8b',
    prompt=prompt,
    format=json_schema,
    options={
        'temperature': 0.1,  # 低温度 = 更稳定
        'top_p': 0.9
    }
)
```

**关键参数**：

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `temperature` | 0.1-0.3 | 提取任务需要精确 |
| `top_p` | 0.9 | 平衡准确性和多样性 |
| `模型` | 7B+ | 小模型效果差 |

---

## 📝 Prompt Engineering 最佳实践

### 系统提示设计

```python
SYSTEM_PROMPT = """
You are an action item extraction assistant.

RULES:
1. Only extract clear, specific actions that someone should do
2. Ignore greetings, pleasantries, and context
3. Remove formatting markers like "-", "•", "[ ]"
4. Keep each item concise but complete

EXAMPLES:
Input: "Let's schedule a follow-up meeting."
Output: ["Schedule a follow-up meeting"]

Input: "Hi everyone, thanks for coming."
Output: []
"""
```

### 提示工程要素

| 要素 | 说明 | 例子 |
|------|------|------|
| **明确角色** | 告诉 LLM 它是谁 | "You are an extraction assistant" |
| **具体规则** | 5 条明确的规则 | "Only extract actions, not greetings" |
| **示例驱动** | 正面和负面示例 | Input → Output 对比 |
| **输出格式** | 明确期望格式 | "Return JSON with action_items array" |

---

## ⚠️ 常见误区与陷阱

### ❌ 初学者常犯错误

| 错误 | ✅ 正确做法 |
|------|-----------|
| 假设 LLM 输出总是有效 JSON | 使用 JSON Schema 约束 |
| 直接在生产使用大模型 | 先用小模型测试 |
| 忽视 prompt 工程重要性 | 花时间优化 prompt |
| 没有设置超时和资源限制 | 设置超时时间，监控内存 |
| 一次性实现所有功能 | 渐进式构建：启发式 → LLM |

### 💡 专家级最佳实践

```python
# 1. Dependency Injection
class Config:
    ollama_base_url: str = "http://localhost:11434"
    model_name: str = "llama3.1:8b"
    timeout: int = 30

# 2. Schema-Driven Design
class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)

# 3. Graceful Degradation
try:
    items = extract_with_llm(text)
except LLMUnavailableError:
    items = extract_heuristic(text)

# 4. 测试分层
# - 单元测试：Mock LLM 调用
# - 集成测试：使用小模型验证
# - 性能测试：基准测试延迟

# 5. 可观测性
# - 记录 LLM 输入/输出
# - 追踪 API 延迟
# - 监控成功率
```

---

## 🎯 使用场景速查表

### 什么时候必须用 Structured Output？

| 场景 | 优先级 | 原因 |
|------|--------|------|
| 数据库直接插入 | 🔴 **必须** | 无容错空间 |
| API 响应字段 | 🔴 **必须** | 破坏合约 |
| 金融/医疗数据 | 🔴 **必须** | 法律风险 |
| 日期/数字解析 | 🟡 **强烈推荐** | 90%+ 出错率 |
| 枚举选择 | 🟡 **强烈推荐** | 容易乱编 |
| 文本生成 | 🟢 **可选** | 容错能力强 |
| 创意写作 | 🟢 **不需要** | 结构限制创意 |

### 快速检查清单

```markdown
□ 代码里有 `json.loads()` 吗？
  → 是：**必须使用 Structured Output**

□ 有 `try/except` 处理格式错误吗？
  → 是：**改用 Structured Output，删除这些代码**

□ 输出会直接用于数据库或 API 吗？
  → 是：**必须使用 Structured Output**

□ 字段必须是特定类型（数字、日期、URL）吗？
  → 是：**必须使用 Structured Output**

□ 允许 LLM 返回任意文本吗？
  → 是：**Structured Output 不必要**
```

---

## 🔗 延伸阅读

- [Ollama 结构化输出](https://ollama.com/blog/structured-outputs)
- [Ollama 模型库](https://ollama.com/library)
- [JSON Schema 规范](https://json-schema.org/)
- [Pydantic 文档](https://docs.pydantic.dev/latest/)

---

## 📊 关键要点总结

| 要点 | 说明 |
|------|------|
| **问题根源** | LLM 输出是概率序列，不可靠 |
| **解决方案** | Structured Output 强制约束 |
| **为什么必需** | 消除 95%+ 格式错误 |
| **何时使用** | 数据库、API、特定类型 |
| **如何实现** | JSON Schema + format='json' |

> **核心金句**：*"不要期望 LLM 遵守格式规则，而要用技术强制它遵守。"*
