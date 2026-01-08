# Week 6 安全漏洞修复计划

> **创建日期**: 2026-01-08
> **状态**: 待执行
> **目标**: 修复3个CRITICAL级别的安全漏洞

---

## 📋 修复概览

| # | 漏洞类型 | 严重程度 | 文件 | 行号 | 修复策略 |
|---|---------|---------|------|-----|---------|
| 1 | SQL注入 | CRITICAL | week6/backend/app/routers/notes.py | 71-79 | 使用参数化查询 |
| 2 | eval代码执行 | CRITICAL | week6/backend/app/routers/notes.py | 102-105 | 删除端点 |
| 3 | 命令注入 | CRITICAL | week6/backend/app/routers/notes.py | 108-113 | 删除端点 |

---

## 🔍 Phase 1: 代码探索完成

### 当前代码结构

**文件**: `week6/backend/app/routers/notes.py`

**已可用的导入**:
```python
from sqlalchemy import asc, desc, select, text
from sqlalchemy.orm import Session
```

**数据库模式**:
- 使用 `get_db()` 依赖注入
- SQLAlchemy Session对象
- 自动commit/rollback/close

**Note模型**:
```python
class Note(Base, TimestampMixin):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
```

### 发现的额外问题

探索时还发现了2个额外的安全漏洞（不在Semgrep报告中）：

| # | 漏洞 | 端点 | 行号 |
|---|------|------|------|
| 4 | SSRF (服务器端请求伪造) | `/debug/fetch` | 116-122 |
| 5 | 路径遍历 | `/debug/read` | 125-131 |

---

## 📐 Phase 2: 修复设计

### 修复方案

#### 修复1: SQL注入 (`/unsafe-search`)

**当前危险代码** (第69-92行):
```python
@router.get("/unsafe-search", response_model=list[NoteRead])
def unsafe_search(q: str, db: Session = Depends(get_db)) -> list[NoteRead]:
    sql = text(
        f"""
        SELECT id, title, content, created_at, updated_at
        FROM notes
        WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'
        ORDER BY created_at DESC
        LIMIT 50
        """
    )
    rows = db.execute(sql).all()
    # ...
```

**修复后安全代码**:
```python
from sqlalchemy import or_

@router.get("/unsafe-search", response_model=list[NoteRead])
def unsafe_search(q: str, db: Session = Depends(get_db)) -> list[NoteRead]:
    # 使用ORM查询，自动防止SQL注入
    notes = db.query(Note).filter(
        or_(
            Note.title.like(f"%{q}%"),
            Note.content.like(f"%{q}%")
        )
    ).order_by(Note.created_at.desc()).limit(50).all()

    return [NoteRead.model_validate(note) for note in notes]
```

**为什么安全**:
- SQLAlchemy自动参数化查询
- 用户输入只作为数据值，不作为SQL代码
- 类型安全的ORM操作

#### 修复2-5: 删除所有调试端点

**需要删除的端点** (第102-131行):

```python
# ❌ 删除: eval代码执行 (第102-105行)
@router.get("/debug/eval")
def debug_eval(expr: str) -> dict[str, str]:
    result = str(eval(expr))  # noqa: S307
    return {"result": result}

# ❌ 删除: 命令注入 (第108-113行)
@router.get("/debug/run")
def debug_run(cmd: str) -> dict[str, str]:
    import subprocess
    completed = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {"returncode": str(completed.returncode), "stdout": completed.stdout, "stderr": completed.stderr}

# ❌ 删除: SSRF漏洞 (第116-122行)
@router.get("/debug/fetch")
def debug_fetch(url: str) -> dict[str, str]:
    from urllib.request import urlopen
    with urlopen(url) as res:
        body = res.read(1024).decode(errors="ignore")
    return {"body": body}

# ❌ 删除: 路径遍历 (第125-131行)
@router.get("/debug/read")
def debug_read(path: str) -> dict[str, str]:
    try:
        content = open(path, "r").read(1024)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"snippet": content}
```

