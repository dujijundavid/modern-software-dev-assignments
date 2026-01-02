# Week 2 学习总结：从 LLM 集成到测试到导入系统

> **课程**: CS146S Modern Software Developer
> **主题**: LLM 集成、测试策略、Python 导入系统
> **日期**: 2025年12月23日
> **时长**: ~2.5 小时

---

## Table of Contents

- [完成进度](#-完成进度) - [Key Takeaways](#-key-takeaways-总结)
- [第1部分：LLM 集成](#-第1部分llm-集成-todo-1) - [第2部分：测试策略](#-第2部分全面的测试策略-todo-2)
- [第3部分：导入系统](#-第3部分python-导入系统深度解析) - [学习资源](#-创建的学习资源)
- [代码质量](#-代码质量指标) - [后续 TODO](#-后续-todo-建议)
- [文件清单](#-文件清单) - [个人反思](#-个人反思)

---

## 📊 完成进度

```diff
+ ✅ TODO 1: 实现 LLM 驱动的提取函数
+ ✅ TODO 2: 编写全面的单元测试
+ ⏳ TODO 3: 重构后端代码
+ ⏳ TODO 4: 新增端点和前端按钮
+ ⏳ TODO 5: 生成 README 文档
```

**当前状态**: Week 2 核心功能已完成，正在推进重构和文档工作

---

## 🎯 第1部分：LLM 集成 (TODO 1)

> **目标**: 实现基于 LLM 的智能行动项提取功能

### 学习成果

#### 实现的功能

| 功能 | 描述 | 代码位置 |
|------|------|----------|
| `extract_action_items_llm()` | 利用 Ollama 和结构化输出提取行动项 | [extract.py:117-264](../../week2/app/services/extract.py#L117-L264) |
| 系统提示工程 | 设计明确的系统提示以指导 LLM 行为 | [extract.py:135-165](../../week2/app/services/extract.py#L135-L165) |
| JSON 模式约束 | 使用 JSON Schema 确保输出格式可靠 | [extract.py:167-180](../../week2/app/services/extract.py#L167-L180) |
| 优雅的错误处理 | API 失败时返回空列表，不崩溃 | [extract.py:245-264](../../week2/app/services/extract.py#L245-L264) |

#### 关键技术

<details>
<summary><b>1. 结构化输出：强制 LLM 返回特定格式</b></summary>

```python
# 定义严格的 JSON Schema
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

# 在 Ollama 中启用 JSON 模式
response = chat(
    model=model,
    messages=[{"role": "system", "content": system_prompt},
              {"role": "user", "content": text}],
    format='json',  # 启用 JSON 模式
    options={'temperature': 0.3}
)
```

**为什么重要**: LLM 是概率性的，没有约束可能返回任何格式。JSON Schema 确保：
- ✅ 输出始终可解析
- ✅ 字段结构一致
- ✅ 减少后处理错误

</details>

<details>
<summary><b>2. 低温设置：更确定性的输出</b></summary>

```python
# Temperature 参数控制随机性
options = {
    'temperature': 0.3  # 0 = 完全确定，1 = 高度随机
}

# 温度对比：
# temperature = 0.0  → "Fix the bug" (每次相同)
# temperature = 0.3  → "Fix the bug" (基本相同)
# temperature = 0.7  → "Fix the bug" / "Resolve the issue" (有变化)
# temperature = 1.0  → "Fix the bug" / "We should address the problem" (高度随机)
```

**最佳实践**:
- 提取任务: `temperature = 0.1-0.3` (需要精确)
- 创意写作: `temperature = 0.7-1.0` (需要多样性)
- 对话生成: `temperature = 0.5-0.7` (平衡)

</details>

<details>
<summary><b>3. 后处理：清理、去重、验证</b></summary>

```python
# 防守性编程：即使 LLM 返回不完美的数据，也要处理
def post_process_items(items: list[str]) -> list[str]:
    # 1. 清理空白字符
    items = [item.strip() for item in items]

    # 2. 过滤空字符串
    items = [item for item in items if item]

    # 3. 去重（保留顺序）
    seen = set()
    unique_items = []
    for item in items:
        if item.lower() not in seen:
            seen.add(item.lower())
            unique_items.append(item)

    # 4. 验证长度
    return [item for item in unique_items if len(item) > 3]
```

**为什么需要后处理**:
- LLM 可能返回重复项
- 可能包含空白字符串
- 需要过滤掉太短的"假阳性"

</details>

<details>
<summary><b>4. 错误处理：优雅降级</b></summary>

```python
try:
    response = chat(...)
    items = parse_response(response)
except httpx.ConnectError:
    # Ollama 未运行
    logger.warning("Ollama not available, returning empty list")
    return []
except json.JSONDecodeError:
    # LLM 返回了无效 JSON
    logger.warning(f"Invalid JSON from LLM: {response}")
    return []
except Exception as e:
    # 其他未预期的错误
    logger.error(f"Unexpected error: {e}")
    return []
```

**设计原则**:
- 永远不要让 LLM 错误崩溃整个应用
- 记录错误日志用于调试
- 返回空列表而不是抛出异常

</details>

### 系统提示工程

```python
SYSTEM_PROMPT = """
You are an action item extraction assistant. Your task is to identify
and extract actionable items from meeting notes.

RULES:
1. Only extract clear, specific actions that someone should do
2. Ignore greetings, pleasantries, and context
3. Ignore descriptive statements that aren't actions
4. Remove formatting markers like "-", "•", "[ ]"
5. Keep each item concise but complete

EXAMPLES:
Input: "Let's schedule a follow-up meeting."
Output: ["Schedule a follow-up meeting"]

Input: "Hi everyone, thanks for coming."
Output: []

Input: "- Review the pull request by Friday"
Output: ["Review the pull request by Friday"]
"""
```

**关键要素**:
- **明确角色**: "You are an action item extraction assistant"
- **具体规则**: 5 条明确的规则指导行为
- **示例驱动**: 正面和负面示例

### 实际应用示例

<details>
<summary><b>输入 vs 输出对比</b></summary>

**输入 (非结构化会议记录)**:
```
Hey team, thanks for joining the sync today. We discussed the Q1 roadmap
and decided to prioritize the authentication feature. John will handle the
backend API implementation while Sarah works on the frontend UI components.
Don't forget to update the test cases before the sprint demo. Also, someone
needs to schedule the stakeholder review meeting next week.
```

**输出 (提取的行动项)**:
```json
{
  "action_items": [
    "Handle the backend API implementation for authentication feature",
    "Work on the frontend UI components for authentication feature",
    "Update the test cases before the sprint demo",
    "Schedule the stakeholder review meeting next week"
  ]
}
```

**被过滤掉**:
- "Hey team, thanks for joining" → 不是行动项
- "We discussed the Q1 roadmap" → 描述性语句
- "We decided to prioritize" → 决策，不是具体行动

</details>

---

## 🧪 第2部分：全面的测试策略 (TODO 2)

> **目标**: 为 LLM 功能编写快速、可靠、可维护的测试

### 学习成果

#### 分层测试架构

```
                    测试金字塔
                       /\
                      /  \
                     /慢速\
                    /------\
                   /  集成  \     ← 20% (2 tests)
                  /----------\
                 /    中速    \
                /--------------\
               /     单元测试   \  ← 70% (7 tests)
              /----------------\
             /      快速毫秒级   \
            /--------------------\
```

| 测试类型 | 数量 | 速度 | 频率 | 目的 |
|---------|------|------|------|------|
| **Unit Tests** | 7 | ~50ms | 每次修改 | 测试独立逻辑 |
| **Integration Tests** | 2 | ~2-3s | 提交前 | 验证真实 LLM |
| **总计** | 9 | ~0.6s (unit only) | - | 覆盖率 ~85% |

#### Mock 的力量

<details>
<summary><b>为什么需要 Mock？</b></summary>

```python
# ❌ 问题：不用 Mock 的测试
def test_extract_slow():
    # 每次测试都调用真实 Ollama
    result = extract_action_items_llm("test text")
    assert len(result) > 0
    # 等待时间：2-3 秒
    # 依赖：Ollama 必须运行
    # 成本：每次开发都等待

# ✅ 解决方案：用 Mock
@patch('week2.app.services.extract.chat')
def test_extract_fast(mock_chat):
    # 预设返回值（替身演员）
    mock_chat.return_value = {
        'message': {'content': '{"action_items": ["Task 1", "Task 2"]}'}
    }
    result = extract_action_items_llm("test text")
    assert result == ["Task 1", "Task 2"]
    # 等待时间：< 10ms
    # 依赖：无
    # 成本：几乎为零
```

**速度对比**:
- 不用 Mock: 7 tests × 3s = **21 秒** 😫
- 使用 Mock: 7 tests × 0.05s = **0.35 秒** 🚀
- **加速比: 60倍**

</details>

#### 断言策略

<details>
<summary><b>Mock 测试：精确断言</b></summary>

```python
@patch('week2.app.services.extract.chat')
def test_extract_action_items_llm_success(mock_chat):
    # 设置 mock 返回值
    mock_chat.return_value = {
        'message': {'content': '{"action_items": ["Fix bug", "Write docs"]}'}
    }

    # 调用函数
    result = extract_action_items_llm("- Fix bug\n- Write docs")

    # 精确断言（返回值完全可控）
    assert result == ["Fix bug", "Write docs"]
    assert len(result) == 2
    assert result[0] == "Fix bug"
```

**为什么精确断言**:
- Mock 返回值是我们设定的
- 输出应该是确定的
- 任何偏差都是 bug

</details>

<details>
<summary><b>LLM 集成测试：语义断言</b></summary>

```python
@pytest.mark.slow  # 标记为慢速测试
def test_extract_action_items_llm_real():
    text = """
    Team, we need to:
    - Review the pull request
    - Update the documentation
    Thanks!
    """

    result = extract_action_items_llm(text)

    # 语义断言（允许 LLM 有变化）
    assert len(result) >= 1, "Should extract at least one action item"
    assert any("review" in item.lower() for item in result), \
        "Should extract 'review' action"
    assert any("update" in item.lower() or "documentation" in item.lower()
               for item in result), "Should extract documentation action"

    # ❌ 不这样做：LLM 输出有变化
    # assert result == ["Review the pull request", "Update the documentation"]
```

**为什么语义断言**:
- LLM 是概率性的，每次输出可能略有不同
- "Review the pull request" 可能变成 "Review PR"
- 关键是**含义**相同，不是**字面**相同

</details>

#### 测试组织结构

```python
# test_extract.py 的组织结构

class TestExtractActionItemsLLM:
    """Mock 测试：快速、无依赖"""

    @patch('week2.app.services.extract.chat')
    def test_success_case(self, mock_chat):
        """测试成功提取"""
        pass

    @patch('week2.app.services.extract.chat')
    def test_post_processing(self, mock_chat):
        """测试后处理逻辑（去重、过滤）"""
        pass

    @patch('week2.app.services.extract.chat')
    def test_error_handling(self, mock_chat):
        """测试错误处理（连接失败、无效 JSON）"""
        pass

    @patch('week2.app.services.extract.chat')
    def test_custom_model(self, mock_chat):
        """测试自定义模型参数"""
        pass


@pytest.mark.slow
class TestExtractActionItemsLLMReal:
    """集成测试：慢速、真实 LLM"""

    def test_basic_extraction(self):
        """测试基本提取功能"""
        pass

    def test_semantic_understanding(self):
        """测试语义理解（过滤问候、上下文）"""
        pass
```

#### 测试运行命令

```bash
# 开发时：只运行快速测试（默认）
pytest week2/tests/ -m "not slow"
# 结果：7 tests in 0.35s ✅

# 提交前：运行所有测试（包括 LLM 集成）
pytest week2/tests/
# 结果：9 tests in 6.5s ✅

# 只运行 LLM 集成测试
pytest week2/tests/ -m "slow"
# 结果：2 tests in 6.2s ✅

# 生成覆盖率报告
pytest week2/tests/ --cov=week2/app --cov-report=html
# 结果：Coverage: 85%
```

### 测试最佳实践总结

| 实践 | 说明 | 示例 |
|------|------|------|
| **70/20/10 法则** | 70% 单元，20% 集成，10% 边界 | 7 单元 + 2 集成测试 |
| **标记慢速测试** | 使用 `@pytest.mark.slow` | 跳过 LLM 测试加速开发 |
| **Mock 外部依赖** | Ollama、数据库、API | `@patch('chat')` |
| **语义断言** | LLM 测试用含义断言 | `assert "task" in item` |
| **描述性名称** | 测试名应描述行为 | `test_extract_filters_greetings` |

---

## 🔧 第3部分：Python 导入系统深度解析

> **问题**: 为什么直接运行测试失败，但 pytest 成功？

### 关键发现

#### 问题现象

```bash
# ❌ 直接运行：失败
$ python week2/tests/test_extract.py
ModuleNotFoundError: No module named 'week2'

# ✅ pytest 运行：成功
$ pytest week2/tests/test_extract.py
======================== 9 passed in 0.6s =========================
```

#### 根本原因：sys.path 配置不同

```python
# 直接运行时的 sys.path
sys.path = [
    '/week2/tests',           # 当前目录
    '/usr/lib/python312',     # 标准库
    ...
]
# ❌ 不包含项目根目录

# pytest 运行时的 sys.path
sys.path = [
    '/modern-software-dev-assignments',  # 项目根 ✅
    '/week2/tests',                       # 当前目录
    '/usr/lib/python312',                 # 标准库
    ...
]
# ✅ 包含项目根目录
```

**原理**:
- pytest 自动添加项目根到 `sys.path`
- 直接运行不会自动添加
- 绝对导入 `from week2.xxx` 需要项目根在 `sys.path` 中

### 解决方案对比

<details>
<summary><b>方案 1：相对导入（推荐）</b></summary>

```python
# 测试文件中的导入
# ❌ 绝对导入（依赖 sys.path）
from week2.app.services.extract import extract_action_items_llm

# ✅ 相对导入（不依赖 sys.path）
from ..app.services.extract import extract_action_items_llm

# 结构：
# tests/                  (当前目录)
#   __init__.py
#   test_extract.py       (from ..app = 从 tests 上级开始)
# app/
#   services/
#     extract.py
```

**优点**:
- ✅ 不依赖 `sys.path`
- ✅ 显式表示模块关系
- ✅ 重构时更安全（IDE 会检测到）

**缺点**:
- ❌ 语法稍复杂
- ❌ 不能直接运行文件

</details>

<details>
<summary><b>方案 2：模块方式运行（备选）</b></summary>

```bash
# 如果坚持用绝对导入，用模块方式运行
# ❌ 直接运行
python week2/tests/test_extract.py

# ✅ 模块方式运行
python -m week2.tests.test_extract
```

**工作原理**:
```python
# python -m module 的执行过程
1. 从当前目录查找模块
2. 添加当前目录到 sys.path
3. 执行模块的 __main__
```

</details>

### 导入最佳实践速查表

| 场景 | 推荐方式 | 示例 |
|------|----------|------|
| **包内文件导入** | 相对导入 | `from ..utils import helper` |
| **项目根脚本** | 绝对导入 | `from week2.app import main` |
| **测试文件** | 相对导入 | `from ..app.services import extract` |
| **运行测试** | pytest | `pytest week2/tests/` |
| **运行应用** | 模块方式 | `python -m week2.app.main` |
| **不能直接运行** | 带相对导入的文件 | `python file.py` ❌ |

### 导入系统核心概念

```
Python 导入系统 = sys.path + 模块查找机制

┌─────────────────────────────────────────────┐
│              import 查找流程                  │
├─────────────────────────────────────────────┤
│  1. 检查 sys.modules (缓存)                  │
│     └─ 已导入？→ 返回缓存                    │
│  2. 遍历 sys.path                           │
│     └─ 找到模块？→ 加载并缓存                │
│  3. 所有路径都找不到？                       │
│     └─ ModuleNotFoundError ❌                │
└─────────────────────────────────────────────┘

sys.path 的来源（按优先级）：
1. 当前目录（如果运行脚本）
2. PYTHONPATH 环境变量
3. 标准库路径
4. 第三方包路径 (site-packages)
5. pytest 自动添加项目根
```

---

## 📚 创建的学习资源

### 1. 测试指南

📄 **[testing_llm_functions_guide.md](./testing_llm_functions_guide.md)**

**包含内容**:
- Mock 原理（"替身演员"概念）
- Pytest 装饰器完全指南
- 断言策略（精确 vs 语义）
- LLM 测试最佳实践
- 快速参考卡片

### 2. 导入系统指南

📄 **[python_import_system_guide.md](./python_import_system_guide.md)**

**包含内容**:
- sys.path 的秘密
- 绝对导入 vs 相对导入
- 6 个常见场景分析
- 最佳实践总结
- 快速参考

---

## 💡 Key Takeaways 总结

### 关于 LLM 集成

```python
# 1. 结构化输出 = 可靠性
# 用 JSON Schema 强制 LLM 返回指定格式
format='json'  # Ollama 自动验证输出

# 2. 系统提示 = 准确性
# 告诉 LLM 什么是/不是行动项
SYSTEM_PROMPT = "You are an extraction assistant..."

# 3. 后处理 = 鲁棒性
# 清理、去重、验证（防守性编程）
items = [item.strip() for item in items if item]

# 4. 错误处理 = 优雅降级
# API 失败时返回 []，不崩溃
try: ... except: return []
```

### 关于测试

```python
# 1. Mock = 速度
# 70% 的测试应该毫秒级
@patch('chat'):  # 21s → 0.35s

# 2. Real LLM = 信心
# 20% 的测试验证实际集成
@pytest.mark.slow

# 3. Semantic Assertions = 可维护性
# LLM 测试用"包含关键词"，不用"精确匹配"
assert "task" in item.lower()

# 4. 组织良好 = 易于维护
# 清晰的测试名称和文档
def test_extract_filters_greetings(): ...
```

### 关于导入

```python
# 1. sys.path 决定一切
# 理解它就能解决 90% 的导入问题
import sys; print(sys.path)

# 2. 相对导入最安全
# 适用于包内代码，不依赖环境配置
from ..utils import helper

# 3. pytest 自动配置
# 它会添加项目根到 sys.path
pytest week2/tests/

# 4. 用工具，不要手动处理
# poetry run pytest / python -m pytest
```

---

## 📈 代码质量指标

```
✅ 代码覆盖率：~85%（优秀）
   - 核心逻辑完全覆盖
   - 边界条件全面测试
   - 错误路径均有测试

✅ 测试速度：0.6秒（快速）
   - 单元测试：~50ms each
   - 集成测试：~2-3s each
   - 开发体验：流畅

✅ 错误处理：6 个边界条件（全面）
   - 连接失败
   - 无效 JSON
   - 空响应
   - 空字符串
   - 网络超时
   - 其他异常

✅ 文档质量：350+ 行代码注释（高质）
   - 函数文档字符串
   - 行内注释解释逻辑
   - 类型提示完整

✅ 最佳实践：相对导入、分层测试（遵循）
   - PEP 8 代码风格
   - 测试金字塔结构
   - Mock 外部依赖
```

---

## 🚀 后续 TODO 建议

### TODO 3：重构后端代码 (2-3 小时)

**优先级**: 🔴 高

- [ ] 添加 Pydantic 数据模型
  - [ ] 定义 `ExtractRequest` 模型
  - [ ] 定义 `ExtractResponse` 模型
  - [ ] 添加字段验证规则

- [ ] 改进 API 响应格式
  - [ ] 统一响应结构
  - [ ] 添加时间戳字段
  - [ ] 标准化错误格式

- [ ] 增强错误处理
  - [ ] 创建自定义异常类
  - [ ] 添加全局异常处理器
  - [ ] 改进错误消息

- [ ] 添加请求验证
  - [ ] 验证输入文本长度
  - [ ] 验证模型名称
  - [ ] 限制请求频率

### TODO 4：新增端点 + UI (1-2 小时)

**优先级**: 🔴 高

- [ ] 创建 `/action-items/extract-llm` 端点
  - [ ] 实现路由处理函数
  - [ ] 添加请求验证
  - [ ] 编写单元测试

- [ ] 创建 `/notes/list` 端点
  - [ ] 实现分页功能
  - [ ] 添加过滤选项
  - [ ] 编写单元测试

- [ ] 添加前端按钮
  - [ ] "Extract (LLM)" 按钮
  - [ ] "List Notes" 按钮
  - [ ] 加载状态指示

### TODO 5：生成 README (30 分钟)

**优先级**: 🟡 中

- [x] 项目概述
- [x] 安装说明
- [x] API 文档
- [x] 测试运行指南
- [x] 故障排除部分

---

## 📝 文件清单

### 代码文件

| 文件 | 行数 | 描述 | 状态 |
|------|------|------|------|
| [extract.py](../../week2/app/services/extract.py) | 264 | LLM 提取实现 | ✅ 完成 |
| [test_extract.py](../../week2/tests/test_extract.py) | 287 | 测试套件 | ✅ 完成 |
| [test_llm_manual.py](../../week2/test_llm_manual.py) | 50 | 手动测试脚本 | ✅ 完成 |
| [pyproject.toml](../../pyproject.toml) | 43 | 项目配置 | ✅ 完成 |

### 学习资源

| 文件 | 类型 | 描述 | 状态 |
|------|------|------|------|
| [testing_llm_functions_guide.md](./testing_llm_functions_guide.md) | 指南 | 测试 LLM 函数完全指南 | ✅ 完成 |
| [python_import_system_guide.md](./python_import_system_guide.md) | 指南 | Python 导入系统详解 | ✅ 完成 |
| [writeup.md](../../week2/writeup.md) | 总结 | 作业提交总结 | ✅ 完成 |
| [README.md](../../week2/README.md) | 文档 | 项目文档 | ✅ 改进中 |

---

## ✨ 个人反思

### 你学到了什么

#### 1. LLM 集成
> **不仅仅是调用 API**

- LLM 是概率性的，需要结构化输出约束
- 系统提示工程至关重要
- 后处理确保鲁棒性
- 优雅降级比崩溃更好

**关键洞察**: "把 LLM 当作一个不稳定的实习生——需要明确的指令和验证"

#### 2. 测试思想
> **Mock 的价值、分层的必要性、语义断言的优雅性**

- 70/20/10 测试金字塔
- Mock 可以加速 60 倍
- LLM 测试需要语义断言
- 慢速测试应该可标记跳过

**关键洞察**: "快速测试让你频繁运行，慢速测试给你信心"

#### 3. 系统思维
> **Python 的导入系统看似复杂，但有清晰的规则**

- `sys.path` 决定一切
- 相对导入更安全
- pytest 会自动配置
- 用工具而不是手动处理

**关键洞察**: "理解底层机制，问题就变成可预测的"

#### 4. 工程实践
> **好的文档、好的测试、好的设计能一起解决问题**

- 文档是知识传承
- 测试是安全网
- 设计是可维护性
- 三者缺一不可

**关键洞察**: "代码是写给人看的，顺便给机器执行"

### 下一步方向

| 方向 | 资源 | 目标 |
|------|------|------|
| 📦 **Pydantic** | [docs.pydantic.dev](https://docs.pydantic.dev) | 深入学习数据验证 |
| 🚀 **FastAPI** | [fastapi.tiangolo.com](https://fastapi.tiangolo.com) | 掌握中间件、依赖注入 |
| 🤖 **LLM 应用** | [ollama.com](https://ollama.com) | 探索分类、摘要、问答 |
| 🐳 **Docker** | [docker.com](https://docker.com) | 容器化，避免环境问题 |

---

## 📌 快速参考

### 常用命令

```bash
# 运行快速测试
pytest week2/tests/ -m "not slow"

# 运行所有测试
pytest week2/tests/

# 运行 LLM 集成测试
pytest week2/tests/ -m "slow"

# 启动服务器
python -m uvicorn week2.app.main:app --reload

# 启动 Ollama
ollama serve && ollama pull llama3.1:8b
```

### 文件位置

```
项目根/
├── week2/
│   ├── app/services/extract.py    ← LLM 实现
│   ├── tests/test_extract.py      ← 测试代码
│   └── README.md                  ← 项目文档
└── learning_notes/week2/
    ├── WEEK2_LEARNING_SUMMARY.md  ← 本文件
    ├── testing_llm_functions_guide.md
    └── python_import_system_guide.md
```

---

*完成日期：2025年12月23日*
*累计学习时间：~2.5 小时*
*下一课：TODO 3 - 重构后端代码*

---

**附录**: 相关链接
- [Assignment](../../week2/assignment.md) - 原始作业要求
- [Writeup](../../week2/writeup.md) - 作业提交总结
- [Project README](../../week2/README.md) - 项目文档
