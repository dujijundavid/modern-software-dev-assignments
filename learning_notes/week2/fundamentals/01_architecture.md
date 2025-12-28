# Week 2 架构设计

> FastAPI + SQLite 分层架构最佳实践

---

## 🏗️ 分层架构

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                  │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Router Layer (routers/)                        │    │
│  │  - @router.post("/extract")                     │    │
│  │  - Pydantic 验证请求/响应                        │    │
│  └───────────────┬─────────────────────────────────┘    │
│                  ↓                                       │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Service Layer (services/)                      │    │
│  │  - extract_action_items_llm()                  │    │
│  │  - 业务逻辑                                     │    │
│  └───────────────┬─────────────────────────────────┘    │
│                  ↓                                       │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Database Layer (db.py)                        │    │
│  │  - CRUD 操作                                   │    │
│  │  - 返回 dict，屏蔽实现细节                      │    │
│  └─────────────────────────────────────────────────┘    │
│                                                           │
└─────────────────────────────────────────────────────────┘
                            ↓
                    ┌───────────────┐
                    │  Ollama LLM    │
                    │  llama3.1:8b  │
                    └───────────────┘
```

### 设计原则

| 原则 | 说明 |
|------|------|
| **单一职责** | 每层只做自己的事 |
| **向上抽象** | 下层向上层提供简单接口 |
| **类型安全** | 尽早捕获错误 |

---

## 📦 Pydantic 数据验证

### 为什么需要 Schemas

**问题**：松散的类型导致运行时错误

```python
# ❌ Before: 松散的类型
@router.post("/extract")
def extract(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = str(payload.get("text", "")).strip()
    if not text:
        raise HTTPException(400, "text required")
    # 手动验证、手动转换...
    return {"items": [...]}
```

**解决方案**：Pydantic Schemas

```python
# ✅ After: 类型安全
from pydantic import BaseModel, Field

class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    save_note: bool = Field(default=False)

class ActionItemResponse(BaseModel):
    id: int
    text: str
    note_id: Optional[int]
    done: bool
    created_at: str

@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    # text 已自动验证！无需手动检查
    items = extract_action_items(payload.text)
    return ExtractResponse(items=[...])
```

### 好处

| 好处 | 说明 |
|------|------|
| **自动验证** | `min_length=1` 自动验证，无需手动 `if not text` |
| **IDE 补全** | 自动补全字段名和类型 |
| **OpenAPI 文档** | 自动生成 API 文档 |
| **类型安全** | 早期捕获错误，不是运行时才发现 |

---

## 🗄️ Database 层设计

### 设计决策：函数 vs 类

| 选择 | 适用场景 |
|------|---------|
| **函数** | 简单项目，直接明了 |
| **类** | 需要依赖注入、测试、多实例 |

对于 Week 2 项目：**函数式更直接**

### 返回 Dict 而非 sqlite3.Row

```python
# ❌ Before: 暴露底层实现
def get_note(note_id: int) -> Optional[sqlite3.Row]:
    return cursor.fetchone()

# Router 中需要手动转换
note = db.get_note(note_id)
return {"id": note["id"], "text": note["text"]}  # 重复逻辑

# ✅ After: 返回 dict
def get_note(note_id: int) -> Optional[dict]:
    row = cursor.fetchone()
    return dict(row) if row else None

# Router 直接使用
note = db.get_note(note_id)
return note  # 已经是 dict
```

### 统一错误处理

```python
class DatabaseError(Exception):
    """自定义异常，包装 sqlite 错误"""
    pass

def insert_note(content: str) -> int:
    try:
        cursor.execute("INSERT INTO notes ...")
        return cursor.lastrowid
    except sqlite3.Error as e:
        logger.error(f"DB error: {e}")
        raise DatabaseError(f"Failed to insert note: {e}") from e

# Router 中统一处理
@router.post("/notes")
def create_note(request: CreateNoteRequest):
    try:
        note_id = db.insert_note(request.text)
        return {"id": note_id}
    except DatabaseError as e:
        raise HTTPException(500, str(e))
```

### 好处

| 好处 | 说明 |
|------|------|
| **封装细节** | Router 不需要知道 sqlite3 存在 |
| **统一错误** | 统一的异常类型，便于处理 |
| **可替换性** | 日后切换数据库只需改这一层 |

---

## 📝 请求/响应流程

### 完整流程图

```
用户请求
   ↓
┌─────────────────────────────────────┐
│ 1. Pydantic 验证请求                  │
│    - text: min_length=1             │
│    - save_note: bool default False  │
└──────────────┬──────────────────────┘
               ↓ (验证通过)
┌─────────────────────────────────────┐
│ 2. Router 处理                       │
│    @router.post("/extract")          │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ 3. Service 调用 LLM                  │
│    extract_action_items_llm(text)   │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ 4. Database 存储（可选）             │
│    db.insert_action_item(...)        │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ 5. Pydantic 验证响应                  │
│    response_model=ExtractResponse    │
└──────────────┬──────────────────────┘
               ↓
         返回 JSON 给用户
```

### 代码示例

```python
# 1. Router
from fastapi import APIRouter, HTTPException
from app.schemas import ExtractRequest, ExtractResponse
from app.services import extract as svc

router = APIRouter()

@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    """提取任务项"""
    # 2. Service 调用
    items = svc.extract_action_items_llm(payload.text)

    # 3. 可选：保存到数据库
    if payload.save_note:
        note_id = svc.insert_note(payload.text, items)
    else:
        note_id = None

    # 4. 返回响应（Pydantic 自动验证）
    return ExtractResponse(items=items, note_id=note_id)

# 5. 错误处理
@router.exception_handler(DatabaseError)
async def db_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Database error", "detail": str(exc)}
    )
