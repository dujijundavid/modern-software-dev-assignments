# Serena MCP 最佳实践指南

> 深入理解 Serena AI 项目内存系统和上下文管理

---

## 什么是 Serena？

**Serena** 是一个专为 AI 项目设计的**持久化内存和上下文管理系统**，通过 `.serena/` 目录实现：

- **项目级配置管理** - 集中管理 AI 代理的行为和工具
- **持久化内存系统** - 跨会话保存项目知识、决策和学习
- **跨机器协作** - 通过 Git 共享配置和记忆，实现多设备同步
- **MCP 工具集成** - 提供标准化的内存读写工具接口

### 核心价值主张

| 特性 | 传统方式 | Serena 方式 | 改进 |
|------|---------|------------|------|
| **会话上下文** | 每次重新解释 | 从内存恢复 | 90%+ 时间节省 |
| **知识积累** | 分散在文件中 | 集中式记忆库 | 可搜索、可复用 |
| **多设备协作** | 手动同步配置 | Git 自动同步 | 零配置一致性 |
| **AI 行为控制** | 散落各处的 prompt | 统一配置文件 | 一致性保证 |

---

## 与 Claude Code 的关系

```
Claude Code (主代理)
    │
    ├─► CLAUDE.md (项目级行为指南)
    │       └─► AI 团队配置、工作流定义
    │
    └─► .serena/ (项目级内存系统)
            ├─► project.yml (代理配置)
            ├─► memories/ (持久化知识)
            └─► .gitignore (共享策略)
```

### 对比说明

| 维度 | CLAUDE.md | Serena |
|------|-----------|--------|
| **本质** | 静态配置文件 | 动态内存系统 |
| **作用** | 定义 AI 如何工作 | 存储 AI 学到了什么 |
| **更新频率** | 项目初始化后较少 | 持续更新 |
| **内容类型** | 角色定义、工作流 | 决策记录、错误解决方案 |
| **生命周期** | 项目存在期间 | 随项目演进 |

---

## 系统架构概览

```
.serena/
├── project.yml              # 主配置文件
│   ├─ languages            # 语言服务器配置
│   ├─ encoding             # 文件编码
│   ├─ ignored_paths        # 忽略路径
│   ├─ excluded_tools       # 排除工具
│   └─ initial_prompt       # 初始提示词
│
├── .gitignore               # Git 共享策略
│   └─ /cache              # 排除机器特定缓存
│
├── memories/                # 持久化内存
│   ├── project_context_and_goals.md     # 项目愿景
│   ├── architecture_decisions.md        # 架构决策
│   ├── code_patterns.md                 # 代码模式
│   ├── development_workflow.md          # 工作流程
│   ├── testing_strategies.md            # 测试策略
│   ├── tech_stack.md                    # 技术栈
│   ├── common_issues_solutions.md       # 常见问题
│   ├── agent_communication_log.md       # 代理交互日志
│   ├── learning_progress.md             # 学习进度
│   ├── security_considerations.md       # 安全考虑
│   ├── llm_integration_patterns.md      # LLM 集成模式
│   ├── session_history.md               # 会话历史
│   └── weekly_assignments.md            # 每周作业
│
└── cache/                   # 机器特定缓存 (不提交)
```

---

## 快速开始

### 1. 初始化 Serena

```bash
# 在项目根目录创建 .serena/ 结构
mkdir -p .serena/memories
mkdir -p .serena/cache

# 创建基础配置
cat > .serena/project.yml << 'EOF'
languages:
  - python

encoding: "utf-8"
ignore_all_files_in_gitignore: true
ignored_paths: []
read_only: false
excluded_tools: []
initial_prompt: ""
project_name: "your-project-name"
included_optional_tools: []
EOF

# 设置 Git 共享策略
cat > .serena/.gitignore << 'EOF'
/cache
EOF

# 提交到 Git
git add .serena/
git commit -m "feat: add Serena configuration"
```

### 2. 配置 Git 共享

