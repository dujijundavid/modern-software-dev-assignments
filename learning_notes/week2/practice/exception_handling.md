# Claude Code 交互学习笔记：异常处理重构

> **日期**: 2024-12-23
> **主题**: 使用 Claude Code 进行异常处理重构
> **目标**: 学习如何与 AI 编码助手高效协作

---

## 背景

在 week2 项目中，我选中了 `db.py` 中的异常类定义：

```python
class DatabaseError(Exception):
    """Custom exception for database operations."""
    pass


class NotFoundError(Exception):
    """Exception for resource not found errors."""
    pass
```

提问："这个设置是否合理？为什么都是 pass？"

这引发了 Claude Code 对整个代码库的深度分析和重构。

---

## 第一阶段：代码审查（Code Review）

### Claude 的分析方法

Claude 没有直接回答"是否合理"，而是：

1. **启动 Explore Agent** - 全面扫描 week2 目录结构
2. **识别模式** - 查找所有异常使用场景
3. **建立上下文** - 理解架构和问题关联

### 发现的核心问题

| 问题 | 严重程度 | 说明 |
|------|----------|------|
| `NotFoundError` 未使用 | 高 | 定义了但从未 raise/catch |
| 空 `pass` 异常 | 中 | 没有携带上下文信息 |
| 缺少 HTTP 映射 | 高 | 异常不转换为合适的 HTTP 状态码 |
| 代码重复 | 中 | 响应构建逻辑重复 3 次 |

**关键洞察**：Claude 不是看单个文件，而是理解整个系统的异常流。

---

## 第二阶段：需求澄清（AskUserQuestion）

### Claude 的提问策略

在开始重构前，Claude 提出了两个关键问题：

```
1. 重构的深度范围是什么？
   - 最小改动：仅修复核心问题
   - 中度重构：修复核心 + 改进异常类
   - 全面重构：完整异常层次 + Repository 模式

2. 是否需要保持向后兼容的 API 接口？
   - 保持兼容：只改内部实现
   - 允许优化：可以改进错误响应格式
```

### 我的回答
- **范围**: 最小改动
- **API**: 允许优化

**学习点**：AI 不会假设你的需求，而是主动澄清。这避免了过度工程化。

---

## 第三阶段：计划设计（Plan Agent）

### Claude 创建的计划

```python
# 计划文件: .claude/plans/declarative-spinning-quill.md

1. 增强 DatabaseError 和 NotFoundError（添加属性）
2. get_note() 抛出 NotFoundError 而非返回 None
3. mark_action_item_done() 检查 rowcount 并抛出 NotFoundError
4. schemas.py 添加 from_dict() 类方法
5. main.py 添加全局异常处理器
6. 简化 routers（移除手动 None 检查）
```

### 计划的特点

| 特点 | 说明 |
|------|------|
| **具体** | 每个改动都有文件名和行号范围 |
| **可验证** | 明确测试验证步骤 |
| **最小化** | 只改必要的内容 |

**学习点**：好的计划让执行变得机械化和可预测。

---

## 第四阶段：执行与测试

### 执行过程

Claude 按计划依次修改文件：

```python
# 1. db.py - 增强异常类
class DatabaseError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class NotFoundError(Exception):
    def __init__(self, resource_type: str, resource_id: int):
        self.resource_type = resource_type
        self.resource_id = resource_id
        message = f"{resource_type} with id {resource_id} not found"
        super().__init__(message)
```

```python
# 2. db.py - 修改 get_note()
def get_note(note_id: int) -> dict:  # 返回类型不再是 Optional
    if row is None:
        raise NotFoundError("note", note_id)  # 抛出而非返回 None
    return dict(row)
```

```python
# 3. main.py - 全局异常处理器
@app.exception_handler(db.NotFoundError)
async def notfound_error_handler(request, exc: db.NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})
```

### 测试结果

```
26 passed in 3.51s
```

其中一个测试需要更新（从期望 None 改为期望异常）：

