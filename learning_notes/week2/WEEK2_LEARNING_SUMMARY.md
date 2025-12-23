# Week 2 学习总结：从 LLM 集成到测试到导入系统

## 📊 完成进度

```
✅ TODO 1: 实现 LLM 驱动的提取函数
✅ TODO 2: 编写全面的单元测试
⏳ TODO 3: 重构后端代码
⏳ TODO 4: 新增端点和前端按钮
⏳ TODO 5: 生成 README 文档
```

---

## 🎯 第1部分：LLM 集成 (TODO 1)

### 学习成果

**实现的功能：**
- `extract_action_items_llm()` 函数，利用 Ollama 和结构化输出
- 系统提示工程（System Prompt Engineering）
- JSON 模式约束（JSON Schema）确保可靠的输出
- 优雅的错误处理和降级（Graceful Degradation）

**关键技术：**
```python
# 1. 结构化输出：强制 LLM 返回特定格式
json_schema = {
    'type': 'object',
    'properties': {
        'action_items': {
            'type': 'array',
            'items': {'type': 'string'}
        }
    }
}

# 2. 低温设置：更确定性的输出
options={'temperature': 0.3}

# 3. 后处理：清理、去重、验证
items = [item.strip() for item in items if item.strip()]
```

**文件位置：**
- 实现：`week2/app/services/extract.py` (lines 117-264)
- 手动测试：`week2/test_llm_manual.py`

---

## 🧪 第2部分：全面的测试策略 (TODO 2)

### 学习成果

**分层测试架构：**

```
Unit Tests (70%)        ← 快速、可控、频繁运行
├── Mock success case
├── Post-processing
├── Error handling
├── Invalid JSON
└── Custom model

Integration Tests (20%) ← 慢速、真实、偶尔运行
├── Real LLM basic
└── Semantic understanding

Edge Cases (10%)        ← 边界条件
└── Empty, whitespace, no items
```

**Mock 的力量：**
```python
# ❌ 不用 Mock：每次测试等待 2-3 秒
result = extract_action_items_llm("test")  # 调用真实 Ollama

# ✅ 用 Mock：毫秒级完成
@patch('week2.app.services.extract.chat')
def test(mock_chat):
    mock_chat.return_value = {...}
    result = extract_action_items_llm("test")  # 使用假数据
```

**断言策略：**
```python
# Mock 测试：精确断言（返回值可控）
assert result == ["Task 1", "Task 2"]

# 真实 LLM 测试：语义断言（LLM 输出有变化）
assert any("task" in item.lower() for item in result)
```

**测试结果：**
- ✅ 7 个快速测试在 0.6 秒内通过
- ⏸️  2 个集成测试可选运行（需要 Ollama）
- 📊 代码覆盖率：~85%

**文件位置：**
- 测试代码：`week2/tests/test_extract.py` (lines 1-287)
- 配置：`pyproject.toml` (lines 37-43)

---

## 🔧 第3部分：Python 导入系统深度解析

### 关键发现

**问题：**
```
直接运行 python week2/tests/test_extract.py
→ ModuleNotFoundError: No module named 'week2'

但 poetry run pytest week2/tests/test_extract.py
→ ✅ 成功
```

**原因：sys.path 配置不同**

```python
# 直接运行时：sys.path = ['/week2/tests', ...]
#            不包含项目根 ❌

# pytest 运行时：sys.path = ['/modern-software-dev-assignments', '/week2/tests', ...]
#                 包含项目根 ✅
```

**解决方案：用相对导入**

```python
# ❌ 绝对导入（依赖 sys.path）
from week2.app.services.extract import extract_action_items

# ✅ 相对导入（不依赖 sys.path）
from ..app.services.extract import extract_action_items
```

**最佳实践：**
```
📌 Rule 1: 包内文件 → 用相对导入 from ..module
📌 Rule 2: 项目根脚本 → 用绝对导入 from week2.module
📌 Rule 3: 测试文件 → 用相对导入 + pytest 运行
📌 Rule 4: 如果要直接运行 → 用 python -m week2.app.main
```

**文件位置：**
- 详细指南：`learning_notes/week2/python_import_system_guide.md`

