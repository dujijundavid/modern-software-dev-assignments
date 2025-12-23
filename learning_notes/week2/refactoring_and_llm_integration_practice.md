# Week 2: API 重构与 LLM 集成实战总结

> **学习目标**: 通过重构现有 FastAPI 项目，理解专业代码组织方式、类型安全、LLM 集成最佳实践

---

## 📋 任务背景

**项目**: Action Item Extractor (FastAPI + SQLite)
- 初始状态: 功能可用但结构松散
- 目标: 专业化重构 + 添加 LLM 智能提取

---

## Part 1: 代码重构 (TODO 3)

### 🎯 重构目标

将"能跑的代码"升级为"可维护的专业代码"

### 问题诊断思路

#### 1. API Contracts 缺失
**症状**:
```python
# ❌ Before: 松散的类型
@router.post("/extract")
def extract(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = str(payload.get("text", "")).strip()
    # 手动验证、手动转换...
```

**问题**:
- 无类型检查 → 运行时才发现错误
- 手动验证 → 重复代码、易遗漏
- 手动构造响应 → 容易拼错字段名

#### 2. Database 层混乱
**症状**:
```python
# 返回 sqlite3.Row，router 需要手动转换
def get_note(note_id: int) -> Optional[sqlite3.Row]:
    return cursor.fetchone()

# Router 中
note = db.get_note(note_id)
return {"id": note["id"], ...}  # 重复转换逻辑
```

**问题**:
- 暴露底层实现细节（sqlite3.Row）
- Router 和 DB 层耦合
- 无统一错误处理

#### 3. 配置和日志混乱
```python
# ❌ 硬编码路径
DB_PATH = "/path/to/db.sqlite"

# ❌ print() 到处都是
print(f"🔍 Processing: {text}")
```

---

### 💡 重构方案设计

#### 设计原则

```
分层架构:
┌─────────────────────┐
│   Router Layer      │ ← Pydantic models: 类型安全入口
├─────────────────────┤
│   Service Layer     │ ← 业务逻辑 (extract.py)
├─────────────────────┤
│   Database Layer    │ ← 返回 dict, 屏蔽实现细节
└─────────────────────┘
```

**核心思想**:
1. **单一职责**: 每层只做自己的事
2. **向上抽象**: 下层向上层提供简单接口
3. **类型安全**: 尽早捕获错误

---

### 🔨 实施步骤

#### Step 1: 定义 Pydantic Schemas

**为什么先做这个?**
- Schema 是"契约"，定义了数据流
- 有了 schema 才能改 router

```python
# week2/app/schemas.py
from pydantic import BaseModel, Field

class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=1)
    save_note: bool = Field(default=False)

class ActionItemResponse(BaseModel):
    id: int
    text: str
    note_id: Optional[int]
    done: bool
    created_at: str
```

**好处**:
- ✅ `min_length=1` 自动验证，无需手动 `if not text`
- ✅ IDE 自动补全
- ✅ 自动生成 OpenAPI 文档

---

#### Step 2: Router 使用 Schemas

```python
# ❌ Before
def extract(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = str(payload.get("text", "")).strip()
    if not text:
        raise HTTPException(400, "text required")
    return {"items": [...]}

# ✅ After
@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    # text 已自动验证！
    items = extract_action_items(payload.text)
    return ExtractResponse(items=[...])
```

**关键点**:
- `response_model` 确保返回值符合 schema
- Pydantic 自动做所有验证
- 代码更简洁、更安全

---

#### Step 3: Database 层返回 Dict

**设计决策**: 函数 vs 类？
- **选择函数**: 当前项目简单，函数式更直接
- 如果需要依赖注入/测试，再重构为类

```python
# ❌ Before: 暴露 sqlite3.Row
def get_note(note_id: int) -> Optional[sqlite3.Row]:
    return cursor.fetchone()

# ✅ After: 返回 dict
def get_note(note_id: int) -> Optional[dict]:
    row = cursor.fetchone()
    return dict(row) if row else None
```