```python
# Before
def test_db_get_note_nonexistent_returns_none():
    result = db.get_note(999999)
    assert result is None

# After
def test_db_get_note_nonexistent_returns_none():
    with pytest.raises(db.NotFoundError, match="note with id 999999 not found"):
        db.get_note(999999)
```

---

## 核心学习点

### 1. 最小改动原则（Minimal Changes）

**问题**: 有很多可以改进的地方（Repository 模式、完整异常层次等）

**Claude 的选择**: 只改用户批准的范围

```python
# ❌ 没有做的：完整异常层次
class ValidationError(Exception): ...  # 未添加
class ConflictError(Exception): ...   # 未添加

# ✅ 实际做的：增强现有异常
class NotFoundError(Exception):
    def __init__(self, resource_type: str, resource_id: int): ...
```

**学习点**：
- 避免"既然在这不如把那也改了"的诱惑
- 每个改动应该有明确的理由
- 可测试的小改动 > 大爆炸式重构

---

### 2. 异常设计的演进

#### 阶段 1: 空 pass（初始状态）

```python
class NotFoundError(Exception):
    pass
```

**问题**：
- 不知道是什么资源没找到
- 不知道是哪个 ID
- 需要解析错误消息字符串

#### 阶段 2: 带上下文（重构后）

```python
class NotFoundError(Exception):
    def __init__(self, resource_type: str, resource_id: int):
        self.resource_type = resource_type  # "note", "action item"
        self.resource_id = resource_id      # 999
        message = f"{resource_type} with id {resource_id} not found"
        super().__init__(message)
```

**好处**：
- 可编程访问：`exc.resource_type`, `exc.resource_id`
- 一致的错误消息格式
- 便于日志聚合（按 resource_type 分组）

#### 阶段 3: 未来可能的扩展（未实现）

```python
# 可能的未来改进
class NotFoundError(DatabaseError):
    """继承自 DatabaseError 建立层次"""
    pass
```

---

### 3. 错误流的变化

#### Before: 分散的错误处理

```
db.get_note(999)
    ↓
returns None
    ↓
router checks `if row is None`
    ↓
router raises HTTPException(404)
```

**问题**：
- 每个 router 都要写 if 检查
- 容易遗漏某个端点
- 错误消息不一致

#### After: 集中的错误处理

```
db.get_note(999)
    ↓
raises NotFoundError("note", 999)
    ↓
global handler catches it
    ↓
returns JSONResponse(404, {"detail": "note with id 999 not found"})
```

**好处**：
- router 代码更简洁
- 错误处理逻辑集中在一处
- 所有端点行为一致

---

### 4. 消除代码重复

#### 问题: 响应构建重复 3 次

```python
# 在 extract() 中
return ExtractResponse(
    items=[
        ActionItemResponse(
            id=item_id,
            text=created_items_map[item_id]["text"],
            note_id=created_items_map[item_id]["note_id"],
            done=bool(created_items_map[item_id]["done"]),
            created_at=created_items_map[item_id]["created_at"],
        )
        for item_id in ids
    ],
)

# 在 list_all() 中 - 类似的重复
# 在 extract_llm() 中 - 又是同样的重复
```

#### 解决: from_dict() 工厂方法

```python
# schemas.py 中添加
class ActionItemResponse(BaseModel):
    @classmethod
    def from_dict(cls, data: dict) -> "ActionItemResponse":
        return cls(
            id=data["id"],
            text=data["text"],
            note_id=data.get("note_id"),
            done=bool(data["done"]),
            created_at=data["created_at"],
        )

# 现在使用
return ExtractResponse(
    items=[
        ActionItemResponse.from_dict(created_items_map[item_id])
        for item_id in ids
    ],
)
```

**好处**：
- 一次修改，到处生效
- 类型转换逻辑集中
- 代码更简洁

---

## 与 Claude Code 协作的模式

### 1. 提问的艺术

**好的提问**:
- ❌ "这个代码有问题吗？"（太模糊）
- ✅ "这个设置是否合理？为什么都是 pass？"（具体、指出观察）

**Claude 的响应**:
- 深度分析而非表面回答
- 提供上下文和替代方案
- 主动询问澄清问题

---

### 2. 计划-执行循环

