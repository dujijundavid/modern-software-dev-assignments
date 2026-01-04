# Claude Code 架构指南

> 面向：新接触 Claude Code 的开发/Tech Lead/PM  
> 用途：5 分钟速览 Skills / Slash Commands / Subagents / Super Claude 的职责边界与调用链

## 概述

Claude Code 生态系统由四个核心概念组成，它们形成了一个分层的架构体系。本文档详细解释这些概念的区别、联系以及使用场景。

---

## 四个核心概念

### 1. Claude Skills (MCP Skills) - 工具层

**定位**：领域特定的工具和知识库

**调用方式**：通过 `Skill` 工具

**协议**：基于 MCP (Model Context Protocol)

**例子**：
- `docx` - Word 文档处理
- `pdf` - PDF 操作
- `xlsx` - Excel 表格处理
- `pptx` - PowerPoint 演示文稿
- `algorithmic-art` - 算法艺术生成

**本质**：通过 MCP 协议提供的能力扩展

**使用场景**：
- 需要处理特定文件格式（Word、PDF、Excel）
- 需要 API 文档查询
- 需要结构化的知识检索

**存放位置**：
- 官方 Skills: `~/.claude/plugins/marketplaces/anthropic-agent-skills/skills/`
- 自定义 Skills: `~/.claude/skills/`

---

### 2. Slash Commands - 接口层

**定位**：用户可编程的命令快捷方式

**调用方式**：`/command-name`

**本质**：预定义的 prompt 模板

**例子**：
- `/sc:implement` - 功能实现命令
- `/sc:design` - 架构设计命令
- `/sc:pm` - 项目管理命令
- `/commit` - Git 提交命令

**使用场景**：
- 快速复用常用的提示词
- 简化复杂工作流的触发
- 个性化命令别名

**存放位置**：`~/.claude/commands/`

---

### 3. Subagents - 执行层

**定位**：专业化的子代理

**调用方式**：通过 `Task` 工具启动

**本质**：独立运行的专业代理

**例子**：
- `rails-backend-expert` - Rails 后端专家
- `python-expert` - Python 专家
- `react-component-architect` - React 组件架构师
- `frontend-developer` - 前端开发者

**特点**：
- 每个代理独立运行
- 有自己的工具集和专长
- 可并发执行
- 独立的上下文管理

**使用场景**：
- 需要特定领域的专业知识
- 需要并发执行多个任务
- 需要独立的上下文和工具集

---

### 4. Super Claude - 编排层

**定位**：元编排框架 (Meta-Orchestration Framework)

**调用方式**：`/sc:*` 命令

**包含**：
- 32+ Slash Commands 定义
- 多个专业化 Subagents（core, specialized, universal, orchestrators）
- 任务分解和路由逻辑

**本质**：任务分解与协调系统

**使用场景**：
- 复杂的多步骤项目
- 需要多个专业领域协作
- 需要结构化的工作流

**存放位置**：`~/Desktop/github_repos/claude-code-config/`

---

## 架构层次关系

```
┌─────────────────────────────────────────────────────────┐
│                    用户输入                               │
└───────────────────────────┬─────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
     ┌──────────┐    ┌──────────┐   ┌──────────┐
     │Slash Cmd │    │Super Claude│  │直接对话   │
     └─────┬────┘    └─────┬────┘   └─────┬────┘
           │              │              │
           │         ┌────┴────┐         │
           │         ▼         ▼         │
           │    ┌─────────┐ ┌─────────┐  │
           │    │Orchestr.│ │Special. │  │
           │    │Agents   │ │Agents   │  │
           │    └────┬────┘ └────┬────┘  │
           │         │            │       │
           └─────────┴────┬───────┘       │
                         ▼               │
                    ┌─────────┐           │
                    │ Skills  │◄──────────┘
                    │(MCP)    │
                    └─────────┘
```

---

## 典型调用链