**统一错误处理**:
```python
class DatabaseError(Exception):
    """自定义异常，包装 sqlite 错误"""
    pass

def insert_note(content: str) -> int:
    try:
        # ... SQL 操作
    except sqlite3.Error as e:
        logger.error(f"DB error: {e}")
        raise DatabaseError(f"Failed: {e}") from e
```

**好处**:
- Router 不需要知道 sqlite3 存在
- 统一的错误类型，便于上层处理
- 日后切换数据库只需改这一层

---

#### Step 4: Logging 替代 Print

```python
# ❌ Before
print(f"🔍 Processing {text}")
print(f"✅ Extracted {len(items)} items")

# ✅ After
import logging
logger = logging.getLogger(__name__)

logger.info(f"Extracting from text (len={len(text)})")
logger.debug(f"Items: {items}")
```

**为什么**:
- `print()` 无法控制级别（生产环境噪音）
- `logging` 支持 DEBUG/INFO/ERROR，可配置
- 可以输出到文件、发送到监控系统

---

### 📊 重构效果对比

| 维度 | Before | After |
|------|--------|-------|
| **类型安全** | Dict[str, Any] | Pydantic models |
| **输入验证** | 手动 if 检查 | 自动验证 + 清晰错误 |
| **DB 耦合** | Router 知道 sqlite3.Row | Router 只知道 dict |
| **错误处理** | 原始 sqlite 异常 | DatabaseError 包装 |
| **日志** | print() 到处都是 | logging 分级控制 |
| **可测试性** | 难（依赖具体类型） | 易（清晰接口） |

---

### 🧪 测试策略

创建 `test_refactoring.py` 验证改进：

```python
def test_schema_validation():
    """测试 Pydantic 自动验证"""
    with pytest.raises(ValidationError):
        ExtractRequest(text="")  # min_length=1 应失败

def test_db_returns_dict():
    """测试 DB 层返回类型"""
    note = db.get_note(1)
    assert isinstance(note, dict)  # 不是 sqlite3.Row
    assert "id" in note
```

**测试覆盖**:
- Schema 验证 (3 tests)
- DB 返回类型 (4 tests)  
- Router 集成 (3 tests)
- 端到端流程 (1 test)

---

## Part 2: LLM 集成与调优 (TODO 1 & 4)

### 🎯 问题: 规则式提取的局限

**启发式规则**:
```python
def _is_action_line(line: str) -> bool:
    # 只能识别格式
    if line.startswith("-"):  # bullet
        return True
    if "todo:" in line.lower():  # keyword
        return True
```

**问题**:
- ❌ "help" → 提取（但太模糊）
- ❌ "你是谁" → 提取（不是 action item）
- ❌ "deploy app" (无 bullet) → 不提取
- **根本问题**: 只看格式，不理解语义

---

### 💡 LLM 方案设计

#### 核心思路

```
用户输入 → LLM 理解语义 → 结构化输出 → 后处理过滤
```

**为什么用 Structured Output?**

```python
# ❌ 不用 structured output
prompt = "Extract action items, return as JSON"
response = llm(prompt)  
# 可能返回: "Here are the items:\n- item1\n- item2"
# 需要复杂正则解析 😫

# ✅ 用 structured output
json_schema = {
    'type': 'object',
    'properties': {
        'action_items': {'type': 'array', 'items': {'type': 'string'}}
    }
}
response = chat(..., format=json_schema)
# 保证返回: {"action_items": ["item1", "item2"]} ✅
```

**好处**:
- 无需正则解析
- 类型保证（不会返回非 JSON）
- 减少 LLM 幻觉

---

### 🔧 实现细节

#### 1. System Prompt 设计

