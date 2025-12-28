# 测试核心概念

> Mock、测试金字塔和断言策略

---

## 🧪 为什么需要 Mock

### 问题：不用 Mock 的测试

```python
# ❌ 问题：每次测试都调用真实 Ollama
def test_extract_slow():
    result = extract_action_items_llm("test text")
    assert len(result) > 0
    # 等待时间：2-3 秒
    # 依赖：Ollama 必须运行
```

**问题**：
- 每次测试 2-3 秒
- 需要 Ollama 运行
- 外部依赖导致测试不稳定

### 解决方案：用 Mock

```python
# ✅ 解决方案：用 Mock
from unittest.mock import patch

@patch('week2.app.services.extract.chat')
def test_extract_fast(mock_chat):
    # 预设返回值（替身演员）
    mock_chat.return_value = {
        'message': {'content': '{"action_items": ["Task 1", "Task 2"]}'}
    }
    result = extract_action_items_llm("test text")
    assert result == ["Task 1", "Task 2"]
    # 等待时间：< 10ms
```

### 速度对比

| 方式 | 7 个测试时间 | 依赖 |
|------|------------|------|
| 不用 Mock | 21 秒 | Ollama |
| 使用 Mock | 0.35 秒 | 无 |
| **加速比** | **60 倍** | - |

---

## 📊 测试金字塔

```
              测试金字塔
                 /\
                /  \
               /慢速\
              /------\
             /  集成  \     ← 20%
            /----------\
           /   中速    \
          /--------------\
         /    单元测试   \  ← 70%
        /----------------\
       /      快速毫秒级  \
      /--------------------\
```

### 70/20/10 法则

| 测试类型 | 数量 | 速度 | 目的 |
|---------|------|------|------|
| **单元测试** | 70% | ~50ms | 测试独立逻辑 |
| **集成测试** | 20% | ~2-3s | 验证真实 LLM |
| **边界测试** | 10% | 可变 | 测试极端情况 |

---

## 🎯 断言策略

### Mock 测试：精确断言

```python
@patch('chat')
def test_extract_success(mock_chat):
    mock_chat.return_value = {
        'message': {'content': '{"action_items": ["Fix bug"]}'}
    }
    result = extract_action_items_llm("- Fix bug")
    assert result == ["Fix bug"]  # 精确匹配
```

### LLM 测试：语义断言

```python
@pytest.mark.slow
def test_extract_real_llm():
    text = "- Review the pull request"
    result = extract_action_items_llm(text)
    # 语义断言（允许变化）
    assert len(result) >= 1
    assert any("review" in item.lower() for item in result)
    # ❌ 不这样做：LLM 输出有变化
    # assert result == ["Review the pull request"]
```

---

## 🔧 Pytest 装饰器

### 标记慢速测试

```python
@pytest.mark.slow
def test_with_real_llm():
    """这个测试标记为慢速"""
    pass
```

### 运行特定测试

```bash
# 开发时：只运行快速测试
pytest week2/tests/ -m "not slow"

# 提交前：运行所有测试
pytest week2/tests/

# 只运行 LLM 集成测试
pytest week2/tests/ -m "slow"
```

---

## 📋 测试组织结构

```python
# test_extract.py

class TestExtractActionItemsLLM:
    """Mock 测试：快速、无依赖"""

    @patch('chat')
    def test_success_case(self, mock_chat):
        """测试成功提取"""
        pass

    @patch('chat')
    def test_error_handling(self, mock_chat):
        """测试错误处理"""
        pass


@pytest.mark.slow
class TestExtractActionItemsLLMReal:
    """集成测试：慢速、真实 LLM"""

    def test_basic_extraction(self):
        """测试基本提取"""
        pass
```

---

## 🎯 关键要点

| 要点 | 说明 |
|------|------|
| **Mock = 速度** | 70% 的测试应该毫秒级 |
| **Real LLM = 信心** | 20% 的测试验证实际集成 |
| **语义断言** | LLM 测试用含义断言，不精确匹配 |
| **标记慢速测试** | 使用 `@pytest.mark.slow` |
| **分层测试** | 单元 + 集成 + 边界 |

---

## 🔗 延伸阅读

详见 [../practice/testing_patterns.md](../practice/testing_patterns.md)