```

---

## 🔧 Logging 最佳实践

### 替换 print() 为 logging

```python
# ❌ Before
print(f"🔍 Processing {text}")
print(f"✅ Extracted {len(items)} items")

# ✅ After
import logging

logger = logging.getLogger(__name__)

logger.info(f"Extracting from text (len={len(text)})")
logger.debug(f"Items: {items}")
logger.error(f"Failed to extract: {e}")
```

### 为什么

| print() | logging |
|---------|---------|
| 无法控制级别 | DEBUG/INFO/WARNING/ERROR |
| 生产环境噪音多 | 可配置输出级别 |
| 只能输出到控制台 | 可输出到文件、监控系统 |
| 无法格式化 | 支持格式化、时间戳 |

### 配置示例

```python
# app/main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 生产环境
# logging.basicConfig(level=logging.WARNING)  # 减少噪音
```

---

## 📂 目录结构

```
week2/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry
│   ├── db.py                # Database layer
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── notes.py         # Notes endpoints
│   │   └── action_items.py  # Action items endpoints
│   └── services/
│       ├── __init__.py
│       └── extract.py       # LLM extraction logic
├── tests/
│   ├── conftest.py          # pytest fixtures
│   ├── test_notes.py
│   └── test_extract.py
└── data/
    └── database.db          # SQLite database
```

---

## 🎯 关键要点

### Before → After 对比

| 方面 | Before | After |
|------|--------|-------|
| **类型** | `Dict[str, Any]` | `ExtractRequest` |
| **验证** | 手动 `if not text` | Pydantic 自动验证 |
| **数据库** | 返回 `sqlite3.Row` | 返回 `dict` |
| **日志** | `print()` | `logging` |
| **错误** | 500 错误 | `DatabaseError` + HTTPException |

### 核心原则

1. **Pydantic First** - 所有 API 用 Pydantic 验证
2. **返回 Dict** - Database 层返回简单类型
3. **统一错误** - 自定义异常类
4. **使用 Logging** - 替换 print()
5. **分层清晰** - Router → Service → Database

---

## 🔗 延伸阅读

- [FastAPI 依赖注入](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Pydantic 数据验证](https://docs.pydantic.dev/latest/concepts/models/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [Python Logging](https://docs.python.org/3/howto/logging.html)
