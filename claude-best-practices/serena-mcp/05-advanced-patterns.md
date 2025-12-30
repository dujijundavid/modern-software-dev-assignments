# Serena 高级模式和技巧

> MCP 工具集成、性能优化和多项目管理策略

---

## 目录

1. [MCP 工具集成模式](#mcp-工具集成模式)
2. [依赖注入和上下文管理](#依赖注入和上下文管理)
3. [会话上下文管理](#会话上下文管理)
4. [性能优化技巧](#性能优化技巧)
5. [多项目管理策略](#多项目管理策略)
6. [故障排查指南](#故障排查指南)
7. [与 SuperClaude 配合](#与-superclaude-配合)

---

## MCP 工具集成模式

### 1.1 Memory 工具高级用法

#### 批量写入记忆

```python
# 在会话中批量记录多个决策

user: "我们做了几个技术决策"

AI:
# 1. 读取现有架构决策
existing = read_memory("architecture_decisions")

# 2. 追加新决策
new_content = existing + """

## Decision: Use Redis for Caching

**Date**: 2025-12-30

**Options Considered**:
1. In-memory caching
2. Memcached
3. Redis ✅ CHOSEN

**Rationale**:
- Built-in persistence
- Rich data structures
- Excellent performance

"""

# 3. 写回记忆
write_memory("architecture_decisions", new_content)

# 4. 更新相关记忆
code_patterns = read_memory("code_patterns")
code_patterns += """

## Redis Caching Pattern

```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def cache_get(key: str) -> str | None:
    return r.get(key)

def cache_set(key: str, value: str, ttl: int = 3600):
    r.setex(key, ttl, value)
```
"""

write_memory("code_patterns", code_patterns)

# 5. 记录到会话历史
session_log = read_memory("session_history")
session_log += f"\n\n## {datetime.now()}: Decided on Redis caching"
write_memory("session_history", session_log)
```

#### 搜索记忆内容

```yaml
# AI 工作流: 查找相关记忆

用户: "我们如何处理数据库连接？"

AI 流程:
  1. 列出所有记忆
     memories = list_memories()
     # ["architecture_decisions", "code_patterns", "tech_stack", ...]

  2. 搜索相关内容
     for memory in memories:
         content = read_memory(memory)
         if "database" in content.lower():
             print(f"Found in {memory}")

  3. 读取并综合
     decisions = read_memory("architecture_decisions")
     patterns = read_memory("code_patterns")

  4. 回答用户
     根据架构决策和代码模式回答
```

### 1.2 自定义 Memory 命名空间

#### 层次化命名

```
传统平面命名:
├── database_decisions.md
├── api_decisions.md
├── frontend_decisions.md
└── ...

层次化命名:
├── architecture/
│   ├── database.md
│   ├── api.md
│   └── frontend.md
├── development/
│   ├── workflow.md
│   └── testing.md
└── knowledge/
    ├── issues.md
    └── patterns.md
```

#### 使用子目录

```bash
# 创建层次化记忆结构
mkdir -p .serena/memories/architecture
mkdir -p .serena/memories/development
mkdir -p .serena/memories/knowledge

# 创建记忆
write_memory("architecture/database", content)
write_memory("development/workflow", content)
write_memory("knowledge/issues", content)
```

### 1.3 Memory 模板系统

#### 模板定义

```markdown
# .serena/memories/.templates/decision.md

# ADR-{number}: {Title}

**Date**: {YYYY-MM-DD}
**Status**: {Proposed | Accepted | Rejected}
**Decision Maker**: {Role}

---

## Context

{What problem are we solving?}

---

## Decision

{What are we deciding?}

---

## Options

### Option 1: {Title}
- **Pros**: {Pros}
- **Cons**: {Cons}

### Option 2: {Title} ✅ CHOSEN
- **Pros**: {Pros}
- **Cons**: {Cons}

---

## Consequences

- **Positive**: {Benefits}
- **Negative**: {Drawbacks}
```

#### 使用模板

```python
# AI 使用模板创建新记忆

template = read_memory(".templates/decision")

# 填充模板
new_decision = template.replace("{title}", "Use PostgreSQL")
new_decision = new_decision.replace("{date}", "2025-12-30")
new_decision = new_decision.replace("{number}", "001")
# ...

write_memory("architecture_decisions", new_decision)
```

---

## 依赖注入和上下文管理

### 2.1 Context 注入模式

#### 在 initial_prompt 中注入

```yaml
# .serena/project.yml

initial_prompt: |
  You are working on {project_name}.

  ============ Project Context ============
  {context_from_memories}

  ============ Tech Stack ============
  {tech_stack_info}
```

#### 动态加载上下文

```python
# MCP 工具: load_context

@mcp.tool()
async def load_context() -> str:
    """加载项目上下文"""
    context = []

    # 1. 项目愿景
    context.append(read_memory("project_context_and_goals"))

    # 2. 技术栈
    context.append(read_memory("tech_stack"))

    # 3. 代码模式
    context.append(read_memory("code_patterns"))

    return "\n\n---\n\n".join(context)
```

### 2.2 会话初始化模式

#### 标准 onboarding 流程

```python
@mcp.tool()
async def onboarding() -> str:
    """执行项目入职分析"""

    # 1. 检查是否已入职
    if check_onboarding_performed():
        return "Onboarding already completed. Loading context..."

    # 2. 分析项目结构
    structure = await analyze_project_structure()

    # 3. 识别技术栈
    tech_stack = await identify_tech_stack()

    # 4. 创建初始记忆
    await create_initial_memories(structure, tech_stack)

    # 5. 生成报告
    return generate_onboarding_report(structure, tech_stack)
```

#### 自动上下文恢复

```python
@mcp.tool()
async def prepare_for_new_conversation() -> str:
    """为新会话准备上下文"""

    # 1. 读取上次会话摘要
    last_session = read_memory("session_history")
    last_summary = extract_last_summary(last_session)

    # 2. 读取当前进度
    progress = read_memory("learning_progress")

    # 3. 读取待办事项
    todo = read_memory("session_context")

    return f"""
    ============ Session Context ============

    Last Session Summary:
    {last_summary}

    Current Progress:
    {progress}

    Next Actions:
    {todo}
    """
```

---

## 会话上下文管理

### 3.1 Session Context 记忆

#### 标准格式

```markdown
# session_context

> 当前会话的完整状态快照

---

## Current Focus

**Week**: 2
**Task**: 实现 LLM action item 提取
**Status**: 70% complete

---

## Today's Goals

- [x] 完成 ExtractService 实现
- [x] 添加单元测试
- [ ] 集成测试
- [ ] 文档更新

---

## Active Files

- `week2/app/services/extract.py` - 正在编辑
- `week2/tests/test_extract.py` - 需要更新

---

## Recent Decisions

1. 使用 Ollama llama3.1:8b 模型
2. JSON schema 强制输出
3. 过滤短于 6 个字符的 item

---

## Blockers

- None

---

## Next Session Priorities

1. 完成集成测试
2. 改进错误处理
3. 性能测试
```

### 3.2 会话总结模式

```python
@mcp.tool()
async def summarize_changes() -> str:
    """提供变更总结指令"""

    return """
    Please summarize the changes made in this session:

    1. **Files Modified**: List all files that were changed
    2. **Features Added**: Describe new features implemented
    3. **Bugs Fixed**: List bugs that were resolved
    4. **Decisions Made**: Record any architectural or design decisions
    5. **Learnings**: Capture any insights or lessons learned

    Format:
    - Use Markdown
- Include code snippets for key changes
    - Link to related memories
    - Update session_context
    """
```

#### 自动会话总结

```yaml
# 在会话结束时自动执行

用户: "结束会话"

AI 流程:
  1. 调用 summarize_changes
  2. 收集所有变更
  3. 生成总结
  4. 写入 session_history
  5. 更新 session_context
  6. 提示用户提交到 Git
```

### 3.3 状态检查点

```python
@mcp.tool()
async def save_checkpoint(name: str) -> str:
    """保存当前状态检查点"""

    # 1. 收集当前状态
    state = {
        "timestamp": datetime.now().isoformat(),
        "files": get_modified_files(),
        "tests": get_test_results(),
        "context": read_memory("session_context")
    }

    # 2. 写入检查点记忆
    checkpoint_name = f"checkpoints/{name}"
    write_memory(checkpoint_name, json.dumps(state))

    return f"Checkpoint '{name}' saved"

@mcp.tool()
async def restore_checkpoint(name: str) -> str:
    """恢复状态检查点"""

    # 1. 读取检查点
    checkpoint = read_memory(f"checkpoints/{name}")
    state = json.loads(checkpoint)

    # 2. 恢复上下文
    write_memory("session_context", state["context"])

    # 3. 显示差异
    show_diff(state["files"])

    return f"Checkpoint '{name}' restored from {state['timestamp']}"
```

---

## 性能优化技巧

### 4.1 记忆加载优化

#### 懒加载策略

```python
# ❌ 不推荐: 一次性加载所有记忆

def load_all_memories():
    memories = {}
    for name in list_memories():
        memories[name] = read_memory(name)
    return memories  # 可能很大

# ✅ 推荐: 按需加载

def get_memory(name: str) -> str:
    # 检查缓存
    if name in cache:
        return cache[name]

    # 按需加载
    content = read_memory(name)
    cache[name] = content
    return content
```

#### 记忆索引

```python
# 创建记忆索引

index = {
    "architecture": ["architecture_decisions", "tech_stack"],
    "development": ["code_patterns", "testing_strategies"],
    "workflow": ["development_workflow", "agent_communication_log"]
}

# 快速查找相关记忆
def get_memories_by_category(category: str) -> list[str]:
    return index.get(category, [])
```

### 4.2 增量更新策略

#### 追加模式

```python
# ❌ 不推荐: 每次重写整个文件

def update_architecture_decision(new_decision: str):
    all_decisions = read_memory("architecture_decisions")
    all_decisions += f"\n\n{new_decision}"
    write_memory("architecture_decisions", all_decisions)

# ✅ 推荐: 使用追加

def append_architecture_decision(new_decision: str):
    # 直接追加到文件
    with open(".serena/memories/architecture_decisions.md", "a") as f:
        f.write(f"\n\n{new_decision}")
```

### 4.3 缓存策略

#### 内存缓存

```python
from functools import lru_cache

@lru_cache(maxsize=32)
def get_memory_cached(name: str) -> str:
    """带缓存的记忆读取"""
    return read_memory(name)

# 清除缓存
def invalidate_cache():
    get_memory_cached.cache_clear()
```

#### 磁盘缓存

```bash
# .serena/cache/memories_index.json

{
  "last_update": "2025-12-30T10:00:00",
  "memories": {
    "architecture_decisions": {
      "size": 4096,
      "tags": ["architecture", "database"],
      "last_modified": "2025-12-30"
    }
  }
}
```

---

## 多项目管理策略

### 5.1 Monorepo 配置

```yaml
# .serena/project.yml

project_name: "monorepo"

# 多语言配置
languages:
  - python      # backend/
  - typescript  # frontend/

# 为不同子项目设置不同的 initial_prompt
initial_prompt: |
  You are working on a monorepo with:
  - backend/ (Python/FastAPI)
  - frontend/ (TypeScript/React)

  Check .serena/memories/ for project-specific patterns.
```

#### 子项目记忆

```
.serena/memories/
├── backend/
│   ├── architecture_decisions.md
│   ├── code_patterns.md
│   └── testing_strategies.md
├── frontend/
│   ├── architecture_decisions.md
│   ├── code_patterns.md
│   └── testing_strategies.md
└── shared/
    └── common_patterns.md
```

### 5.2 多仓库共享配置

#### 共享记忆仓库

```bash
# 创建共享配置仓库
mkdir serena-shared-config
cd serena-shared-config

# 初始化
git init

# 创建共享模板
mkdir -p templates/memories

# 提交到 GitHub
git remote add origin git@github.com:org/serena-shared-config.git
git push -u origin main
```

#### 在项目中引用

```bash
# 使用 git subtree 包含共享配置
git subtree add --prefix=.serena/shared \
  git@github.com:org/serena-shared-config.git main

# 更新共享配置
git subtree pull --prefix=.serena/shared \
  git@github.com:org/serena-shared-config.git main
```

### 5.3 环境特定配置

```yaml
# .serena/project.yml (基础配置)
languages:
  - python

# .serena/project.dev.yml (开发环境)
languages:
  - python
  - typescript

initial_prompt: |
  Development environment with hot reload enabled.

# .serena/project.prod.yml (生产环境)
languages:
  - python

initial_prompt: |
  Production environment. Focus on stability and security.
```

---

## 故障排查指南

### 6.1 诊断命令

```bash
#!/bin/bash
# scripts/serena-doctor.sh

echo "=== Serena Diagnostics ==="

# 1. 检查目录结构
echo "[1] Checking .serena structure..."
test -d .serena || echo "ERROR: .serena/ not found"
test -f .serena/project.yml || echo "ERROR: project.yml not found"
test -d .serena/memories || echo "ERROR: memories/ not found"

# 2. 验证 YAML 语法
echo "[2] Validating YAML..."
if command -v yq &> /dev/null; then
  yq eval . .serena/project.yml > /dev/null
  if [ $? -eq 0 ]; then
    echo "✓ YAML syntax valid"
  else
    echo "✗ YAML syntax error"
  fi
fi

# 3. 检查 Git 追踪状态
echo "[3] Checking Git tracking..."
if [ -d .git ]; then
  if git check-ignore -q .serena/project.yml; then
    echo "✗ project.yml is ignored"
  else
    echo "✓ project.yml is tracked"
  fi

  if git check-ignore -q .serena/cache/; then
    echo "✓ cache/ is ignored"
  else
    echo "✗ cache/ is not ignored"
  fi
fi

# 4. 检查记忆文件
echo "[4] Analyzing memories..."
MEMORY_COUNT=$(ls -1 .serena/memories/*.md 2>/dev/null | wc -l)
echo "Found $MEMORY_COUNT memory files"

# 5. 检查语言服务器
echo "[5] Language server status..."
# (需要 MCP 工具)

echo "=== Diagnostics Complete ==="
```

### 6.2 常见问题

| 问题 | 症状 | 解决方案 |
|------|------|----------|
| **配置未生效** | AI 不使用新模式 | 重启语言服务器 |
| **记忆未同步** | 新设备看不到记忆 | 检查 .gitignore 配置 |
| **缓存过大** | cache/ 目录很大 | 清理并重新生成 |
| **冲突频繁** | 总是合并冲突 | 使用分支策略 |

---

## 与 SuperClaude 配合

### 7.1 PM Agent 集成

```markdown
# 在 /sc:pm 中使用 Serena

## Session Start Protocol

1. **Restore Context**: Read .serena/memories/session_context
2. **Load Progress**: Read .serena/memories/learning_progress
3. **Check Last Session**: Read .serena/memories/session_history
4. **Generate Report**: Summarize current state

## Session End Protocol

1. **Write Summary**: Update session_history with today's work
2. **Update Progress**: Mark completed items in learning_progress
3. **Save Context**: Write current state to session_context
4. **Commit Changes**: Suggest git commit for memories
```

### 7.2 与 MCP 工具配合

```yaml
# SuperClaude MCP 服务器配置

mcp-servers:
  - serena        # Serena 内置
  - sequential    # 串行执行
  - context7      # 上下文管理
  - magic         # 文件操作增强

# 使用 Serena 内存指导其他 MCP 服务器
```

### 7.3 高级工作流示例

```yaml
场景: 使用 Serena + SuperClaude 实现功能

1. PM Agent 启动
   ├─ 读取 .serena/memories/session_context
   ├─ 恢复上次会话状态
   └─ 确定今天任务

2. 用户请求: "实现用户认证"

3. PM Agent 委托
   ├─ @api-architect: 设计 API
   │  └─ 读取 .serena/memories/architecture_decisions
   ├─ @fastapi-expert: 实现
   │  └─ 读取 .serena/memories/code_patterns
   ├─ @python-testing-expert: 测试
   │  └─ 读取 .serena/memories/testing_strategies
   └─ @code-reviewer: 审查
      └─ 更新 .serena/memories/agent_communication_log

4. PM Agent 记录
   ├─ 写入 .serena/memories/architecture_decisions
   ├─ 更新 .serena/memories/session_context
   └─ 提交变更到 Git
```

---

## 相关文档

| 主题 | 文档 |
|------|------|
| **架构概览** | [01-architecture-overview.md](01-architecture-overview.md) |
| **配置指南** | [02-configuration-guide.md](02-configuration-guide.md) |
| **内存系统** | [03-memory-system-design.md](03-memory-system-design.md) |
| **跨机器同步** | [04-cross-machine-sync.md](04-cross-machine-sync.md) |

---

## 完成学习

恭喜！你已经完成了 Serena MCP 最佳实践指南的全部学习。

### 掌握的技能

- [x] 理解 Serena 系统架构
- [x] 配置 project.yml
- [x] 设计和管理内存系统
- [x] 跨机器 Git 协作
- [x] 高级 MCP 工具集成
- [x] 性能优化策略
- [x] 多项目管理
- [x] 与 SuperClaude 配合

### 下一步

1. **实战项目**: 在你的项目中应用 Serena
2. **分享经验**: 贡献你的记忆模板
3. **社区参与**: 在 GitHub 讨论 Serena 最佳实践

---

**祝你在 AI 工程之旅中取得成功！**