**删除理由**:
1. 调试端点不应存在于生产环境
2. 这些端点没有任何安全价值
3. 删除是最安全的修复方式
4. 符合最小攻击面原则

---

## 🎯 Phase 3: 实施步骤

### Step 1: 修复SQL注入漏洞

**文件**: `week6/backend/app/routers/notes.py`

**操作**:
1. 在文件顶部添加导入（如果不存在）: `from sqlalchemy import or_`
2. 找到 `unsafe_search` 函数 (第69-92行)
3. 替换函数体，使用安全的ORM查询

**详细代码变更**:
```python
# 在文件顶部导入区域添加
from sqlalchemy import or_

# 替换 unsafe_search 函数
@router.get("/unsafe-search", response_model=list[NoteRead])
def unsafe_search(q: str, db: Session = Depends(get_db)) -> list[NoteRead]:
    """
    安全的搜索功能 - 使用参数化查询防止SQL注入

    Args:
        q: 搜索关键词
        db: 数据库会话

    Returns:
        匹配的笔记列表
    """
    # 使用SQLAlchemy ORM进行安全查询
    # like() 方法会自动转义特殊字符，防止SQL注入
    notes = db.query(Note).filter(
        or_(
            Note.title.like(f"%{q}%"),
            Note.content.like(f"%{q}%")
        )
    ).order_by(Note.created_at.desc()).limit(50).all()

    # 转换为Pydantic模型
    return [NoteRead.model_validate(note) for note in notes]
```

### Step 2: 删除调试端点

**文件**: `week6/backend/app/routers/notes.py`

**操作**:
1. 找到第102-131行
2. 删除以下4个端点:
   - `debug_eval` (第102-105行)
   - `debug_run` (第108-113行)
   - `debug_fetch` (第116-122行)
   - `debug_read` (第125-131行)

**删除的代码块**:
```python
# ========== 删除以下所有代码 ==========

@router.get("/debug/eval")
def debug_eval(expr: str) -> dict[str, str]:
    result = str(eval(expr))  # noqa: S307
    return {"result": result}


@router.get("/debug/run")
def debug_run(cmd: str) -> dict[str, str]:
    import subprocess

    completed = subprocess.run(cmd, shell=True, capture_output=True, text=True)  # noqa: S602,S603
    return {"returncode": str(completed.returncode), "stdout": completed.stdout, "stderr": completed.stderr}


@router.get("/debug/fetch")
def debug_fetch(url: str) -> dict[str, str]:
    from urllib.request import urlopen

    with urlopen(url) as res:  # noqa: S310
        body = res.read(1024).decode(errors="ignore")
    return {"body": body}


@router.get("/debug/read")
def debug_read(path: str) -> dict[str, str]:
    try:
        content = open(path, "r").read(1024)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc))
    return {"snippet": content}
```

### Step 3: 验证修复

**操作**:
1. 进入week6目录: `cd week6`
2. 激活Python环境（如果使用conda）
3. 运行测试: `pytest backend/tests/ -v`
4. 确保所有测试通过
5. 启动服务器验证功能: `uvicorn backend.app.main:app --reload`

---

## ✅ Phase 4: 验证计划

### 测试检查清单

#### 功能测试

1. **搜索功能测试**:
   ```bash
   # 测试正常搜索
   curl "http://localhost:8000/notes/unsafe-search?q=python"

   # 测试SQL注入尝试（应该失败）
   curl "http://localhost:8000/notes/unsafe-search?q='; DROP TABLE notes; --"
   ```

2. **调试端点已删除**:
   ```bash
   # 这些应该返回404 Not Found
   curl "http://localhost:8000/notes/debug/eval?expr=1+1"
   curl "http://localhost:8000/notes/debug/run?cmd=ls"
   curl "http://localhost:8000/notes/debug/fetch?url=http://example.com"
   curl "http://localhost:8000/notes/debug/read?path=/etc/passwd"
   ```

