# Serena 架构概览

> 深入理解 Serena 的系统架构、核心组件和设计哲学

---

## 目录

1. [系统架构图](#系统架构图)
2. [核心组件详解](#核心组件详解)
3. [设计哲学](#设计哲学)
4. [与传统配置的区别](#与传统配置的区别)
5. [使用场景](#使用场景)

---

## 系统架构图

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Serena 系统架构                                      │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                        Claude Code 主代理                            │  │
│  │                                                                      │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │  │
│  │  │ 会话管理器    │  │ 上下文加载器  │  │ 工具路由器    │              │  │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │  │
│  │         │                 │                 │                      │  │
│  └─────────┼─────────────────┼─────────────────┼──────────────────────┘  │
│            │                 │                 │                          │
└────────────┼─────────────────┼─────────────────┼──────────────────────────┘
             │                 │                 │
             ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            .serena/ 目录                                     │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        project.yml                                  │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐        │   │
│  │  │ languages      │  │ encoding       │  │ ignored_paths  │        │   │
│  │  │ [python]       │  │ utf-8          │  │ []             │        │   │
│  │  └────────────────┘  └────────────────┘  └────────────────┘        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      memories/ (持久化内存)                           │   │
│  │  ┌───────────────────┐  ┌───────────────────┐  ┌─────────────────┐  │   │
│  │  │ project_context   │  │ architecture_     │  │ code_patterns   │  │   │
│  │  │ _and_goals.md     │  │ decisions.md      │  │ .md             │  │   │
│  │  └───────────────────┘  └───────────────────┘  └─────────────────┘  │   │
│  │  ┌───────────────────┐  ┌───────────────────┐  ┌─────────────────┐  │   │
│  │  │ development_      │  │ testing_          │  │ tech_stack.md   │  │   │
│  │  │ workflow.md       │  │ strategies.md     │  │                 │  │   │
│  │  └───────────────────┘  └───────────────────┘  └─────────────────┘  │   │
│  │  ┌───────────────────┐  ┌───────────────────┐  ┌─────────────────┐  │   │
│  │  │ common_issues_    │  │ agent_            │  │ learning_       │  │   │
│  │  │ solutions.md      │  │ communication_    │  │ progress.md     │  │   │
│  │  │                   │  │ log.md            │  │                 │  │   │
│  │  └───────────────────┘  └───────────────────┘  └─────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        cache/ (机器特定)                             │   │
│  │  ┌───────────────────┐  ┌───────────────────┐                       │   │
│  │  │ language_server_  │  │ symbol_cache      │                       │   │
│  │  │ state.json        │  │ .json             │                       │   │
│  │  └───────────────────┘  └───────────────────┘                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        .gitignore                                    │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │ /cache                                                      │    │   │
│  │  │  ↑ 排除机器特定缓存，共享其他所有内容                          │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Git 远程仓库                                       │
│                                                                              │
│  ✓ project.yml          ✓ memories/             ✗ cache/                    │
│  ✓ .gitignore            ✓ .serena/.gitignore                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 MCP 工具集成架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        MCP (Model Context Protocol)                          │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         Serena MCP Server                           │   │
│  │                                                                      │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │                      Memory Operations                        │   │   │
│  │  │                                                              │   │   │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │   │   │
│  │  │  │ write_memory │  │ read_memory  │  │list_memories │      │   │   │
│  │  │  └──────────────┘  └──────────────┘  └──────────────┘      │   │   │
│  │  │                                                              │   │   │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │   │   │
│  │  │  │delete_memory │  │update_memory │  │search_memory │      │   │   │
│  │  │  └──────────────┘  └──────────────┘  └──────────────┘      │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  │                                                                      │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │                      Configuration                           │   │   │
│  │  │                                                              │   │   │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │   │   │
│  │  │  │get_config    │  │set_config    │  │validate_     │      │   │   │
│  │  │  │              │  │              │  │config        │      │   │   │
│  │  │  └──────────────┘  └──────────────┘  └──────────────┘      │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  │                                                                      │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │                      Session Management                      │   │   │
│  │  │                                                              │   │   │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │   │   │
│  │  │  │onboarding    │  │prepare_for_  │  │summarize_    │      │   │   │
│  │  │  │              │  │new_conversation│changes        │      │   │   │
│  │  │  └──────────────┘  └──────────────┘  └──────────────┘      │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│                          ↕ stdio / SSE                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AI Agent (Claude/GPT)                                │
│                                                                              │
│  通过 MCP 工具调用:                                                           │
│  - "从内存中读取架构决策"                                                     │
│  - "记录这个错误解决方案"                                                     │
│  - "恢复上次会话的上下文"                                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.3 语言服务器架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Language Server Integration                          │
│                                                                              │
│  project.yml 配置:                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  languages:                                                          │   │
│  │    - python          ← 启动 Python Language Server (Pyright)        │   │
│  │    - typescript      ← 启动 TypeScript Language Server              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                  │                                          │
│                                  ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Language Server Process                        │   │
│  │                                                                      │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │ 代码补全      │  │ 语法检查      │  │ 跳转定义      │              │   │
│  │  │ Completion   │  │ Diagnostics  │  │ Go to Def    │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  │                                                                      │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │ 查找引用      │  │ 符号搜索      │  │ 代码重构      │              │   │
│  │  │ Find Refs    │  │ Symbol Search│  │ Refactoring  │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                  │                                          │
│                                  ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Cache (/cache)                                │   │
│  │  ┌───────────────────┐  ┌───────────────────┐                       │   │
│  │  │ language_server_  │  │ symbol_cache.json │                       │   │
│  │  │ state.json        │  │                   │                       │   │
│  │  └───────────────────┘  └───────────────────┘                       │   │
│  │   ↑ 机器特定，不提交到 Git                                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 核心组件详解

### 2.1 project.yml 配置系统

#### 完整配置结构

```yaml
# ============ 语言服务器配置 ============
languages:
  - python              # 第一个是默认语言
  # - typescript        # 多语言按顺序匹配
  # - go
  # - rust

# ============ 文件编码 ============
encoding: "utf-8"

# ============ Git 忽略策略 ============
ignore_all_files_in_gitignore: true
# 说明: 是否使用项目根目录的 .gitignore 来忽略文件

# ============ 额外忽略路径 ============
ignored_paths:
  - "tmp/**"           # 临时目录
  - "build/**"         # 构建产物
  - "dist/**"          # 分发文件
  - "**/*.min.js"      # 压缩文件

# ============ 只读模式 ============
read_only: false
# 说明: 禁用所有编辑工具，保护重要项目

# ============ 工具排除列表 ============
excluded_tools: []
# 说明: 禁用的 MCP 工具列表
# 推荐: 保持为空，让 AI 自主选择

# ============ 初始提示词 ============
initial_prompt: |
  You are working on {project_name}.
  Follow the patterns documented in .serena/memories/code_patterns.md
  For testing, refer to .serena/memories/testing_strategies.md

# ============ 项目名称 ============
project_name: "modern-software-dev-assignments"

# ============ 可选工具包含列表 ============
included_optional_tools: []
```

#### 关键配置说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `languages` | `string[]` | `[]` | 启动的语言服务器列表 |
| `encoding` | `string` | `"utf-8"` | 项目文件编码 |
| `ignore_all_files_in_gitignore` | `boolean` | `false` | 是否使用项目 .gitignore |
| `ignored_paths` | `string[]` | `[]` | 额外忽略的路径模式 |
| `read_only` | `boolean` | `false` | 是否启用只读模式 |
| `excluded_tools` | `string[]` | `[]` | 禁用的工具名称列表 |
| `initial_prompt` | `string` | `""` | 会话开始时的提示词 |
| `project_name` | `string` | 必填 | 项目标识名称 |

### 2.2 memories/ 内存系统

#### 内存文件分类

```yaml
项目级内存 (Project Memories):
  ├── project_context_and_goals.md      # 项目愿景和目标
  ├── architecture_decisions.md         # 技术决策记录
  ├── tech_stack.md                     # 技术栈定义
  └── weekly_assignments.md             # 每周作业规划

开发级内存 (Development Memories):
  ├── code_patterns.md                  # 代码模式规范
  ├── development_workflow.md           # 开发工作流
  └── testing_strategies.md             # 测试策略

知识级内存 (Knowledge Memories):
  ├── common_issues_solutions.md        # 常见问题解决方案
  ├── llm_integration_patterns.md       # LLM 集成模式
  └── security_considerations.md        # 安全考虑

协作级内存 (Collaboration Memories):
  ├── agent_communication_log.md        # AI 代理交互日志
  ├── learning_progress.md              # 学习进度追踪
  └── session_history.md                # 会话历史记录
```

#### 标准化内存模板

```markdown
# {Memory Title}

> {Brief description of this memory's purpose}

---

## Metadata

| 字段 | 值 |
|------|-----|
| **创建时间** | {YYYY-MM-DD} |
| **最后更新** | {YYYY-MM-DD} |
| **维护者** | {Role/Agent} |
| **状态** | {Active/Archived} |
| **相关记忆** | {Links} |

---

## Purpose

{Why this memory exists}

---

## Content

{Main content of the memory}

---

## Examples

### Example 1: {Title}

**Context**: {When this applies}

**Solution**: {What to do}

```yaml
# Code/Config example
```

---

## Related Resources

- [Related Memory 1](../path/to/memory.md)
- [Related Memory 2](../path/to/memory.md)

---

## Changelog

| 日期 | 变更 | 作者 |
|------|------|------|
| {YYYY-MM-DD} | {Change description} | {Author} |
```

### 2.3 .gitignore 策略

#### 标准配置

```gitignore
# .serena/.gitignore

# 只排除机器特定的缓存
/cache

# 确保其他所有内容被追踪:
# - project.yml ✓
# - memories/*.md ✓
# - .gitignore ✓
```

#### 工作原理

```
项目根目录 .gitignore:
  [...其他规则...]

  # 默认忽略 .serena/
  .serena/

  # 但明确排除 cache 子目录
  !.serena/
  .serena/cache/

    ↓

结果:
  .serena/project.yml          ✓ 被追踪
  .serena/.gitignore            ✓ 被追踪
  .serena/memories/*.md         ✓ 被追踪
  .serena/cache/                ✗ 被忽略
  .serena/cache/**              ✗ 被忽略
```

### 2.4 MCP 工具集成

#### Memory 工具集

```python
# Serena MCP Server 提供的工具

# 1. write_memory
@mcp.tool()
async def write_memory(name: str, content: str) -> str:
    """
    写入或更新项目记忆

    Args:
        name: 记忆文件名（不含 .md 扩展名）
        content: 记忆内容（Markdown 格式）

    Returns:
        操作结果消息
    """

# 2. read_memory
@mcp.tool()
async def read_memory(name: str) -> str:
    """
    读取项目记忆

    Args:
        name: 记忆文件名

    Returns:
        记忆内容
    """

# 3. list_memories
@mcp.tool()
async def list_memories() -> list[str]:
    """
    列出所有项目记忆

    Returns:
        记忆文件名列表
    """

# 4. delete_memory
@mcp.tool()
async def delete_memory(name: str) -> str:
    """
    删除项目记忆

    Args:
        name: 记忆文件名

    Returns:
        操作结果消息
    """
```

#### Session 工具集

```python
# 会话管理工具

# 1. onboarding
@mcp.tool()
async def onboarding() -> str:
    """
    执行项目入职分析
    识别项目结构和基本任务
    """

# 2. prepare_for_new_conversation
@mcp.tool()
async def prepare_for_new_conversation() -> str:
    """
    为新会话准备上下文
    从历史记忆中恢复必要信息
    """

# 3. summarize_changes
@mcp.tool()
async def summarize_changes() -> str:
    """
    提供变更总结指令
    帮助记录会话中的更改
    """
```

### 2.5 语言服务器支持

#### 支持的语言

```yaml
# 完整支持列表
languages:
  - al                 # Ada
  - bash               # Bash/Shell
  - csharp             # C# (.NET)
  - cpp                # C/C++
  - clojure            # Clojure
  - dart               # Dart
  - elixir             # Elixir
  - elm                # Elm
  - erlang             # Erlang
  - fortran            # Fortran
  - go                 # Go
  - haskell            # Haskell
  - java               # Java
  - javascript         # JavaScript (使用 typescript)
  - julia              # Julia
  - kotlin             # Kotlin
  - lua                # Lua
  - markdown           # Markdown
  - nix                # Nix
  - perl               # Perl
  - php                # PHP
  - python             # Python
  - python_jedi        # Python (Jedi)
  - r                  # R
  - rego               # Rego
  - ruby               # Ruby
  - ruby_solargraph    # Ruby (Solargraph)
  - rust               # Rust
  - scala              # Scala
  - swift              # Swift
  - terraform          # Terraform
  - typescript         # TypeScript
  - typescript_vts     # TypeScript (VTS)
  - yaml               # YAML
  - zig                # Zig
```

#### 语言服务器选择策略

```
文件: app/main.py
    ↓
按顺序检查 languages 列表:
    1. python?     YES → 使用 Pyright
    2. typescript? (跳过)

文件: components/Button.tsx
    ↓
按顺序检查 languages 列表:
    1. python?     NO
    2. typescript? YES → 使用 TypeScript Language Server
```

---

## 设计哲学

### 3.1 核心原则

| 原则 | 说明 | 实现 |
|------|------|------|
| **显式优于隐式** | 配置应该清晰可见 | project.yml 而非隐藏配置 |
| **可共享优于隔离** | 多设备协作是第一需求 | Git 追踪配置和记忆 |
| **持久化优于临时** | 知识应该被保存 | memories/ 而非会话变量 |
| **工具化优于手动** | 自动化重复任务 | MCP 工具接口 |
| **分层优于平铺** | 清晰的层次结构 | memories/ 分类组织 |

### 3.2 与传统配置的区别

#### 传统方式 (VS Code Settings)

```
.vscode/
├── settings.json         # 本地设置，不共享
├── launch.json          # 调试配置
└── extensions.json      # 扩展推荐

问题:
  - 每个设备需要手动配置
  - 配置散落在多个文件
  - 无法持久化项目知识
  - AI 无法访问配置
```

#### Serena 方式

```
.serena/
├── project.yml          # 集中配置，Git 共享
├── memories/            # 持久化知识库
└── .gitignore          # 明确共享策略

优势:
  ✓ 一次配置，多设备同步
  ✓ AI 可读可写
  ✓ 知识持续积累
  ✓ 与 MCP 深度集成
```

### 3.3 设计权衡

| 决策 | 选择 | 理由 |
|------|------|------|
| **配置格式** | YAML | 人类可读，AI 易解析 |
| **记忆格式** | Markdown | 可读性强，支持格式化 |
| **共享机制** | Git | 已有的版本控制基础设施 |
| **工具接口** | MCP | 标准化协议，跨平台 |

---

## 使用场景

### 4.1 场景矩阵

| 场景 | Serena 解决方案 | 传统方式 |
|------|----------------|----------|
| **新设备设置** | Git pull，立即可用 | 手动配置 VS Code、扩展 |
| **记录决策** | 写入架构决策记忆 | 散落在 Git commit 中 |
| **跨会话恢复** | AI 自动读取记忆 | 手动重新解释上下文 |
| **团队协作** | 共享配置和记忆 | 各自维护配置 |
| **知识积累** | 持续增长的记忆库 | 知识分散难以查找 |

### 4.2 典型工作流

#### 工作流 1: 项目初始化

```bash
# 1. 创建项目
mkdir my-project && cd my-project
git init

# 2. 初始化 Serena
mkdir -p .serena/memories
cat > .serena/project.yml << 'EOF'
languages: [python]
encoding: "utf-8"
project_name: "my-project"
EOF

# 3. 设置 Git 忽略
cat > .serena/.gitignore << 'EOF'
/cache
EOF

# 4. 创建基础记忆
cat > .serena/memories/project_context.md << 'EOF'
# Project Context

## Vision
{Project vision}

## Goals
- {Goal 1}
- {Goal 2}
EOF

# 5. 提交
git add .serena/
git commit -m "feat: add Serena configuration"
```

#### 工作流 2: 记录架构决策

```yaml
用户: "我们决定使用 FastAPI 而非 Flask"

AI 流程:
  1. 读取现有架构决策记忆
  2. 追加新决策
  3. 使用标准化模板格式化
  4. 写入 .serena/memories/architecture_decisions.md

结果:
  ✓ 决策被持久化
  ✓ 未来 AI 可以访问
  ✓ Git 版本控制
  ✓ 团队成员可见
```

#### 工作流 3: 跨会话恢复

```yaml
会话 1 (Day 1):
  用户: "实现用户认证功能"
  AI: 设计方案，开始实现
  AI: 写入 session/context 记忆

会话 2 (Day 2):
  AI: 自动读取 session/context
  AI: "昨天我们实现了认证功能的一半..."
  用户: "继续实现"
  AI: 基于昨天的进度继续
```

---

## 相关文档

| 主题 | 文档 |
|------|------|
| **配置详解** | [02-configuration-guide.md](02-configuration-guide.md) |
| **内存系统** | [03-memory-system-design.md](03-memory-system-design.md) |
| **跨机器协作** | [04-cross-machine-sync.md](04-cross-machine-sync.md) |
| **高级模式** | [05-advanced-patterns.md](05-advanced-patterns.md) |

---

**下一步**: 阅读 [配置完全指南](02-configuration-guide.md) 了解详细配置选项