```bash
# 确保 .serena/ 被跟踪
# .gitignore 中应该有：
# !.serena/
# .serena/cache/

# 验证哪些文件会被提交
git check-ignore -v .serena/project.yml  # 不应该被忽略
git check-ignore -v .serena/cache/       # 应该被忽略
```

### 3. 创建第一个内存

```bash
# 创建项目上下文记忆
cat > .serena/memories/project_context.md << 'EOF'
# Project Context

## Vision
Brief description of project vision.

## Goals
- Goal 1
- Goal 2

## Success Criteria
- [ ] Criteria 1
- [ ] Criteria 2
EOF
```

---

## 学习路径

### 初级（第 1-2 周）

**目标**: 理解基础，配置项目

| 任务 | 文件 | 时间 |
|------|------|------|
| 理解架构 | [01-architecture-overview.md](01-architecture-overview.md) | 30 分钟 |
| 配置项目 | [02-configuration-guide.md](02-configuration-guide.md) | 1 小时 |
| 创建基础记忆 | [03-memory-system-design.md](03-memory-system-design.md) | 1 小时 |

**检查点**:
- [ ] 项目有完整的 .serena/ 结构
- [ ] project.yml 配置正确
- [ ] Git 共享策略工作正常
- [ ] 至少创建了 3 个基础记忆文件

### 中级（第 3-4 周）

**目标**: 深入使用，跨机器协作

| 任务 | 文件 | 时间 |
|------|------|------|
| 设置跨机器同步 | [04-cross-machine-sync.md](04-cross-machine-sync.md) | 1 小时 |
| 学习高级模式 | [05-advanced-patterns.md](05-advanced-patterns.md) | 2 小时 |
| 与 CLAUDE.md 配合 | [03-claude-md-best-practices.md](../project-patterns/03-claude-md-best-practices.md) | 1 小时 |

**检查点**:
- [ ] 在多台机器间同步配置成功
- [ ] 理解 MCP 工具集成模式
- [ ] Serena 与 CLAUDE.md 配合使用
- [ ] 建立了完整的记忆更新流程

### 高级（第 5 周以上）

**目标**: 系统优化，自定义扩展

| 任务 | 说明 | 时间 |
|------|------|------|
| 性能优化 | 优化内存加载和索引 | 2 小时 |
| 自定义 MCP 工具 | 扩展 Serena 工具集 | 4 小时 |
| 多项目管理 | 统一多个项目的 Serena | 3 小时 |
| 与 SuperClaude 集成 | 高级工作流自动化 | 4 小时 |

**检查点**:
- [ ] 建立了项目特定的记忆模板
- [ ] 实现了自动化记忆更新
- [ ] 与 SuperClaude 深度集成
- [ ] 分享了最佳实践给团队

---

## 核心概念速查

### 配置层

| 配置项 | 作用 | 示例值 |
|--------|------|--------|
| `languages` | 启动的语言服务器 | `["python"]` |
| `encoding` | 文件编码 | `"utf-8"` |
| `ignored_paths` | 额外忽略路径 | `["tmp/**", "build/**"]` |
| `excluded_tools` | 禁用的工具 | `[]` |
| `initial_prompt` | 项目初始提示 | 项目级指令 |

### 内存类型

| 类型 | 用途 | 更新频率 |
|------|------|----------|
| **项目上下文** | 愿景、目标、成功标准 | 季度 |
| **架构决策** | 技术选择记录 | 按需 |
| **代码模式** | 编码规范、约定 | 每月 |
| **工作流程** | 开发流程规范 | 双周 |
| **问题解决** | 错误和解决方案 | 实时 |

### MCP 工具

| 工具 | 用法 | 示例 |
|------|------|------|
| `write_memory` | 写入记忆 | `write_memory("decision", content)` |
| `read_memory` | 读取记忆 | `read_memory("decision")` |
| `list_memories` | 列出所有记忆 | `list_memories()` |
| `delete_memory` | 删除记忆 | `delete_memory("old-decision")` |

---

## 常见使用场景

### 场景 1: 新设备设置