```python
system_prompt = """You are an expert assistant that extracts actionable tasks.

**Extract these:**
- Concrete, actionable items (things to DO)
- "Set up database" ✓
- "Fix bug #123" ✓

**Ignore these:**
- Greetings, context ("The meeting was productive")
- Questions ("What should we do?")
- Statements ("Database is set up")

Remove formatting: bullets, checkboxes, TODO: prefixes
"""
```

**关键点**:
- 明确什么是/不是 action item
- 给例子（few-shot learning）
- 说明输出格式

---

#### 2. Temperature 调优

**实验发现**:

| Temperature | 行为 | 问题 |
|-------------|------|------|
| 0.3 (初始) | 稍有随机性 | 相同输入有时提取 "help"，有时不提取 |
| 0.1 (改进) | 高度确定性 | 相同输入稳定输出 ✓ |

**从日志观察到**:
```
输入: "-help\n- develop pydantic"
第1次: ["develop pydantic"]         # 过滤了 help
第2次: ["help", "develop pydantic"]  # 包含了 help ❌
```

**解决**: `temperature=0.1` 大幅提高一致性

---

#### 3. 后处理过滤

**为什么需要?**
- LLM 有时仍会提取模糊项（如 "help"）
- 加一层规则过滤更保险

```python
# Post-processing filter
for item in llm_output:
    words = item.split()
    if len(words) == 1 and len(item) < 6:
        # 过滤单字且 < 6 字符的模糊词
        continue  # "help", "go", "fix" 被过滤
    cleaned.append(item)
```

**过滤规则**:
- 单词 < 6 字符 → 过滤（"help", "go"）
- 问句（ending with ?） → 过滤
- 纯符号 → 过滤

---

### 📊 效果对比

#### 测试用例

```python
test_input = "-help\n- set up database\n- go"
```

| 方法 | 结果 | 评价 |
|------|------|------|
| 规则式 | ["help", "set up database", "go"] | ❌ 过多误报 |
| LLM (temp=0.3) | 不稳定 | ❌ 一致性差 |
| LLM (temp=0.1) + 过滤 | ["set up database"] | ✅ 准确 |

---

### 🎓 经验总结

#### LLM 集成最佳实践

1. **Structured Output 是必须的**
   - 省去解析噩梦
   - 提高可靠性

2. **Temperature 要调优**
   - 创意任务: 0.7-0.9
   - 提取任务: 0.1-0.3
   - 关键: 用实际数据测试

3. **后处理不能省**
   - LLM 不是 100% 可靠
   - 加规则兜底

4. **Prompt 工程**
   - 明确定义任务边界
   - 给正反例
   - 迭代改进

---

## Part 3: 前后端集成 (TODO 4)

### 🎯 需求

- 前端两个按钮: "Extract (Rules)" vs "Extract (LLM)"
- 后端两个 endpoint

### 实现

#### 后端: 添加 LLM endpoint

```python
@router.post("/extract-llm", response_model=ExtractResponse)
def extract_llm(payload: ExtractRequest) -> ExtractResponse:
    items = extract_action_items_llm(payload.text)
    # ... 保存到数据库
    return ExtractResponse(items=[...])
```

#### 前端: 重构提取逻辑

```javascript
// 提取为可复用函数
async function extractItems(endpoint) {
    const res = await fetch(endpoint, {
        method: 'POST',
        body: JSON.stringify({ text, save_note })
    });
    // ... 渲染结果
}

// 两个按钮共用
btnRules.addEventListener('click', () => 
    extractItems('/action-items/extract'));
    
btnLLM.addEventListener('click', () => 
    extractItems('/action-items/extract-llm'));
```

