# Serena 配置完全指南

> project.yml 完整参考、配置策略和最佳实践

---

## 目录

1. [配置文件结构](#配置文件结构)
2. [配置项详解](#配置项详解)
3. [环境变量管理](#环境变量管理)
4. [最佳实践清单](#最佳实践清单)
5. [常见配置陷阱](#常见配置陷阱)

---

## 配置文件结构

### 1.1 完整示例

```yaml
# ============================================
# Serena 项目配置文件
# ============================================
# 位置: .serena/project.yml
# 用途: 定义 AI 代理的行为、工具和项目特性
# ============================================

# ============ 语言服务器配置 ============
# 支持的语言列表 (按优先级排序)
# 第一个语言是默认语言
languages:
  - python
  # - typescript   # 取消注释以启用
  # - go
  # - rust

# ============ 文件编码 ============
# 项目文本文件的编码格式
# 参考列表: https://docs.python.org/3.11/library/codecs.html#standard-encodings
encoding: "utf-8"

# ============ Git 忽略策略 ============
# 是否使用项目的 .gitignore 文件来忽略文件
# 添加于 2025-04-07
ignore_all_files_in_gitignore: true

# ============ 额外忽略路径 ============
# 与 Git ignore 相同的语法 (* 和 **)
# 曾用名: ignored_dirs (请更新旧配置)
# 添加于 2025-04-07
ignored_paths:
  - "tmp/**"
  - "build/**"
  - "dist/**"
  - "**/*.min.js"
  - "**/*.min.css"
  - "node_modules/**"

# ============ 只读模式 ============
# 如果为 true，所有编辑工具将被禁用
# 尝试使用编辑工具将返回错误
# 添加于 2025-04-18
read_only: false

# ============ 工具排除列表 ============
# 不推荐排除任何工具，详见 README
# 以下是完整工具列表供参考
# 要获取最新列表和描述，运行:
#   uv run scripts/print_tool_overview.py
excluded_tools: []

# ============ 初始提示词 ============
# 激活项目时总是提供给 LLM 的提示词
# (与记忆不同，记忆是按需加载的)
initial_prompt: |
  You are working on {project_name}.
  This is a CS146S Modern Software Developer course project.

  Important guidelines:
  - Follow patterns in .serena/memories/code_patterns.md
  - Refer to .serena/memories/testing_strategies.md for testing
  - Use fastapi-expert for API development
  - Always run code-reviewer before committing

# ============ 项目名称 ============
project_name: "modern-software-dev-assignments"

# ============ 可选工具包含列表 ============
included_optional_tools: []
```

### 1.2 最小配置

```yaml
# 最小可行配置
languages:
  - python

encoding: "utf-8"

project_name: "my-project"

# 其他字段使用默认值
```

### 1.3 多语言项目配置

```yaml
# Python + TypeScript 前端
languages:
  - python        # 后端 API
  - typescript    # 前端

# 第一个语言 (python) 是默认语言
# 当文件匹配多个语言时使用第一个
```

---

## 配置项详解

### 2.1 languages 配置

#### 支持的语言服务器

| 语言 | 配置值 | Language Server | 特殊要求 |
|------|--------|----------------|----------|
| **Python** | `python` | Pyright | 无 |
| **TypeScript/JavaScript** | `typescript` | TypeScript Language Server | 无 |
| **Go** | `go` | gopls | 无 |
| **Rust** | `rust` | rust-analyzer | 无 |
| **Java** | `java` | Eclipse JDT LS | 无 |
| **C/C++** | `cpp` | clangd | 无 |
| **C#** | `csharp` | OmniSharp | 需要 .sln 文件 |
| **Ruby** | `ruby` 或 `ruby_solargraph` | Solargraph | 无 |
| **PHP** | `php` | Intelephense | 无 |
| **Lua** | `lua` | Lua LS | 无 |
| **Markdown** | `markdown` | Marksman | 无 |
| **YAML** | `yaml` | YAML LS | 无 |

#### 语言选择策略

```
文件: app/main.py
    ↓
检查 languages 列表 (按顺序):
    1. python?     YES → 使用 Pyright ✓
    (不再检查其他语言)

文件: components/Button.tsx
    ↓
检查 languages 列表 (按顺序):
    1. python?     NO
    2. typescript? YES → 使用 TypeScript LS ✓
```

#### 多语言项目示例

```yaml
# 全栈项目: Python 后端 + TypeScript 前端
languages:
  - python        # 优先级 1: 后端 API
  - typescript    # 优先级 2: 前端组件

# 文件匹配:
# - app/main.py           → Python LS
# - frontend/app.tsx      → TypeScript LS
# - shared/types.ts       → TypeScript LS
```

```yaml
# 数据科学项目: Python + R
languages:
  - python        # 主要语言
  - r             # R 脚本

# 文件匹配:
# - analysis/model.py      → Python LS
# - analysis/clean.R       → R LS
# - notebooks/analysis.ipynb → 取决于第一个匹配的语言服务器
```

#### 特殊场景

**场景 1: C# 项目**

```yaml
languages:
  - csharp       # 需要在项目文件夹中有 .sln 文件

# 如果没有 .sln 文件，语言服务器不会启动
# 错误: "No solution file found"
```

**场景 2: JavaScript 项目**

```yaml
# JavaScript 使用 TypeScript 语言服务器
languages:
  - typescript   # 同时支持 .js 和 .ts 文件

# 文件匹配:
# - app.js               → TypeScript LS
# - component.tsx        → TypeScript LS
# - utils.ts             → TypeScript LS
```

### 2.2 encoding 配置

#### 常见编码值

| 编码 | 用途 | 备注 |
|------|------|------|
| `"utf-8"` | 通用 | **推荐默认值** |
| `"utf-8-sig"` | 带 BOM 的 UTF-8 | Windows 兼容 |
| `"latin-1"` | 西欧语言 | ISO-8859-1 |
| `"ascii"` | 纯 ASCII | 不推荐国际化项目 |
| `"cp1252"` | Windows 西欧 | 区域特定 |

#### 编码问题排查

```python
# 问题: 文件读取错误
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff

# 解决方案 1: 更改 encoding
encoding: "latin-1"

# 解决方案 2: 转换文件为 UTF-8
iconv -f ISO-8859-1 -t UTF-8 input.txt > output.txt
```

#### 最佳实践

```yaml
# ✅ 推荐: 使用 UTF-8
encoding: "utf-8"

# ❌ 避免: 使用区域特定编码
encoding: "cp1252"  # 限制跨平台兼容性
```

### 2.3 ignore_all_files_in_gitignore 配置

#### 工作原理

```yaml
# 当设置为 true 时
ignore_all_files_in_gitignore: true

# Serena 会读取项目根目录的 .gitignore
# 并将那些规则应用到自己的文件扫描中
```

#### 示例对比

```yaml
# === 项目 .gitignore ===
__pycache__/
*.pyc
.env
.venv/
build/
dist/

# === Serena 行为 ===

# ignore_all_files_in_gitignore: false
Serena 扫描结果:
  - __pycache__/module.pyc    ✓ 被扫描
  - .env                      ✓ 被扫描
  - build/lib.o               ✓ 被扫描

# ignore_all_files_in_gitignore: true
Serena 扫描结果:
  - __pycache__/module.pcy    ✗ 被忽略
  - .env                      ✗ 被忽略
  - build/lib.o               ✗ 被忽略
```

#### 使用建议

```yaml
# ✅ 推荐: 启用此选项
ignore_all_files_in_gitignore: true

# 好处:
# - 避免扫描构建产物
# - 减少语言服务器负载
# - 提高性能
```

### 2.4 ignored_paths 配置

#### 语法说明

```yaml
ignored_paths:
  # 单目录
  - "tmp"

  # 目录下所有内容
  - "tmp/**"

  # 所有 .min.js 文件
  - "**/*.min.js"

  # 特定模式
  - "node_modules/**"
  - "*.log"
  - ".env*"
```

#### 常见模式

| 模式 | 匹配 | 说明 |
|------|------|------|
| `"tmp/**"` | `tmp/a`, `tmp/b/c` | tmp 目录及所有子目录 |
| `"**/*.min.js"` | `a.min.js`, `build/b.min.js` | 所有 .min.js 文件 |
| `"*.log"` | `debug.log` | 根目录 .log 文件 |
| `"**/test_*"` | `test_a.py`, `src/test_b.py` | 所有 test_ 前缀文件 |

#### 完整示例

```yaml
ignored_paths:
  # 构建产物
  - "build/**"
  - "dist/**"
  - "target/**"         # Rust
  - "out/**"            # TypeScript

  # 依赖
  - "node_modules/**"
  - "vendor/**"
  - ".venv/**"

  # 压缩文件
  - "**/*.min.js"
  - "**/*.min.css"
  - "**/*.bundle.js"

  # 临时文件
  - "tmp/**"
  - "*.log"
  - ".env*"
  - "*.swp"
  - "*.bak"

  # 缓存
  - ".cache/**"
  - "__pycache__/**"
  - "*.pyc"
  - ".pytest_cache/**"

  # IDE
  - ".idea/**"
  - ".vscode/**"
  - "*.code-workspace"
```

### 2.5 read_only 配置

#### 使用场景

```yaml
# 场景 1: 保护重要项目
read_only: true

# 适用:
# - 历史归档项目
# - 只读参考项目
# - 生产代码库

# 效果:
# - AI 无法修改文件
# - 编辑工具返回错误
# - 只能读取和分析
```

```yaml
# 场景 2: 正常开发
read_only: false

# 适用:
# - 活跃开发项目
# - 学习项目
# - 原型开发

# 效果:
# - AI 可以读写文件
# - 所有编辑工具可用
```

#### 错误示例

```yaml
# 当 read_only: true 时
用户: "帮我添加一个新端点"

AI 尝试:
  - write_file("app/new_endpoint.py", ...)

结果:
  Error: Project is in read-only mode.
  Editing tools are disabled.
```

### 2.6 excluded_tools 配置

#### 完整工具列表

```yaml
# === 文件操作工具 ===
# - create_text_file: 创建/覆盖文件
# - read_file: 读取文件
# - delete_lines: 删除行范围
# - replace_lines: 替换行范围
# - insert_at_line: 在指定行插入
# - insert_before_symbol: 在符号前插入
# - insert_after_symbol: 在符号后插入
# - replace_symbol_body: 替换符号定义

# === 目录操作工具 ===
# - list_dir: 列出目录内容

# === 搜索工具 ===
# - search_for_pattern: 搜索模式
# - find_symbol: 查找符号
# - find_referencing_symbols: 查找引用符号
# - find_referencing_code_snippets: 查找引用代码片段
# - get_symbols_overview: 获取符号概览

# === 内存工具 ===
# - write_memory: 写入记忆
# - read_memory: 读取记忆
# - list_memories: 列出记忆
# - delete_memory: 删除记忆

# === 会话工具 ===
# - onboarding: 执行入职
# - prepare_for_new_conversation: 准备新会话
# - summarize_changes: 总结变更
# - check_onboarding_performed: 检查入职状态

# === 项目工具 ===
# - activate_project: 激活项目
# - remove_project: 移除项目
# - get_current_config: 获取当前配置
# - initial_instructions: 获取初始指令
# - switch_modes: 切换模式

# === Shell 工具 ===
# - execute_shell_command: 执行 shell 命令

# === 语言服务器工具 ===
# - restart_language_server: 重启语言服务器

# === 思考工具 ===
# - think_about_collected_information: 思考信息完整性
# - think_about_task_adherence: 思考任务一致性
# - think_about_whether_you_are_done: 思考是否完成
```

#### 排除策略

```yaml
# ❌ 不推荐: 排除大部分工具
excluded_tools:
  - execute_shell_command
  - delete_lines
  - replace_lines
  # ... 更多的排除

问题:
  - 限制 AI 能力
  - 无法完成某些任务
  - 用户需要明确启用
```

```yaml
# ✅ 推荐: 最小排除
excluded_tools: []

# 或者只排除有风险的工具
excluded_tools:
  - execute_shell_command  # 如果担心安全问题

# 让 AI 自主选择需要的工具
```

### 2.7 initial_prompt 配置

#### 基础模板

```yaml
# 简洁模板
initial_prompt: |
  You are working on {project_name}.
  Follow the patterns in .serena/memories/
```

#### 详细模板

```yaml
initial_prompt: |
  You are working on {project_name}, a CS146S Modern Software Developer course project.

  ============ Project Context ============
  - Vision: Build an AI-powered productivity assistant
  - Current Week: 2 (LLM-Powered Applications)
  - Tech Stack: FastAPI, Ollama, SQLite, pytest

  ============ Guidelines ============
  1. Always check .serena/memories/code_patterns.md for code patterns
  2. Refer to .serena/memories/testing_strategies.md for testing approach
  3. Use fastapi-expert for API development
  4. Use python-testing-expert for testing tasks
  5. Always run code-reviewer before committing

  ============ Workflow ============
  For new features:
  1. Use @code-archaeologist to understand existing code
  2. Design approach with appropriate expert
  3. Implement following project patterns
  4. Add comprehensive tests
  5. Review with @code-reviewer
  6. Commit with conventional format

  ============ Important ============
  - Maintain >80% test coverage
  - Follow Black formatting (line-length: 100)
  - Use async patterns for I/O operations
  - Write memories for significant decisions
```

#### 动态变量

| 变量 | 说明 | 示例值 |
|------|------|--------|
| `{project_name}` | 项目名称 | `"modern-software-dev-assignments"` |

---

## 环境变量管理

### 3.1 环境变量配置

```yaml
# project.yml 不支持直接引用环境变量
# 但可以在 initial_prompt 中说明

initial_prompt: |
  Project uses these environment variables:
  - DATABASE_URL: PostgreSQL connection string
  - OLLAMA_BASE_URL: Ollama service URL
  - LOG_LEVEL: Logging level (DEBUG/INFO/WARNING/ERROR)
```

### 3.2 .env 文件管理

```bash
# .env 示例 (不提交到 Git)
DATABASE_URL=postgresql://user:pass@localhost/db
OLLAMA_BASE_URL=http://localhost:11434
LOG_LEVEL=DEBUG

# .env.example 示例 (提交到 Git)
DATABASE_URL=postgresql://user:pass@localhost/db
OLLAMA_BASE_URL=http://localhost:11434
LOG_LEVEL=INFO
```

### 3.3 Serena 与 .env

```yaml
# 确保 .env 被 ignored_paths 或 .gitignore 覆盖
ignored_paths:
  - ".env*"
  - ".env.local"
```

---

## 最佳实践清单

### 4.1 配置检查清单

#### 初始化检查

- [ ] `languages` 配置匹配项目需求
- [ ] `encoding` 设置为 `"utf-8"`
- [ ] `project_name` 正确设置
- [ ] `.serena/.gitignore` 只排除 `/cache`
- [ ] `.gitignore` 允许 `.serena/` 被追踪

#### 多设备检查

- [ ] 配置文件已提交到 Git
- [ ] memories/ 目录被追踪
- [ ] cache/ 目录被忽略
- [ ] 在新设备验证配置工作

#### 性能检查

- [ ] `ignore_all_files_in_gitignore: true`
- [ ] `ignored_paths` 排除构建产物
- [ ] `ignored_paths` 排除依赖目录
- [ ] `ignored_paths` 排除压缩文件

#### 安全检查

- [ ] 敏感信息不在 `initial_prompt` 中
- [ ] `.env*` 在 `ignored_paths` 中
- [ ] API keys 不在配置文件中
- [ ] `read_only` 用于重要项目

### 4.2 配置模板

#### Python Web 项目

```yaml
languages:
  - python

encoding: "utf-8"

ignore_all_files_in_gitignore: true

ignored_paths:
  - "__pycache__/**"
  - "*.pyc"
  - ".venv/**"
  - "build/**"
  - "dist/**"
  - "*.egg-info/**"
  - ".pytest_cache/**"
  - ".mypy_cache/**"

read_only: false

excluded_tools: []

initial_prompt: |
  Python web project using FastAPI.
  Check .serena/memories/ for project patterns.

project_name: "my-python-web-app"
```

#### 全栈项目

```yaml
languages:
  - python
  - typescript

encoding: "utf-8"

ignore_all_files_in_gitignore: true

ignored_paths:
  - "__pycache__/**"
  - "*.pyc"
  - ".venv/**"
  - "node_modules/**"
  - "build/**"
  - "dist/**"
  - "**/*.min.js"
  - "**/*.min.css"

read_only: false

excluded_tools: []

initial_prompt: |
  Full-stack project: Python (FastAPI) + TypeScript (React).
  Backend in app/, frontend in frontend/.

project_name: "my-fullstack-app"
```

#### 数据科学项目

```yaml
languages:
  - python
  - r

encoding: "utf-8"

ignore_all_files_in_gitignore: true

ignored_paths:
  - "__pycache__/**"
  - "*.pyc"
  - ".venv/**"
  - "*.Rhistory"
  - ".Rproj.user"
  - "*.RData"

read_only: false

excluded_tools: []

initial_prompt: |
  Data science project: Python + R.
  Notebooks in notebooks/, analysis in analysis/.

project_name: "my-data-science-project"
```

---

## 常见配置陷阱

### 5.1 语言服务器问题

#### 问题: 语言服务器未启动

```yaml
# 配置
languages:
  - python

# 错误: Language server failed to start

# 可能原因:
1. Pyright 未安装
2. Python 不在 PATH 中
3. 虚拟环境未激活

# 解决方案:
pyproject.toml:
  [tool.serena]
  dependencies = ["pyright"]
```

#### 问题: C# 语言服务器不工作

```yaml
# 配置
languages:
  - csharp

# 错误: No solution file found

# 原因: csharp 需要 .sln 文件

# 解决方案:
# 确保 .sln 文件在项目根目录
dotnet new sln -n my-project
```

### 5.2 编码问题

#### 问题: 文件读取错误

```yaml
# 错误
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff

# 原因: 文件使用不同编码

# 解决方案:
# 选项 1: 更改 encoding
encoding: "latin-1"

# 选项 2: 转换文件
iconv -f ISO-8859-1 -t UTF-8 file.py > file_utf8.py
```

### 5.3 Git 同步问题

#### 问题: 配置未同步到新设备

```bash
# 症状: 新设备上 Serena 不工作

# 诊断:
git check-ignore -v .serena/project.yml
# 输出: .serena/project.yml  被忽略

# 原因: .gitignore 配置错误

# 修复项目 .gitignore:
# 删除或注释:
# .serena/

# 确保 .serena/.gitignore:
# /cache
```

#### 问题: cache 被提交到 Git

```bash
# 症状: cache 文件出现在提交中

# 诊断:
git status
# 显示: .serena/cache/state.json

# 修复 .serena/.gitignore:
echo "/cache" > .serena/.gitignore

# 清除已追踪的文件:
git rm -r --cached .serena/cache
git commit -m "chore: remove cache from tracking"
```

### 5.4 工具排除问题

#### 问题: AI 无法执行基本操作

```yaml
# 配置
excluded_tools:
  - execute_shell_command
  - create_text_file
  - write_file
  # ... 更多排除

# 症状: AI 报错 "Tool not available"

# 建议: 保持 excluded_tools 为空
excluded_tools: []

# 如果必须排除，只排除有风险的:
excluded_tools:
  - execute_shell_command  # 仅在沙箱环境中
```

### 5.5 性能问题

#### 问题: 扫描很慢

```yaml
# 原因: 扫描了不必要的文件

# 解决方案:
ignore_all_files_in_gitignore: true

ignored_paths:
  - "node_modules/**"     # 大型依赖目录
  - "build/**"            # 构建产物
  - "dist/**"
  - "**/*.min.js"         # 压缩文件
  - "**/*.bundle.js"
```

---

## 配置验证脚本

### 验证配置

```bash
#!/bin/bash
# validate-serena-config.sh

echo "=== Serena Configuration Validation ==="

# 1. 检查 .serena/ 目录
if [ ! -d ".serena" ]; then
  echo "ERROR: .serena/ directory not found"
  exit 1
fi

# 2. 检查 project.yml
if [ ! -f ".serena/project.yml" ]; then
  echo "ERROR: project.yml not found"
  exit 1
fi

# 3. 检查 .gitignore
if [ ! -f ".serena/.gitignore" ]; then
  echo "WARNING: .serena/.gitignore not found"
fi

# 4. 检查 memories/ 目录
if [ ! -d ".serena/memories" ]; then
  echo "WARNING: memories/ directory not found"
fi

# 5. 验证 YAML 语法
if command -v yq &> /dev/null; then
  yq eval . .serena/project.yml > /dev/null
  if [ $? -ne 0 ]; then
    echo "ERROR: Invalid YAML syntax in project.yml"
    exit 1
  fi
fi

# 6. 检查 Git 追踪状态
if [ -d ".git" ]; then
  if git check-ignore -q .serena/project.yml; then
    echo "ERROR: .serena/project.yml is ignored by Git"
    exit 1
  fi

  if ! git check-ignore -q .serena/cache/; then
    echo "WARNING: .serena/cache/ is not ignored"
  fi
fi

echo "=== Validation Complete ==="
echo "All checks passed!"
```

---

## 相关文档

| 主题 | 文档 |
|------|------|
| **架构概览** | [01-architecture-overview.md](01-architecture-overview.md) |
| **内存系统** | [03-memory-system-design.md](03-memory-system-design.md) |
| **跨机器同步** | [04-cross-machine-sync.md](04-cross-machine-sync.md) |

---

**下一步**: 阅读 [内存系统设计](03-memory-system-design.md) 了解如何组织项目记忆