```bash
# 1. Clone repository
git clone repo-url
cd repo

# 2. 验证 Serena 配置已同步
ls .serena/
# .gitignore, memories/, project.yml

# 3. 验证配置正确
cat .serena/project.yml

# 4. 开始工作，AI 自动加载记忆
# "从 .serena/memories/ 恢复项目上下文..."
```

### 场景 2: 记录架构决策

```yaml
# AI 工作流
1. 用户: "我们选择了 PostgreSQL 而非 MongoDB"
2. AI: 使用 @documentation-specialist
3. 写入: .serena/memories/architecture_decisions.md
4. 格式: 标准化决策记录模板
5. Git: 自动提交到版本控制
```

### 场景 3: 跨会话恢复

```yaml
会话 1:
  - 用户: "实现用户认证"
  - AI: 分析现有代码，设计方案
  - 结果: 写入 session/context

会话 2 (第二天):
  - AI: 自动读取 session/context
  - AI: "昨天我们设计了认证系统..."
  - 用户: "继续实现"
  - AI: 基于昨天的工作继续
```

---

## 文件导航

### 核心文档

| 文件 | 内容 | 目标读者 |
|------|------|----------|
| [README.md](README.md) | 本文件 - 概览和导航 | 所有用户 |
| [01-architecture-overview.md](01-architecture-overview.md) | 系统架构和组件 | 技术决策者 |
| [02-configuration-guide.md](02-configuration-guide.md) | 配置完全指南 | 配置管理员 |
| [03-memory-system-design.md](03-memory-system-design.md) | 内存系统设计 | 知识管理者 |
| [04-cross-machine-sync.md](04-cross-machine-sync.md) | 跨机器协作 | 多设备用户 |
| [05-advanced-patterns.md](05-advanced-patterns.md) | 高级模式和技巧 | 高级用户 |

### 相关资源

| 资源 | 链接 |
|------|------|
| **项目配置** | [../../CLAUDE.md](../../CLAUDE.md) |
| **子代理系统** | [../project-patterns/02-subagent-system.md](../project-patterns/02-subagent-system.md) |
| **Skills 设计** | [../project-patterns/04-skill-design-best-practices.md](../project-patterns/04-skill-design-best-practices.md) |
| **MCP 协议** | https://modelcontextprotocol.io |

---

## 最佳实践摘要

### DO - 推荐做法

```yaml
配置:
  - 使用 Git 追踪 .serena/ 目录
  - 只排除 cache/ 子目录
  - 使用明确的 ignored_paths

内存:
  - 使用标准化模板
  - 按主题组织记忆
  - 定期更新过时内容

协作:
  - 在多台设备间测试同步
  - 使用分支管理记忆更新
  - 记录配置变更原因
```

### DON'T - 避免做法

```yaml
配置:
  - 不要忽略整个 .serena/ 目录
  - 不要在记忆中存储敏感信息
  - 不要频繁更改 languages 配置

内存:
  - 不要创建重复的记忆
  - 不要混合不同主题的内容
  - 不要忽视记忆的更新

协作:
  - 不要手动合并 .serena/ 冲突
  - 不要在不测试时推送配置变更
  - 不要假设所有设备配置相同
```

---

## 故障排查速查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 配置未同步 | .gitignore 错误 | 检查 `!.serena/` 规则 |
| 内存丢失 | cache 被提交 | 添加 `/cache` 到 .serena/.gitignore |
| 语言服务器未启动 | languages 配置错误 | 验证语言名称正确 |
| 工具不可用 | 被排除列表包含 | 检查 excluded_tools |

---

## 社区和贡献

### 获取帮助

- **GitHub Issues**: 报告问题和建议
- **文档 PR**: 改进文档和示例
- **分享模板**: 贡献记忆模板

### 贡献指南

1. **文档改进**: 修正错误、补充示例
2. **模板分享**: 提供行业特定的记忆模板
3. **工具集成**: 开发 Serena 扩展工具

---

## 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2025-12-30 | 初始版本，完整文档集 |

---

**开始你的 Serena 之旅！** 推荐从 [架构概览](01-architecture-overview.md) 开始。