**设计思想**: DRY (Don't Repeat Yourself)

---

## 🎓 AI Builder 能力提升

### 1. 系统性思考能力

**Before**: "代码能跑就行"
**After**: 考虑：
- 类型安全（编译时捕获错误）
- 可测试性（解耦、清晰接口）
- 可维护性（日志、错误处理）

### 2. 分层架构理解

```
User Input
    ↓
Router (类型验证、路由)
    ↓
Service (业务逻辑、LLM 调用)
    ↓
Database (数据持久化)
```

**关键**: 每层有清晰职责，向上提供简单接口

### 3. LLM 工程实践

- **不是调用就完事**: 需要 prompt 工程、温度调优、后处理
- **监控和迭代**: 从日志发现问题（温度不一致）→ 调优
- **防御式编程**: 即使有 structured output，也要 try-catch

### 4. 测试驱动改进

```python
# 先写测试定义期望行为
def test_schema_rejects_empty():
    with pytest.raises(ValidationError):
        ExtractRequest(text="")

# 再实现（Pydantic 自动验证）
class ExtractRequest(BaseModel):
    text: str = Field(min_length=1)
```

**好处**: 测试即文档，重构不怕破坏

---

## 🛠️ 工具链和工作流

### 开发流程

```bash
# 1. 分析问题 → 设计方案
# 2. 写测试
poetry run pytest week2/tests/test_refactoring.py -v

# 3. 实现功能
# 4. 重跑测试确保通过
poetry run pytest week2/tests/ -v

# 5. 启动服务验证
poetry run uvicorn week2.app.main:app --reload

# 6. 浏览器手动测试
open http://127.0.0.1:8000
```

### 调试技巧

1. **日志分级**: 
   ```python
   logger.debug("详细信息")  # 开发时看
   logger.info("关键流程")   # 生产保留
   logger.error("错误")      # 告警
   ```

2. **类型检查**: 
   ```bash
   mypy week2/app/
   ```

3. **API 文档**: 
   - 访问 `/docs` 看自动生成的文档
   - 直接在浏览器测试 API

---

## 📚 进阶学习路径

### 1. 当前项目可改进的地方

- [ ] 添加配置管理 (pydantic-settings)
- [ ] 全局异常处理器
- [ ] 日志输出到文件
- [ ] 添加 API 认证
- [ ] 数据库迁移工具 (Alembic)

### 2. 扩展阅读

- **FastAPI 官方文档**: https://fastapi.tiangolo.com/
- **Pydantic**: https://docs.pydantic.dev/
- **Ollama Structured Output**: https://ollama.com/blog/structured-outputs
- **Clean Architecture**: Robert C. Martin

### 3. 类似项目实践

用相同模式实现：
- 发票信息提取器（图片 → LLM → 结构化数据）
- 会议纪要生成器（音频 → 转录 → LLM 总结）
- 代码审查助手（代码 → LLM 分析 → 建议）

---

## 💡 关键收获

### 技术层面

1. **类型安全的价值**: Pydantic 让错误在编码时暴露，而非运行时
2. **分层的意义**: 每层职责单一，修改影响范围小
3. **LLM 不是魔法**: 需要 engineering（prompt、temperature、后处理）

### 思维层面

1. **重构不是一次性**: 先让它工作 → 再让它优雅 → 持续改进
2. **测试是信心来源**: 有测试才敢重构
3. **日志是运行时的眼睛**: 没有日志，生产问题是盲目的

### AI Builder 心态

1. **系统性思考**: 不只是"调 API"，而是设计整个系统
2. **迭代改进**: 从日志发现问题 → 分析 → 改进 → 验证
3. **文档意识**: 代码注释、测试、README 都是文档

---

## 🎯 检验清单

完成 Week 2 后，你应该能：

- [ ] 解释为什么用 Pydantic 而非 Dict[str, Any]
- [ ] 说明 DB 层返回 dict vs Row 的权衡
- [ ] 设计一个 LLM prompt 并调优 temperature
- [ ] 从服务器日志发现不一致问题并解决
- [ ] 写测试验证重构没有破坏功能
- [ ] 画出项目的分层架构图

---

**下一步**: Week 3 - MCP Server 开发，学习构建可被 AI 调用的工具！
