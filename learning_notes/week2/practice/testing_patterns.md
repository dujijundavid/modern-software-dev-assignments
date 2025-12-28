# 测试 LLM 函数完全指南 (Testing LLM Functions Guide)

## 📚 目录
1. [Mock 的原理](#mock-的原理)
2. [Pytest 装饰器详解](#pytest-装饰器详解)
3. [断言策略](#断言策略)
4. [LLM 测试最佳实践](#llm-测试最佳实践)

---

## 🎭 Mock 的原理

### 核心概念：替身演员

想象你在拍电影：

```
真实场景：主角要从100层楼跳下（危险、昂贵、慢）
Mock场景：用替身 + 绿幕拍摄（安全、便宜、快）
```

在编程中：

```python
# 真实场景：你的函数调用外部服务
def send_email(to, subject, body):
    gmail_api.send(to, subject, body)  # 真的发邮件！

# 测试时的问题：
# ❌ 真的发了1000封邮件（测试跑1000次）
# ❌ 需要网络连接
# ❌ 如果Gmail挂了，测试失败（但不是你的代码问题）
```

**Mock 解决方案：**

```python
from unittest.mock import patch

# 用假的 gmail_api 替换真的
@patch('myapp.gmail_api')
def test_send_email(mock_gmail):
    # 现在 gmail_api 是假的，不会真发邮件
    send_email("test@example.com", "Hello", "World")
    
    # 验证"假演员"被正确调用了
    mock_gmail.send.assert_called_once_with(
        "test@example.com", "Hello", "World"
    )
```

### Mock 在 Action Item Extractor 中的应用

```python
# week2/app/services/extract.py
def extract_action_items_llm(text: str, model: str = "llama3.1:8b") -> List[str]:
    response = chat(  # ← 这里调用 Ollama API（慢，依赖外部服务）
        model=model,
        messages=[...],
        format={...}
    )
    
    # 解析响应
    content = response["message"]["content"]
    data = json.loads(content)
    items = data.get("action_items", [])
    
    # 后处理
    return [item.strip() for item in items if item.strip()]
```

**测试难度分析：**

| 步骤 | 是否依赖外部 | 测试难度 |
|-----|------------|---------|
| 调用 `chat()` | ✅ 依赖Ollama | 🔴 难（慢、不稳定） |
| 解析JSON | ❌ 纯逻辑 | 🟢 易 |
| 后处理（去空格、去重） | ❌ 纯逻辑 | 🟢 易 |

**Mock 策略：替换 `chat()`，只测试我们的逻辑**

### Mock 实战示例

#### 示例 1：最简单的 Mock

```python
from unittest.mock import patch

@patch('week2.app.services.extract.chat')  # ← 替换 chat 函数
def test_basic_mock(mock_chat):
    # 1. 设置"假演员"的台词（返回值）
    mock_chat.return_value = {
        "message": {
            "content": '{"action_items": ["Task 1", "Task 2"]}'
        }
    }
    
    # 2. 调用真实函数（但它会用假的 chat）
    result = extract_action_items_llm("任意输入")
    
    # 3. 验证结果
    assert result == ["Task 1", "Task 2"]
    
    # 4. 验证 chat 被调用了（可选）
    mock_chat.assert_called_once()
```

**执行流程：**
```
1. Python 看到 @patch，把真的 chat() 藏起来
2. 创建假的 mock_chat 对象
3. 设置 return_value（假数据）
4. 执行 extract_action_items_llm()
   - 内部调用 chat() → 实际调用 mock_chat
   - 返回我们设置的假数据
5. 测试你的解析逻辑是否正确
```

#### 示例 2：测试后处理逻辑（去重、去空格）

```python
@patch('week2.app.services.extract.chat')
def test_post_processing(mock_chat):
    # 返回有问题的数据：重复、空格、空字符串
    mock_chat.return_value = {
        "message": {
            "content": '{"action_items": ["  Task 1  ", "Task 1", "", "Task 2"]}'
        }
    }
    
    result = extract_action_items_llm("test")
    
    # 验证后处理逻辑
    assert result == ["Task 1", "Task 2"]  # 去重 + 去空格 + 过滤空
    assert len(result) == 2
```

**测试的是什么？**
- ✅ 你的代码能否正确去重
- ✅ 你的代码能否清理空格
- ✅ 你的代码能否过滤空字符串
- ❌ 不测试 LLM 的能力（那是 Ollama 的责任）

#### 示例 3：测试错误处理

```python
@patch('week2.app.services.extract.chat')
def test_api_error(mock_chat):
    # 模拟 API 崩溃
    mock_chat.side_effect = Exception("Ollama服务挂了")
    
    # 你的函数应该优雅降级，不崩溃
    result = extract_action_items_llm("test")
    
    assert result == []  # 返回空列表，而非抛异常
```

**`side_effect` vs `return_value`:**
```python
# return_value：模拟正常返回
mock.return_value = "成功"

# side_effect：模拟抛异常
mock.side_effect = Exception("失败")
```

### Mock 常见用法总结

```python
from unittest.mock import patch, Mock

# 1. 最基本：替换函数
@patch('module.function_name')
def test(mock_func):
    mock_func.return_value = "假数据"

# 2. 替换类方法
@patch('module.ClassName.method_name')
def test(mock_method):
    mock_method.return_value = "假数据"

# 3. 模拟异常
@patch('module.function')
def test(mock_func):
    mock_func.side_effect = Exception("错误")

# 4. 验证调用
@patch('module.function')
def test(mock_func):
    my_function()
    mock_func.assert_called_once()  # 确保被调用1次
    mock_func.assert_called_with(arg1, arg2)  # 确保传了正确参数

# 5. 多个 Mock
@patch('module.function2')
@patch('module.function1')
def test(mock_func1, mock_func2):  # 注意顺序反过来！
    pass
```

---

## 🎨 Pytest 装饰器详解

### 装饰器是什么？

```python
# 装饰器 = 给函数"穿衣服"，增加额外功能

# 没穿衣服的函数
def my_test():
    print("测试")

# 穿了 @patch 衣服的函数
@patch('some.function')
def my_test(mock_func):
    print("测试，但function被替换了")
```

### 常用 Pytest 装饰器

#### 1. `@patch` - Mock装饰器

```python
from unittest.mock import patch

@patch('week2.app.services.extract.chat')
def test_with_mock(mock_chat):
    # mock_chat 会自动作为参数传入
    pass
```

#### 2. `@pytest.mark.parametrize` - 参数化测试

**用途：用不同数据跑同一个测试**

```python
import pytest

# 用3组数据测试同一个函数
@pytest.mark.parametrize("input_text,expected_count", [
    ("- Task 1\n- Task 2", 2),           # 测试数据1
    ("TODO: Fix bug", 1),                 # 测试数据2
    ("No action items here", 0),          # 测试数据3
])
def test_extraction(input_text, expected_count):
    result = extract_action_items_llm(input_text)
    assert len(result) == expected_count
```

**效果：1个测试函数 = 3个测试用例**

```bash
test_extraction[input0-2] PASSED
test_extraction[input1-1] PASSED  
test_extraction[input2-0] PASSED
```

#### 3. `@pytest.mark.slow` - 标记慢速测试

```python
import pytest

@pytest.mark.slow  # 标记为慢速测试
def test_real_llm():
    result = extract_action_items_llm("test")  # 真实调用，慢
    assert len(result) >= 0
```

**用法：**
```bash
# 跳过慢速测试
pytest -m "not slow"

# 只跑慢速测试
pytest -m "slow"

# 跑所有测试
pytest
```

**配置文件 `pytest.ini`：**
```ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
```

#### 4. `@pytest.fixture` - 测试夹具（共享数据）

**用途：多个测试共享相同的准备工作**

```python
import pytest

# 夹具：准备测试数据
@pytest.fixture
def sample_notes():
    return "- Buy milk\n- Fix bug\nTODO: Write tests"

# 使用夹具
def test_extract_bullets(sample_notes):
    result = extract_action_items(sample_notes)
    assert len(result) == 3

def test_extract_keywords(sample_notes):
    result = extract_action_items(sample_notes)
    assert any("test" in item.lower() for item in result)
```

#### 5. 多个装饰器组合

```python
@pytest.mark.slow
@patch('week2.app.services.extract.chat')
def test_complex(mock_chat):
    # 既是慢速测试，又使用 Mock
    pass

@pytest.mark.parametrize("text,expected", [
    ("- Task", ["Task"]),
    ("", []),
])
@patch('week2.app.services.extract.chat')
def test_parametrized_mock(mock_chat, text, expected):
    # 参数化 + Mock
    mock_chat.return_value = {"message": {"content": f'{{"action_items": {expected}}}'}}
    result = extract_action_items_llm(text)
    assert result == expected
```

---

## ✅ 断言策略

### 断言的本质

```python
# 断言 = 检查点 = "这里必须是真的，否则测试失败"

assert 1 + 1 == 2  # ✅ 通过
assert 1 + 1 == 3  # ❌ 失败：AssertionError
```

### 基础断言类型

#### 1. 相等性断言

```python
# 精确相等
assert result == ["Task 1", "Task 2"]

# 不等
assert result != []

# 近似相等（浮点数）
assert abs(result - 3.14159) < 0.0001
```

#### 2. 类型断言

```python
assert isinstance(result, list)
assert isinstance(result[0], str)
assert type(result) == list
```

#### 3. 长度/存在性断言

```python
# 长度
assert len(result) == 3
assert len(result) > 0

# 包含
assert "Task 1" in result
assert "Bug" not in result

# 为空
assert result  # 非空即真
assert not result  # 空即真
```

#### 4. 逻辑断言

```python
# any：至少一个为真
assert any("bug" in item.lower() for item in result)

# all：全部为真
assert all(isinstance(item, str) for item in result)
assert all(len(item) > 0 for item in result)

# 多个条件
assert len(result) > 0 and all(isinstance(i, str) for i in result)
```

### 针对 LLM 测试的断言策略

#### 策略 1：Mock测试 - 精确断言

```python
@patch('week2.app.services.extract.chat')
def test_mock(mock_chat):
    mock_chat.return_value = {
        "message": {"content": '{"action_items": ["Fix bug", "Write tests"]}'}
    }
    
    result = extract_action_items_llm("test")
    
    # ✅ 可以用精确断言（因为Mock返回值固定）
    assert result == ["Fix bug", "Write tests"]
    assert len(result) == 2
    assert result[0] == "Fix bug"
```

#### 策略 2：Real LLM测试 - 语义断言

```python
@pytest.mark.slow
def test_real_llm():
    text = "Meeting notes:\n- Fix bug #123\n* Write unit tests"
    result = extract_action_items_llm(text)
    
    # ❌ 不要精确断言（LLM输出有变化）
    # assert result == ["Fix bug #123", "Write unit tests"]
    
    # ✅ 语义断言（检查内容而非格式）
    assert len(result) >= 2, "应该至少提取2个项目"
    
    # 检查是否包含关键词
    assert any("bug" in item.lower() and "123" in item for item in result)
    assert any("test" in item.lower() for item in result)
    
    # 检查类型
    assert all(isinstance(item, str) for item in result)
    
    # 检查没有空字符串
    assert all(len(item.strip()) > 0 for item in result)
```

#### 策略 3：边界条件断言

```python
def test_empty_input():
    result = extract_action_items_llm("")
    
    # 空输入应该返回空列表
    assert result == []
    assert len(result) == 0
    assert not result  # 空列表是 False
```

### 常见断言错误与改进

#### 错误 1：断言太宽松

```python
# ❌ 太宽松
assert len(result) > 0  # 只要有数据就过，可能是错的数据

# ✅ 改进
assert len(result) == 2
assert "expected_keyword" in str(result)
```

#### 错误 2：断言太严格

```python
# ❌ 太严格（LLM测试）
assert result == ["Fix Bug #123"]  # 大小写、标点变化就失败

# ✅ 改进
assert any("fix" in item.lower() and "bug" in item.lower() for item in result)
```

#### 错误 3：没有错误信息

```python
# ❌ 失败时不知道为什么
assert len(result) == 2

# ✅ 添加错误信息
assert len(result) == 2, f"Expected 2 items, got {len(result)}: {result}"
```

---

## 🎯 LLM 测试最佳实践

### 测试金字塔

```
┌─────────────────────────────────────┐
│   Integration Tests (Real LLM)     │  ← 少量（20-30%）
├─────────────────────────────────────┤
│   Unit Tests (Mocked LLM)          │  ← 大量（60-70%）
├─────────────────────────────────────┤
│   Edge Case Tests                  │  ← 适量（10-20%）
└─────────────────────────────────────┘
```

### 为什么这样分配？

| 测试类型 | 速度 | 稳定性 | 成本 | 运行频率 |
|---------|------|--------|------|---------|
| Mock Tests | ⚡️ 毫秒 | 100% | 低 | 每次保存 |
| Real Tests | 🐌 秒级 | ~80% | 高 | CI/CD |
| Edge Tests | ⚡️ 毫秒 | 100% | 低 | 每次保存 |

### 测试组织建议

```python
# test_extract.py

# ========== Existing Test ==========
def test_extract_bullets_and_checkboxes():
    """原有的 heuristic 测试"""
    pass

# ========== Unit Tests (Mocked) - 快速、稳定 ==========
@patch('week2.app.services.extract.chat')
def test_llm_extract_mock_success(mock_chat):
    """测试正常解析和返回"""
    pass

@patch('week2.app.services.extract.chat')
def test_llm_extract_mock_post_processing(mock_chat):
    """测试去重、空格清理、空字符串过滤"""
    pass

# ========== Integration Tests (Real LLM) - 慢速、真实 ==========
@pytest.mark.slow
def test_llm_extract_real_basic():
    """测试基本提取能力"""
    pass

# ========== Edge Cases - 快速、全面 ==========
def test_llm_extract_edge_cases():
    """测试边界条件"""
    pass
```

### 快速参考卡片

```python
# ===== Mock =====
@patch('path.to.function')
def test(mock_func):
    mock_func.return_value = "数据"
    mock_func.side_effect = Exception()
    mock_func.assert_called_once_with(arg1, arg2)

# ===== Pytest装饰器 =====
@pytest.mark.parametrize("input,expected", [...])
@pytest.mark.slow
@pytest.fixture
def my_fixture():
    return "共享数据"

# ===== 断言 =====
assert result == expected
assert len(result) > 0
assert "keyword" in result
assert any(condition for item in result)
assert all(condition for item in result)
mock.assert_called_once()
```

### 运行测试的命令

```bash
# 运行所有测试
poetry run pytest week2/tests/

# 只运行快速测试（跳过慢速）
poetry run pytest week2/tests/ -m "not slow"

# 只运行慢速测试
poetry run pytest week2/tests/ -m "slow"

# 显示详细输出
poetry run pytest week2/tests/ -v

# 显示print输出
poetry run pytest week2/tests/ -s

# 只运行特定测试
poetry run pytest week2/tests/test_extract.py::test_llm_extract_mock_success
```

---

## 📊 总结

### 三者的关系

```python
from unittest.mock import patch  # Mock工具
import pytest  # 测试框架

# 装饰器：给测试函数增加能力
@pytest.mark.slow           # 标记为慢速测试
@patch('module.function')   # Mock外部依赖
def test_example(mock_func):  # mock_func 由 @patch 自动传入
    # Mock：设置假数据
    mock_func.return_value = "假数据"
    
    # 执行
    result = my_function()
    
    # 断言：验证结果
    assert result == "预期输出"
    assert isinstance(result, str)
    mock_func.assert_called_once()
```

**三者分工：**
- **Mock**：隔离外部依赖（快速、可控）
- **装饰器**：组织和配置测试（参数化、标记、夹具）
- **断言**：验证结果（精确或语义）

### 关键要点

1. **Mock是为了测试你的代码，不是测试别人的代码**
2. **大部分测试应该是快速的（用Mock）**
3. **少量集成测试验证真实行为**
4. **断言要有明确的错误信息**
5. **测试应该独立、可重复**

---

*作者：AI Pair Programming Partner*  
*日期：2025年12月23日*  
*课程：Week 2 - Modern Software Development*