#### 自动化测试

```bash
# 运行所有测试
cd week6
pytest backend/tests/ -v

# 运行特定测试文件
pytest backend/tests/test_notes.py -v

# 查看测试覆盖率
pytest backend/tests/ --cov=backend/app --cov-report=term-missing
```

#### 重新扫描Semgrep

```bash
# 从week6目录运行
semgrep scan --config auto --include="*.py" .

# 预期结果：
# - SQL注入: 应该消失
# - eval执行: 应该消失
# - 命令注入: 应该消失
```

---

## 📊 预期结果

### 修复前Semgrep扫描结果

```
6 Code Findings (all blocking)
├── python.fastapi.security.wildcard-cors.wildcard-cors (main.py:24)
├── python.sqlalchemy.security.audit.avoid-sqlalchemy-text.avoid-sqlalchemy-text (notes.py:71)
├── python.lang.security.audit.eval-detected.eval-detected (notes.py:104)
├── python.lang.security.audit.subprocess-shell-true.subprocess-shell-true (notes.py:112)
├── python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected (notes.py:120)
└── javascript.browser.security.insecure-document-method.insecure-document-method (app.js:14)
```

### 修复后Semgrep扫描结果

```
2 Code Findings (remaining, not in scope)
├── python.fastapi.security.wildcard-cors.wildcard-cors (main.py:24)
└── javascript.browser.security.insecure-document-method.insecure-document-method (app.js:14)
```

**说明**: CORS和XSS不在本周修复范围内（作业只要求3个）

---

## 🔐 安全原则

### 遵循的安全原则

1. **最小权限原则**: 删除不必要的调试端点
2. **防御深度**: 使用ORM而不是手动SQL拼接
3. **白名单优于黑名单**: 删除所有调试端点而不是尝试"安全化"它们
4. **默认安全**: 使用框架提供的安全特性（SQLAlchemy ORM）

### 不会做的事情

❌ **不会**: 尝试"安全化" eval端点
- 原因: eval()没有安全用法
- 即使使用asteval也有绕过风险

❌ **不会**: 尝试"安全化" shell命令执行
- 原因: shell命令执行本质上危险
- 白名单也难以保证安全

❌ **不会**: 只修复3个漏洞，忽略额外的2个
- 原因: 删除端点的成本很低
- 一次性清理所有调试代码

---

## 📝 需要修改的文件

| 文件 | 操作 | 行号 |
|------|------|------|
| `week6/backend/app/routers/notes.py` | 修复SQL注入 | 69-92 |
| `week6/backend/app/routers/notes.py` | 删除eval端点 | 102-105 |
| `week6/backend/app/routers/notes.py` | 删除run端点 | 108-113 |
| `week6/backend/app/routers/notes.py` | 删除fetch端点 | 116-122 |
| `week6/backend/app/routers/notes.py` | 删除read端点 | 125-131 |

---

## 📚 参考资料

### 学习笔记
- [learning_notes/week6/security_vulnerabilities_explained.md](../learning_notes/week6/security_vulnerabilities_explained.md) - 详细的漏洞原理讲解

### Semgrep扫描结果
- [semgrep_scan_results.md](semgrep_scan_results.md) - 完整的扫描报告

### 作业要求
- [week6_assignment.md](week6_assignment.md) - Week 6作业要求

---

## ✅ 执行检查清单

在开始修复前，确认:
- [ ] 已阅读学习笔记，理解漏洞原理
- [ ] 已查看Semgrep扫描结果
- [ ] 已理解修复方案
- [ ] 已同意修复策略

修复完成后:
- [ ] 代码已修改
- [ ] 测试已通过
- [ ] Semgrep重新扫描，确认漏洞已修复
- [ ] 服务器已启动，手动验证功能正常
- [ ] 已更新week6_writeup.md

---

> **计划创建者**: Claude (AI Coding Assistant)
> **最后更新**: 2026-01-08
> **状态**: ✅ 计划完成，等待执行