```
用户输入: /sc:implement
    ↓
Super Claude 路由到 implement 命令
    ↓
implement 命令分析任务，分解需求
    ↓
调用合适的 subagent (如 python-expert)
    ↓
subagent 可能使用 skill (如 docx) 处理文档
```

---

## 关键区别对比

| 维度 | Skills | Slash Commands | Subagents | Super Claude |
|------|--------|----------------|-----------|--------------|
| **抽象层级** | 工具 | 快捷方式 | 执行者 | 编排器 |
| **主要作用** | 扩展能力 | 复用 prompt | 专业化执行 | 任务编排 |
| **独立性** | 依赖调用者 | 依赖调用者 | 完全独立 | 顶层协调 |
| **可组合性** | 高 | 中 | 高 | 最高 |
| **并发能力** | 无 | 无 | 有 | 有 |
| **上下文** | 共享 | 共享 | 独立 | 协调 |

---

## 使用决策树

```
你的需求是什么？
    │
    ├─ 需要处理特定格式文件？
    │   └─→ 使用 Claude Skills (docx, pdf, xlsx)
    │
    ├─ 需要复用常用提示词？
    │   └─→ 创建 Slash Command
    │
    ├─ 需要专业领域知识？
    │   └─→ 调用 Subagent
    │
    └─ 复杂多步骤项目？
        └─→ 使用 Super Claude
```

---

## 设计原则

### 职责分离

每一层都有明确的职责边界：
- **Skills** → 提供工具能力
- **Subagents** → 使用工具解决问题
- **Commands** → 暴露简洁接口
- **Framework** → 编排整体流程

### 可组合性

不同层级的能力可以自由组合：
```
Slash Command
    ↓ 可调用
Super Claude
    ↓ 可调度
Subagents
    ↓ 可使用
Skills
```

### 独立性

- Skills 可以被任何层使用
- Subagents 独立运行，互不干扰
- Slash Commands 可以独立定义
- Super Claude 作为可选的编排层

---

## 目录结构参考

```
~/.claude/
├── commands/           # Slash Commands
│   └── sc/            # Super Claude 命令
├── skills/            # 自定义 MCP Skills
└── plugins/           # 已安装的插件
    └── marketplaces/
        └── anthropic-agent-skills/
            └── skills/    # 官方 Skills

~/Desktop/github_repos/
└── claude-code-config/    # Super Claude 框架
    ├── skills/            # Slash Command 定义
    ├── agents/            # Subagent 配置
    └── superclaude/       # 核心逻辑
```

---

## 实践建议

### 1. 保留 `~/.claude/skills/` 文件夹

即使目前为空，建议保留，原因：
- 为未来自定义 MCP skills 预留空间
- 这是官方支持的自定义技能扩展点
- 保持架构完整性

### 2. 何时使用什么？

| 需求 | 选择 | 示例 |
|------|------|------|
| "我经常重复这个 prompt" | Slash Command | `/commit` |
| "我需要处理 Word/PDF/Excel" | Claude Skill | `docx`, `pdf` |
| "我需要 Python/Rails 专家" | Subagent | `python-expert` |
| "我有个复杂项目要做" | Super Claude | `/sc:implement` |

### 3. 扩展顺序

建议的学习和扩展顺序：
1. 先掌握 Slash Commands（最简单）
2. 理解 Subagents 概念
3. 学习使用官方 Skills
4. 最后创建自定义 Skills
5. 根据需要使用 Super Claude 框架

---

## 相关资源

- [SuperClaude 架构深度分析](../02-understand/superclaude-architecture.md)
- [Skills 系统完全指南](./skills-system-guide.md)
- [子代理系统架构](../02-understand/subagent-system.md)
- [Document Skills 使用指南](../03-create/document-skills-guide.md)

## 下一步阅读

- 想进一步了解编排与路由：去看 `../02-understand/superclaude-architecture.md`
- 想做命令 vs Skills 取舍：参考 `../05-learning_mode_design/commands-vs-skills.md`