```
你的问题
    ↓
Claude 分析代码库
    ↓
Claude 提出澄清问题
    ↓
你回答（范围、约束）
    ↓
Claude 创建详细计划
    ↓
你批准计划
    ↓
Claude 执行修改
    ↓
运行测试验证
```

**关键**：每一步都有确认点，避免 AI 跑偏。

---

### 3. 测试驱动验证

**Claude 的做法**：
1. 修改代码
2. 立即运行测试
3. 如果失败，分析原因
4. 更新测试或代码

```python
# 测试失败：期望 None，实际得到异常
# Claude 识别：这是新行为的预期结果
# Claude 更新：测试改为期望异常
```

---

## 实用技巧

### 技巧 1: 利用 AskUserQuestion

当 Claude 问你问题时，认真回答：

```
Q: 重构深度？
A1: "全面重构" → Claude 会做很多改动
A2: "最小改动" → Claude 只改核心问题
```

选择影响工作量范围。

---

### 技巧 2: 阅读 Claude 的计划

在执行前，Claude 会保存计划到：
```
.claude/plans/declarative-spinning-quill.md
```

**建议**：
- 阅读计划了解将要发生什么
- 如有问题，可以在批准前提出

---

### 技巧 3: 测试失败是正常的

重构后测试可能失败，这不一定是坏事：

```python
# 测试期望旧行为（返回 None）
assert result is None

# 代码改变了行为（抛出异常）
raise NotFoundError("note", note_id)
```

**Claude 的处理**：
- 识别这是行为改变，不是 bug
- 更新测试以匹配新行为

---

## 扩展思考

### 如果要做全面重构会怎样？

Claude 的 Plan Agent 提到了"全面重构"选项，包括：

1. **完整异常层次**
```python
Exception
├── DatabaseError
│   ├── NotFoundError
│   └── ConflictError
├── ValidationError
└── ServiceUnavailableError
```

2. **Repository 模式**
```python
class NoteRepository(ABC):
    @abstractmethod
    def get(self, id: int) -> Note: ...

class SQLiteNoteRepository(NoteRepository):
    def get(self, id: int) -> Note: ...
```

3. **依赖注入**
```python
def get_notes(repo: NoteRepository): ...  # 而非直接用 db
```

**但这次选择了"最小改动"**，这是正确的选择：
- 先让异常系统工作起来
- 后续可以根据需要迭代

---

## 总结

### 与 Claude Code 协作的关键

1. **提出具体问题** - 指出你观察到的现象
2. **明确需求范围** - 回答澄清问题时说明约束
3. **审查计划** - 执行前了解将要发生什么
4. **信任但验证** - 运行测试确保结果正确

### 从这次交互学到

| 方面 | 学习 |
|------|------|
| **代码审查** | AI 能发现人眼容易忽略的模式（未使用的异常、重复代码） |
| **计划优先** | 先设计再执行，减少返工 |
| **最小改动** | 小步快跑，每步都可验证 |
| **测试驱动** | 测试是重构的信心来源 |
| **异常设计** | 带上下文的异常 > 空异常 |
| **集中处理** | 全局异常处理器 > 分散的 if 检查 |

---

## 后续改进方向

基于这次重构，未来可以考虑：

1. **添加更多异常类型**
```python
class ValidationError(DatabaseError):
    """输入验证失败"""
    pass

class ConflictError(DatabaseError):
    """资源冲突（如外键约束）"""
    pass
```

2. **添加请求 ID 追踪**
```python
class NotFoundError(Exception):
    def __init__(self, resource_type: str, resource_id: int, request_id: str = None):
        self.request_id = request_id  # 便于日志追踪
```

3. **添加国际化支持**
```python
message = get_localized_message(
    f"{resource_type}.not_found",
    locale="zh-CN",
    args={"id": resource_id}
)
```

---

## 参考资料

- **FastAPI 异常处理**: https://fastapi.tiangolo.com/tutorial/handling-errors/
- **Python 异常最佳实践**: https://docs.python.org/3/tutorial/errors.html
- **Claude Code 文档**: https://github.com/anthropics/claude-code