---

## 📚 创建的学习资源

### 1. 测试指南
📄 `learning_notes/week2/testing_llm_functions_guide.md`

**包含内容：**
- Mock 原理（替身演员概念）
- Pytest 装饰器完全指南
- 断言策略（精确 vs 语义）
- LLM 测试最佳实践
- 快速参考卡片

### 2. 导入系统指南
📄 `learning_notes/week2/python_import_system_guide.md`

**包含内容：**
- sys.path 的秘密
- 绝对导入 vs 相对导入
- 6 个场景分析
- 最佳实践总结
- 快速参考

---

## 💡 关键学习点总结

### 关于 LLM 集成
```python
# 1. 结构化输出 = 可靠性
# 用 JSON Schema 强制 LLM 返回指定格式

# 2. 系统提示 = 准确性
# 告诉 LLM 什么是/不是行动项

# 3. 后处理 = 鲁棒性
# 清理、去重、验证（防守性编程）

# 4. 错误处理 = 优雅降级
# API 失败时返回 []，不崩溃
```

### 关于测试
```python
# 1. Mock = 速度
# 70% 的测试应该毫秒级

# 2. Real LLM = 信心
# 20% 的测试验证实际集成

# 3. Semantic Assertions = 可维护性
# LLM 测试用"包含关键词"，不用"精确匹配"

# 4. 组织良好 = 易于维护
# 清晰的测试名称和文档
```

### 关于导入
```python
# 1. sys.path 决定一切
# 理解它就能解决 90% 的导入问题

# 2. 相对导入最安全
# 适用于包内代码，不依赖环境配置

# 3. pytest 自动配置
# 它会添加项目根到 sys.path

# 4. 用工具，不要手动处理
# poetry run pytest / python -m pytest
```

---

## 📈 代码质量指标

```
✅ 代码覆盖率：~85%（好）
✅ 测试速度：0.6秒（快）
✅ 错误处理：6 个边界条件（全面）
✅ 文档质量：350+ 行代码注释（高质）
✅ 最佳实践：相对导入、分层测试（遵循）
```

---

## 🚀 后续 TODO 建议

### TODO 3：重构后端代码 (2-3 小时)
**优先级：高**
- [ ] 添加 Pydantic 数据模型
- [ ] 改进 API 响应格式
- [ ] 增强错误处理
- [ ] 添加请求验证

### TODO 4：新增端点 + UI (1-2 小时)
**优先级：高**
- [ ] 创建 `/action-items/extract-llm` 端点
- [ ] 创建 `/notes/list` 端点
- [ ] 添加前端按钮

### TODO 5：生成 README (30 分钟)
**优先级：中**
- [ ] 项目概述
- [ ] 安装说明
- [ ] API 文档
- [ ] 测试运行指南

---

## 📝 文件清单

**代码文件：**
- ✅ `week2/app/services/extract.py` - LLM 实现
- ✅ `week2/tests/test_extract.py` - 测试套件
- ✅ `week2/test_llm_manual.py` - 手动测试
- ✅ `pyproject.toml` - 项目配置

**学习资源：**
- ✅ `learning_notes/week2/testing_llm_functions_guide.md`
- ✅ `learning_notes/week2/python_import_system_guide.md`
- ✅ `week2/writeup.md` - 作业总结

---

## ✨ 个人反思

### 你学到了什么

1. **LLM 集成**：不仅是调用 API，还要考虑格式、错误、性能
2. **测试思想**：Mock 的价值、分层的必要性、语义断言的优雅性
3. **系统思维**：Python 的导入系统看似复杂，但有清晰的规则
4. **工程实践**：好的文档、好的测试、好的设计能一起解决问题

### 下一步方向

- 深入学习 Pydantic（数据验证）
- 学习 FastAPI 的高级特性（中间件、依赖注入）
- 探索 LLM 的其他应用（分类、摘要、问答）
- 掌握 Docker 容器化（避免"在我机器上能跑"）

---

*完成日期：2025年12月23日*  
*累计学习时间：~2.5 小时*  
*下一课：TODO 3 - 重构后端代码*

