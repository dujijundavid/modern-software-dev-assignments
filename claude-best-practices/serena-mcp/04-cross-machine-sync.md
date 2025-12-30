# Serena 跨机器协作指南

> 通过 Git 实现 .serena 配置和记忆的多设备同步

---

## 目录

1. [Git 共享策略详解](#git-共享策略详解)
2. [敏感信息处理](#敏感信息处理)
3. [合并冲突解决](#合并冲突解决)
4. [缓存管理策略](#缓存管理策略)
5. [实战工作流示例](#实战工作流示例)

---

## Git 共享策略详解

### 1.1 .gitignore 设计原理

#### 目录结构

```
.serena/
├── .gitignore          ← Serena 自己的 gitignore
├── project.yml         ← 共享: 配置文件
├── memories/           ← 共享: 记忆文件
│   ├── *.md
│   └── ...
└── cache/              ← 不共享: 机器特定缓存
    ├── language_server_state.json
    └── symbol_cache.json
```

#### .serena/.gitignore 内容

```gitignore
# .serena/.gitignore
# 只排除机器特定的缓存目录

/cache
```

#### 项目根 .gitignore 配置

```gitignore
# .gitignore (项目根)

# 传统方式: 忽略整个 .serena/
# .serena/

# Serena 方式: 明确排除 cache，共享其他内容
!.serena/
.serena/cache/
```

### 1.2 Git 忽略规则工作原理

```
规则优先级 (从高到低):
  1. 否定规则 (!pattern)
  2. 目录规则 (pattern/)
  3. 文件规则 (pattern)
  4. 通配符规则 (*, **)

示例:
  .serena/         # 忽略 .serena/ 目录
  !.serena/        # 但不忽略 .serena/ 目录本身
  .serena/cache/   # 忽略 .serena/cache/ 目录

结果:
  .serena/project.yml        ✓ 被追踪
  .serena/.gitignore         ✓ 被追踪
  .serena/memories/*.md      ✓ 被追踪
  .serena/cache/             ✗ 被忽略
```

### 1.3 验证 Git 追踪状态

```bash
# 检查文件是否被忽略
git check-ignore -v .serena/project.yml
# 预期: (无输出，表示不被忽略)

git check-ignore -v .serena/cache/
# 预期: .serena/cache/  被忽略

# 查看当前追踪的文件
git ls-files .serena/
# 预期输出:
# .serena/.gitignore
# .serena/project.yml
# .serena/memories/agent_communication_log.md
# .serena/memories/architecture_decisions.md
# ...

# 查看 Git 状态
git status
# 预期: .serena/cache/ 不应该出现在未追踪列表中
```

### 1.4 初始化跨机器共享

#### 机器 A (首次设置)

```bash
# 1. 创建 .serena/ 结构
mkdir -p .serena/memories
mkdir -p .serena/cache

# 2. 创建配置文件
cat > .serena/project.yml << 'EOF'
languages:
  - python
encoding: "utf-8"
project_name: "my-project"
EOF

# 3. 创建 .gitignore
cat > .serena/.gitignore << 'EOF'
/cache
EOF

# 4. 设置项目 .gitignore
# 确保 .gitignore 包含:
!.serena/
.serena/cache/

# 5. 创建初始记忆
cat > .serena/memories/project_context.md << 'EOF'
# Project Context

## Vision
{Project vision}

## Goals
- {Goal 1}
EOF

# 6. 提交到 Git
git add .serena/
git commit -m "feat: add Serena configuration"

# 7. 推送到远程
git push origin main
```

#### 机器 B (克隆和同步)

```bash
# 1. 克隆仓库
git clone repo-url
cd repo

# 2. 验证 .serena/ 已同步
ls -la .serena/
# 应该看到:
# .gitignore
# memories/
# project.yml

# 3. 验证配置
cat .serena/project.yml

# 4. 创建本地 cache 目录
mkdir -p .serena/cache

# 5. 开始工作
# AI 会自动从 .serena/memories/ 加载上下文
```

---

## 敏感信息处理

### 2.1 什么不应该提交

```yaml
# ❌ 不要在 memories/ 中包含:
- API keys
- Passwords
- Personal access tokens
- Database credentials
- SSH keys
- 机器特定路径
- 个人配置

# ✅ 应该包含:
- 项目架构决策
- 代码模式和规范
- 测试策略
- 常见问题解决方案
- 项目上下文和目标
```

### 2.2 环境变量处理

#### 正确方式

```markdown
# .serena/memories/tech_stack.md

## Environment Variables

This project uses the following environment variables:

| Variable | Purpose | Example |
|----------|---------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost/db` |
| `OLLAMA_BASE_URL` | Ollama service URL | `http://localhost:11434` |
| `LOG_LEVEL` | Logging level | `DEBUG` or `INFO` |

**Setup**: Create a `.env` file in the project root with your actual values.
```

```bash
# .env (不提交到 Git)
DATABASE_URL=postgresql://realuser:realpass@localhost/realdb
OLLAMA_BASE_URL=http://localhost:11434
LOG_LEVEL=DEBUG
```

```bash
# .env.example (提交到 Git)
DATABASE_URL=postgresql://user:pass@localhost/db
OLLAMA_BASE_URL=http://localhost:11434
LOG_LEVEL=INFO
```

### 2.3 机器特定配置

#### 使用 local.*.yml

```yaml
# .serena/project.yml (共享)
languages:
  - python

encoding: "utf-8"

project_name: "my-project"
```

```yaml
# .serena/project.local.yml (不共享，添加到 .gitignore)
languages:
  - python
  - typescript    # 机器特定的额外语言

initial_prompt: |
  Machine-specific prompt customization
```

#### 更新 .gitignore

```bash
# .serena/.gitignore
/cache
*.local.yml
```

---

## 合并冲突解决

### 3.1 常见冲突场景

#### 场景 1: 同时更新同一个记忆

```
机器 A (上午):
  编辑: .serena/memories/architecture_decisions.md
  追加: Decision: Use PostgreSQL
  提交: "docs: add PostgreSQL decision"
  推送: ✓

机器 B (下午):
  编辑: .serena/memories/architecture_decisions.md
  追加: Decision: Use Redis for caching
  提交: "docs: add Redis decision"
  推送: ✗ 冲突!
```

#### 解决方案: 手动合并

```bash
# 机器 B: 拉取时发现冲突
git pull origin main
# CONFLICT (content): Merge conflict in .serena/memories/architecture_decisions.md

# 查看冲突
cat .serena/memories/architecture_decisions.md
```

```
<<<<<<< HEAD
## Decision: Use Redis for Caching

**Date**: 2025-12-30

...
=======
## Decision: Use PostgreSQL

**Date**: 2025-12-30

...
>>>>>>> origin/main
```

```bash
# 手动合并
# 保留两个决策，按日期排序

## Decision: Use PostgreSQL

**Date**: 2025-12-30 09:00

...

## Decision: Use Redis for Caching

**Date**: 2025-12-30 14:00

...

# 添加并提交
git add .serena/memories/architecture_decisions.md
git commit -m "docs: merge PostgreSQL and Redis decisions"
git push origin main
```

### 3.2 冲突预防策略

#### 策略 1: 频繁同步

```bash
# 工作开始前
git pull origin main

# 工作结束后
git add .
git commit -m "docs: update memory"
git push origin main
```

#### 策略 2: 使用分支

```bash
# 创建分支进行记忆更新
git checkout -b update-serena-memories

# 编辑记忆
vim .serena/memories/architecture_decisions.md

# 提交并推送分支
git add .
git commit -m "docs: add new decision"
git push origin update-serena-memories

# 创建 PR，审查后合并
```

#### 策略 3: 按文件分工

```
开发者 A:
  - architecture_decisions.md
  - code_patterns.md
  - testing_strategies.md

开发者 B:
  - common_issues_solutions.md
  - llm_integration_patterns.md
  - security_considerations.md
```

### 3.3 自动化合并助手

```bash
#!/bin/bash
# scripts/merge-serena-memories.sh

echo "=== Serena Memory Merge Helper ==="

# 1. 拉取最新
git pull origin main

# 2. 检查冲突
CONFLICTS=$(git diff --name-only --diff-filter=U)

if [ -z "$CONFLICTS" ]; then
  echo "No conflicts found."
  exit 0
fi

# 3. 列出冲突文件
echo "Conflicts in:"
echo "$CONFLICTS" | grep .serena/

# 4. 提供合并建议
echo ""
echo "Merge strategies:"
echo "1. Keep both changes (append)"
echo "2. Keep local changes"
echo "3. Keep remote changes"
echo "4. Manual merge"

read -p "Choose strategy (1-4): " choice

case $choice in
  1)
    # 追加两个版本
    for file in $(echo "$CONFLICTS" | grep .serena/); do
      echo "Appending changes in $file"
      # 自定义逻辑: 追加冲突标记之间的内容
    done
    ;;
  2)
    # 保留本地
    git checkout --ours .serena/
    ;;
  3)
    # 保留远程
    git checkout --theirs .serena/
    ;;
  4)
    # 手动合并
    echo "Please resolve conflicts manually"
    ;;
esac

git add .serena/
echo "Conflicts resolved. Please review and commit."
```

---

## 缓存管理策略

### 4.1 缓存目录结构

```
.serena/cache/
├── language_server_state.json    # 语言服务器状态
├── symbol_cache.json             # 符号索引缓存
└── ...                           # 其他机器特定缓存
```

### 4.2 .serena/.gitignore 策略

```gitignore
# .serena/.gitignore

# 排除整个 cache 目录
/cache

# 如果需要更细粒度控制:
# /cache/*.json
# /cache/language_server_*
```

### 4.3 清理缓存

```bash
# 清理所有缓存
rm -rf .serena/cache/*

# 清理特定缓存
rm .serena/cache/language_server_state.json
rm .serena/cache/symbol_cache.json

# Git 确认缓存未被追踪
git status
# .serena/cache/ 不应该出现在未追踪列表
```

### 4.4 缓存恢复

```bash
# 缓存会在以下情况自动重建:
# 1. 语言服务器重启
# 2. 符号搜索
# 3. 项目重新扫描

# 手动触发缓存重建
# (通过 MCP 工具)
restart_language_server
```

---

## 实战工作流示例

### 5.1 场景: 多设备开发工作流

#### 家庭电脑 (工作开始)

```bash
# 1. 同步最新
git pull origin main

# 2. 开始开发
# AI 自动加载 .serena/memories/

# 3. 记录新决策
# AI 写入 architecture_decisions.md

# 4. 提交变更
git add .serena/memories/architecture_decisions.md
git commit -m "docs: record caching strategy decision"
git push origin main
```

#### 办公室电脑 (继续工作)

```bash
# 1. 同步最新
git pull origin main
# 已包含: 家庭电脑的新决策

# 2. AI 加载更新的记忆
# AI 知道: "我们昨天决定使用 Redis 缓存"

# 3. 基于新决策继续开发
# 实现缓存功能

# 4. 记录实现细节
# AI 写入 code_patterns.md

# 5. 提交变更
git add .serena/memories/code_patterns.md
git commit -m "docs: add Redis cache pattern"
git push origin main
```

### 5.2 场景: 团队协作工作流

#### 开发者 A (后端)

```bash
# 1. 更新架构决策
vim .serena/memories/architecture_decisions.md
# 添加: "Decision: Use FastAPI for backend"

git add .serena/memories/architecture_decisions.md
git commit -m "docs: add FastAPI decision"
git push origin main
```

#### 开发者 B (前端)

```bash
# 1. 同步后端决策
git pull origin main
# 看到: FastAPI 决策

# 2. 更新前端架构
vim .serena/memories/architecture_decisions.md
# 添加: "Decision: Use React for frontend (to match FastAPI backend)"

git add .serena/memories/architecture_decisions.md
git commit -m "docs: add React decision"
git push origin main
```

#### 开发者 A (审查)

```bash
# 1. 拉取前端决策
git pull origin main
# 看到: React 决策

# 2. 验证一致性
# AI 读取完整架构决策
# AI: "前后端技术栈一致"
```

### 5.3 场景: 问题解决和知识共享

#### 开发者 A (遇到问题)

```bash
# 问题: pytest 测试失败

# AI 记录问题
# 写入 .serena/memories/common_issues_solutions.md
git add .serena/memories/common_issues_solutions.md
git commit -m "docs: record pytest fixture issue"
git push origin main
```

#### 开发者 B (遇到同样问题)

```bash
# 同步
git pull origin main

# AI 读取记忆
# AI: "根据记录，这个问题通过使用 fixture 参数化解决"

# 应用解决方案
# 问题解决!
```

### 5.4 场景: CI/CD 集成

#### .github/workflows/validate-serena.yml

```yaml
name: Validate Serena Configuration

on:
  push:
    paths:
      - '.serena/**'
  pull_request:
    paths:
      - '.serena/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check .serena structure
        run: |
          test -d .serena || exit 1
          test -f .serena/project.yml || exit 1
          test -f .serena/.gitignore || exit 1
          test -d .serena/memories || exit 1

      - name: Validate YAML syntax
        run: |
          pip install yq
          yq eval . .serena/project.yml > /dev/null

      - name: Check Git tracking
        run: |
          # project.yml should be tracked
          git ls-files --error-unmatch .serena/project.yml

          # cache/ should NOT be tracked
          ! git ls-files --error-unmatch .serena/cache/ 2>/dev/null

      - name: Validate memory files
        run: |
          for file in .serena/memories/*.md; do
            echo "Validating $file"
            # 检查 Markdown 格式
            head -1 "$file" | grep -q "^# " || exit 1
          done
```

---

## 故障排查

### 6.1 问题: 配置未同步

| 症状 | 原因 | 解决方案 |
|------|------|----------|
| 新设备没有 .serena/ | .gitignore 错误 | 检查 `!.serena/` 规则 |
| memories/ 为空 | 未提交到 Git | `git add .serena/memories/` |
| 缓存被提交 | .gitignore 缺失 | 添加 `/cache` 到 .serena/.gitignore |

### 6.2 问题: 冲突频繁

| 症状 | 原因 | 解决方案 |
|------|------|----------|
| 总是合并冲突 | 多人同时编辑同一文件 | 分工: 按文件或分支 |
| 难以解决冲突 | 缺少自动化工具 | 使用合并助手脚本 |

---

## 相关文档

| 主题 | 文档 |
|------|------|
| **架构概览** | [01-architecture-overview.md](01-architecture-overview.md) |
| **配置指南** | [02-configuration-guide.md](02-configuration-guide.md) |
| **内存系统** | [03-memory-system-design.md](03-memory-system-design.md) |
| **高级模式** | [05-advanced-patterns.md](05-advanced-patterns.md) |

---

**下一步**: 阅读 [高级模式和技巧](05-advanced-patterns.md) 了解更深层的用法
